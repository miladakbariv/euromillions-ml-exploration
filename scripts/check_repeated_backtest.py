import random

import numpy as np
import pandas as pd

from src.evaluator import backtest_method, summarize_backtest


df = pd.read_csv("data/processed/draws_clean.csv")

methods = ["random", "frequency", "hybrid"]

number_of_runs = 30

all_summaries = []

for run_id in range(1, number_of_runs + 1):
    print(f"\nRun {run_id}/{number_of_runs}")

    random.seed(run_id)
    np.random.seed(run_id)

    for method in methods:
        print(f"  Backtesting method: {method}")

        results = backtest_method(
            df=df,
            method=method,
            start_index=200,
        )

        summary = summarize_backtest(results)
        summary["run_id"] = run_id

        all_summaries.append(summary)


all_summaries_df = pd.DataFrame(all_summaries)

detailed_output_path = "outputs/repeated_backtest_detailed.csv"
all_summaries_df.to_csv(detailed_output_path, index=False)

final_summary = (
    all_summaries_df
    .groupby("method")
    .agg(
        runs=("run_id", "count"),
        mean_avg_main_matches=("avg_main_matches", "mean"),
        std_avg_main_matches=("avg_main_matches", "std"),
        mean_avg_star_matches=("avg_star_matches", "mean"),
        std_avg_star_matches=("avg_star_matches", "std"),
        mean_avg_total_matches=("avg_total_matches", "mean"),
        std_avg_total_matches=("avg_total_matches", "std"),
        best_avg_total_matches=("avg_total_matches", "max"),
        worst_avg_total_matches=("avg_total_matches", "min"),
    )
    .reset_index()
)

numeric_columns = final_summary.select_dtypes(include=["float"]).columns

for column in numeric_columns:
    final_summary[column] = final_summary[column].round(4)

summary_output_path = "outputs/repeated_backtest_summary.csv"
final_summary.to_csv(summary_output_path, index=False)

print("\nRepeated backtest summary:")
print(final_summary)

print(f"\nSaved detailed results to: {detailed_output_path}")
print(f"Saved final summary to: {summary_output_path}")