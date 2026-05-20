from src.data_loader import load_all_raw_data, basic_cleaning, validate_draws


raw_df = load_all_raw_data("data/raw")

print("Raw data loaded successfully.")
print("Raw shape:", raw_df.shape)
print("\nRaw columns:")
print(raw_df.columns.tolist())
print("\nRaw preview:")
print(raw_df.head())

clean_df = basic_cleaning(raw_df)

validate_draws(clean_df)

print("\nClean data created successfully.")
print("Clean shape:", clean_df.shape)
print("\nClean preview:")
print(clean_df.head())

print("\nDate range:")
print("First draw:", clean_df["date"].min())
print("Last draw:", clean_df["date"].max())

clean_df.to_csv("data/processed/draws_clean.csv", index=False)

print("\nCleaned data saved to:")
print("data/processed/draws_clean.csv")