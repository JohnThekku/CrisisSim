import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from state_model import EscalationLevel, STATE_NAMES
from simulation_engine import run_monte_carlo
from news_fetcher import fetch_headlines
from llm_extractor import (
    extract_events_from_headlines,
    extract_events_from_hypothetical,
)

load_dotenv()

app = FastAPI(
    title="CrisisSim API",
    description="AI-powered geopolitical crisis simulator",
    version="2.1.0",
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LiveSimulationRequest(BaseModel):
    conflict: str
    turns: int = 10
    num_simulations: int = 1000


class HypotheticalSimulationRequest(BaseModel):
    conflict: str
    scenario_description: str
    turns: int = 10
    num_simulations: int = 1000


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CrisisSim API"}


@app.post("/simulate/live")
@limiter.limit("10/hour")
async def simulate_live(request: Request, payload: LiveSimulationRequest):
    try:
        headlines = fetch_headlines(payload.conflict, max_articles=10)

        if not headlines:
            raise HTTPException(
                status_code=404,
                detail=f"No headlines found for '{payload.conflict}'"
            )

        extraction = extract_events_from_headlines(headlines, payload.conflict)
        detected_events = extraction["detected_events"]
        detected_state = extraction["starting_state"]

        starting = EscalationLevel(detected_state)
        results = run_monte_carlo(
            starting_state=starting,
            active_events=detected_events,
            turns=payload.turns,
            num_simulations=payload.num_simulations,
        )

        return {
            "mode": "live",
            "conflict": payload.conflict,
            "headlines_analyzed": len(headlines),
            "detected_starting_state": STATE_NAMES[starting],
            "detected_starting_state_level": detected_state,
            "detected_events": detected_events,
            "ai_confidence": extraction["confidence"],
            "ai_reasoning": extraction["reasoning"],
            "simulation": results,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate/hypothetical")
@limiter.limit("20/hour")
async def simulate_hypothetical(request: Request, payload: HypotheticalSimulationRequest):
    try:
        if not payload.scenario_description.strip():
            raise HTTPException(
                status_code=400,
                detail="scenario_description cannot be empty"
            )

        extraction = extract_events_from_hypothetical(
            scenario_description=payload.scenario_description,
            conflict_context=payload.conflict,
        )
        detected_events = extraction["detected_events"]
        detected_state = extraction["starting_state"]

        starting = EscalationLevel(detected_state)
        results = run_monte_carlo(
            starting_state=starting,
            active_events=detected_events,
            turns=payload.turns,
            num_simulations=payload.num_simulations,
        )

        return {
            "mode": "hypothetical",
            "conflict": payload.conflict,
            "scenario_description": payload.scenario_description,
            "detected_starting_state": STATE_NAMES[starting],
            "detected_starting_state_level": detected_state,
            "detected_events": detected_events,
            "ai_confidence": extraction["confidence"],
            "ai_reasoning": extraction["reasoning"],
            "simulation": results,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/states")
def get_states():
    return {
        "states": [
            {"level": level.value, "name": STATE_NAMES[level]}
            for level in EscalationLevel
        ]
    }