from pathlib import Path
import pandas as pd


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Data.csv"


def load_data():
    """Load and clean the Noongar seasonal calendar dataset."""

    df = pd.read_csv(DATA_PATH)

    # Remove accidental spaces from column names
    df.columns = df.columns.str.strip()

    # Clean text fields
    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].fillna("").astype(str).str.strip()

    return df

# whenever you need the dataset, you simply do:
# from data_processing.data_loader import load_data
# df = load_data()