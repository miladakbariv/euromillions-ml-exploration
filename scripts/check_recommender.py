import pandas as pd

from src.recommender import EuroMillionsRecommender


df = pd.read_csv("data/processed/draws_clean.csv")

recommender = EuroMillionsRecommender(df)

print("Random ticket:")
print(recommender.recommend(method="random"))

print("\nFrequency-based ticket:")
print(recommender.recommend(method="frequency"))

print("\nHybrid ticket:")
print(recommender.recommend(method="hybrid"))

print("\nFive hybrid tickets:")
for _ in range(5):
    print(recommender.recommend(method="hybrid"))