"""
PowerPoint export functionality.
"""

from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from ai_gen.data_normalizer import get_field


def add_wrapped_paragraph(frame, text, font_size=11, bold=False, level=0):
    """
    Add a wrapped paragraph to a text frame.
    
    Args:
        frame: PowerPoint text frame
        text: Text content
        font_size: Font size in points
        bold: Whether text is bold
        level: Paragraph level (for indentation)
    
    Returns:
        Paragraph object
    """
    p = frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.level = level
    p.word_wrap = True
    return p


def export_to_pptx(consolidated, fig1, fig2, rec_data):
    """
    Export consolidated roadmap and baseball cards to PowerPoint.
    
    Args:
        consolidated: Consolidated roadmap dictionary
        fig1: 8-week roadmap figure
        fig2: 3-year roadmap figure
        rec_data: List of recommendation data items
    
    Returns:
        BytesIO: PowerPoint file as bytes
    """
    prs = Presentation()
    
    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Consolidated Roadmap & Baseball Cards"

    # Roadmap slides
    for title, fig in [("8-Week Roadmap", fig1), ("3-Year Roadmap", fig2)]:
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = title
        img = BytesIO()
        fig.savefig(img, format="png", bbox_inches="tight")
        img.seek(0)
        slide.shapes.add_picture(img, Inches(0.5), Inches(1.5), width=Inches(8))

    # Per-category baseball card slides
    for item in rec_data:
        cat = item["category"]
        data = item["data_normalized"]  # normalized form we saved
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = f"{cat} Baseball Cards"

        # Left column: Executive
        tf = slide.shapes.add_textbox(Inches(0.3), Inches(1.3), Inches(4.2), Inches(5)).text_frame
        tf.clear()
        add_wrapped_paragraph(tf, "EXECUTIVE Baseball Card", 14, True)
        exec_block = data.get("executive", {}) or {}
        # summary + recommendation
        summary = get_field(exec_block, "summary")
        rec = get_field(exec_block, "recommendation")
        if summary:
            add_wrapped_paragraph(tf, f"Summary: {summary}", 11)
        if rec:
            add_wrapped_paragraph(tf, f"Recommendation: {rec}", 11)
        activities = get_field(exec_block, "activities", "project_activities")
        if activities and isinstance(activities, list):
            add_wrapped_paragraph(tf, "Project Activities:", 11, True)
            for a in activities:
                add_wrapped_paragraph(tf, f"• {a}", 10, False, 1)
        assumptions = get_field(exec_block, "assumptions")
        if assumptions and isinstance(assumptions, list):
            add_wrapped_paragraph(tf, "Assumptions:", 11, True)
            for a in assumptions:
                add_wrapped_paragraph(tf, f"• {a}", 10, False, 1)

        # Right column: Technical
        tf2 = slide.shapes.add_textbox(Inches(4.8), Inches(1.3), Inches(4.2), Inches(5)).text_frame
        tf2.clear()
        add_wrapped_paragraph(tf2, "TECHNICAL Baseball Card", 14, True)
        tech_block = data.get("technical", {}) or {}
        summary_t = get_field(tech_block, "summary")
        rec_t = get_field(tech_block, "recommendation")
        if summary_t:
            add_wrapped_paragraph(tf2, f"Summary: {summary_t}", 11)
        if rec_t:
            add_wrapped_paragraph(tf2, f"Recommendation: {rec_t}", 11)
        t_activities = get_field(tech_block, "activities", "project_activities")
        if t_activities and isinstance(t_activities, list):
            add_wrapped_paragraph(tf2, "Project Activities:", 11, True)
            for a in t_activities:
                add_wrapped_paragraph(tf2, f"• {a}", 10, False, 1)
        assumptions_t = get_field(tech_block, "assumptions")
        if assumptions_t and isinstance(assumptions_t, list):
            add_wrapped_paragraph(tf2, "Assumptions:", 11, True)
            for a in assumptions_t:
                add_wrapped_paragraph(tf2, f"• {a}", 10, False, 1)
        # team
        team = get_field(tech_block, "team")
        if team and isinstance(team, list):
            add_wrapped_paragraph(tf2, "Initial Team (3-6 months):", 11, True)
            for t in team:
                add_wrapped_paragraph(tf2, f"• {t}", 10, False, 1)

    # final summary slide (top 3 priorities)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Executive Summary — Top Priorities"
    tf3 = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(8.5), Inches(5)).text_frame
    tf3.clear()
    add_wrapped_paragraph(tf3, "Top 3 Priorities (by impact)", 18, True)

    # derive priorities from consolidated (if present)
    items = []
    if consolidated:
        for s in ["sprint1", "sprint2", "sprint3", "sprint4"]:
            items.extend(consolidated.get("focus_8w", {}).get(s, []))
        for y in ["year1", "year2", "year3"]:
            items.extend(consolidated.get("plan_3y", {}).get(y, []))
    top3 = items[:3]
    for t in top3:
        add_wrapped_paragraph(tf3, f"• {t}", 14)

    out = BytesIO()
    prs.save(out)
    out.seek(0)
    return out

