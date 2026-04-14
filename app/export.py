"""
PowerPoint export functionality.
"""

from io import BytesIO
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
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
    p.font.color.rgb = RGBColor(31, 41, 55)
    p.level = level
    p.word_wrap = True
    return p


def _clean_text(value, max_chars=240):
    """Normalize and trim text for reliable slide rendering."""
    text = " ".join(str(value or "").split()).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def _line_cost(text, chars_per_line=60):
    """Approximate rendered line count for a text fragment."""
    text = str(text or "")
    if not text:
        return 1
    return max(1, math.ceil(len(text) / chars_per_line))


def _add_card_content(frame, title, block, include_team=False):
    """
    Add card content with a line budget to prevent overflow.
    """
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.TOP

    add_wrapped_paragraph(frame, title, 12, True)
    line_budget = 32
    lines_used = 2

    def try_add_text(label, raw, font_size=10):
        nonlocal lines_used
        if not raw:
            return
        text = _clean_text(raw, 260 if label == "Summary" else 300)
        paragraph = f"{label}: {text}"
        needed = _line_cost(paragraph, 58)
        if lines_used + needed > line_budget:
            return
        add_wrapped_paragraph(frame, paragraph, font_size)
        lines_used += needed

    def try_add_list(label, items, max_items=4, item_chars=120):
        nonlocal lines_used
        if not items or not isinstance(items, list):
            return
        filtered = [_clean_text(i, item_chars) for i in items if str(i).strip()]
        if not filtered:
            return

        # section header
        if lines_used + 1 > line_budget:
            return
        add_wrapped_paragraph(frame, f"{label}:", 10, True)
        lines_used += 1

        shown = 0
        for item in filtered[:max_items]:
            needed = _line_cost(f"• {item}", 56)
            if lines_used + needed > line_budget:
                break
            add_wrapped_paragraph(frame, f"• {item}", 9, False, 1)
            lines_used += needed
            shown += 1

        remaining = len(filtered) - shown
        if remaining > 0 and lines_used + 1 <= line_budget:
            add_wrapped_paragraph(frame, f"• +{remaining} more items (see app/PPT notes)", 9, False, 1)
            lines_used += 1

    try_add_text("Summary", get_field(block, "summary"))
    try_add_text("Recommendation", get_field(block, "recommendation"))
    try_add_list("Project Activities", get_field(block, "activities", "project_activities"), max_items=5, item_chars=120)
    try_add_list("Assumptions", get_field(block, "assumptions"), max_items=3, item_chars=110)
    if include_team:
        try_add_list("Initial Team (3-6 months)", get_field(block, "team"), max_items=5, item_chars=80)


def _add_roadmap_text_slide(prs, title, sections, accent_rgb):
    """
    Create an editable roadmap slide using bordered text boxes.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = title

    cols = len(sections)
    if cols == 0:
        return

    left_margin = 0.4
    right_margin = 0.4
    top = 1.2
    height = 5.8
    gap = 0.25
    usable_width = 13.333 - left_margin - right_margin - (gap * (cols - 1))
    col_width = usable_width / cols

    for idx, (section_title, items) in enumerate(sections):
        left = left_margin + idx * (col_width + gap)
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left),
            Inches(top),
            Inches(col_width),
            Inches(height),
        )

        # White card with subtle border for easy editing.
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = RGBColor(*accent_rgb)
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.08)
        tf.margin_right = Inches(0.08)
        tf.margin_top = Inches(0.06)
        tf.margin_bottom = Inches(0.06)

        header = tf.paragraphs[0]
        header.text = section_title
        header.font.bold = True
        header.font.size = Pt(13)
        header.font.color.rgb = RGBColor(*accent_rgb)

        if not items:
            add_wrapped_paragraph(tf, "No initiatives added.", 10)
            continue

        shown = 0
        for item in items:
            if shown >= 8:
                break
            cleaned = _clean_text(item, 120)
            add_wrapped_paragraph(tf, f"• {cleaned}", 10, False, 0)
            shown += 1

        remaining = len(items) - shown
        if remaining > 0:
            add_wrapped_paragraph(tf, f"• +{remaining} more items", 10, False, 0)


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
    # Use standard widescreen format (16:9) for modern presentation layouts.
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Consolidated Roadmap & Baseball Cards"

    # Roadmap slides as editable text boxes (not static images).
    focus_sections = [
        ("Sprint 1", (consolidated or {}).get("focus_8w", {}).get("sprint1", [])),
        ("Sprint 2", (consolidated or {}).get("focus_8w", {}).get("sprint2", [])),
        ("Sprint 3", (consolidated or {}).get("focus_8w", {}).get("sprint3", [])),
        ("Sprint 4", (consolidated or {}).get("focus_8w", {}).get("sprint4", [])),
    ]
    _add_roadmap_text_slide(prs, "8-Week Roadmap", focus_sections, accent_rgb=(37, 99, 235))

    plan_sections = [
        ("Year 1", (consolidated or {}).get("plan_3y", {}).get("year1", [])),
        ("Year 2", (consolidated or {}).get("plan_3y", {}).get("year2", [])),
        ("Year 3", (consolidated or {}).get("plan_3y", {}).get("year3", [])),
    ]
    _add_roadmap_text_slide(prs, "3-Year Roadmap", plan_sections, accent_rgb=(124, 58, 237))

    # Per-category baseball card slides
    for item in rec_data:
        cat = item["category"]
        data = item["data_normalized"]  # normalized form we saved
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = f"{cat} Baseball Cards"

        # Left column: Executive
        tf = slide.shapes.add_textbox(Inches(0.35), Inches(1.2), Inches(6.15), Inches(5.6)).text_frame
        exec_block = data.get("executive", {}) or {}
        _add_card_content(tf, "EXECUTIVE Baseball Card", exec_block, include_team=False)

        # Right column: Technical
        tf2 = slide.shapes.add_textbox(Inches(6.85), Inches(1.2), Inches(6.15), Inches(5.6)).text_frame
        tech_block = data.get("technical", {}) or {}
        _add_card_content(tf2, "TECHNICAL Baseball Card", tech_block, include_team=True)

    # final summary slide (top 3 priorities)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Executive Summary — Top Priorities"
    tf3 = slide.shapes.add_textbox(Inches(0.6), Inches(1.35), Inches(12.1), Inches(5.6)).text_frame
    tf3.clear()
    add_wrapped_paragraph(tf3, "Top 3 Priorities (by impact)", 16, True)

    # derive priorities from consolidated (if present)
    items = []
    if consolidated:
        for s in ["sprint1", "sprint2", "sprint3", "sprint4"]:
            items.extend(consolidated.get("focus_8w", {}).get(s, []))
        for y in ["year1", "year2", "year3"]:
            items.extend(consolidated.get("plan_3y", {}).get(y, []))
    top3 = items[:3]
    for t in top3:
        add_wrapped_paragraph(tf3, f"• {_clean_text(t, 160)}", 12)

    out = BytesIO()
    prs.save(out)
    out.seek(0)
    return out

