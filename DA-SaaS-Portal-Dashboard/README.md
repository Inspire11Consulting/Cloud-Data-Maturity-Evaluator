
  # Data & AI Maturity Tool (Frontend)

  This folder contains the React + Vite frontend for the **Data & AI Maturity Tool**.
  It calls the Python backend API (FastAPI) from the repo root.

  ## Running the code

  ### 1) Start the backend API (repo root)

  ```bash
  python -m uvicorn backend.api:app --reload --port 8000
  ```

  ### 2) Start the frontend (this folder)

  Run `npm i` to install the dependencies.

  Run `npm run dev` to start the development server (opens `http://localhost:3000`).
  