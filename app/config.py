"""
App configuration for Streamlit UI: constants, styling, and default values.
"""

# Maturity Levels
MATURITY_LEVELS = {
    1: "Greenfield",
    2: "Emerging",
    3: "Developing",
    4: "Established",
    5: "Optimized"
}

# Categories Structure
CATEGORIES_STRUCTURE = {
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

# Streamlit Styling
STREAMLIT_CSS = """
<style>
  .category-header { background: linear-gradient(90deg,#1976d2,#42a5f5); color:white; padding:6px; border-radius:6px; font-weight:700; margin-bottom:6px; }
  div.stButton > button, div.stDownloadButton > button {
    background-color: #1976d2 !important;
    color: white !important;
    border-radius: 6px !important;
    padding: 8px 14px !important;
    font-weight: 600 !important;
  }
  div.stButton > button:hover, div.stDownloadButton > button:hover {
    background-color: #1565c0 !important;
    color: white !important;
  }
</style>
"""

# App Configuration
APP_TITLE = "Cloud & Data Maturity Evaluator"
APP_PAGE_TITLE = "Cloud & AI Maturity Evaluator"
APP_DESCRIPTION = "Assess maturity, generate executive & technical guidance, and produce baseball-card project summaries and a consolidated roadmap."

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

