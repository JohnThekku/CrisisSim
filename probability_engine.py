import numpy as np
from state_model import EscalationLevel, BASE_TRANSITION_MATRIX
from events import apply_events


def get_next_state(
    current_state: EscalationLevel,
    transition_matrix: dict,
) -> EscalationLevel:

    if current_state not in transition_matrix:
        return current_state

    possible_states = list(transition_matrix[current_state].keys())
    probabilities = list(transition_matrix[current_state].values())

    chosen = np.random.choice(
        a=len(possible_states),
        p=probabilities,
    )

    return possible_states[chosen]


def build_adjusted_matrix(active_events: list[str]) -> dict:
    if not active_events:
        return BASE_TRANSITION_MATRIX
    return apply_events(BASE_TRANSITION_MATRIX, active_events)