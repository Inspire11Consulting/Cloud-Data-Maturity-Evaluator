"""
Business logic for assessment calculations and data processing.
"""

import numpy as np
from typing import Dict, List


def calculate_category_average(scores: Dict[str, int]) -> float:
    """
    Calculate average maturity score for a category.
    
    Args:
        scores: Dictionary of sub-capability scores
    
    Returns:
        float: Average score rounded to 1 decimal place
    """
    if not scores:
        return 0.0
    return round(np.mean(list(scores.values())), 1)


def get_included_categories(assessments: Dict, category_inclusion: Dict, category_comments: Dict) -> List[str]:
    """
    Get list of categories that are included in assessment.
    A category is included if:
    - The include checkbox is checked, OR
    - There is a comment present
    
    Args:
        assessments: Dictionary of all assessments
        category_inclusion: Dictionary mapping category to inclusion flag
        category_comments: Dictionary mapping category to comments
    
    Returns:
        List[str]: List of category names to process
    """
    return [
        cat for cat in assessments.keys()
        if category_inclusion.get(cat, False) or (category_comments.get(cat, "").strip() != "")
    ]


def process_scores(categories_structure: Dict, all_scores: Dict) -> Dict:
    """
    Process scores for all categories and calculate averages.
    
    Args:
        categories_structure: Structure of categories and sub-capabilities
        all_scores: Dictionary of scores by category
    
    Returns:
        Dict: Processed scores with averages
    """
    processed = {}
    for category, sub_caps in categories_structure.items():
        sub_scores = all_scores.get(category, {}).get("sub_capabilities", {})
        avg = calculate_category_average(sub_scores)
        processed[category] = {
            "average": avg,
            "sub_capabilities": sub_scores
        }
    return processed

