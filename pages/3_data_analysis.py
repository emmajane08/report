import streamlit as st
import pandas as pd

from data_processing.data_loader import load_data


SEASON_ORDER = ["Birak", "Bunuru", "Djeran", "Makuru", "Djilba", "Kambarang"]


st.set_page_config(
    page_title="Seasonal Indicators",
    page_icon="📊",
    layout="wide",
)


df = load_data()

st.title("📊 Seasonal Indicators")

st.subheader("Temperature changes with the seasons")
temperature_data = df[
    df["Indicator_Name"].isin(["Max Temperature ℃", "Min Temperature ℃"])
].copy()
temperature_data["Description"] = pd.to_numeric(temperature_data["Description"])

chart_data = temperature_data.pivot(
    index="Season_Name",
    columns="Indicator_Name",
    values="Description",
).reindex(SEASON_ORDER)

st.line_chart(chart_data, color=["#ff2424", "#5c6fff"])

st.subheader("Rainfall Changes with the season")
rainfall_data = df[df["Indicator_Name"] == "Rainfall (mm)"].copy()
rainfall_data["Description"] = pd.to_numeric(rainfall_data["Description"])

chart_data = rainfall_data.pivot(
    index="Season_Name",
    columns="Indicator_Name",
    values="Description",
).reindex(SEASON_ORDER)

st.line_chart(chart_data, color="#4e95c2")

st.subheader("Dataset")
st.dataframe(df, use_container_width=True)