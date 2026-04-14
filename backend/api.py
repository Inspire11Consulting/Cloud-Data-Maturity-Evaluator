from __future__ import annotations

from io import BytesIO
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from ai_gen.data_normalizer import get_field, normalize_baseball_card
from ai_gen.json_parser import try_load_json
from ai_gen.ai_client import AIClient
from ai_gen.prompts import build_category_assessment_prompt, build_consolidation_prompt
from app import business_logic, export, visualization
from app.schema import CATEGORIES_STRUCTURE, MATURITY_LEVELS


app = FastAPI(title="Data & AI Maturity Tool API")

# In dev, the React app runs on http://localhost:3000. In prod, prefer a reverse proxy.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CategoryScores(BaseModel):
    average: float | None = None
    sub_capabilities: dict[str, int] = Field(default_factory=dict)


class AssessRequest(BaseModel):
    # Company context (kept similar to the previous Streamlit sidebar)
    industry: str = ""
    company_size: str = ""
    it_size: str = ""
    uses_cloud: str = ""
    cloud_platform: str = ""
    priority_projects: str = ""
    overall_context: str = ""
    seed_scenario_text: str = ""

    # Assessment inputs
    all_scores: dict[str, CategoryScores] = Field(default_factory=dict)
    category_inclusion: dict[str, bool] = Field(default_factory=dict)
    category_comments: dict[str, str] = Field(default_factory=dict)


class CategoryFragment(BaseModel):
    category: str
    focus_8w: list[str] = Field(default_factory=list)
    plan_3y: list[str] = Field(default_factory=list)


class ConsolidateRequest(BaseModel):
    category_fragments: list[CategoryFragment] = Field(default_factory=list)


class ExportPptxRequest(BaseModel):
    consolidated: dict[str, Any]
    recommendation_data: list[dict[str, Any]] = Field(default_factory=list)


@app.get("/api/schema")
def get_schema():
    return {
        "categories_structure": CATEGORIES_STRUCTURE,
        "maturity_levels": MATURITY_LEVELS,
        "scale": {"min": 1, "max": 5},
    }


@app.post("/api/assess")
def assess(req: AssessRequest):
    try:
        client = AIClient()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Convert pydantic models to plain dicts
    all_scores = {k: v.model_dump() for k, v in req.all_scores.items()}

    categories_to_process = business_logic.get_included_categories(
        CATEGORIES_STRUCTURE, req.category_inclusion, req.category_comments
    )
    if not categories_to_process:
        return {
            "recommendation_data": [],
            "category_fragments": [],
            "consolidated": None,
        }

    recommendation_data: list[dict[str, Any]] = []
    category_fragments: list[dict[str, Any]] = []
    raw_ai_outputs: dict[str, str] = {}

    for category in categories_to_process:
        include_flag = req.category_inclusion.get(category, False)
        comment_text = (req.category_comments.get(category) or "").strip()
        scores = all_scores.get(category, {}) or {}
        avg = scores.get("average")
        sub_capability_scores = scores.get("sub_capabilities", {}) or {}

        prompt = build_category_assessment_prompt(
            industry=req.industry,
            company_size=req.company_size,
            it_size=req.it_size,
            uses_cloud=req.uses_cloud,
            cloud_platform=req.cloud_platform,
            priority_projects=req.priority_projects,
            category=category,
            include_flag=include_flag,
            avg_maturity=avg,
            sub_capability_scores=sub_capability_scores,
            category_comments=comment_text,
            overall_context=req.overall_context,
            seed_scenario_text=req.seed_scenario_text,
        )

        try:
            raw = client.call_ai(prompt, max_tokens=1000, temperature=0.4)
            raw_ai_outputs[category] = raw
            parsed = try_load_json(raw)
            normalized = normalize_baseball_card(parsed)

            recommendation_data.append(
                {
                    "category": category,
                    "raw": raw,
                    "parsed": parsed,
                    "data_normalized": normalized,
                    "show_avg": include_flag,
                    "avg": avg if include_flag else None,
                }
            )

            exec_block = normalized.get("executive", {}) or {}
            exec_focus = get_field(exec_block, "focus_8w") or []
            exec_plan3 = get_field(exec_block, "plan_3y") or []
            if isinstance(exec_focus, str):
                exec_focus = [exec_focus]
            if isinstance(exec_plan3, str):
                exec_plan3 = [exec_plan3]

            category_fragments.append(
                {"category": category, "focus_8w": exec_focus, "plan_3y": exec_plan3}
            )
        except Exception as e:
            # Keep going for other categories; return details for troubleshooting.
            recommendation_data.append(
                {
                    "category": category,
                    "raw": raw_ai_outputs.get(category, ""),
                    "error": str(e),
                    "data_normalized": {"executive": {}, "technical": {}},
                    "show_avg": include_flag,
                    "avg": avg if include_flag else None,
                }
            )

    return {
        "recommendation_data": recommendation_data,
        "category_fragments": category_fragments,
        "raw_ai_outputs": raw_ai_outputs,
    }


@app.post("/api/consolidate")
def consolidate(req: ConsolidateRequest):
    try:
        client = AIClient()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    fragments = [f.model_dump() for f in req.category_fragments]
    prompt = build_consolidation_prompt(fragments)

    try:
        raw = client.call_ai(prompt, max_tokens=800, temperature=0.4)
        consolidated = try_load_json(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consolidation failed: {e}")

    # Normalize structure
    consolidated.setdefault("focus_8w", {})
    consolidated.setdefault("plan_3y", {})
    for s in ["sprint1", "sprint2", "sprint3", "sprint4"]:
        if s not in consolidated["focus_8w"] or not isinstance(consolidated["focus_8w"][s], list):
            consolidated["focus_8w"][s] = []
    for y in ["year1", "year2", "year3"]:
        if y not in consolidated["plan_3y"] or not isinstance(consolidated["plan_3y"][y], list):
            consolidated["plan_3y"][y] = []

    return {"consolidated": consolidated}


@app.post("/api/export/pptx")
def export_pptx(req: ExportPptxRequest):
    consolidated = req.consolidated or {}

    try:
        fig1 = visualization.draw_8week_roadmap_figure(consolidated.get("focus_8w", {}))
        fig2 = visualization.draw_3year_roadmap_figure(consolidated.get("plan_3y", {}))
        pptx_bytes = export.export_to_pptx(consolidated, fig1, fig2, req.recommendation_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PPTX export failed: {e}")

    if isinstance(pptx_bytes, BytesIO):
        pptx_bytes.seek(0)

    return StreamingResponse(
        pptx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": 'attachment; filename="Consolidated_Roadmap_and_Cards.pptx"'},
    )


@app.get("/health")
def health():
    return JSONResponse({"ok": True})

