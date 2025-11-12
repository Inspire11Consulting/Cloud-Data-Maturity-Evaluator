"""
Main Streamlit application for Cloud & Data Maturity Evaluator.
Orchestrates UI components, business logic, AI generation, and exports.
"""

import streamlit as st
import json
from app.config import (
    APP_PAGE_TITLE,
    APP_TITLE,
    APP_DESCRIPTION,
    STREAMLIT_CSS,
    CATEGORIES_STRUCTURE,
    MATURITY_LEVELS
)
from ai_gen.config import OPENAI_API_KEY
from app import ui_components, business_logic, visualization, export
from ai_gen.openai_client import OpenAIClient
from ai_gen.prompts import build_category_assessment_prompt, build_consolidation_prompt
from ai_gen.json_parser import try_load_json
from ai_gen.data_normalizer import normalize_baseball_card, get_field


def initialize_session_state():
    """Initialize session state variables."""
    if "recommendation_data" not in st.session_state:
        st.session_state["recommendation_data"] = []
    if "category_fragments" not in st.session_state:
        st.session_state["category_fragments"] = []
    if "consolidated_json" not in st.session_state:
        st.session_state["consolidated_json"] = None
    if "raw_ai_outputs" not in st.session_state:
        st.session_state["raw_ai_outputs"] = {}


def generate_assessments(
    client: OpenAIClient,
    categories_to_process: list,
    all_scores: dict,
    category_inclusion: dict,
    category_comments: dict,
    industry: str,
    company_size: str,
    it_size: str,
    uses_cloud: str,
    cloud_platform: str,
    priority_projects: str,
    overall_input: str,
    seed_scenario_text: str
):
    """
    Generate AI assessments for selected categories.
    
    Args:
        client: OpenAI client instance
        categories_to_process: List of category names to process
        all_scores: Dictionary of all scores
        category_inclusion: Dictionary of inclusion flags
        category_comments: Dictionary of comments
        industry: Industry name
        company_size: Company size description
        it_size: IT department size
        uses_cloud: Cloud usage status
        cloud_platform: Cloud platform name
        priority_projects: Priority projects description
        overall_input: Overall context
        seed_scenario_text: Seed scenario text
    """
    # Reset storage for fresh run
    st.session_state["recommendation_data"] = []
    st.session_state["category_fragments"] = []
    st.session_state["raw_ai_outputs"] = {}
    st.session_state["consolidated_json"] = None

    if not categories_to_process:
        st.info("No categories selected — check 'Include' for categories to evaluate or add a comment to include it.")
        return

    with st.spinner("Calling AI for selected categories..."):
        for category in categories_to_process:
            include_flag = category_inclusion.get(category, False)
            comment_text = category_comments.get(category, "").strip()
            scores = all_scores.get(category, {})
            avg = scores.get("average")
            sub_capability_scores = scores.get("sub_capabilities", {})

            # Build prompt
            prompt = build_category_assessment_prompt(
                industry=industry,
                company_size=company_size,
                it_size=it_size,
                uses_cloud=uses_cloud,
                cloud_platform=cloud_platform,
                priority_projects=priority_projects,
                category=category,
                include_flag=include_flag,
                avg_maturity=avg,
                sub_capability_scores=sub_capability_scores,
                category_comments=comment_text,
                overall_context=overall_input,
                seed_scenario_text=seed_scenario_text
            )

            try:
                raw = client.call_openai(prompt, max_tokens=1000, temperature=0.4)
                st.session_state["raw_ai_outputs"][category] = raw
                
                # Parse robustly
                parsed = try_load_json(raw)
                normalized = normalize_baseball_card(parsed)
                
                # Store both raw, parsed and normalized for debugging & export
                st.session_state["recommendation_data"].append({
                    "category": category,
                    "raw": raw,
                    "parsed": parsed,
                    "data_normalized": normalized,
                    "show_avg": include_flag,
                    "avg": avg if include_flag else None
                })
                
                # For consolidation, use executive.focus_8w and plan_3y if present
                exec_focus = get_field(normalized["executive"], "focus_8w") or []
                exec_plan3 = get_field(normalized["executive"], "plan_3y") or []
                if isinstance(exec_focus, str):
                    exec_focus = [exec_focus]
                if isinstance(exec_plan3, str):
                    exec_plan3 = [exec_plan3]
                
                st.session_state["category_fragments"].append({
                    "category": category,
                    "focus_8w": exec_focus,
                    "plan_3y": exec_plan3
                })
            except Exception as e:
                st.error(f"Failed to generate/parse JSON for '{category}': {e}")
                # Save raw text for debugging if available
                raw_text = locals().get('raw', "<no raw captured>")
                st.session_state["raw_ai_outputs"][category] = raw_text


def consolidate_roadmap(client: OpenAIClient):
    """Consolidate category fragments into a unified roadmap."""
    fragments = st.session_state["category_fragments"]
    prompt = build_consolidation_prompt(fragments)
    
    try:
        raw = client.call_openai(prompt, max_tokens=800, temperature=0.4)
        st.session_state["raw_ai_outputs"]["consolidate"] = raw
        consolidated = try_load_json(raw)
        
        # Normalize structure
        consolidated.setdefault("focus_8w", {})
        consolidated.setdefault("plan_3y", {})
        for s in ["sprint1", "sprint2", "sprint3", "sprint4"]:
            if s not in consolidated["focus_8w"] or not isinstance(consolidated["focus_8w"][s], list):
                consolidated["focus_8w"][s] = []
        for y in ["year1", "year2", "year3"]:
            if y not in consolidated["plan_3y"] or not isinstance(consolidated["plan_3y"][y], list):
                consolidated["plan_3y"][y] = []
        
        st.session_state["consolidated_json"] = consolidated
    except Exception as e:
        st.error(f"Failed to consolidate roadmap: {e}")
        with st.expander("Raw consolidation output"):
            st.write(st.session_state["raw_ai_outputs"].get("consolidate", "<no raw>"))


def run_app():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(page_title=APP_PAGE_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.markdown(APP_DESCRIPTION)
    
    # Apply CSS styling
    st.markdown(STREAMLIT_CSS, unsafe_allow_html=True)
    
    # Check for OpenAI API key
    if not OPENAI_API_KEY:
        st.error("⚠️ OpenAI API key not found! Please create a .env file with your OPENAI_API_KEY. See .env_template for reference.")
        st.stop()
    
    # Initialize OpenAI client
    try:
        client = OpenAIClient()
    except RuntimeError as e:
        st.error(f"⚠️ {e}")
        st.stop()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    sidebar_data = ui_components.render_sidebar()
    industry, company_size, it_size, uses_cloud, cloud_platform, priority_projects, use_seed_scenario, seed_scenario_text = sidebar_data
    
    # Render maturity sliders
    slider_data = ui_components.render_maturity_sliders(CATEGORIES_STRUCTURE)
    all_scores, category_comments, category_inclusion, overall_input = slider_data
    
    # Generate AI assessments button
    if st.button("Generate AI-Powered Strategic Assessment"):
        categories_to_process = business_logic.get_included_categories(
            CATEGORIES_STRUCTURE,
            category_inclusion,
            category_comments
        )
        
        generate_assessments(
            client=client,
            categories_to_process=categories_to_process,
            all_scores=all_scores,
            category_inclusion=category_inclusion,
            category_comments=category_comments,
            industry=industry,
            company_size=company_size,
            it_size=it_size,
            uses_cloud=uses_cloud,
            cloud_platform=cloud_platform,
            priority_projects=priority_projects,
            overall_input=overall_input,
            seed_scenario_text=seed_scenario_text
        )
    
    # Display baseball cards
    if st.session_state.get("recommendation_data"):
        ui_components.render_baseball_cards(
            st.session_state["recommendation_data"],
            MATURITY_LEVELS
        )
    
    # Consolidated roadmap section
    st.markdown("---")
    st.markdown("## Consolidated Roadmap")
    
    if not st.session_state.get("category_fragments"):
        st.info("No roadmap fragments yet — generate AI recommendations first for at least one category (Include it or add a comment).")
    
    if st.session_state.get("category_fragments"):
        if st.button("Show Consolidated Roadmap"):
            consolidate_roadmap(client)
    
    # Display consolidated roadmap if available
    if st.session_state.get("consolidated_json"):
        consolidated = st.session_state["consolidated_json"]
        fig1 = visualization.draw_8week_roadmap_figure(consolidated.get("focus_8w", {}))
        fig2 = visualization.draw_3year_roadmap_figure(consolidated.get("plan_3y", {}))

        st.markdown("### 8-Week Roadmap Diagram")
        st.pyplot(fig1)

        st.markdown("### 3-Year Roadmap Diagram")
        st.pyplot(fig2)

        # Pretty print consolidated text
        ui_components.render_consolidated_roadmap_text(consolidated)

        # PPTX export
        try:
            pptx_bytes = export.export_to_pptx(
                consolidated,
                fig1,
                fig2,
                st.session_state["recommendation_data"]
            )
            st.download_button(
                "📥 Download Roadmap and Baseball Cards (PowerPoint)",
                data=pptx_bytes,
                file_name="Consolidated_Roadmap_and_Cards.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        except Exception as e:
            st.error(f"PPTX export failed: {e}")
    
    st.markdown("---")

