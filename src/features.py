import pandas as pd


def main_number_frequencies(df: pd.DataFrame) -> pd.Series:
    """
    Count how often each main number appeared.

    EuroMillions main numbers are from 1 to 50.
    """
    main_columns = ["n1", "n2", "n3", "n4", "n5"]

    all_numbers = df[main_columns].values.flatten()

    frequencies = pd.Series(all_numbers).value_counts().sort_index()

    return frequencies.reindex(range(1, 51), fill_value=0)


def star_frequencies(df: pd.DataFrame) -> pd.Series:
    """
    Count how often each Lucky Star appeared.

    EuroMillions Lucky Stars are from 1 to 12.
    """
    star_columns = ["star1", "star2"]

    all_stars = df[star_columns].values.flatten()

    frequencies = pd.Series(all_stars).value_counts().sort_index()

    return frequencies.reindex(range(1, 13), fill_value=0)


def get_hot_numbers(df: pd.DataFrame, top_k: int = 10) -> pd.Series:
    """
    Return the most frequent main numbers.
    """
    frequencies = main_number_frequencies(df)

    return frequencies.sort_values(ascending=False).head(top_k)


def get_cold_numbers(df: pd.DataFrame, top_k: int = 10) -> pd.Series:
    """
    Return the least frequent main numbers.
    """
    frequencies = main_number_frequencies(df)

    return frequencies.sort_values(ascending=True).head(top_k)


def get_hot_stars(df: pd.DataFrame, top_k: int = 5) -> pd.Series:
    """
    Return the most frequent Lucky Stars.
    """
    frequencies = star_frequencies(df)

    return frequencies.sort_values(ascending=False).head(top_k)


def get_cold_stars(df: pd.DataFrame, top_k: int = 5) -> pd.Series:
    """
    Return the least frequent Lucky Stars.
    """
    frequencies = star_frequencies(df)

    return frequencies.sort_values(ascending=True).head(top_k)


def add_draw_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple statistical features for each draw.

    These features are useful for exploratory data analysis.
    """
    df = df.copy()

    main_columns = ["n1", "n2", "n3", "n4", "n5"]

    df["main_sum"] = df[main_columns].sum(axis=1)
    df["main_mean"] = df[main_columns].mean(axis=1)
    df["main_min"] = df[main_columns].min(axis=1)
    df["main_max"] = df[main_columns].max(axis=1)
    df["main_range"] = df["main_max"] - df["main_min"]

    df["odd_count"] = df[main_columns].apply(
        lambda row: sum(number % 2 == 1 for number in row),
        axis=1,
    )

    df["even_count"] = 5 - df["odd_count"]

    df["low_count"] = df[main_columns].apply(
        lambda row: sum(number <= 25 for number in row),
        axis=1,
    )

    df["high_count"] = 5 - df["low_count"]

    return df