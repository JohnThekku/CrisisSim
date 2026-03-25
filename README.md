# CrisisSim

AI-powered geopolitical crisis simulator using live news ingestion, 
LLM event extraction, and Monte Carlo simulations to estimate likely 
escalation outcomes.

## What it does

CrisisSim models how a geopolitical crisis evolves over time. It fetches 
live news headlines about any conflict, uses Claude AI to extract structured 
crisis events from those headlines, then runs thousands of probabilistic 
simulations to produce a distribution of likely outcomes.

**Example:** Type "XYZ conflict" and get:
- Full Escalation: X%
- Limited Conflict: Y%
- Military Posturing: Z%
- Most likely trajectory: Military Posturing → Limited Conflict → Full Escalation

## How it works
```
You provide a conflict query
        ↓
NewsAPI fetches live headlines
        ↓
Claude AI extracts structured crisis events
        ↓
Monte Carlo engine runs 1000 simulations
        ↓
Probability distribution of outcomes
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

| Event | Description |
|-------|-------------|
| `sanctions` | Economic sanctions or asset freezes |
| `military_exercise` | Military drills or troop movements |
| `border_clash` | Armed incidents or exchanges of fire |
| `peace_talks` | Diplomatic negotiations |
| `economic_pressure` | Trade restrictions or supply chain disruption |
| `ceasefire` | Formal ceasefire or withdrawal agreements |

## How to run
```bash
# Install dependencies
pip install -r requirements.txt

# Add your API keys
cp .env.example .env
# Edit .env with your NEWSAPI_KEY and ANTHROPIC_API_KEY

# Run live simulation (fetches real news + AI analysis)
python live_sim.py "Russia Ukraine"

# Start from a specific escalation state
python live_sim.py "Israel Iran conflict" --state 3

# Control simulation parameters
python live_sim.py "South China Sea" --state 2 --turns 15 --sims 2000

# Run with a manual scenario (no API keys needed)
python main.py --scenario scenarios/example_scenario.json --save
```

## CLI options
```
python live_sim.py [conflict] [options]

positional arguments:
  conflict       Conflict to analyze e.g. "Russia Ukraine"

options:
  --state        Starting escalation level 0-5 (default: 2)
  --turns        Simulation turns (default: 10)
  --sims         Number of simulations (default: 1000)
```

## Project structure
```
crisissim/
├── main.py                  # CLI entry point for manual scenarios
├── live_sim.py              # Live simulation pipeline
├── state_model.py           # Escalation states and transition matrix
├── events.py                # Event definitions and probability adjustments
├── probability_engine.py    # Weighted state sampling
├── simulation_engine.py     # Single run and Monte Carlo aggregation
├── news_fetcher.py          # NewsAPI integration
├── llm_extractor.py         # Claude AI event extraction + prompt engineering
├── scenarios/               # JSON scenario configurations
└── results/                 # Simulation outputs (gitignored)
```

## Environment setup

Create a `.env` file in the project root:
```
NEWSAPI_KEY=your_newsapi_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Get your keys:
- NewsAPI: https://newsapi.org (free tier, 100 requests/day)
- Anthropic: https://console.anthropic.com

## Roadmap

- [x] Phase 1 — Probabilistic simulation engine + Monte Carlo analysis
- [x] Phase 2 — Live news ingestion + LLM event extraction
- [ ] Phase 3 — FastAPI backend + React dashboard with real-time visualization
- [ ] Custom scenario builder UI
- [ ] Multi-conflict comparison
- [ ] Historical scenario replay