import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from openai import OpenAI

# ---- App Configuration (MUST BE FIRST) ----
st.set_page_config(page_title="Cloud & AI Maturity", layout="wide")

# ---- Set your OpenAI key ----
api_key = "sk-APIKey"  # Replace with your actual API key
client = OpenAI(api_key=api_key)

# ---- Custom CSS for professional blue theme ----
st.markdown("""
<style>    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        color: #000000 !important;  
        border: none !important;      
        #border: 2px solid #2196f3;
        #border-radius: 5px;
    }
    
    /* Category header styling */
    .category-header {
        background: linear-gradient(90deg, #1976d2, #42a5f5);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    
    /* Button styling - blue theme */
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
    
    
    /* Caption styling for maturity level labels */
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

# ---- Define Categories and Sub-capabilities (6 per category) ----
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
    "Analytics": [
        "Descriptive Analytics",
        "Diagnostic Analytics", 
        "Predictive Analytics",
        "Prescriptive Analytics",
        "Self-Service Analytics",
        "Advanced Visualization"
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

# ---- Data Storage for Scores and Comments ----
all_scores = {}
category_comments = {}

# ---- Category Assessment Interface ----
for category, sub_caps in categories_structure.items():
    st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
    
    # Create columns for sub-capabilities (3 columns for 6 items)
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
    
    # Calculate category average
    category_avg = round(np.mean(list(sub_scores.values())))
    all_scores[category] = {
        'average': category_avg,
        'sub_capabilities': sub_scores
    }
    
    # Add comment textbox for each category
    comment = st.text_area(
        f"Key considerations for {category}:",
        placeholder="Enter specific challenges, priorities, or context for this area...",
        key=f"comment_{category}",
        height=80
    )
    category_comments[category] = comment
    
    st.markdown("---")

# ---- Spider Chart Visualization for Each Category ----
def draw_spider_charts(all_scores):
    fig, axes = plt.subplots(2, 3, figsize=(20, 14), subplot_kw=dict(projection='polar'))
    fig.suptitle('Cloud & Data Maturity Assessment - Spider Chart Analysis', fontsize=18, fontweight='bold')
    
    categories = list(all_scores.keys())
    
    # Professional blue color scheme for spider charts
    colors = ['#1976d2', '#42a5f5', '#64b5f6', '#90caf9', '#bbdefb', '#e3f2fd']
    
    for idx, (category, scores_data) in enumerate(all_scores.items()):
        row, col = divmod(idx, 3)
        ax = axes[row, col]
        
        # Get sub-capability data
        sub_caps = list(scores_data['sub_capabilities'].keys())
        values = list(scores_data['sub_capabilities'].values())
        
        # Number of variables
        N = len(sub_caps)
        
        # Angles for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        # Values for plotting
        values += values[:1]  # Complete the circle
        
        # Plot the spider chart
        ax.plot(angles, values, 'o-', linewidth=3, label=category, color='#1976d2', markersize=8)
        ax.fill(angles, values, alpha=0.25, color='#1976d2')
        
        # Add labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(sub_caps, fontsize=10, fontweight='bold')
        
        # Set y-axis limits and labels
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1\nGreenfield', '2\nEmerging', '3\nDeveloping', '4\nEstablished', '5\nOptimized'], 
                          fontsize=8)
        
        # Add gridlines
        ax.grid(True, alpha=0.3)
        
        # Category title with average
        ax.set_title(f"{category}\nAverage: {scores_data['average']:.1f} ({levels[scores_data['average']]})", 
                    fontsize=14, fontweight='bold', pad=20, color='#1565c0')
        
        # Add value labels on the chart
        for angle, value, sub_cap in zip(angles[:-1], values[:-1], sub_caps):
            ax.annotate(f'{value}', 
                       xy=(angle, value), 
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=9, 
                       fontweight='bold',
                       color='#0d47a1',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    # Hide empty subplot if odd number of categories
    if len(categories) % 2 != 0:
        axes[1, 2].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)

# ---- Display Spider Chart Visualization ----
st.markdown("### Maturity Assessment - Spider Chart Analysis")
draw_spider_charts(all_scores)

# ---- Create Roadmap Diagram ----
def draw_roadmap_diagram():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Define phases
    phases = [
        {
            'name': 'Foundation\n(0-6 months)',
            'color': '#e3f2fd',
            'border': '#1976d2',
            'items': ['Infrastructure Assessment', 'Data Quality Baseline', 'Governance Framework']
        },
        {
            'name': 'Development\n(6-12 months)', 
            'color': '#f3e5f5',
            'border': '#7b1fa2',
            'items': ['Cloud Migration', 'Analytics Platform', 'Initial AI Pilots']
        },
        {
            'name': 'Integration\n(12-18 months)',
            'color': '#e8f5e8', 
            'border': '#388e3c',
            'items': ['Advanced Analytics', 'ML Operations', 'Business Integration']
        },
        {
            'name': 'Optimization\n(18+ months)',
            'color': '#fff3e0',
            'border': '#f57c00', 
            'items': ['AI Excellence', 'Continuous Innovation', 'Strategic Advantage']
        }
    ]
    
    # Draw phases as connected boxes
    box_width = 3
    box_height = 2
    spacing = 1
    
    for i, phase in enumerate(phases):
        x_pos = i * (box_width + spacing)
        
        # Main phase box
        rect = patches.FancyBboxPatch(
            (x_pos, 2), box_width, box_height,
            boxstyle="round,pad=0.1",
            facecolor=phase['color'],
            edgecolor=phase['border'],
            linewidth=2
        )
        ax.add_patch(rect)
        
        # Phase title
        ax.text(x_pos + box_width/2, 3.5, phase['name'], 
               ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Phase items
        for j, item in enumerate(phase['items']):
            ax.text(x_pos + box_width/2, 2.8 - j*0.3, f"• {item}", 
                   ha='center', va='center', fontsize=9)
        
        # Arrow to next phase
        if i < len(phases) - 1:
            arrow = patches.FancyArrowPatch(
                (x_pos + box_width, 3),
                (x_pos + box_width + spacing, 3),
                arrowstyle='->',
                mutation_scale=20,
                color='#666666'
            )
            ax.add_patch(arrow)
    
    ax.set_xlim(-0.5, len(phases) * (box_width + spacing))
    ax.set_ylim(1, 5)
    ax.set_title('18-Month Strategic Roadmap', fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)

# ---- AI Evaluation Button ----
if st.button("Generate AI-Powered Strategic Assessment", type="primary"):
    
    # Calculate overall scores for context
    category_averages = {cat: data['average'] for cat, data in all_scores.items()}
    
    st.markdown("### Strategic Recommendations by Focus Area")
    
    recommendation_data = []
    
    with st.spinner("Analyzing maturity levels and generating strategic insights..."):
        
        for category, scores_data in all_scores.items():
            avg_level = scores_data['average']
            sub_cap_details = scores_data['sub_capabilities']
            user_comments = category_comments.get(category, "")
            
            # Enhanced prompt for better business-focused recommendations
            prompt = (
                f"You are a senior cloud and data transformation advisor specializing in the {industry} industry. "
                f"Analyze the maturity assessment for '{category}' where the overall level is '{levels[avg_level]}' (Level {avg_level}). "
                f"Sub-capability breakdown: {sub_cap_details}. "
                f"Client context and priorities: {user_comments if user_comments else 'No specific context provided'}. "
                f"Provide strategic recommendations that focus on business value creation and competitive advantage. "
                f"Format your response with: "
                f"1) Executive Summary (2-3 sentences focusing on business impact) "
                f"2) Strategic Priorities (3-4 numbered recommendations with business rationale) "
                f"3) Success Metrics (key indicators of transformation progress) "
                f"Ensure recommendations are practical and aligned with {industry} industry best practices."
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
    
    # Display recommendations in organized format
    for item in recommendation_data:
        with st.expander(f"📊 {item['Area']} - {item['Level']}", expanded=True):
            
            # Show sub-capability breakdown
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(item['Content'])
            
            with col2:
                st.markdown("**Sub-capability Levels:**")
                for sub_cap, level in item['Sub_Details'].items():
                    st.markdown(f"• {sub_cap}: Level {level}")
    
    # Generate comprehensive roadmap
    st.markdown("### Strategic 18-Month Transformation Roadmap")
    
    # Visual roadmap diagram
    st.markdown("#### Transformation Journey Overview")
    draw_roadmap_diagram()
    
    # Detailed roadmap text
    st.markdown("#### Detailed Implementation Plan")
    
    roadmap_prompt = (
        f"As a strategic transformation advisor for the {industry} industry, create a comprehensive 18-month roadmap "
        f"based on these current maturity levels: {category_averages}. "
        f"Industry context: {industry}. "
        f"Structure the roadmap in 4 phases (0-6 months, 6-12 months, 12-18 months, 18+ months) with: "
        f"- Strategic objectives for each phase "
        f"- Key initiatives and deliverables "
        f"- Success criteria and milestones "
        f"- Resource requirements and investment priorities "
        f"- Risk mitigation strategies "
        f"Focus on business value creation, competitive advantage, and sustainable transformation. "
        f"Consider industry-specific challenges and opportunities in {industry}."
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
            
            st.markdown(roadmap_content)
            
    except Exception as e:
        st.error(f"Error generating roadmap: {str(e)}")
    
    # Summary insights
    st.markdown("### Key Strategic Insights")
    
    # Calculate insights
    high_maturity = [cat for cat, data in all_scores.items() if data['average'] >= 4]
    low_maturity = [cat for cat, data in all_scores.items() if data['average'] <= 2]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Maturity", f"{np.mean([data['average'] for data in all_scores.values()]):.1f}")
    
    with col2:
        st.metric("Strength Areas", len(high_maturity))
        if high_maturity:
            st.caption(", ".join(high_maturity))
    
    with col3:
        st.metric("Priority Areas", len(low_maturity))
        if low_maturity:
            st.caption(", ".join(low_maturity))

# ---- Footer ----
st.markdown("---")
