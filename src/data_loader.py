from pathlib import Path
import pandas as pd


def load_raw_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load one raw EuroMillions CSV file.

    The Austrian/German lottery CSV files usually use semicolon as separator.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    encodings_to_try = ["utf-8", "utf-8-sig", "latin1", "ISO-8859-1"]

    last_error = None

    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(
                file_path,
                sep=";",
                encoding=encoding,
            )
            df["source_file"] = file_path.name
            return df
        except UnicodeDecodeError as error:
            last_error = error

    raise ValueError(f"Could not read file: {file_path}. Last error: {last_error}")


def load_all_raw_data(folder_path: str | Path) -> pd.DataFrame:
    """
    Load all CSV files from a folder and combine them into one DataFrame.
    """
    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    csv_files = sorted(folder_path.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {folder_path}")

    dataframes = []

    for csv_file in csv_files:
        df = load_raw_data(csv_file)
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df


def clean_date_column(date_series: pd.Series) -> pd.Series:
    """
    Clean German/Austrian date strings like:
    'Di. 03.01.2017'
    'Fr. 06.01.2017'

    and convert them to pandas datetime.
    """
    extracted_dates = date_series.astype(str).str.extract(r"(\d{2}\.\d{2}\.\d{4})")[0]

    return pd.to_datetime(
        extracted_dates,
        format="%d.%m.%Y",
        errors="coerce",
    )


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the EuroMillions dataset.

    Expected final columns:
    date, n1, n2, n3, n4, n5, star1, star2
    """
    df = df.copy()

    df.columns = [col.strip().lower() for col in df.columns]

    possible_column_mapping = {
        "ziehungstag": "date",
        "drawdate": "date",
        "draw date": "date",
        "date": "date",

        "zahl1": "n1",
        "zahl2": "n2",
        "zahl3": "n3",
        "zahl4": "n4",
        "zahl5": "n5",

        "ball 1": "n1",
        "ball 2": "n2",
        "ball 3": "n3",
        "ball 4": "n4",
        "ball 5": "n5",

        "number 1": "n1",
        "number 2": "n2",
        "number 3": "n3",
        "number 4": "n4",
        "number 5": "n5",

        "n1": "n1",
        "n2": "n2",
        "n3": "n3",
        "n4": "n4",
        "n5": "n5",

        "stern1": "star1",
        "stern2": "star2",

        "lucky star 1": "star1",
        "lucky star 2": "star2",
        "star 1": "star1",
        "star 2": "star2",
        "star1": "star1",
        "star2": "star2",
    }

    df = df.rename(columns=possible_column_mapping)

    required_columns = ["date", "n1", "n2", "n3", "n4", "n5", "star1", "star2"]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Available columns: {df.columns.tolist()}"
        )

    df = df[required_columns]

    df["date"] = clean_date_column(df["date"])

    number_columns = ["n1", "n2", "n3", "n4", "n5", "star1", "star2"]

    for col in number_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=required_columns)

    for col in number_columns:
        df[col] = df[col].astype(int)

    df = df.drop_duplicates()
    df = df.sort_values("date").reset_index(drop=True)

    return df


def validate_draws(df: pd.DataFrame) -> None:
    """
    Validate EuroMillions number rules.

    Main numbers must be between 1 and 50.
    Lucky Stars must be between 1 and 12.
    Main numbers must be unique inside each draw.
    Lucky Stars must be unique inside each draw.
    """
    main_columns = ["n1", "n2", "n3", "n4", "n5"]
    star_columns = ["star1", "star2"]

    for idx, row in df.iterrows():
        main_numbers = row[main_columns].tolist()
        lucky_stars = row[star_columns].tolist()

        if not all(1 <= n <= 50 for n in main_numbers):
            raise ValueError(f"Invalid main number at row {idx}: {main_numbers}")

        if not all(1 <= s <= 12 for s in lucky_stars):
            raise ValueError(f"Invalid Lucky Star at row {idx}: {lucky_stars}")

        if len(set(main_numbers)) != 5:
            raise ValueError(f"Duplicate main numbers at row {idx}: {main_numbers}")

        if len(set(lucky_stars)) != 2:
            raise ValueError(f"Duplicate Lucky Stars at row {idx}: {lucky_stars}")