from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Data.csv"


@st.cache_data
def load_data():
    """Load and clean the Noongar seasonal calendar dataset."""

    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    text_columns = df.select_dtypes(include="object").columns
    for column in text_columns:
        df[column] = df[column].fillna("").astype(str).str.strip()

    return df