import pandas as pd

from src.recommender import EuroMillionsRecommender


def evaluate_ticket(
    predicted_main: list[int],
    predicted_stars: list[int],
    true_main: list[int],
    true_stars: list[int],
) -> tuple[int, int]:
    """
    Count how many main numbers and Lucky Stars matched.
    """
    main_matches = len(set(predicted_main) & set(true_main))
    star_matches = len(set(predicted_stars) & set(true_stars))

    return main_matches, star_matches


def backtest_method(
    df: pd.DataFrame,
    method: str,
    start_index: int = 200,
) -> pd.DataFrame:
    """
    Backtest one recommendation method chronologically.

    For each draw, only previous draws are used as historical data.
    """
    results = []

    main_columns = ["n1", "n2", "n3", "n4", "n5"]
    star_columns = ["star1", "star2"]

    for i in range(start_index, len(df)):
        history = df.iloc[:i]
        current_draw = df.iloc[i]

        recommender = EuroMillionsRecommender(history)
        ticket = recommender.recommend(method=method)

        true_main = current_draw[main_columns].tolist()
        true_stars = current_draw[star_columns].tolist()

        main_matches, star_matches = evaluate_ticket(
            predicted_main=ticket["main_numbers"],
            predicted_stars=ticket["lucky_stars"],
            true_main=true_main,
            true_stars=true_stars,
        )

        results.append(
            {
                "date": current_draw["date"],
                "method": method,
                "predicted_main": ticket["main_numbers"],
                "predicted_stars": ticket["lucky_stars"],
                "true_main": true_main,
                "true_stars": true_stars,
                "main_matches": main_matches,
                "star_matches": star_matches,
                "total_matches": main_matches + star_matches,
            }
        )

    return pd.DataFrame(results)


def summarize_backtest(results_df: pd.DataFrame) -> dict:
    """
    Summarize backtest results using normal Python numeric types.
    """
    return {
        "method": str(results_df["method"].iloc[0]),
        "number_of_tests": int(len(results_df)),
        "avg_main_matches": float(round(results_df["main_matches"].mean(), 4)),
        "avg_star_matches": float(round(results_df["star_matches"].mean(), 4)),
        "avg_total_matches": float(round(results_df["total_matches"].mean(), 4)),
        "max_main_matches": int(results_df["main_matches"].max()),
        "max_star_matches": int(results_df["star_matches"].max()),
        "max_total_matches": int(results_df["total_matches"].max()),
    }