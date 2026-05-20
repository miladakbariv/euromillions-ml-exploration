import random

import numpy as np
import pandas as pd

from src.baselines import random_ticket
from src.features import main_number_frequencies, star_frequencies


class EuroMillionsRecommender:
    """
    A responsible EuroMillions number recommender.

    This class does not claim to predict lottery outcomes.
    It generates candidate tickets using random and statistical strategies.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def recommend(self, method: str = "random") -> dict:
        """
        Generate one EuroMillions ticket using the selected method.
        """
        if method == "random":
            return random_ticket()

        if method == "frequency":
            return self._frequency_ticket()

        if method == "hybrid":
            return self._hybrid_ticket()

        raise ValueError(f"Unknown method: {method}")

    def _frequency_ticket(self) -> dict:
        """
        Generate a ticket using historical frequency as probability weight.

        Numbers that appeared more often in the past receive higher sampling weight.
        """
        main_freq = main_number_frequencies(self.df)
        star_freq = star_frequencies(self.df)

        main_numbers = self._weighted_sample_without_replacement(
            items=list(range(1, 51)),
            weights=main_freq.values,
            k=5,
        )

        lucky_stars = self._weighted_sample_without_replacement(
            items=list(range(1, 13)),
            weights=star_freq.values,
            k=2,
        )

        return {
            "main_numbers": sorted(main_numbers),
            "lucky_stars": sorted(lucky_stars),
            "method": "frequency",
        }

    def _hybrid_ticket(self) -> dict:
        """
        Generate a hybrid ticket.

        Strategy:
        - 2 numbers from hot main numbers
        - 2 numbers from cold main numbers
        - 1 random main number
        - 1 star from hot Lucky Stars
        - 1 random Lucky Star
        """
        main_freq = main_number_frequencies(self.df)
        star_freq = star_frequencies(self.df)

        hot_main = main_freq.sort_values(ascending=False).head(15).index.tolist()
        cold_main = main_freq.sort_values(ascending=True).head(15).index.tolist()

        selected_main = set()

        selected_main.update(random.sample(hot_main, 2))
        selected_main.update(random.sample(cold_main, 2))

        while len(selected_main) < 5:
            selected_main.add(random.randint(1, 50))

        hot_stars = star_freq.sort_values(ascending=False).head(5).index.tolist()

        selected_stars = set()

        selected_stars.update(random.sample(hot_stars, 1))

        while len(selected_stars) < 2:
            selected_stars.add(random.randint(1, 12))

        return {
            "main_numbers": sorted(selected_main),
            "lucky_stars": sorted(selected_stars),
            "method": "hybrid",
        }

    @staticmethod
    def _weighted_sample_without_replacement(items, weights, k):
        """
        Sample k unique items using probability weights.
        """
        items = np.array(items)
        weights = np.array(weights, dtype=float)

        if weights.sum() == 0:
            weights = np.ones_like(weights)

        probabilities = weights / weights.sum()

        selected = np.random.choice(
            items,
            size=k,
            replace=False,
            p=probabilities,
        )

        return selected.tolist()