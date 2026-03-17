"""
Shared schema/constants for the Data & AI Maturity Tool.

This module is intentionally UI-agnostic so it can be used by the API backend
and any future clients (e.g., React).
"""

from __future__ import annotations

# Categories Structure (moved from the Streamlit app)
CATEGORIES_STRUCTURE: dict[str, list[str]] = {
    "Cloud Architecture": [
        "Infrastructure Design",
        "Scalability & Performance",
        "Multi-cloud Strategy",
        "Cost Optimization",
        "Disaster Recovery",
        "Service Architecture",
    ],
    "Data Management": [
        "Data Quality",
        "Data Integration",
        "Master Data Management",
        "Data Lifecycle",
        "Data Storage Strategy",
        "Real-time Processing",
    ],
    "Data Visualization & Insights": [
        "Dashboard Design",
        "Data Storytelling",
        "Interactive Visualizations",
        "Advanced Analytics Techniques",
        "Self-Service Analytics",
        "Insight Communication",
    ],
    "AI/ML Integration": [
        "Model Development",
        "MLOps & Deployment",
        "AI Ethics & Bias",
        "Business Integration",
        "AutoML Capabilities",
        "AI Governance",
    ],
    "Governance & Security": [
        "Data Privacy",
        "Compliance Management",
        "Access Controls",
        "Risk Management",
        "Audit & Monitoring",
        "Policy Enforcement",
    ],
    "Business Engagement": [
        "Stakeholder Alignment",
        "Change Management",
        "Skills & Training",
        "Value Measurement",
        "Business Process Integration",
        "Strategic Planning",
    ],
}

# Maturity Levels (1-5)
MATURITY_LEVELS: dict[int, str] = {
    1: "Greenfield",
    2: "Emerging",
    3: "Developing",
    4: "Established",
    5: "Optimized",
}

