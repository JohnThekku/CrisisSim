from dataclasses import dataclass, field
from state_model import EscalationLevel


@dataclass
class Event:
    name: str
    description: str
    adjustments: dict = field(default_factory=dict)


EVENTS = {
    "sanctions": Event(
        name="sanctions",
        description="Economic sanctions imposed on one actor",
        adjustments={
            (EscalationLevel.STABLE, EscalationLevel.POLITICAL_TENSION): +0.10,
            (EscalationLevel.POLITICAL_TENSION, EscalationLevel.DIPLOMATIC_CONFLICT): +0.10,
            (EscalationLevel.DIPLOMATIC_CONFLICT, EscalationLevel.MILITARY_POSTURING): +0.08,
        },
    ),
    "military_exercise": Event(
        name="military_exercise",
        description="Large-scale military exercise near disputed territory",
        adjustments={
            (EscalationLevel.POLITICAL_TENSION, EscalationLevel.DIPLOMATIC_CONFLICT): +0.15,
            (EscalationLevel.DIPLOMATIC_CONFLICT, EscalationLevel.MILITARY_POSTURING): +0.15,
            (EscalationLevel.MILITARY_POSTURING, EscalationLevel.LIMITED_CONFLICT): +0.12,
        },
    ),
    "border_clash": Event(
        name="border_clash",
        description="Armed incident at a contested border",
        adjustments={
            (EscalationLevel.DIPLOMATIC_CONFLICT, EscalationLevel.MILITARY_POSTURING): +0.20,
            (EscalationLevel.MILITARY_POSTURING, EscalationLevel.LIMITED_CONFLICT): +0.20,
            (EscalationLevel.LIMITED_CONFLICT, EscalationLevel.FULL_ESCALATION): +0.15,
        },
    ),
    "peace_talks": Event(
        name="peace_talks",
        description="Diplomatic negotiations initiated between actors",
        adjustments={
            (EscalationLevel.POLITICAL_TENSION, EscalationLevel.STABLE): +0.15,
            (EscalationLevel.DIPLOMATIC_CONFLICT, EscalationLevel.POLITICAL_TENSION): +0.20,
            (EscalationLevel.MILITARY_POSTURING, EscalationLevel.DIPLOMATIC_CONFLICT): +0.15,
        },
    ),
    "economic_pressure": Event(
        name="economic_pressure",
        description="Sustained economic pressure through trade restrictions",
        adjustments={
            (EscalationLevel.STABLE, EscalationLevel.POLITICAL_TENSION): +0.08,
            (EscalationLevel.POLITICAL_TENSION, EscalationLevel.DIPLOMATIC_CONFLICT): +0.08,
        },
    ),
    "ceasefire": Event(
        name="ceasefire",
        description="Formal ceasefire agreement reached",
        adjustments={
            (EscalationLevel.FULL_ESCALATION, EscalationLevel.LIMITED_CONFLICT): +0.25,
            (EscalationLevel.LIMITED_CONFLICT, EscalationLevel.MILITARY_POSTURING): +0.20,
            (EscalationLevel.MILITARY_POSTURING, EscalationLevel.DIPLOMATIC_CONFLICT): +0.15,
        },
    ),
}


def apply_events(transition_matrix: dict, active_events: list[str]) -> dict:
    import copy
    adjusted = copy.deepcopy(transition_matrix)

    for event_name in active_events:
        if event_name not in EVENTS:
            print(f"Warning: unknown event '{event_name}' — skipping")
            continue

        event = EVENTS[event_name]

        for (from_state, to_state), adjustment in event.adjustments.items():
            if from_state not in adjusted:
                continue
            if to_state not in adjusted[from_state]:
                adjusted[from_state][to_state] = 0.0
            adjusted[from_state][to_state] += adjustment

        for from_state in adjusted:
            total = sum(adjusted[from_state].values())
            adjusted[from_state] = {
                state: prob / total
                for state, prob in adjusted[from_state].items()
            }

    return adjusted