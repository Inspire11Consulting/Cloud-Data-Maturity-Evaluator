"""
Convenience entry point for the Data & AI Maturity Tool backend API.

Recommended dev command:
  python -m uvicorn backend.api:app --reload --port 8000
"""

from __future__ import annotations

import uvicorn


def main() -> None:
    uvicorn.run("backend.api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()

