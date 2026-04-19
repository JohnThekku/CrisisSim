import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from state_model import EscalationLevel, STATE_NAMES
from simulation_engine import run_monte_carlo
from news_fetcher import fetch_headlines
from llm_extractor import extract_events_from_headlines

load_dotenv()

app = FastAPI(
    title="CrisisSim API",
    description="AI-powered geopolitical crisis simulator",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    conflict: str
    starting_state: int = 2
    turns: int = 10
    num_simulations: int = 1000
    use_live_news: bool = True


class ManualSimulationRequest(BaseModel):
    conflict: str
    starting_state: int = 2
    turns: int = 10
    num_simulations: int = 1000
    events: list[str] = []


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CrisisSim API"}


@app.post("/simulate/live")
async def simulate_live(request: SimulationRequest):
    try:
        headlines = fetch_headlines(request.conflict, max_articles=10)

        if not headlines:
            raise HTTPException(
                status_code=404,
                detail=f"No headlines found for '{request.conflict}'"
            )

        extraction = extract_events_from_headlines(headlines, request.conflict)
        detected_events = extraction["detected_events"]

        starting = EscalationLevel(request.starting_state)
        results = run_monte_carlo(
            starting_state=starting,
            active_events=detected_events,
            turns=request.turns,
            num_simulations=request.num_simulations,
        )

        return {
            "conflict": request.conflict,
            "headlines_analyzed": len(headlines),
            "detected_events": detected_events,
            "ai_confidence": extraction["confidence"],
            "ai_reasoning": extraction["reasoning"],
            "simulation": results,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate/manual")
async def simulate_manual(request: ManualSimulationRequest):
    try:
        starting = EscalationLevel(request.starting_state)
        results = run_monte_carlo(
            starting_state=starting,
            active_events=request.events,
            turns=request.turns,
            num_simulations=request.num_simulations,
        )

        return {
            "conflict": request.conflict,
            "detected_events": request.events,
            "simulation": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events")
def get_events():
    return {
        "events": [
            {"id": "sanctions", "label": "Sanctions", "description": "Economic sanctions imposed"},
            {"id": "military_exercise", "label": "Military Exercise", "description": "Large-scale military drills"},
            {"id": "border_clash", "label": "Border Clash", "description": "Armed incident at border"},
            {"id": "peace_talks", "label": "Peace Talks", "description": "Diplomatic negotiations"},
            {"id": "economic_pressure", "label": "Economic Pressure", "description": "Trade restrictions"},
            {"id": "ceasefire", "label": "Ceasefire", "description": "Formal ceasefire agreement"},
        ]
    }


@app.get("/states")
def get_states():
    return {
        "states": [
            {"level": level.value, "name": STATE_NAMES[level]}
            for level in EscalationLevel
        ]
    }