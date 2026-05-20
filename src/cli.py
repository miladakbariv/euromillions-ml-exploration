import argparse
import pandas as pd

from src.recommender import EuroMillionsRecommender


def main():
    """
    Command-line interface for generating EuroMillions ticket recommendations.
    """
    parser = argparse.ArgumentParser(
        description="Generate EuroMillions ticket recommendations."
    )

    parser.add_argument(
        "--method",
        type=str,
        default="hybrid",
        choices=["random", "frequency", "hybrid"],
        help="Recommendation method to use.",
    )

    parser.add_argument(
        "--data-path",
        type=str,
        default="data/processed/draws_clean.csv",
        help="Path to the cleaned EuroMillions CSV file.",
    )

    parser.add_argument(
        "--tickets",
        type=int,
        default=1,
        help="Number of tickets to generate.",
    )

    args = parser.parse_args()

    df = pd.read_csv(args.data_path)

    recommender = EuroMillionsRecommender(df)

    print("EuroMillions Ticket Recommendation")
    print("----------------------------------")
    print(f"Method: {args.method}")
    print(f"Number of tickets: {args.tickets}")
    print()

    for i in range(args.tickets):
        ticket = recommender.recommend(method=args.method)

        print(f"Ticket {i + 1}")
        print(f"Main numbers: {ticket['main_numbers']}")
        print(f"Lucky Stars:  {ticket['lucky_stars']}")
        print()


if __name__ == "__main__":
    main()