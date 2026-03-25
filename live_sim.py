import argparse
from dotenv import load_dotenv
from news_fetcher import fetch_headlines, format_headlines_for_prompt
from llm_extractor import extract_events_from_headlines
from state_model import EscalationLevel, STATE_NAMES
from simulation_engine import run_monte_carlo

load_dotenv()


def run_live_simulation(
    conflict_query: str,
    starting_state: int = 2,
    turns: int = 10,
    num_simulations: int = 1000,
    max_articles: int = 10,
):
    print(f"\n{'='*60}")
    print(f"  CRISISSIM LIVE — {conflict_query.upper()}")
    print(f"{'='*60}")

    print(f"\n[1/3] Fetching live news for '{conflict_query}'...")
    headlines = fetch_headlines(conflict_query, max_articles=max_articles)
    print(f"      Found {len(headlines)} recent articles")

    if not headlines:
        print("      No headlines found. Try a different search query.")
        return

    print("\n[2/3] Extracting crisis events with AI...")
    extraction = extract_events_from_headlines(headlines, conflict_query)
    detected_events = extraction["detected_events"]
    confidence = extraction["confidence"]
    reasoning = extraction["reasoning"]

    print(f"      Detected events: {detected_events if detected_events else 'none'}")
    print(f"      Confidence: {confidence}")
    print(f"      AI reasoning: {reasoning[:150]}...")

    if not detected_events:
        print("\n      No events detected — running with base probabilities")

    print(f"\n[3/3] Running {num_simulations} simulations...")
    starting = EscalationLevel(starting_state)

    results = run_monte_carlo(
        starting_state=starting,
        active_events=detected_events,
        turns=turns,
        num_simulations=num_simulations,
    )

    print(f"\n{'='*60}")
    print(f"  LIVE SIMULATION RESULTS")
    print(f"{'='*60}")
    print(f"  Conflict:       {conflict_query}")
    print(f"  Starting state: {STATE_NAMES[starting]}")
    print(f"  AI events used: {', '.join(detected_events) if detected_events else 'none (base only)'}")
    print(f"{'-'*60}")
    print(f"  OUTCOME PROBABILITIES:")

    for state, probability in sorted(
        results["outcome_probabilities"].items(),
        key=lambda x: x[1],
        reverse=True,
    ):
        bar = "█" * int(probability / 2)
        print(f"  {state:<25} {probability:>5.1f}%  {bar}")

    print(f"{'-'*60}")
    print(f"  Average final escalation: {results['average_final_level']} / 5")
    print(f"  Most likely trajectory:")
    print(f"  {results['most_common_trajectory']}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="CrisisSim Live — AI-powered geopolitical crisis simulator"
    )
    parser.add_argument(
        "conflict",
        type=str,
        help="Conflict to analyze e.g. 'Russia Ukraine' or 'South China Sea'",
    )
    parser.add_argument(
        "--state",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4, 5],
        help="Starting escalation state 0-5 (default: 2)",
    )
    parser.add_argument(
        "--turns",
        type=int,
        default=10,
        help="Number of simulation turns (default: 10)",
    )
    parser.add_argument(
        "--sims",
        type=int,
        default=1000,
        help="Number of simulations to run (default: 1000)",
    )

    args = parser.parse_args()

    run_live_simulation(
        conflict_query=args.conflict,
        starting_state=args.state,
        turns=args.turns,
        num_simulations=args.sims,
    )


if __name__ == "__main__":
    main()