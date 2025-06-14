import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from openai import OpenAI

# ---- Set your OpenAI key ----
api_key = "sk-APIKey"
client = OpenAI(api_key=api_key)

# ---- Maturity Labels ----
levels = {
    1: "Nascent",
    2: "Emerging",
    3: "Developing",
    4: "Established",
    5: "Optimized"
}

# ---- App Layout ----
st.set_page_config(page_title="Cloud & AI Maturity")
st.title("Cloud & Data Maturity Heatmap + AI Insights")
st.markdown("Evaluate maturity and generate an AI-powered roadmap for your industry.")

# ---- Industry and Inputs ----
industry = st.selectbox("Select Industry", [
    "Homebuilding & Real Estate", "Healthcare", "Manufacturing", "Retail", "Financial Services"
])

st.markdown("### Select Maturity Levels")
st.markdown("1 = Nascent; 2 = Emerging; 3 = Developing; 4 = Established; 5 = Optimized")

categories = [
    "Cloud Architecture", "Data Management", "Analytics",
    "AI/ML Integration", "Governance & Security", "Business Engagement"
]

scores = {}
for cat in categories:
    col1, col2 = st.columns([4, 1])
    with col1:
        score = st.slider(f"{cat}", 1, 5, 3, format="%d", key=cat)
    with col2:
        st.markdown(f"**{levels[score]}**", unsafe_allow_html=True)
    scores[cat] = score

# ---- Heatmap ----
def draw_cube_heatmap(scores):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(0, len(scores))
    ax.set_ylim(0, 1)
    ax.axis('off')

    color_map = {
        1: "#d6e4f0",  # Light Blue
        2: "#a9c9e2",
        3: "#78abd5",
        4: "#4f90c6",
        5: "#2d72b8"   # Deep Blue
    }

    for i, (category, level) in enumerate(scores.items()):
        rect = patches.Rectangle((i, 0), 1, 1, linewidth=1, edgecolor='white', facecolor=color_map[level])
        ax.add_patch(rect)
        ax.text(i + 0.5, 0.75, category, ha='center', va='center', fontsize=8, wrap=True)
        ax.text(i + 0.5, 0.25, f"Level {level}\n({levels[level]})", ha='center', va='center', fontsize=8, color='black')

    st.pyplot(fig)

st.markdown("### Maturity Heatmap")
draw_cube_heatmap(scores)

# ---- Evaluate Button ----
if st.button("Evaluate with AI"):
    st.markdown("### AI-Powered Recommendations by Area")
    recommendation_data = []

    for area, level in scores.items():
        prompt = (
            f"You are a senior cloud and data consultant in the {industry} industry. "
            f"The maturity level for '{area}' is '{levels[level]}'. "
            f"Provide strategic and practical recommendations tailored to this industry and maturity level. "
            f"Start with a concise executive summary, followed by 3–5 numbered recommendations. "
            f"End with a conclusion starting with 'By following these recommendations...'"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        suggestion_full = response.choices[0].message.content.strip()

        lines = suggestion_full.strip().splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        summary_line = lines[0]
        conclusion_line = ""
        recommendation_lines = []

        for line in lines[1:]:
            if line.startswith("By following"):
                conclusion_line = line
            elif line[0].isdigit() or line.startswith("-"):
                recommendation_lines.append(line)

        recommendation_data.append({
            "Area": area,
            "Level": levels[level],
            "Summary": summary_line,
            "Steps": recommendation_lines,
            "Conclusion": conclusion_line
        })

    # ---- Render Results ----
    for item in recommendation_data:
        st.markdown(f"### {item['Area']} ({item['Level']})")
        st.markdown(f"{item['Summary']}")

        if item['Steps']:
            st.markdown("Recommendations:")
            steps_df = pd.DataFrame({
                "Step": [i + 1 for i in range(len(item['Steps']))],
                "Action": item["Steps"]
            })
            st.dataframe(steps_df, use_container_width=True)

        if item["Conclusion"]:
            st.markdown(f"Final Thought: _{item['Conclusion']}_")



    # ---- Roadmap v1----
    st.markdown("### 18-Month AI Roadmap")
    roadmap_prompt = (
        f"Act as a cloud and AI strategy advisor for a {industry} firm. "
        f"Based on the maturity levels: {scores}, generate a phased 18-month roadmap with specific cloud, data, and AI initiatives."
    )
    roadmap_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": roadmap_prompt}]
    )
    roadmap = roadmap_response.choices[0].message.content
    st.markdown(roadmap)



# # ---- Roadmap v2 ----
# st.markdown("### AI-Suggested Roadmap (0–18 months)")
# roadmap_prompt = (
#     f"Act as a digital strategy advisor for a {industry} firm. "
#     f"Based on the following maturity scores: {scores}, create a short phased roadmap (0–18 months) "
#     f"for cloud and AI transformation including key initiatives per phase."
# )
# messages = [{"role": "user", "content": roadmap_prompt}]
# response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
# roadmap = response.choices[0].message.content
# st.write(roadmap)

# # ---- Visual Roadmap Arrows ----
# def draw_roadmap_arrow_diagram():
#     phases = [
#         ("Modernize\nData Estate", "Near-Term"),
#         ("Deploy AI\nUse Cases", "6–12 Months"),
#         ("Pilot\nGenerative AI", "12–18 Months"),
#         ("Establish\nAI CoE", "18+ Months")
#     ]
#     fig, ax = plt.subplots(figsize=(4, 6))
#     arrow_colors = ["#dce4f7", "#b2c5ea", "#8da8dc", "#5e84cc"]
#     for i, (text, phase) in enumerate(reversed(phases)):
#         ypos = i * 1.2
#         ax.arrow(0.5, ypos, 0, 0.9, width=0.25, head_width=0.35, head_length=0.3,
#                  length_includes_head=True, color=arrow_colors[i], zorder=2)
#         ax.text(0.5, ypos + 0.45, f"{text}\n({phase})", ha='center', va='center', fontsize=10, weight='bold', color='black')
#     ax.set_xlim(0, 1)
#     ax.set_ylim(0, len(phases) * 1.2)
#     ax.axis('off')
#     st.markdown("### Roadmap for Closing Gaps")
#     st.pyplot(fig)

# draw_roadmap_arrow_diagram()
