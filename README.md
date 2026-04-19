# CrisisSim

AI-powered geopolitical crisis simulator using live news, LLM-based event extraction, 
and Monte Carlo simulation to model escalation outcomes.

**🔴 Live demo:** [crisissim.vercel.app](https://crisissim.vercel.app)

> ⚠️ Educational and research tool. Outputs are probabilistic models, 
> not predictions or political statements.

---

## What it does

Type any real-world conflict ("Russia Ukraine", "Taiwan Strait") or describe 
a hypothetical scenario ("China deploys naval fleet to disputed islands"), 
and CrisisSim will:

1. Fetch live news headlines (Live mode) or analyze your scenario (Hypothetical mode)
2. Use Claude AI to detect the current escalation state and active crisis events
3. Run 1000 Monte Carlo simulations across 6 escalation levels
4. Return a probability distribution of likely outcomes

## How it works
```
                    ┌──────────────────────────┐
                    │   User                   │
                    │   crisissim.vercel.app   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   React dashboard        │
                    │   (Vercel)               │
                    └────────────┬─────────────┘
                                 │ HTTPS
                                 ▼
                    ┌──────────────────────────┐
                    │   FastAPI backend        │
                    │   (Railway)              │
                    │   + Rate limiting        │
                    └──┬──────────────┬────────┘
                       │              │
            ┌──────────▼────┐   ┌─────▼────────┐
            │   NewsAPI     │   │   Claude AI  │
            │   (Live mode) │   │   (Haiku)    │
            └──────────┬────┘   └─────┬────────┘
                       │              │
                       └──────┬───────┘
                              ▼
                    ┌──────────────────────────┐
                    │   Monte Carlo engine     │
                    │   1000 simulations       │
                    │   6 escalation states    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Probability results    │
                    │   + AI assessment        │
                    └──────────────────────────┘
```

## Escalation states

| Level | State |
|-------|-------|
| 0 | Stable |
| 1 | Political Tension |
| 2 | Diplomatic Conflict |
| 3 | Military Posturing |
| 4 | Limited Conflict |
| 5 | Full Escalation |

## Detected events

`sanctions`, `military_exercise`, `border_clash`, `peace_talks`, 
`economic_pressure`, `ceasefire`

## Stack

**Backend**
- Python 3.11, FastAPI, Pydantic, NumPy
- Anthropic Claude (Haiku 4.5)
- NewsAPI
- slowapi (rate limiting)

**Frontend**
- React 18 (Vite), Recharts
- Axios, Vercel Analytics

**Deployment**
- Railway (backend) + Vercel (frontend)
- Auto-deploy on push to main

## Running locally

```bash
# Clone and enter
git clone https://github.com/JohnThekku/CrisisSim.git
cd CrisisSim

# Backend setup
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Add your NEWSAPI_KEY and ANTHROPIC_API_KEY to .env

# Run backend
cd backend
python -m uvicorn api:app --reload

# Run frontend (new terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

## API endpoints

| Method | Endpoint | Description | Rate limit |
|--------|----------|-------------|------------|
| GET | `/health` | Health check | — |
| POST | `/simulate/live` | Live news + AI simulation | 10/hour |
| POST | `/simulate/hypothetical` | Hypothetical scenario simulation | 20/hour |
| GET | `/states` | List of escalation states | — |

## Project structure

## Roadmap

- [x] Phase 1 — Probabilistic simulation engine + Monte Carlo analysis
- [x] Phase 2 — Live news + LLM event extraction
- [x] Phase 3 — FastAPI backend + React dashboard
- [x] Phase 4 — Production deployment (Vercel + Railway)
- [x] Phase 5 — AI-detected starting state + hypothetical scenarios
- [x] Phase 6 — Rate limiting + usage analytics