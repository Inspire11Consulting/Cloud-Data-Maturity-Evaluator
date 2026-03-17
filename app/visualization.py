"""
Visualization functions for charts, diagrams, and heatmaps.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_8week_roadmap_figure(focus_dict):
    """
    Draw 8-week roadmap diagram.
    
    Args:
        focus_dict: Dictionary with sprint1, sprint2, sprint3, sprint4 keys
    
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    for i, sprint in enumerate(["sprint1", "sprint2", "sprint3", "sprint4"]):
        x = i
        items = focus_dict.get(sprint, [])
        if isinstance(items, str):
            items = [items]
        lines = [f"• {it}" for it in items] if items else ["(no items)"]
        text = f"Sprint {i+1}\n" + "\n".join(lines)
        ax.add_patch(
            patches.FancyBboxPatch(
                (x + 0.05, 0.05), 0.9, 0.9,
                boxstyle="round,pad=0.02",
                facecolor="#e3f2fd",
                edgecolor="#1976d2"
            )
        )
        ax.text(x + 0.08, 0.5, text, ha="left", va="center", fontsize=8, wrap=True)
    
    plt.tight_layout()
    return fig


def draw_3year_roadmap_figure(plan_dict):
    """
    Draw 3-year roadmap diagram.
    
    Args:
        plan_dict: Dictionary with year1, year2, year3 keys
    
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    for i, year in enumerate(["year1", "year2", "year3"]):
        x = i
        items = plan_dict.get(year, [])
        if isinstance(items, str):
            items = [items]
        lines = [f"• {it}" for it in items] if items else ["(no items)"]
        text = f"Year {i+1}\n" + "\n".join(lines)
        ax.add_patch(
            patches.FancyBboxPatch(
                (x + 0.05, 0.05), 0.9, 0.9,
                boxstyle="round,pad=0.02",
                facecolor="#e8f5e9",
                edgecolor="#2e7d32"
            )
        )
        ax.text(x + 0.08, 0.5, text, ha="left", va="center", fontsize=8, wrap=True)
    
    plt.tight_layout()
    return fig

