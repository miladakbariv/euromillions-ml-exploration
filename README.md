# EuroMillions ML Exploration

A compact ML-engineering case study on **responsible evaluation of stochastic strategies** using historical EuroMillions draw data.

This repository is not a lottery predictor. EuroMillions draws are random by design; the project is intentionally built around that constraint. The engineering goal is to demonstrate data cleaning, baseline design, leakage-aware chronological backtesting, repeated evaluation across random seeds, reproducibility, testing, and a lightweight Streamlit interface.

## Problem

Historical frequency patterns can look persuasive even when the underlying process is random. The core question here is therefore not “which numbers will win?”, but:

> Can simple frequency-informed strategies demonstrate a stable advantage over a random baseline under chronological, leakage-free evaluation?

## Approach

The pipeline compares three ticket-generation strategies:

- **Random baseline** — uniform sampling of 5 main numbers and 2 Lucky Stars.
- **Frequency-based** — weighted sampling from historical occurrence frequencies.
- **Hybrid** — a controlled mix of historically hot, cold, and random selections.

Evaluation is chronological: for each test draw, only earlier draws are available to the recommender. Because all three strategies contain stochastic components, the backtest is repeated across multiple random seeds rather than relying on a single lucky run.

## Evaluation

The committed summary contains **30 repeated backtest runs per method**.

| Method | Avg. main matches | Avg. star matches | Avg. total matches | Std. total |
| --- | ---: | ---: | ---: | ---: |
| Frequency | 0.5052 | 0.3345 | **0.8397** | 0.0254 |
| Hybrid | 0.4989 | 0.3319 | 0.8308 | 0.0250 |
| Random | 0.4957 | 0.3302 | 0.8259 | 0.0333 |

### Main conclusion

The methods remain close to the random baseline. The small observed differences are not evidence of a predictive edge and should not be interpreted as improved odds of winning. That result is the point of the exercise: a credible ML workflow should preserve a strong baseline and communicate uncertainty instead of turning noise into a prediction claim.

The exact aggregate results used above are stored in [`outputs/repeated_backtest_summary.csv`](outputs/repeated_backtest_summary.csv).

## Project Structure

```text
.
├── app/
│   └── streamlit_app.py
├── data/
│   └── processed/
│       └── draws_clean.csv
├── outputs/
│   └── repeated_backtest_summary.csv
├── scripts/
│   ├── check_backtest.py
│   ├── check_repeated_backtest.py
│   └── plot_*.py
├── src/
│   ├── baselines.py
│   ├── data_loader.py
│   ├── evaluator.py
│   ├── features.py
│   └── recommender.py
├── tests/
│   └── test_core.py
├── requirements.txt
├── requirements-dev.txt
└── runtime.txt
```

## Quick Start

Python 3.11 is the reference runtime.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Generate a ticket from the CLI:

```bash
python -m src.cli --method random
python -m src.cli --method frequency
python -m src.cli --method hybrid
```

Run the repeated backtest:

```bash
python -m scripts.check_repeated_backtest
```

Launch the Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

## Tests

Development dependencies are kept separate from the runtime dependencies.

```bash
pip install -r requirements-dev.txt
pytest -q
```

GitHub Actions runs the same test suite on pushes and pull requests.

## Data

The repository includes the cleaned dataset used by the app at `data/processed/draws_clean.csv`. Raw yearly files are intentionally not redistributed. They were sourced from win2day.at and should be downloaded from the original provider if the preprocessing step needs to be reproduced from source files.

## What This Project Demonstrates

- Baseline-first experimental design
- Chronological evaluation without future-data leakage
- Repeated stochastic experiments and variance reporting
- Responsible interpretation of statistical results
- Modular Python project structure
- Automated tests and CI
- Reproducible Streamlit packaging

## Limitations

- EuroMillions draws are random and independent.
- Historical frequency does not establish future predictability.
- The reported gaps between methods are small and may be explained by randomness.
- This project is educational and does not provide gambling or financial advice.

## Future Work

- Add confidence intervals and formal significance testing around repeated backtests.
- Automate data refresh and validation while preserving chronological evaluation.
- Add containerized reproducibility for the app and experiment scripts.

## License

Released under the [MIT License](LICENSE).
