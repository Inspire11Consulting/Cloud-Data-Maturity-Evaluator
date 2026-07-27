# Session Handoff

Last updated: 2026-07-26

## Current state

The app is functional and up to date with the codebase (post-restructure: `app/` + `ai_gen/` package layout). README, [CLAUDE.md](CLAUDE.md) now match the actual code. No feature work was done this session — this was a review/docs/environment pass.

## What changed this session

- **README.md**: fixed stale run instructions and project structure section that still referenced pre-restructure files (`MaturityLevelEvaluation.py`, `MaturityLevelEvaluation+AI7_v2.py`), which no longer exist. Now points to `python -m streamlit run main.py` and the real `app/`/`ai_gen/` layout.
- **CLAUDE.md**: created — architecture map, data flow, and conventions for future Claude sessions.
- **This file**: created.
- **Local environment set up to run the app** (see below).

## Security note (resolved twice this session)

`.env_template` was found on disk with the placeholder `OPENAI_API_KEY` replaced by what looked like a real, live OpenAI key. It was **not** in git history (checked `git log -p` — the committed version has the placeholder), so nothing was pushed. `.env_template` was reset to the placeholder.

This then happened a **second time** — the user pasted a real key directly into `.env_template` again while setting up to run the app. Same fix applied: the key was moved into `.env` (gitignored, confirmed via `git status`) and `.env_template` reset to the placeholder again. **Be careful in future sessions: this repo's contributors have a habit of pasting real keys into `.env_template` instead of `.env`.** Consider renaming `.env_template` to something less easy to confuse (e.g. `.env.example`) or adding a pre-commit check, if this keeps recurring.

**The key itself was not revoked** — it is currently live in `.env` and was used successfully to run the app this session.

## Local environment

- System has multiple Python installs; **Python 3.13 (`C:\Program Files\Python313`) is broken** — its `Lib\encodings` directory is missing, so `python`/`pip` fail with `ModuleNotFoundError: No module named 'encodings'` immediately. Do not use it.
- Python 3.11 (`C:\Users\FeliceChuang\AppData\Local\Programs\Python\Python311`) works correctly.
- A `.venv` was created in the repo root using Python 3.11, and `requirements.txt` was installed into it successfully (streamlit 1.60.0, pandas 3.0.5, numpy 2.4.6, openai 2.48.0, etc.).
- `.venv/` is not yet in `.gitignore` — it currently has no venv-specific ignore entry (only `env/`, `venv/`, `ENV/` patterns exist). Add `.venv/` if keeping this venv around, or delete it and let each contributor create their own.

## To run the app

```bash
.venv\Scripts\python.exe -m streamlit run main.py
```

Needs a `.env` file (not currently present) with a real `OPENAI_API_KEY` — the app will not start without one (see `app/main.py`, it calls `st.stop()`).

## Known gaps / next steps

- App was launched this session (`.venv\Scripts\python.exe -m streamlit run main.py`) with a live key in `.env` and confirmed serving HTTP 200 on `localhost:8501`. The AI-generation button (real OpenAI call) was not clicked/verified interactively — only server boot was confirmed.
- No automated tests anywhere in the repo.
- `ai_gen/openai_client.py` hardcodes `gpt-3.5-turbo` — worth revisiting given newer/cheaper models are available.
- README claims MIT License; no LICENSE file exists. User chose to leave this as-is for now.
- `.venv/` gitignore status unresolved (see above).
