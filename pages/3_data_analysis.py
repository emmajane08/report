import streamlit as st
import pandas as pd

from data_processing.data_loader import load_data


st.set_page_config(
    page_title="Data & Visualisations",
    page_icon="📊",
    layout="wide"
)


df = load_data()


st.title("📊 Data & Visualisations")


st.subheader("Indicators by type")

indicator_counts = (
    df["Indicator_type"]
    .value_counts()
)

st.bar_chart(indicator_counts)


st.subheader("Indicators by season")

season_counts = (
    df["Season_Name"]
    .value_counts()
)

st.bar_chart(season_counts)


st.subheader("Dataset")

st.dataframe(
    df,
    use_container_width=True
)