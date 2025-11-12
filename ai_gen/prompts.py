"""
Prompt templates and generation schemas for AI assessments.
"""

GENERATION_SCHEMA = """
You are an experienced CTO advisor. Return ONLY valid JSON that exactly follows this structure (no explanatory text, no markdown fences):

{
  "executive": {
    "summary": "2-3 sentence summary",
    "recommendation": "2+ sentence justification",
    "activities": ["Activity 1", "Activity 2", "..."],
    "focus_8w": ["Sprint1 item", "Sprint2 item", "..."],
    "plan_3y": ["Year1 item", "Year2 item", "..."],
    "assumptions": ["Assumption 1", "..."]
  },
  "technical": {
    "summary": "2-3 sentence summary",
    "recommendation": "2+ sentence technical justification",
    "activities": ["Tactic 1", "Tactic 2", "..."],
    "focus_8w": ["Sprint-level technical task", "..."],
    "plan_3y": ["Year1 technical plan", "..."],
    "assumptions": ["Assumption A", "..."],
    "team": ["Role: count", "..."]
  }
}

Make sure:
- All keys are double quoted.
- All lists are JSON arrays.
- Keep entries concise.
- Use the inputs below for context.
"""

CONSOLIDATION_SCHEMA = """
You are a CTO. Consolidate these category-level fragments into ONE JSON roadmap. Return ONLY JSON matching this structure:

{
  "focus_8w": {
    "sprint1": ["..."],
    "sprint2": ["..."],
    "sprint3": ["..."],
    "sprint4": ["..."]
  },
  "plan_3y": {
    "year1": ["..."],
    "year2": ["..."],
    "year3": ["..."]
  }
}
"""


def build_category_assessment_prompt(
    industry,
    company_size,
    it_size,
    uses_cloud,
    cloud_platform,
    priority_projects,
    category,
    include_flag,
    avg_maturity,
    sub_capability_scores,
    category_comments,
    overall_context,
    seed_scenario_text
):
    """
    Build a detailed prompt for category assessment.
    
    Args:
        industry: Company industry
        company_size: Company size description
        it_size: IT department size
        uses_cloud: Whether company uses cloud
        cloud_platform: Cloud platform(s) used
        priority_projects: Priority projects description
        category: Category name being assessed
        include_flag: Whether category is included
        avg_maturity: Average maturity score
        sub_capability_scores: Dict of sub-capability scores
        category_comments: Comments for the category
        overall_context: Overall context/constraints
        seed_scenario_text: Optional seed scenario text
    
    Returns:
        str: Complete prompt for AI assessment
    """
    import json
    
    prompt = GENERATION_SCHEMA + f"""

Context:
Industry: {industry}
Company size: {company_size}
IT department size: {it_size}
Uses cloud: {uses_cloud} {cloud_platform}
Priority projects: {priority_projects if priority_projects else 'None'}
Category: {category}
Included flag: {'Yes' if include_flag else 'No'}
Category maturity average (if included): {avg_maturity if include_flag else 'N/A'}
Sub-capability scores: {json.dumps(sub_capability_scores)}
Category comments: {category_comments if category_comments else 'None'}
Overall context: {overall_context if overall_context else 'None'}
Seed scenario: {seed_scenario_text if seed_scenario_text else 'None'}

Return the JSON only, exactly matching the schema at the top.
"""
    return prompt


def build_consolidation_prompt(category_fragments):
    """
    Build a prompt for consolidating roadmap fragments.
    
    Args:
        category_fragments: List of category fragments with focus_8w and plan_3y
    
    Returns:
        str: Complete prompt for consolidation
    """
    import json
    
    prompt = CONSOLIDATION_SCHEMA + f"""

Category fragments:
{json.dumps(category_fragments, indent=2)}

Distribute initiatives sensibly across sprints and years. Return JSON only.
"""
    return prompt

