import os
import json
import anthropic
from dotenv import load_dotenv
from news_fetcher import format_headlines_for_prompt

load_dotenv()

VALID_EVENTS = [
    "sanctions",
    "military_exercise",
    "border_clash",
    "peace_talks",
    "economic_pressure",
    "ceasefire",
]

SYSTEM_PROMPT = """You are a geopolitical intelligence analyst specializing in 
crisis escalation assessment. Your job is to read situational data and extract 
two things: the current escalation state AND the active crisis events.

You must respond with a JSON object in exactly this format:
{
    "starting_state": 0-5,
    "detected_events": ["event1", "event2"],
    "confidence": "high" | "medium" | "low",
    "reasoning": "Brief explanation of your assessment"
}

ESCALATION STATES (you must pick one):
- 0 (Stable): Normal relations, no visible tension
- 1 (Political Tension): Heated rhetoric, diplomatic warnings, verbal hostility
- 2 (Diplomatic Conflict): Sanctions threats, ambassadors recalled, formal disputes
- 3 (Military Posturing): Troop movements, military drills, weapons tests, naval deployments
- 4 (Limited Conflict): Active exchanges of fire, airstrikes, limited military operations
- 5 (Full Escalation): Open warfare, invasion, large-scale military conflict

VALID EVENTS (only use these):
- sanctions: economic sanctions, trade restrictions, asset freezes
- military_exercise: military drills, troop movements, weapons tests
- border_clash: armed incidents, skirmishes, exchanges of fire
- peace_talks: negotiations, diplomatic meetings, ceasefire discussions
- economic_pressure: trade wars, currency manipulation, supply chain disruption
- ceasefire: formal ceasefire, withdrawal agreements, peace deals

Rules:
- Assess the OVERALL situation to pick starting_state
- Only include events clearly supported by the data
- Never invent events not in the valid list
- Be conservative with both assessments
- Return only the JSON object, no other text"""


def _call_claude(user_message: str) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    response_text = message.content[0].text.strip()

    try:
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        result = json.loads(response_text.strip())

        result["detected_events"] = [
            e for e in result.get("detected_events", [])
            if e in VALID_EVENTS
        ]

        state = result.get("starting_state", 2)
        result["starting_state"] = max(0, min(5, int(state)))

        return result
    except (json.JSONDecodeError, ValueError, TypeError):
        return {
            "starting_state": 2,
            "detected_events": [],
            "confidence": "low",
            "reasoning": f"Failed to parse LLM response: {response_text[:200]}"
        }


def extract_events_from_headlines(headlines: list[dict], conflict_context: str) -> dict:
    formatted = format_headlines_for_prompt(headlines)

    user_message = f"""Conflict context: {conflict_context}

Recent headlines:
{formatted}

Analyze these headlines and provide the current escalation state and active crisis events."""

    return _call_claude(user_message)


def extract_events_from_hypothetical(scenario_description: str, conflict_context: str) -> dict:
    user_message = f"""Conflict context: {conflict_context}

Hypothetical scenario(s):
{scenario_description}

Based on these hypothetical developments, assess the implied current escalation state and the crisis events that would be active."""

    return _call_claude(user_message)