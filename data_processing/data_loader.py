# Import Path to build a portable path to the CSV file.
from pathlib import Path

# Import pandas for CSV reading and Streamlit for cached loading.
import pandas as pd
import streamlit as st


# Resolve the dataset path relative to this module's location.
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Data.csv"


# Cache the result so repeated Streamlit reruns do not reread the CSV.
@st.cache_data
def load_data():
    """Load and clean the Noongar seasonal calendar dataset."""

    # Read the CSV file into a pandas DataFrame.
    df = pd.read_csv(DATA_PATH)

    # Remove accidental spaces around column names.
    df.columns = df.columns.str.strip()

    # Find text columns so missing values and surrounding spaces can be cleaned.
    text_columns = df.select_dtypes(include="object").columns
    # Clean each text column by filling blanks, converting to strings, and trimming.
    for column in text_columns:
        df[column] = df[column].fillna("").astype(str).str.strip()

    # Return the cleaned table to the calling page or function.
    return df