import pandas as pd
import matplotlib.pyplot as plt


summary_path = "outputs/repeated_backtest_summary.csv"

summary_df = pd.read_csv(summary_path)

print("Repeated backtest summary loaded:")
print(summary_df)

plt.figure(figsize=(8, 5))

plt.bar(
    summary_df["method"],
    summary_df["mean_avg_total_matches"],
    yerr=summary_df["std_avg_total_matches"],
    capsize=5,
)

plt.title("Repeated Backtest: Average Total Matches by Method")
plt.xlabel("Method")
plt.ylabel("Mean Average Total Matches")
plt.tight_layout()

output_path = "outputs/figures/repeated_backtest_total_matches.png"
plt.savefig(output_path, dpi=300)

print(f"\nPlot saved to: {output_path}")

plt.show()