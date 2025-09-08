import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from openai import OpenAI
import re

# ---- App Configuration ----
st.set_page_config(page_title="Cloud & AI Maturity")

# ---- Set your OpenAI key ----
api_key = "sk-"  # Replace with your actual API key
client = OpenAI(api_key=api_key)

# ---- Custom CSS for professional blue theme ----
st.markdown("""
<style>    
    .category-header {
        background: linear-gradient(90deg, #1976d2, #42a5f5);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #1976d2 !important;
        color: #FFFFFF !important;
        border: 2px solid #1976d2 !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #f5f5f5 !important;
        border-color: #0d47a1 !important;
        color: #0d47a1 !important;
    }
    .stButton > button:active {
        background-color: #e0e0e0 !important;
    }
    .stCaption {
        color: #666666 !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# ---- Maturity Labels ----
levels = {
    1: "Greenfield",
    2: "Emerging", 
    3: "Developing",
    4: "Established",
    5: "Optimized"
}

# ---- Define Categories and Sub-capabilities ----
categories_structure = {
    "Cloud Architecture": [
        "Infrastructure Design",
        "Scalability & Performance", 
        "Multi-cloud Strategy",
        "Cost Optimization",
        "Disaster Recovery",
        "Service Architecture"
    ],
    "Data Management": [
        "Data Quality",
        "Data Integration",
        "Master Data Management",
        "Data Lifecycle",
        "Data Storage Strategy",
        "Real-time Processing"
    ],
    "Data Visualization & Insights": [
        "Dashboard Design",
        "Data Storytelling",
        "Interactive Visualizations",
        "Advanced Analytics Techniques",
        "Self-Service Analytics",
        "Insight Communication"
    ],
    "AI/ML Integration": [
        "Model Development",
        "MLOps & Deployment",
        "AI Ethics & Bias",
        "Business Integration",
        "AutoML Capabilities",
        "AI Governance"
    ],
    "Governance & Security": [
        "Data Privacy",
        "Compliance Management",
        "Access Controls",
        "Risk Management",
        "Audit & Monitoring",
        "Policy Enforcement"
    ],
    "Business Engagement": [
        "Stakeholder Alignment",
        "Change Management",
        "Skills & Training",
        "Value Measurement",
        "Business Process Integration",
        "Strategic Planning"
    ]
}

# ---- App Layout ----
st.title("Cloud & Data Maturity Evaluator")
st.markdown("Evaluate technical maturity and generate strategic insights for your organization's cloud transformation journey.")

# ---- Industry Selection ----
industry = st.selectbox("Select Industry", [
    "Healthcare", "Manufacturing", "Financial Services", "Logistic",
    "Retail", "Food and Beverage", "Homebuilding & Real Estate"
])

st.markdown("---")
st.markdown("### Maturity Assessment")
st.markdown("**Scale:** 1 = Greenfield | 2 = Emerging | 3 = Developing | 4 = Established | 5 = Optimized")

# ---- Data Storage for Scores, Comments, Inclusion ----
all_scores = {}
category_comments = {}
category_inclusion = {}

# ---- Category Assessment Interface ----
for category, sub_caps in categories_structure.items():
    with st.expander(f"{category}", expanded=category_inclusion.get(category, True)):
        st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
        include_cat = st.checkbox(f"Include {category} in strategy & roadmap", value=True, key=f"include_{category}")
        category_inclusion[category] = include_cat
        if include_cat:
            cols = st.columns(3)
            sub_scores = {}
            for i, sub_cap in enumerate(sub_caps):
                with cols[i % 3]:
                    score = st.slider(
                        f"{sub_cap}", 
                        1, 5, 3, 
                        key=f"{category}_{sub_cap}",
                        format="Level %d"
                    )
                    st.caption(f"**{levels[score]}**")
                    sub_scores[sub_cap] = score
            category_avg = round(np.mean(list(sub_scores.values())))
            all_scores[category] = {
                'average': category_avg,
                'sub_capabilities': sub_scores
            }
            comment = st.text_area(
                f"Key considerations for {category}:",
                placeholder="Enter specific challenges, priorities, or context for this area...",
                key=f"comment_{category}",
                height=80
            )
            category_comments[category] = comment
        st.markdown("---")

# ---- Overall Thoughts Section ----
st.markdown('<div class="category-header">Additional Context/Technology Preferences</div>', unsafe_allow_html=True)
overall_input = st.text_area(
    "Overall thoughts, requests, pain points, insights, preferred platforms, etc.",
    placeholder="Share any additional context, business needs, technology preferences, or pain points here...",
    key="overall_input",
    height=100
)

# ---- Dynamic Spider Chart Visualization ----
def draw_spider_charts(selected_scores):
    num_selected = len(selected_scores)
    if num_selected == 0:
        st.info("No categories selected for visualization.")
        return
    rows = (num_selected + 2) // 3
    fig, axes = plt.subplots(rows, 3, figsize=(20, 7 * rows), subplot_kw=dict(projection='polar'))
    axes = axes.flatten() if num_selected > 1 else [axes]
    fig.suptitle('Cloud & Data Maturity Assessment - Spider Chart Analysis', fontsize=18, fontweight='bold')
    colors = ['#1976d2', '#42a5f5', '#64b5f6', '#90caf9', '#bbdefb', '#e3f2fd']
    for idx, (category, scores_data) in enumerate(selected_scores.items()):
        ax = axes[idx]
        sub_caps = list(scores_data['sub_capabilities'].keys())
        values = list(scores_data['sub_capabilities'].values())
        N = len(sub_caps)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        values += values[:1]
        ax.plot(angles, values, 'o-', linewidth=3, label=category, color=colors[idx % len(colors)], markersize=8)
        ax.fill(angles, values, alpha=0.25, color=colors[idx % len(colors)])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(sub_caps, fontsize=10, fontweight='bold')
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1\nGreenfield', '2\nEmerging', '3\nDeveloping', '4\nEstablished', '5\nOptimized'], fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_title(f"{category}\nAverage: {scores_data['average']:.1f} ({levels[scores_data['average']]})", fontsize=14, fontweight='bold', pad=20, color='#1565c0')
        for angle, value, sub_cap in zip(angles[:-1], values[:-1], sub_caps):
            ax.annotate(f'{value}', xy=(angle, value), xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold', color='#0d47a1', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    # Hide unused subplots
    for j in range(idx + 1, len(axes)):
        axes[j].axis('off')
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("### Maturity Assessment - Spider Chart Analysis")
selected_scores = {cat: all_scores[cat] for cat in categories_structure if category_inclusion.get(cat)}
draw_spider_charts(selected_scores)

# ---- Roadmap Diagram ----
def extract_success_criteria(roadmap_content):
    phase_pattern = r'(?:^|\n)\s*##\s*(Phase \d+)\s*\(([^)]+)\)\s*([\s\S]*?)(?=\n\s*##|$)'
    matches = re.findall(phase_pattern, roadmap_content)
    results = []
    for phase_num, duration, block in matches:
        # Extract all lines after 'Success criteria and milestones' until next section or phase
        crit_section = re.search(r'Success criteria and milestones\s*:?[\s\n]*([\s\S]*?)(?=\n\s*[A-Z][^\n]*:|\n\s*##|$)', block, re.IGNORECASE)
        crit_items = []
        if crit_section:
            # Only extract lines that start with a dash (bullet points)
            crit_items = [line.strip()[2:] for line in crit_section.group(1).splitlines() if line.strip().startswith('- ')]
        results.append({
            'phase': f'{phase_num} ({duration})',
            'criteria': crit_items if crit_items else ['No success criteria found.']
        })
    return results

def draw_roadmap_diagram(phases):
    # If all phases have no success criteria, use default diagram
    if all(phase['criteria'] == ['No success criteria found.'] for phase in phases):
        default_roadmap_content = """## Phase 1 (0-6 months)
Success criteria and milestones:
- Establish cloud governance
- Set up data quality frameworks
- Initiate AI/ML ethics guidelines

## Phase 2 (6-12 months)
Success criteria and milestones:
- Migrate initial workloads to cloud
- Develop key data pipelines
- Pilot AI/ML models on cloud

## Phase 3 (12-18 months)
Success criteria and milestones:
- Integrate cloud services with on-premises systems
- Optimize data workflows for performance
- Scale AI/ML models to production

## Phase 4 (18+ months)
Success criteria and milestones:
- Continuously monitor and optimize cloud resources
- Enhance data analytics capabilities
- Expand AI/ML initiatives across the organization"""
        phases = extract_success_criteria(default_roadmap_content)
    fig, ax = plt.subplots(figsize=(8, 7))
    colors = ['#e3f2fd', '#f3e5f5', '#e8f5e9', '#fff3e0']
    borders = ['#1976d2', '#7b1fa2', '#388e3c', '#f57c00']
    box_width = 7
    box_height = 1.2
    spacing = 0.5
    y_start = 7.5
    for i, phase in enumerate(phases):
        y_pos = y_start - i * (box_height + spacing)
        color = colors[i % len(colors)]
        border = borders[i % len(borders)]
        rect = patches.FancyBboxPatch(
            (0.7, y_pos), box_width, box_height,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor=border,
            linewidth=3 if i == 0 else 2
        )
        ax.add_patch(rect)
        ax.text(
            0.7 + box_width/2, y_pos + box_height - 0.2,
            phase['phase'],
            ha='center', va='center',
            fontsize=12, fontweight='bold', color=border
        )
        for j, item in enumerate(phase['criteria']):
            ax.text(
                0.7 + box_width/2, y_pos + box_height - 0.5 - j*0.28,
                f"• {item}",
                ha='center', va='center',
                fontsize=10, fontweight='normal', color=border
            )
        if i < len(phases) - 1:
            arrow = patches.FancyArrowPatch(
                (0.7 + box_width/2, y_pos),
                (0.7 + box_width/2, y_pos - spacing + 0.1),
                arrowstyle='->', mutation_scale=13, color='#666666', linewidth=1.2
            )
            ax.add_patch(arrow)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 9)
    ax.set_title('18-Month Strategic Roadmap', fontsize=15, fontweight='bold', pad=25, color='#1565c0')
    ax.axis('off')
    plt.subplots_adjust(top=0.93, bottom=0.03, left=0.05, right=0.95, hspace=0)
    st.pyplot(fig)

# ---- AI Evaluation Button ----
if st.button("Generate AI-Powered Strategic Assessment", type="primary"):
    selected_categories = [cat for cat in categories_structure if category_inclusion.get(cat)]
    filtered_scores = {cat: all_scores[cat] for cat in selected_categories}
    filtered_comments = {cat: category_comments[cat] for cat in selected_categories}
    category_averages = {cat: data['average'] for cat, data in filtered_scores.items()}
    st.markdown("### Strategic Recommendations by Focus Area")
    recommendation_data = []
    with st.spinner("Analyzing maturity levels and generating strategic insights..."):
        for category in selected_categories:
            scores_data = filtered_scores[category]
            avg_level = scores_data['average']
            sub_cap_details = scores_data['sub_capabilities']
            user_comments = filtered_comments.get(category, "")
            prompt = (
                f"You are a senior cloud and data transformation advisor specializing in the {industry} industry. "
                f"Your task is to analyze the maturity assessment for the category '{category}'. "
                f"The overall maturity level is '{levels[avg_level]}' (Level {avg_level}). "
                f"Sub-capability breakdown: {sub_cap_details}. "
                f"Client context and priorities: {user_comments if user_comments else 'No specific context provided'}. "
                f"\n\nAdditional overall context: {overall_input if overall_input else 'No additional context provided.'} "
                f"\n\nBest practices:\n"
                f"- Focus on business value creation and competitive advantage.\n"
                f"- Use clear, actionable recommendations.\n"
                f"- Structure your response as follows:\n"
                f"  1) Executive Summary (2-3 sentences focusing on business impact)\n"
                f"  2) Strategic Priorities (3-4 numbered recommendations with business rationale)\n"
                f"  3) Success Metrics (key indicators of transformation progress)\n"
                f"- Format output with bullet points and numbered lists.\n"
                f"- Align recommendations with {industry} industry best practices.\n"
            )
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800,
                    temperature=0.7
                )
                suggestion_full = response.choices[0].message.content.strip()
                recommendation_data.append({
                    "Area": category,
                    "Level": f"Level {avg_level} ({levels[avg_level]})",
                    "Content": suggestion_full,
                    "Sub_Details": sub_cap_details
                })
            except Exception as e:
                st.error(f"Error generating recommendations for {category}: {str(e)}")
    for item in recommendation_data:
        with st.expander(f"📊 {item['Area']} - {item['Level']}", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(item['Content'])
            with col2:
                st.markdown("**Sub-capability Levels:**")
                for sub_cap, level in item['Sub_Details'].items():
                    st.markdown(f"• {sub_cap}: Level {level}")
    st.markdown("### Strategic 18-Month Transformation Roadmap")
    st.markdown("#### Transformation Journey Overview")
    # Generate roadmap content from context and selected categories
    roadmap_prompt = (
        f"As a strategic transformation advisor for the {industry} industry, create a comprehensive 18-month roadmap "
        f"based on these current maturity levels: {category_averages}. "
        f"Industry context: {industry}. "
        f"Additional overall context: {overall_input if overall_input else 'No additional context provided.'} "
        f"Only include the following categories in your analysis: {', '.join(selected_categories)}. "
        f"Structure the roadmap in 4 phases (0-6 months, 6-12 months, 12-18 months, 18+ months) with: "
        f"- Strategic objectives for each phase "
        f"- Key initiatives and deliverables "
        f"- Success criteria and milestones "
        f"- Resource requirements and investment priorities "
        f"- Risk mitigation strategies "
        f"Focus on business value creation, competitive advantage, and sustainable transformation. "
        f"Consider industry-specific challenges and opportunities in {industry}. "
        f"Use bullet points and numbered lists for clarity."
    )
    try:
        with st.spinner("Generating comprehensive transformation roadmap..."):
            roadmap_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": roadmap_prompt}],
                max_tokens=1200,
                temperature=0.7
            )
            roadmap_content = roadmap_response.choices[0].message.content
            st.markdown("#### Detailed Implementation Plan")
            st.markdown(roadmap_content)
            st.markdown("#### 18-Month Strategic Roadmap Diagram")
            phases = extract_success_criteria(roadmap_content)
            draw_roadmap_diagram(phases)
    except Exception as e:
        st.error(f"Error generating roadmap: {str(e)}")
        # Fallback to default roadmap diagram
        st.markdown("#### 18-Month Strategic Roadmap Diagram (Default)")
        default_roadmap_content = "## Phase 1: Foundation (0-6 months)\n- Establish cloud governance\n- Set up data quality frameworks\n- Initiate AI/ML ethics guidelines\n\n## Phase 2: Development (6-12 months)\n- Migrate initial workloads to cloud\n- Develop key data pipelines\n- Pilot AI/ML models on cloud\n\n## Phase 3: Integration (12-18 months)\n- Integrate cloud services with on-premises systems\n- Optimize data workflows for performance\n- Scale AI/ML models to production\n\n## Phase 4: Optimization (18+ months)\n- Continuously monitor and optimize cloud resources\n- Enhance data analytics capabilities\n- Expand AI/ML initiatives across the organization"
        phases = extract_success_criteria(default_roadmap_content)
        draw_roadmap_diagram(phases)
    st.markdown("### Key Strategic Insights")
    high_maturity = [cat for cat, data in filtered_scores.items() if data['average'] >= 3]
    low_maturity = [cat for cat, data in filtered_scores.items() if data['average'] <= 2]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Maturity", f"{np.mean([data['average'] for data in filtered_scores.values()]):.1f}")
    with col2:
        st.metric("Strength Areas", len(high_maturity))
        if high_maturity:
            st.caption(", ".join(high_maturity))
    with col3:
        st.metric("Priority Areas", len(low_maturity))
        if low_maturity:
            st.caption(", ".join(low_maturity))
st.markdown("---")
