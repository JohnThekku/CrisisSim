import numpy as np
from collections import Counter
from state_model import EscalationLevel, CrisisState, STATE_NAMES
from probability_engine import get_next_state, build_adjusted_matrix


def run_single_simulation(
    starting_state: EscalationLevel,
    active_events: list[str],
    turns: int,
) -> list[EscalationLevel]:

    matrix = build_adjusted_matrix(active_events)
    crisis = CrisisState(current_level=starting_state)
    crisis.record()

    for _ in range(turns):
        next_state = get_next_state(crisis.current_level, matrix)
        crisis.current_level = next_state
        crisis.turn += 1
        crisis.record()

    return crisis.history


def run_monte_carlo(
    starting_state: EscalationLevel,
    active_events: list[str],
    turns: int,
    num_simulations: int = 1000,
) -> dict:

    all_trajectories = []
    final_states = []

    for _ in range(num_simulations):
        trajectory = run_single_simulation(starting_state, active_events, turns)
        all_trajectories.append(trajectory)
        final_states.append(trajectory[-1])

    final_state_counts = Counter(final_states)
    total = num_simulations

    outcome_probabilities = {
        STATE_NAMES[state]: round(count / total * 100, 1)
        for state, count in sorted(final_state_counts.items())
    }

    avg_final_level = np.mean([state.value for state in final_states])

    trajectory_strings = [
        " → ".join(STATE_NAMES[s] for s in traj)
        for traj in all_trajectories
    ]
    most_common_trajectory = Counter(trajectory_strings).most_common(1)[0][0]

    return {
        "num_simulations": num_simulations,
        "turns": turns,
        "starting_state": STATE_NAMES[starting_state],
        "active_events": active_events,
        "outcome_probabilities": outcome_probabilities,
        "average_final_level": round(avg_final_level, 2),
        "most_common_trajectory": most_common_trajectory,
    }