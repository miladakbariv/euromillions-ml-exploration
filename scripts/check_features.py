import pandas as pd

from src.features import (
    main_number_frequencies,
    star_frequencies,
    get_hot_numbers,
    get_cold_numbers,
    get_hot_stars,
    get_cold_stars,
    add_draw_statistics,
)


df = pd.read_csv("data/processed/draws_clean.csv")

print("Clean data loaded successfully.")
print("Shape:", df.shape)

print("\nMain number frequencies:")
main_freq = main_number_frequencies(df)
print(main_freq)

print("\nLucky Star frequencies:")
star_freq = star_frequencies(df)
print(star_freq)

print("\nTop 10 hot main numbers:")
print(get_hot_numbers(df, top_k=10))

print("\nTop 10 cold main numbers:")
print(get_cold_numbers(df, top_k=10))

print("\nTop 5 hot Lucky Stars:")
print(get_hot_stars(df, top_k=5))

print("\nTop 5 cold Lucky Stars:")
print(get_cold_stars(df, top_k=5))

df_with_stats = add_draw_statistics(df)

print("\nData with extra statistics:")
print(df_with_stats.head())

print("\nSelected statistical columns:")
print(df_with_stats[["main_sum", "main_mean", "odd_count", "even_count", "low_count", "high_count"]].head())