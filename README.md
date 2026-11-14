# GridZero v3.5 — Autonomous Neuro-Symbolic Micro-Grid & Civic Disaster Digital Twin
**NorCal Hacks 27 | Tracks: Sustainability & New Frontiers**

## Architecture Overview
GridZero combines a **12-Node South Bay Deterministic DC Power-Flow & Thermal Constraint Verifier** (`backend/main.py`) with a **3-Agent `gemini-3.8-flash` Neuro-Symbolic Self-Correction Loop** and a **Civic SOS Triage & Mobile Megapack Dispatch Command Center** (`frontend/index.html`).

### Directory Structure
```text
gridzero/
├── backend/
│   └── main.py          # FastAPI server + Open-Meteo San Jose live telemetry + DC Power-Flow Solver + 3 Gemini Agents
├── frontend/
│   └── index.html       # Self-contained Tactical Command Center (HTML5 Canvas + Chart.js + Web Audio + Civic SOS Suite)
├── requirements.txt     # Python dependencies
└── README.md            # Quickstart & API documentation
```

## 60-Second Quickstart

### Option A: Full-Stack Mode (FastAPI Backend + Frontend served on Port 8000)
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-gemini-api-key"   # Optional: falls back to deterministic physics + preset cache if omitted
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Open **http://localhost:8000** in your browser.

### Option B: Zero-Setup Static Mode
Open `frontend/index.html` directly in any browser (or deploy `frontend/` to Vercel/Netlify). It fetches live San Jose solar irradiance & wind telemetry directly from Open-Meteo and runs the complete 12-node physics and neuro-symbolic simulation in-browser.

## Key Endpoints (`backend/main.py`)
- `GET /` — Serves `frontend/index.html` directly.
- `GET /api/telemetry` — Live San Jose Open-Meteo weather (`shortwave_radiation`, `wind_speed_80m`, `temperature_2m`) converted to MW + 12-node DC power-flow state.
- `POST /api/crisis` — Triggers `wildfire`, `metcalf_overload`, or `scada_spoof` and returns both the rejected AGENT-03 Draft #1 (`ERR_LINE_THERMAL_OVERLOAD_118PCT`) and the solver-verified final dispatch plan.
- `POST /api/solve` — Evaluates custom line severing, islanding, battery discharge, and load-shedding overrides.
- `GET /api/sos` & `POST /api/sos` — Civic & Hospital SOS Triage Board and Mobile Megapack fleet dispatch.
- `GET /api/benchmark` — 20-contingency ablation benchmark comparing Raw Unverified LLM vs. GridZero Neuro-Symbolic Solver (0% hospital blackout rate vs. 25%).
