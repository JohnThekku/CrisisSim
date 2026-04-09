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
crisis escalation assessment. Your job is to read news headlines and extract 
structured crisis signals from them.

You will be given a list of recent news headlines about a geopolitical situation.
Your task is to identify which crisis events are present based on the headlines.

You must respond with a JSON object in exactly this format:
{
    "detected_events": ["event1", "event2"],
    "confidence": "high" | "medium" | "low",
    "reasoning": "Brief explanation of why you selected these events"
}

The only valid events you can detect are:
- sanctions: economic sanctions, trade restrictions, asset freezes
- military_exercise: military drills, troop movements, weapons tests
- border_clash: armed incidents, skirmishes, exchanges of fire
- peace_talks: negotiations, diplomatic meetings, ceasefire discussions
- economic_pressure: trade wars, currency manipulation, supply chain disruption
- ceasefire: formal ceasefire, withdrawal agreements, peace deals

Rules:
- Only include events that are clearly supported by the headlines
- You may return an empty list if no events are detected
- Never invent events not in the valid list
- Be conservative — only include high confidence detections
- Return only the JSON object, no other text"""


def extract_events_from_headlines(
    headlines: list[dict],
    conflict_context: str,
) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")

    client = anthropic.Anthropic(api_key=api_key)
    formatted = format_headlines_for_prompt(headlines)

    user_message = f"""Conflict context: {conflict_context}

Recent headlines:
{formatted}

Analyze these headlines and extract the crisis events present."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ],
    )

    response_text = message.content[0].text.strip()

    try:
        # Claude sometimes wraps JSON in ```json ``` blocks — strip that
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        result = json.loads(response_text)
        result["detected_events"] = [
            e for e in result.get("detected_events", [])
            if e in VALID_EVENTS
        ]
        return result
    except json.JSONDecodeError:
        return {
            "detected_events": [],
            "confidence": "low",
            "reasoning": f"Failed to parse LLM response: {response_text[:200]}"
        }