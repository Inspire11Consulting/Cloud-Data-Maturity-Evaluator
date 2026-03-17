"""
UI components for Streamlit app: sidebar, sliders, displays, baseball cards.
"""

import streamlit as st
import numpy as np
from typing import Dict
from ai_gen.data_normalizer import get_field

# Maturity Levels
MATURITY_LEVELS = {
    1: "Greenfield",
    2: "Emerging",
    3: "Developing",
    4: "Established",
    5: "Optimized"
}

# Default Industry Options
INDUSTRY_OPTIONS = [
    "Homebuilding & Real Estate",
    "Healthcare",
    "Manufacturing",
    "Financial Services",
    "Logistics",
    "Retail",
    "Food and Beverage"
]

# Seed Scenario Text
SEED_SCENARIO_TEXT = (
    "The client is a manufacturer and distributor of charitable gaming products. "
    "They operate three business units with silos, ~10 ERPs, no consolidated data, and many long-tenured staff resistant to change."
)


def render_sidebar():
    """
    Render the sidebar with company context inputs.
    
    Returns:
        tuple: (industry, company_size, it_size, uses_cloud, cloud_platform, priority_projects, use_seed_scenario, seed_scenario_text)
    """
    st.sidebar.header("Company Context")
    industry = st.sidebar.selectbox("Industry", INDUSTRY_OPTIONS)
    company_size = st.sidebar.text_input("Company size", "1,200 employees")
    it_size = st.sidebar.text_input("IT department size", "50")
    uses_cloud = st.sidebar.radio("Uses cloud?", ["No", "Yes"], index=1)
    cloud_platform = st.sidebar.text_input("Which cloud platform(s)?", "Azure") if uses_cloud == "Yes" else ""
    priority_projects = st.sidebar.text_area("Priority projects", "ERP consolidation, eCommerce upgrade")
    use_seed_scenario = st.sidebar.checkbox("Seed with charitable gaming scenario", value=True)
    seed_scenario_text = SEED_SCENARIO_TEXT if use_seed_scenario else ""
    
    return industry, company_size, it_size, uses_cloud, cloud_platform, priority_projects, use_seed_scenario, seed_scenario_text


def render_maturity_sliders(categories_structure: Dict) -> tuple:
    """
    Render maturity assessment sliders for all categories.
    
    Args:
        categories_structure: Dictionary of categories and sub-capabilities
    
    Returns:
        tuple: (all_scores, category_comments, category_inclusion)
    """
    st.markdown("---")
    st.markdown("## Maturity Assessment")
    st.markdown("**Scale:** 1 = Greenfield | 2 = Emerging | 3 = Developing | 4 = Established | 5 = Optimized")
    
    all_scores, category_comments, category_inclusion = {}, {}, {}
    
    for category, sub_caps in categories_structure.items():
        with st.expander(category, expanded=False):
            st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
            include_cat = st.checkbox(f"Include {category}", True, key=f"include_{category}")
            category_inclusion[category] = include_cat

            sub_scores = {}
            cols = st.columns(3)
            for i, sub_cap in enumerate(sub_caps):
                with cols[i % 3]:
                    score = st.slider(f"{sub_cap}", 1, 5, 3, key=f"{category}_{sub_cap}", format="Level %d")
                    st.caption(f"**{MATURITY_LEVELS[score]}**")
                    sub_scores[sub_cap] = score
                if (i+1) % 3 == 0 and i < len(sub_caps)-1:
                    cols = st.columns(3)

            all_scores[category] = {"average": round(np.mean(list(sub_scores.values())), 1), "sub_capabilities": sub_scores}
            comment = st.text_area(f"Comments for {category} (optional):", key=f"comment_{category}", height=70)
            category_comments[category] = comment
    
    overall_input = st.text_area("Overall context/constraints (budget, compliance, culture):", height=100)
    
    return all_scores, category_comments, category_inclusion, overall_input


def render_baseball_cards(recommendation_data: list, maturity_levels: Dict):
    """
    Render pretty baseball cards for executive and technical recommendations.
    
    Args:
        recommendation_data: List of recommendation data items
        maturity_levels: Dictionary mapping scores to level names
    """
    if not recommendation_data:
        return
    
    st.markdown("---")
    st.markdown("## AI-generated Baseball Cards (Executive & Technical)")
    
    for item in recommendation_data:
        cat = item["category"]
        normalized = item.get("data_normalized", {})
        raw_text = item.get("raw", "")
        st.subheader(cat)
        
        # Show maturity level when included
        if item.get("show_avg") and item.get("avg") is not None:
            level_label = maturity_levels.get(int(round(item["avg"])), "")
            st.caption(f"Reported maturity average: {item['avg']} — {level_label}")

        # EXECUTIVE card
        st.markdown("**EXECUTIVE Baseball Card**")
        exec_block = normalized.get("executive", {}) or {}
        if exec_block:
            summary = get_field(exec_block, "summary")
            recommendation = get_field(exec_block, "recommendation")
            activities = get_field(exec_block, "activities", "project_activities")
            focus8 = get_field(exec_block, "focus_8w")
            plan3 = get_field(exec_block, "plan_3y")
            assumptions = get_field(exec_block, "assumptions")

            if summary:
                st.markdown(f"- **Summary:** {summary}")
            if recommendation:
                st.markdown(f"- **Recommendation:** {recommendation}")
            if activities and isinstance(activities, list):
                st.markdown("- **Project Activities:**")
                for a in activities:
                    st.markdown(f"  • {a}")
            if focus8 and isinstance(focus8, list):
                st.markdown("- **8-Week Focus:**")
                for f in focus8:
                    st.markdown(f"  • {f}")
            if plan3 and isinstance(plan3, list):
                st.markdown("- **3-Year Plan:**")
                for p in plan3:
                    st.markdown(f"  • {p}")
            if assumptions and isinstance(assumptions, list):
                st.markdown("- **Assumptions:**")
                for a in assumptions:
                    st.markdown(f"  • {a}")
        else:
            st.info("No Executive card generated.")
            with st.expander(f"Raw AI output for '{cat}' (executive missing)"):
                st.code(raw_text)

        st.markdown("---")
        # TECHNICAL card
        st.markdown("**TECHNICAL Baseball Card**")
        tech_block = normalized.get("technical", {}) or {}
        if tech_block:
            summary = get_field(tech_block, "summary")
            recommendation = get_field(tech_block, "recommendation")
            activities = get_field(tech_block, "activities", "project_activities")
            focus8 = get_field(tech_block, "focus_8w")
            plan3 = get_field(tech_block, "plan_3y")
            assumptions = get_field(tech_block, "assumptions")
            team = get_field(tech_block, "team")

            if summary:
                st.markdown(f"- **Summary:** {summary}")
            if recommendation:
                st.markdown(f"- **Recommendation:** {recommendation}")
            if activities and isinstance(activities, list):
                st.markdown("- **Project Activities:**")
                for a in activities:
                    st.markdown(f"  • {a}")
            if focus8 and isinstance(focus8, list):
                st.markdown("- **8-Week Tactical Plan:**")
                for f in focus8:
                    st.markdown(f"  • {f}")
            if plan3 and isinstance(plan3, list):
                st.markdown("- **3-Year Technical Roadmap:**")
                for p in plan3:
                    st.markdown(f"  • {p}")
            if assumptions and isinstance(assumptions, list):
                st.markdown("- **Assumptions:**")
                for a in assumptions:
                    st.markdown(f"  • {a}")
            if team and isinstance(team, list):
                st.markdown("- **Initial Team (3–6 months):**")
                for t in team:
                    st.markdown(f"  • {t}")
        else:
            st.info("No Technical card generated.")
            with st.expander(f"Raw AI output for '{cat}' (technical missing)"):
                st.code(raw_text)


def render_consolidated_roadmap_text(consolidated: Dict):
    """
    Render consolidated roadmap as text.
    
    Args:
        consolidated: Consolidated roadmap dictionary
    """
    if not consolidated:
        return
    
    st.markdown("### Consolidated 8-Week Focus")
    for s in ["sprint1", "sprint2", "sprint3", "sprint4"]:
        st.markdown(f"**{s.capitalize()}**")
        for it in consolidated["focus_8w"].get(s, []):
            st.markdown(f"- {it}")

    st.markdown("### Consolidated 3-Year Plan")
    for y in ["year1", "year2", "year3"]:
        st.markdown(f"**{y.capitalize()}**")
        for it in consolidated["plan_3y"].get(y, []):
            st.markdown(f"- {it}")

