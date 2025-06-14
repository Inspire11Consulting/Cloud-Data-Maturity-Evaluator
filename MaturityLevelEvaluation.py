import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------
# Define categories and options
# ----------------------------
categories = [
    "Cloud Architecture",
    "Data Management",
    "Analytics",
    "AI/ML Integration",
    "Governance & Security",
    "Business Enablement"
]

levels = {
    1: "Nascent",
    2: "Emerging",
    3: "Developing",
    4: "Established",
    5: "Optimized"
}

recommendations = {
    1: "Start with foundational strategy. Set up cloud landing zone and basic data ingestion.",
    2: "Introduce standard tools and platforms like Power BI and Azure Data Factory.",
    3: "Modernize architecture. Implement lakehouse and initial predictive models.",
    4: "Integrate AI/ML into operations. Automate governance and scale self-service BI.",
    5: "Optimize with GenAI and real-time analytics. Run AI CoE and performance tracking."
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Client Cloud & Data Maturity Assessment")

st.markdown("### Select maturity levels for each area")
scores = {}
for cat in categories:
    scores[cat] = st.slider(cat, 1, 5, 3)

st.markdown("---")
st.markdown("### Heatmap of Maturity Levels")

# ----------------------------
# Heatmap
# ----------------------------
df = pd.DataFrame(scores.items(), columns=["Area", "Level"])
df_pivot = df.set_index("Area").T

fig, ax = plt.subplots(figsize=(10, 1.5))
sns.heatmap(df_pivot, annot=True, cmap="YlOrRd", cbar=False, linewidths=1, xticklabels=True, yticklabels=False)
st.pyplot(fig)

# ----------------------------
# Recommendations Table
# ----------------------------
st.markdown("### Recommendations")
for area, level in scores.items():
    st.markdown(f"**{area}** ({levels[level]}): {recommendations[level]}")

# ----------------------------
# Roadmap Suggestion
# ----------------------------
st.markdown("---")
st.markdown("### Suggested Roadmap")

st.markdown("""
**0–3 months (Foundation):** Set priorities, unify key data, implement lakehouse foundation.

**3–6 months (Adoption):** Build dashboards, initial ML pilots, deploy governance policies.

**6–12 months (Expansion):** Scale AI/ML use cases, enable citizen dev, integrate Purview.

**12–18 months (Optimization):** Real-time pipelines, GenAI chatbots, AI-driven ops.
""")
