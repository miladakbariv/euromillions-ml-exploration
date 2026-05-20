import pandas as pd
import matplotlib.pyplot as plt

from src.features import main_number_frequencies, star_frequencies


df = pd.read_csv("data/processed/draws_clean.csv")

main_freq = main_number_frequencies(df)
star_freq = star_frequencies(df)


# Plot main number frequencies
plt.figure(figsize=(12, 5))

plt.bar(
    main_freq.index,
    main_freq.values,
)

plt.title("EuroMillions Main Number Frequencies")
plt.xlabel("Main Number")
plt.ylabel("Frequency")
plt.xticks(range(1, 51))
plt.tight_layout()

main_output_path = "outputs/figures/main_number_frequencies.png"
plt.savefig(main_output_path, dpi=300)

print(f"Main number frequency plot saved to: {main_output_path}")

plt.show()


# Plot Lucky Star frequencies
plt.figure(figsize=(8, 5))

plt.bar(
    star_freq.index,
    star_freq.values,
)

plt.title("EuroMillions Lucky Star Frequencies")
plt.xlabel("Lucky Star")
plt.ylabel("Frequency")
plt.xticks(range(1, 13))
plt.tight_layout()

star_output_path = "outputs/figures/lucky_star_frequencies.png"
plt.savefig(star_output_path, dpi=300)

print(f"Lucky Star frequency plot saved to: {star_output_path}")

plt.show()