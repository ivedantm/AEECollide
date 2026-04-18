# ⚡ Dispatch IQ — Energy Dispatch Intelligence

> AI-powered BTM (Behind-The-Meter) gas vs. grid power arbitrage intelligence for ERCOT & WECC. Built for the AEE Energy Hackathon.

![Bloomberg Terminal Style](https://img.shields.io/badge/style-Bloomberg%20Terminal-0A0E14?style=flat-square&labelColor=111827&color=10B981)
![Python](https://img.shields.io/badge/backend-FastAPI-009688?style=flat-square)
![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB?style=flat-square)

## What It Does

A data center with on-site gas generators faces a decision every 15 minutes:
**Is it cheaper to buy power from the grid (IMPORT) or generate my own (GENERATE)?**

Dispatch IQ answers this with:

| Feature | Description |
|---|---|
| **Live Spread Ticker** | Real-time `LMP − Generation Cost` with GENERATE/IMPORT recommendation |
| **72-Hour Forecast** | Monte Carlo simulation producing p10/p50/p90 confidence bands |
| **Site Selection** | Ranked comparison of 7 candidate data center locations across ERCOT & WECC |
| **Market Regime Detection** | Classifies current conditions (Normal, Heat Dome, Wind Glut, Scarcity, Winter Storm) |
| **AI Operator Briefing** | GPT-4o generated plain-English dispatch directive |
| **Historical Replay** | Animated replay of Winter Storm Uri (2021), Heat Dome (2023), and Wind Glut (2024) |

## The Core Equation

```
Spread = Grid Price (LMP) − Generation Cost
Generation Cost = Gas Price × Heat Rate + O&M
                = $2.41/MMBtu × 7.5 MMBtu/MWh + $3.50 = $21.58/MWh

If Spread > 0 → GENERATE (cheaper to run your own turbine)
If Spread < 0 → IMPORT   (cheaper to buy from the grid)
```

## Architecture

```
┌─────────────────────────────────┐     ┌──────────────────────────────┐
│  Frontend (React + Vite)        │     │  Backend (FastAPI)            │
│  localhost:5173                  │────▶│  localhost:8000               │
│                                 │     │                              │
│  • Site Selection Map (Leaflet) │     │  GET /api/sites              │
│  • Spread Ticker                │     │  GET /api/dispatch/current   │
│  • 72hr Forecast (Recharts)     │     │  GET /api/dispatch/forecast  │
│  • Dispatch Schedule Grid       │     │  GET /api/dispatch/schedule  │
│  • AI Briefing Card             │     │  GET /api/dispatch/briefing  │
│  • Historical Replay Engine     │     │  GET /api/replay/{scenario}  │
└─────────────────────────────────┘     └──────────────────────────────┘
```

## Quick Start

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
cd ..
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Open
Visit `http://localhost:5173`

### Environment Variables (Optional)
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=sk-...    # For AI operator briefings
EIA_API_KEY=...          # For live gas prices from EIA
```

## Data Sources

| Source | Data | Status |
|---|---|---|
| [ERCOT](https://www.ercot.com/) | Real-time LMP at settlement points | Mock (OAuth2 required) |
| [EIA](https://www.eia.gov/opendata/) | Henry Hub & Waha gas spot prices | Ready (API key optional) |
| [OpenAI](https://platform.openai.com/) | GPT-4o operator briefings | Ready (API key optional) |

## Historical Replay Scenarios

| Scenario | Date | What Happened | Value Demonstrated |
|---|---|---|---|
| ❄️ Winter Storm Uri | Feb 2021 | Grid collapse, LMP capped at $9,000/MWh | $56.1M in stranded costs avoided |
| 🔥 Heat Dome | Aug 2023 | 116°F, LMP hit $5,000/MWh | Millions in generation profit captured |
| 🌀 Wind Glut | Apr 2024 | Negative LMP (−$42/MWh) | Losses avoided by switching to IMPORT |

## Tech Stack

- **Backend**: Python 3.9+, FastAPI, NumPy (Monte Carlo), OpenAI SDK
- **Frontend**: React 18, Vite 6, Recharts, React-Leaflet
- **Map**: CartoDB Dark Matter tiles (no API key needed)
- **Design**: Bloomberg Terminal aesthetic — IBM Plex Mono, dark theme

## Team

Built at the AEE Energy Hackathon 2025.
