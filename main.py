import json
import argparse
from state_model import EscalationLevel, STATE_NAMES
from simulation_engine import run_monte_carlo


def load_scenario(filepath: str) -> dict:
    with open(filepath, "r") as f:
        return json.load(f)


def print_results(scenario: dict, results: dict):
    print("\n" + "=" * 60)
    print(f"  CRISISSIM — {scenario['name'].upper()}")
    print("=" * 60)
    print(f"  {scenario['description']}")
    print(f"  Actors: {' vs '.join(scenario['actors'])}")
    print(f"  Starting state: {results['starting_state']}")
    print(f"  Active events: {', '.join(results['active_events'])}")
    print(f"  Turns: {results['turns']} | Simulations: {results['num_simulations']}")
    print("-" * 60)
    print("  OUTCOME PROBABILITIES:")
    for state, probability in sorted(
        results["outcome_probabilities"].items(),
        key=lambda x: x[1],
        reverse=True,
    ):
        bar = "█" * int(probability / 2)
        print(f"  {state:<25} {probability:>5.1f}%  {bar}")
    print("-" * 60)
    print(f"  Average final escalation level: {results['average_final_level']} / 5")
    print(f"  Most likely trajectory:")
    print(f"  {results['most_common_trajectory']}")
    print("=" * 60 + "\n")


def save_results(scenario: dict, results: dict):
    import os
    import json
    from datetime import datetime

    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/{scenario['name'].replace(' ', '_')}_{timestamp}.json"

    output = {"scenario": scenario, "results": results}

    with open(filename, "w") as f:
        json.dump(output, f, indent=2)

    print(f"  Results saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="CrisisSim — Geopolitical Crisis Escalation Simulator"
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default="scenarios/example_scenario.json",
        help="Path to scenario JSON file",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save results to results/ folder",
    )
    args = parser.parse_args()

    scenario = load_scenario(args.scenario)
    starting_state = EscalationLevel(scenario["starting_state"])

    print(f"\nRunning {scenario['num_simulations']} simulations...")

    results = run_monte_carlo(
        starting_state=starting_state,
        active_events=scenario["active_events"],
        turns=scenario["turns"],
        num_simulations=scenario["num_simulations"],
    )

    print_results(scenario, results)

    if args.save:
        save_results(scenario, results)


if __name__ == "__main__":
    main()