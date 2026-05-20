# EuroMillions ML Exploration

A statistical and machine-learning-style exploration of EuroMillions historical draw data.

This project analyzes historical EuroMillions results, builds several number recommendation strategies, compares them through chronological backtesting, and provides a simple Streamlit app for interactive exploration.

## Important Disclaimer

This project is for educational and portfolio purposes only.

It does not predict lottery outcomes and does not increase the probability of winning. EuroMillions draws are random by design. The goal of this project is to practice data cleaning, exploratory data analysis, probability, baseline design, backtesting, repeated experiment evaluation, and responsible interpretation of results.

## Project Goals

The main goals of this project are:

* Load and clean historical EuroMillions draw data
* Analyze number frequencies
* Identify hot and cold numbers
* Generate lottery tickets using different strategies
* Compare strategies using chronological backtesting
* Repeat backtesting across multiple random seeds
* Build a simple Streamlit web app
* Practice an end-to-end data science workflow

## Dataset

The historical EuroMillions draw data used in this project was collected from win2day.at.

The raw files are yearly CSV files containing EuroMillions draw results and additional prize/rank information. During preprocessing, only the actual draw information is extracted and standardized.

Each cleaned draw contains:

* Draw date
* 5 main numbers
* 2 Lucky Stars

The cleaned dataset has the following columns:

```text
date, n1, n2, n3, n4, n5, star1, star2
```

Raw data files are stored locally inside:

```text
data/raw/
```

The cleaned dataset is generated as:

```text
data/processed/draws_clean.csv
```

The raw and processed data folders are not included in GitHub by default. Users who want to reproduce the project should download the historical EuroMillions CSV files from win2day.at and place them inside `data/raw/`.

## Data Source

Historical EuroMillions result files were obtained from win2day.at.

This repository does not redistribute the raw data files. The data folders are excluded from version control, and users should obtain the original files from the data provider if they want to reproduce the analysis.

## Recommendation Methods

### 1. Random Baseline

The random method generates:

* 5 unique main numbers from 1 to 50
* 2 unique Lucky Stars from 1 to 12

This is the baseline method because a fair lottery draw is random.

### 2. Frequency-Based Method

The frequency method gives slightly higher selection probability to numbers that appeared more often in the historical data.

This method is useful for statistical exploration, but it does not prove future predictability.

### 3. Hybrid Method

The hybrid method combines:

* 2 hot main numbers
* 2 cold main numbers
* 1 random main number
* 1 hot Lucky Star
* 1 random Lucky Star

This method balances historical frequency information with randomness.

## Backtesting

The project uses chronological backtesting.

For each historical draw in the test period:

1. Only previous draws are used as historical data.
2. A ticket is generated.
3. The generated ticket is compared with the actual draw.
4. The number of matched main numbers and Lucky Stars is recorded.

This avoids data leakage because future draw results are not used when generating past predictions.

## Repeated Backtesting

Because the recommendation methods include randomness, a single backtest run is not enough.

The project also performs repeated backtesting across multiple random seeds and reports:

* Mean average main matches
* Mean average Lucky Star matches
* Mean average total matches
* Standard deviation
* Best observed run
* Worst observed run

The results show that all methods perform close to the random baseline, which is expected for a fair lottery system.

## Project Structure

```text
euromillions-ml-exploration/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── outputs/
│   └── figures/
│
├── scripts/
│   ├── check_data.py
│   ├── check_features.py
│   ├── check_baselines.py
│   ├── check_recommender.py
│   ├── check_backtest.py
│   ├── check_repeated_backtest.py
│   ├── plot_frequencies.py
│   ├── plot_draw_statistics.py
│   └── plot_backtest_results.py
│
├── src/
│   ├── __init__.py
│   ├── baselines.py
│   ├── cli.py
│   ├── data_loader.py
│   ├── evaluator.py
│   ├── features.py
│   └── recommender.py
│
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Create and activate a Python environment.

Using conda:

```bash
conda create -n euromillions-ml python=3.11
conda activate euromillions-ml
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Important Usage Note

Run all commands from the project root directory, not from inside the `scripts/` folder.

Example project root:

```text
euromillions-ml-exploration/
```

## Data Preparation

Place the raw yearly EuroMillions CSV files inside:

```text
data/raw/
```

Then run:

```bash
python -m scripts.check_data
```

This creates:

```text
data/processed/draws_clean.csv
```

## Run the Command-Line Recommender

Generate one hybrid ticket:

```bash
python -m src.cli --method hybrid
```

Generate five random tickets:

```bash
python -m src.cli --method random --tickets 5
```

Generate three frequency-based tickets:

```bash
python -m src.cli --method frequency --tickets 3
```

## Run Backtesting

Run a single backtest comparison:

```bash
python -m scripts.check_backtest
```

Run repeated backtesting:

```bash
python -m scripts.check_repeated_backtest
```

The repeated backtest creates:

```text
outputs/repeated_backtest_detailed.csv
outputs/repeated_backtest_summary.csv
```

## Generate Plots

Frequency plots:

```bash
python -m scripts.plot_frequencies
```

Draw statistics plots:

```bash
python -m scripts.plot_draw_statistics
```

Backtest comparison plot:

```bash
python -m scripts.plot_backtest_results
```

Generated figures are saved inside:

```text
outputs/figures/
```

## Run the Streamlit App

Start the app:

```bash
streamlit run app/streamlit_app.py
```

The app includes:

* Dataset summary
* Ticket generation
* Random, frequency, and hybrid methods
* Method explanations
* Visual ticket display
* Hot and cold number tables
* Frequency charts
* Repeated backtest results

## Key Learning Outcomes

This project demonstrates:

* Python project organization
* Data loading and cleaning
* Pandas-based exploratory data analysis
* Frequency analysis
* Random sampling
* Weighted sampling
* Baseline design
* Chronological backtesting
* Repeated experiment evaluation
* Streamlit app development
* Responsible communication of model limitations

## Limitations

This project should not be interpreted as a lottery prediction system.

Important limitations:

* Lottery draws are random and independent.
* Historical frequency does not guarantee future occurrence.
* Small differences in backtest performance may be due to randomness.
* The generated tickets are for educational exploration only.
* The project does not provide financial or gambling advice.

## Future Work

Possible improvements:

* Add a multi-label machine learning model
* Add rolling-window frequency features
* Add confidence intervals for repeated backtests
* Add statistical significance testing
* Add unit tests
* Add Docker support
* Deploy the Streamlit app online
* Improve the UI design
* Add automated data update scripts

## License

This project is intended for educational use.

The code may be shared and modified according to the repository license. The raw lottery data is not redistributed in this repository and should be obtained from the original data provider.
