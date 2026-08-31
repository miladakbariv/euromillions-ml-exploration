import random

import numpy as np
import pandas as pd
import pytest

from src.baselines import random_ticket
from src.evaluator import evaluate_ticket
from src.features import add_draw_statistics, main_number_frequencies, star_frequencies
from src.recommender import EuroMillionsRecommender


def sample_history() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"date": "2026-01-01", "n1": 1, "n2": 2, "n3": 3, "n4": 4, "n5": 5, "star1": 1, "star2": 2},
            {"date": "2026-01-08", "n1": 6, "n2": 7, "n3": 8, "n4": 9, "n5": 10, "star1": 3, "star2": 4},
            {"date": "2026-01-15", "n1": 11, "n2": 12, "n3": 13, "n4": 14, "n5": 15, "star1": 5, "star2": 6},
            {"date": "2026-01-22", "n1": 16, "n2": 17, "n3": 18, "n4": 19, "n5": 20, "star1": 7, "star2": 8},
        ]
    )


def assert_valid_ticket(ticket: dict) -> None:
    main_numbers = ticket["main_numbers"]
    lucky_stars = ticket["lucky_stars"]

    assert len(main_numbers) == 5
    assert len(set(main_numbers)) == 5
    assert all(1 <= number <= 50 for number in main_numbers)

    assert len(lucky_stars) == 2
    assert len(set(lucky_stars)) == 2
    assert all(1 <= star <= 12 for star in lucky_stars)


def test_random_ticket_respects_euromillions_rules() -> None:
    random.seed(42)
    ticket = random_ticket()

    assert ticket["method"] == "random"
    assert_valid_ticket(ticket)


@pytest.mark.parametrize("method", ["random", "frequency", "hybrid"])
def test_recommender_methods_return_valid_tickets(method: str) -> None:
    random.seed(42)
    np.random.seed(42)

    ticket = EuroMillionsRecommender(sample_history()).recommend(method=method)

    assert ticket["method"] == method
    assert_valid_ticket(ticket)


def test_recommender_rejects_unknown_method() -> None:
    with pytest.raises(ValueError, match="Unknown method"):
        EuroMillionsRecommender(sample_history()).recommend(method="unknown")


def test_frequency_features_cover_full_number_domains() -> None:
    history = sample_history()

    main_freq = main_number_frequencies(history)
    star_freq = star_frequencies(history)

    assert list(main_freq.index) == list(range(1, 51))
    assert list(star_freq.index) == list(range(1, 13))
    assert int(main_freq.sum()) == len(history) * 5
    assert int(star_freq.sum()) == len(history) * 2


def test_evaluate_ticket_counts_set_intersections() -> None:
    main_matches, star_matches = evaluate_ticket(
        predicted_main=[1, 2, 3, 4, 5],
        predicted_stars=[1, 2],
        true_main=[3, 4, 5, 6, 7],
        true_stars=[2, 3],
    )

    assert main_matches == 3
    assert star_matches == 1


def test_add_draw_statistics_creates_expected_features() -> None:
    enriched = add_draw_statistics(sample_history())
    first = enriched.iloc[0]

    assert first["main_sum"] == 15
    assert first["main_mean"] == 3
    assert first["main_min"] == 1
    assert first["main_max"] == 5
    assert first["main_range"] == 4
    assert first["odd_count"] == 3
    assert first["even_count"] == 2
    assert first["low_count"] == 5
    assert first["high_count"] == 0
