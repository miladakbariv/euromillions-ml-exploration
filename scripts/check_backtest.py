import pandas as pd

from src.evaluator import backtest_method, summarize_backtest


df = pd.read_csv("data/processed/draws_clean.csv")

methods = ["random", "frequency", "hybrid"]

summary_rows = []

for method in methods:
    print(f"\nRunning backtest for method: {method}")

    results = backtest_method(
        df=df,
        method=method,
        start_index=200,
    )

    summary = summarize_backtest(results)
    summary_rows.append(summary)

    print(summary)

    output_path = f"outputs/{method}_backtest_results.csv"
    results.to_csv(output_path, index=False)

    print(f"Saved results to: {output_path}")


summary_df = pd.DataFrame(summary_rows)

summary_output_path = "outputs/backtest_summary.csv"
summary_df.to_csv(summary_output_path, index=False)

print("\nBacktest summary:")
print(summary_df)

print(f"\nSaved summary to: {summary_output_path}")