# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

A Streamlit app that lets a consultant score a client's cloud/data maturity across 6 categories (36 sub-capabilities on a 1-5 scale), then calls OpenAI to generate executive/technical "baseball card" recommendations per category, consolidates them into an 8-week sprint plan and 3-year roadmap, and exports everything to PowerPoint.

## Running it

```bash
python -m streamlit run main.py
```

Requires a `.env` file (copy `.env_template`) with a real `OPENAI_API_KEY`. The app hard-stops (`st.stop()`) in [app/main.py](app/main.py) if the key is missing — this is intentional, not a bug to "fix" with a fallback.

No test suite exists in this repo. There is no lint/format config either — match the existing style (docstrings on every function, type hints on business logic) rather than introducing a new one.

## Architecture

```
main.py            → imports app.main, calls run_app() (Streamlit executes top-to-bottom on import)
app/main.py         → orchestration: page config, session state, wires sidebar → sliders → AI calls → cards → roadmap → export
app/ui_components.py → all st.* rendering: sidebar inputs, sliders, baseball card display
app/business_logic.py → pure functions: score averaging, category inclusion filtering
app/visualization.py → matplotlib figures for the 8-week/3-year roadmap diagrams
app/export.py        → builds the .pptx from consolidated roadmap + baseball card data
ai_gen/openai_client.py → thin wrapper around the OpenAI SDK, hardcoded to gpt-3.5-turbo
ai_gen/prompts.py       → prompt templates (GENERATION_SCHEMA, CONSOLIDATION_SCHEMA) — the JSON contract the model must follow
ai_gen/json_parser.py   → try_load_json(): fallback chain for parsing not-quite-valid JSON out of model responses
ai_gen/data_normalizer.py → normalize_baseball_card(): maps whatever shape the model returned onto {executive, technical}
```

Data flow per run: slider scores + sidebar context → `build_category_assessment_prompt()` per included category → `OpenAIClient.call_openai()` → `try_load_json()` → `normalize_baseball_card()` → stored in `st.session_state["recommendation_data"]` → rendered as cards → fragments consolidated via `build_consolidation_prompt()` into one roadmap → drawn as matplotlib figures → exported to pptx.

## Conventions to preserve

- **Category/sub-capability structure lives in `app/main.py`** (`CATEGORIES_STRUCTURE`) — it's duplicated informationally in the README; if you change one, update the other.
- **AI output is untrusted and often malformed** — always route model responses through `try_load_json()` → `normalize_baseball_card()` rather than parsing JSON directly. Both are deliberately defensive (multiple fallback strategies); don't simplify them into a single `json.loads()`.
- **`get_field()` in `ai_gen/data_normalizer.py`** does case-insensitive key lookup across a small set of accepted aliases (e.g. `activities`/`project_activities`) because model output field names drift. Use it instead of direct dict access when reading normalized cards.
- Every module/function has a docstring; keep that pattern for new code.
- No abstraction layer over Streamlit — `st.*` calls live directly in `ui_components.py` and `app/main.py`. Don't introduce a component framework for a single-page app this size.

## Known gaps (see Session_Handoff.md for status)

- No automated tests.
- Model is hardcoded to `gpt-3.5-turbo` in `ai_gen/openai_client.py` — no config for swapping models.
- No LICENSE file despite README claiming MIT.
