import pandas as pd
import matplotlib.pyplot as plt

from src.features import add_draw_statistics


df = pd.read_csv("data/processed/draws_clean.csv")

df_stats = add_draw_statistics(df)


# Plot distribution of the sum of main numbers
plt.figure(figsize=(10, 5))

plt.hist(
    df_stats["main_sum"],
    bins=30,
    edgecolor="black",
)

plt.title("Distribution of Main Number Sums")
plt.xlabel("Sum of 5 Main Numbers")
plt.ylabel("Number of Draws")
plt.tight_layout()

sum_output_path = "outputs/figures/main_sum_distribution.png"
plt.savefig(sum_output_path, dpi=300)

print(f"Main sum distribution plot saved to: {sum_output_path}")

plt.show()


# Plot odd number count distribution
odd_counts = df_stats["odd_count"].value_counts().sort_index()

plt.figure(figsize=(8, 5))

plt.bar(
    odd_counts.index,
    odd_counts.values,
)

plt.title("Distribution of Odd Number Counts")
plt.xlabel("Number of Odd Main Numbers in a Draw")
plt.ylabel("Number of Draws")
plt.xticks(range(0, 6))
plt.tight_layout()

odd_output_path = "outputs/figures/odd_count_distribution.png"
plt.savefig(odd_output_path, dpi=300)

print(f"Odd count distribution plot saved to: {odd_output_path}")

plt.show()


# Plot low number count distribution
low_counts = df_stats["low_count"].value_counts().sort_index()

plt.figure(figsize=(8, 5))

plt.bar(
    low_counts.index,
    low_counts.values,
)

plt.title("Distribution of Low Number Counts")
plt.xlabel("Number of Low Main Numbers in a Draw")
plt.ylabel("Number of Draws")
plt.xticks(range(0, 6))
plt.tight_layout()

low_output_path = "outputs/figures/low_count_distribution.png"
plt.savefig(low_output_path, dpi=300)

print(f"Low count distribution plot saved to: {low_output_path}")

plt.show()