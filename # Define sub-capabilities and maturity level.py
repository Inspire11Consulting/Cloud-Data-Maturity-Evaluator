# Define four sub-capabilities per category, each with 5 levels of maturity
maturity_subitems = {
    "Cloud Architecture": {
        "Infra Modernization": {
            1: "Mostly on-premises, limited virtualization",
            2: "Initial cloud migration (IaaS)",
            3: "Landing zone setup, basic PaaS",
            4: "Hybrid cloud, containerization",
            5: "Cloud-native, serverless, autoscaling"
        },
        "Cloud Ops & DevSecOps": {
            1: "Manual deployment, no CI/CD",
            2: "Scripted deployments, basic automation",
            3: "CI/CD pipelines, IaC introduced",
            4: "DevSecOps practices integrated",
            5: "Full GitOps, policy-as-code, drift remediation"
        },
        "Scalability & Resilience": {
            1: "Single instance, manual scaling",
            2: "Basic autoscale groups",
            3: "Load balanced services",
            4: "Multi-region failover",
            5: "Self-healing distributed architecture"
        },
        "Cost Optimization": {
            1: "No cost visibility",
            2: "Manual cost tracking",
            3: "Budgets and tags used",
            4: "Automated cost governance",
            5: "Continuous cost optimization (FinOps)"
        }
    },
    "Data Management": {
        "Ingestion & Integration": {
            1: "Manual Excel uploads",
            2: "Flat file imports, no scheduling",
            3: "Scheduled ETL/ELT pipelines",
            4: "Streaming ingestion + CDC",
            5: "Event-driven ingestion with automation"
        },
        "Storage Architecture": {
            1: "On-prem DBs & file shares",
            2: "Cloud blob storage or SQL DW",
            3: "Lakehouse architecture adopted",
            4: "Multi-zone, governed layers",
            5: "Federated data mesh with catalog"
        },
        "Metadata & Cataloging": {
            1: "No catalog or glossary",
            2: "Excel-based definitions",
            3: "Automated scanning (Purview pilot)",
            4: "Role-based catalog and lineage",
            5: "Fully automated cataloging and policies"
        },
        "Data Quality & Stewardship": {
            1: "No defined data quality checks",
            2: "Manual DQ in Excel/SQL",
            3: "Rules implemented in pipelines",
            4: "DQ dashboards and scorecards",
            5: "Proactive DQ alerts and steward accountability"
        }
    }
    # Other categories (Analytics, AI/ML Integration, etc.) will be added similarly
}

maturity_subitems.keys()


# Define sub-capabilities and maturity levels for all six categories
maturity_subitems.update({
    
    "Analytics": {
        "Reporting Maturity": {
            1: "Manual reports in Excel",
            2: "Basic dashboards in Power BI/Tableau",
            3: "Shared semantic models and curated metrics",
            4: "Predictive analytics and drill-downs",
            5: "Prescriptive analytics with scenario planning"
        },
        "Data Literacy & Access": {
            1: "Limited access to data tools",
            2: "Basic training and self-service portals",
            3: "Active internal communities of practice",
            4: "Formal training programs, certifications",
            5: "Data culture embedded across all roles"
        },
        "Business KPI Alignment": {
            1: "Disconnected KPIs",
            2: "Initial standardization",
            3: "Centrally managed KPI library",
            4: "Live metric governance and owner model",
            5: "Real-time business scorecards with action plans"
        },
        "Data Visualization & UX": {
            1: "Raw tables, text-heavy charts",
            2: "Basic bar/pie visuals",
            3: "Interactive and mobile-optimized",
            4: "User-customizable views and filters",
            5: "AI-assisted storyboards and anomaly highlighting"
        }
    },
    "AI/ML Integration": {
        "ML Use Case Coverage": {
            1: "No use cases identified",
            2: "1–2 pilot projects",
            3: "Multiple use cases across departments",
            4: "ML integrated into key workflows",
            5: "Broad GenAI + edge AI applications"
        },
        "Model Lifecycle Mgmt": {
            1: "No model mgmt process",
            2: "Manual retraining on demand",
            3: "Basic MLOps pipeline",
            4: "CI/CD for models, versioning",
            5: "Auto-monitoring, retraining, rollback"
        },
        "AI Governance & Ethics": {
            1: "No AI standards or principles",
            2: "Initial ethics checklist",
            3: "Approved use case registry",
            4: "AI ethics board and compliance rules",
            5: "Continuous audits + responsible AI dashboard"
        },
        "Tooling & Skills": {
            1: "Limited Python or modeling experience",
            2: "Training data scientists, building labs",
            3: "Cross-functional AI/BI squads",
            4: "Data + software engineering blended",
            5: "Distributed AI champions + innovation hubs"
        }
    },
    "Governance & Security": {
        "Access Control": {
            1: "Manual permissions",
            2: "RBAC/MFA adopted",
            3: "Centralized IAM policies",
            4: "Attribute-based access control",
            5: "Policy-as-code with automation"
        },
        "Data Privacy & Classification": {
            1: "No classification framework",
            2: "Manual tagging and spreadsheets",
            3: "Automated scanning and labels",
            4: "Integrated DLP + data zones",
            5: "Proactive risk alerts and remediations"
        },
        "Auditability & Lineage": {
            1: "No lineage tracking",
            2: "Manual mapping for key flows",
            3: "Basic visual lineage in catalog",
            4: "End-to-end automated lineage",
            5: "Automated anomaly detection in data flows"
        },
        "Governance Operating Model": {
            1: "No council or governance roles",
            2: "Informal working group",
            3: "Governance committee chartered",
            4: "Business and IT co-ownership",
            5: "Governed product teams with mandates"
        }
    },
    "Business Engagement": {
        "Citizen Development": {
            1: "All work goes through IT",
            2: "Initial Power BI/Power Apps users",
            3: "Business building their own tools",
            4: "Certified citizen developers & fusion teams",
            5: "Business-led innovation pods"
        },
        "Data Ownership Model": {
            1: "Central IT owns all data",
            2: "BU-specific shadow databases",
            3: "Data stewards nominated per domain",
            4: "Data product owners embedded in BUs",
            5: "Fully federated data ownership with funding"
        },
        "Change Enablement & Comms": {
            1: "One-time launch emails only",
            2: "Periodic newsletters",
            3: "Community champions & trainings",
            4: "Embedded onboarding & playbooks",
            5: "Gamified adoption campaigns + incentive plans"
        },
        "Collaboration & Feedback": {
            1: "No user feedback captured",
            2: "Survey after rollout",
            3: "User groups and forums live",
            4: "Monthly roadmap reviews with users",
            5: "Feedback-driven backlog and feature roadmap"
        }
    }
})

len(maturity_subitems)  # Confirm all 6 categories are fully defined with 4 sub-capabilities each
