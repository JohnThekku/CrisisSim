# CrisisSim

AI-powered geopolitical crisis simulator using probabilistic state transitions 
and Monte Carlo simulations to estimate likely escalation outcomes.

## What it does

CrisisSim models how a geopolitical crisis evolves over time. Starting from an 
initial escalation state, it applies real-world events (sanctions, military 
exercises, peace talks) that shift transition probabilities, then runs thousands 
of simulations to produce a probability distribution of outcomes.

## Escalation states

| Level | State |
|-------|-------|
| 0 | Stable |
| 1 | Political Tension |
| 2 | Diplomatic Conflict |
| 3 | Military Posturing |
| 4 | Limited Conflict |
| 5 | Full Escalation |

## Supported events

- `sanctions` — economic pressure increasing escalation probability
- `military_exercise` — large-scale exercise near disputed territory
- `border_clash` — armed incident at a contested border
- `peace_talks` — diplomatic negotiations de-escalating tension
- `economic_pressure` — sustained trade restrictions
- `ceasefire` — formal ceasefire agreement

## How to run
```bash
# Install dependencies
pip install -r requirements.txt

# Run with example scenario
python main.py

# Run and save results to file
python main.py --save

# Run with a custom scenario
python main.py --scenario scenarios/example_scenario.json
```

## Scenario format

Create a JSON file in `scenarios/` with this structure:
```json
{
    "name": "Your Scenario Name",
    "description": "Brief description",
    "actors": ["Actor A", "Actor B"],
    "starting_state": 2,
    "active_events": ["sanctions", "military_exercise"],
    "turns": 10,
    "num_simulations": 1000
}
```

## Project structure
```
crisissim/
├── main.py                  # CLI entry point
├── state_model.py           # Escalation states and transition matrix
├── events.py                # Event definitions and probability adjustments
├── probability_engine.py    # Weighted state sampling
├── simulation_engine.py     # Single run and Monte Carlo aggregation
├── scenarios/               # JSON scenario configurations
└── results/                 # Simulation outputs (gitignored)
```

## Roadmap

- **Phase 2** — Live news ingestion via NewsAPI + LLM event extraction using Claude
- **Phase 3** — FastAPI backend + React dashboard with real-time visualization