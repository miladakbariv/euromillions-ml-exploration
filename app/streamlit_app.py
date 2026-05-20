import sys
from pathlib import Path

import pandas as pd
import streamlit as st

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.recommender import EuroMillionsRecommender
from src.features import (
    main_number_frequencies,
    star_frequencies,
    get_hot_numbers,
    get_cold_numbers,
    get_hot_stars,
    get_cold_stars,
)


def inject_custom_css() -> None:
    """
    Add custom CSS for ticket visualization and layout.
    """
    st.markdown(
        """
        <style>
        .ticket-box {
            background-color: #0f2d5c;
            padding: 18px 22px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            gap: 14px;
            flex-wrap: wrap;
            margin-top: 8px;
            margin-bottom: 18px;
        }

        .main-ball {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background-color: #16a34a;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 22px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        }

        .stars-group {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-left: 10px;
        }

        .lucky-star {
            width: 60px;
            height: 60px;
            background-color: #f2c94c;
            color: #111111;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 21px;
            clip-path: polygon(
                50% 0%,
                61% 35%,
                98% 35%,
                68% 57%,
                79% 91%,
                50% 70%,
                21% 91%,
                32% 57%,
                2% 35%,
                39% 35%
            );
        }

        .method-note {
            background-color: #f8fafc;
            border-left: 4px solid #2563eb;
            padding: 12px 14px;
            border-radius: 8px;
            margin-top: 8px;
            margin-bottom: 18px;
            color: #1f2937;
            font-size: 15px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 10px;
            margin-bottom: 28px;
        }

        .summary-card {
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 14px 16px;
        }

        .summary-label {
            color: #4b5563;
            font-size: 14px;
            margin-bottom: 6px;
        }

        .summary-value {
            color: #111827;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_ticket_html(main_numbers: list[int], lucky_stars: list[int]) -> str:
    """
    Render a complete EuroMillions ticket as HTML.
    """
    main_html = "".join(
        f'<div class="main-ball">{number}</div>' for number in main_numbers
    )

    stars_html = "".join(
        f'<div class="lucky-star">{star}</div>' for star in lucky_stars
    )

    return f"""
    <div class="ticket-box">
        {main_html}
        <div class="stars-group">
            {stars_html}
        </div>
    </div>
    """


def get_method_explanation(method: str) -> str:
    """
    Return a short explanation for each recommendation method.
    """
    explanations = {
        "random": (
            "Random method chooses 5 main numbers and 2 Lucky Stars completely at random. "
            "This is the fair baseline because EuroMillions draws are designed to be random."
        ),
        "frequency": (
            "Frequency method gives slightly higher selection probability to numbers that appeared "
            "more often in the historical data. It is useful for statistical exploration, but it does "
            "not prove future predictability."
        ),
        "hybrid": (
            "Hybrid method combines 2 hot numbers, 2 cold numbers, and 1 random number. "
            "For Lucky Stars, it combines 1 hot star and 1 random star. This keeps a balance between "
            "historical patterns and randomness."
        ),
    }

    return explanations.get(method, "")


st.set_page_config(
    page_title="EuroMillions ML Exploration",
    layout="centered",
)

inject_custom_css()

st.title("EuroMillions ML Exploration")

st.warning(
    "This project is for educational purposes only. "
    "Lottery draws are random, and this app does not predict winning numbers."
)

data_path = "data/processed/draws_clean.csv"

try:
    df = pd.read_csv(data_path)

    st.subheader("Dataset Summary")

    first_draw = str(df["date"].min())[:10]
    last_draw = str(df["date"].max())[:10]

    st.markdown(
        f"""
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-label">Number of Draws</div>
                <div class="summary-value">{len(df)}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">First Draw</div>
                <div class="summary-value">{first_draw}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">Last Draw</div>
                <div class="summary-value">{last_draw}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Generate Ticket")

    method = st.selectbox(
        "Choose recommendation method",
        ["random", "frequency", "hybrid"],
        index=2,
    )

    st.markdown(
        f"""
        <div class="method-note">
            <strong>Method explanation:</strong><br>
            {get_method_explanation(method)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    number_of_tickets = st.slider(
        "Number of tickets",
        min_value=1,
        max_value=10,
        value=1,
    )

    recommender = EuroMillionsRecommender(df)

    if st.button("Generate"):
        st.subheader("Recommended Tickets")

        for i in range(number_of_tickets):
            ticket = recommender.recommend(method=method)

            st.write(f"Ticket {i + 1}")

            ticket_html = render_ticket_html(
                main_numbers=ticket["main_numbers"],
                lucky_stars=ticket["lucky_stars"],
            )

            st.markdown(ticket_html, unsafe_allow_html=True)

    st.subheader("Historical Number Analysis")

    with st.expander("Show hot and cold number tables"):
        hot_main_df = (
            get_hot_numbers(df, top_k=10)
            .reset_index()
            .rename(columns={"index": "Number", "count": "Frequency"})
        )

        cold_main_df = (
            get_cold_numbers(df, top_k=10)
            .reset_index()
            .rename(columns={"index": "Number", "count": "Frequency"})
        )

        hot_stars_df = (
            get_hot_stars(df, top_k=5)
            .reset_index()
            .rename(columns={"index": "Lucky Star", "count": "Frequency"})
        )

        cold_stars_df = (
            get_cold_stars(df, top_k=5)
            .reset_index()
            .rename(columns={"index": "Lucky Star", "count": "Frequency"})
        )

        st.write("Top 10 Hot Main Numbers")
        st.dataframe(
            hot_main_df,
            hide_index=True,
            use_container_width=True,
        )

        st.write("Top 10 Cold Main Numbers")
        st.dataframe(
            cold_main_df,
            hide_index=True,
            use_container_width=True,
        )

        st.write("Top 5 Hot Lucky Stars")
        st.dataframe(
            hot_stars_df,
            hide_index=True,
            use_container_width=True,
        )

        st.write("Top 5 Cold Lucky Stars")
        st.dataframe(
            cold_stars_df,
            hide_index=True,
            use_container_width=True,
        )

    st.subheader("Frequency Charts")

    main_freq = main_number_frequencies(df)
    star_freq = star_frequencies(df)

    with st.expander("Show frequency charts", expanded=True):
        st.write("Main Number Frequencies")
        st.bar_chart(main_freq)

        st.write("Lucky Star Frequencies")
        st.bar_chart(star_freq)

    st.subheader("Backtest Results")

    backtest_summary_path = "outputs/repeated_backtest_summary.csv"

    try:
        backtest_summary_df = pd.read_csv(backtest_summary_path)

        with st.expander("Show repeated backtest summary", expanded=True):
            st.write(
                "This table compares the recommendation methods over repeated historical backtests. "
                "The values are average matches per ticket, not winning probabilities."
            )

            st.dataframe(
                backtest_summary_df,
                hide_index=True,
                use_container_width=True,
            )

            st.write("Mean Average Total Matches")
            st.bar_chart(
                backtest_summary_df.set_index("method")[
                    "mean_avg_total_matches"
                ]
            )

    except FileNotFoundError:
        st.info(
            "Backtest summary file not found yet. "
            "Run check_repeated_backtest.py to generate it."
        )

except FileNotFoundError:
    st.error(
        "Cleaned data file not found. "
        "Please run check_data.py first to create data/processed/draws_clean.csv."
    )

except Exception as error:
    st.error(f"Something went wrong: {error}")