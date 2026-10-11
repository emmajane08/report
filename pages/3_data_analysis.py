import streamlit as st

from data_processing.data_loader import load_data


st.set_page_config(
    page_title="Seasonal Indicators",
    page_icon="📊",
    layout="wide",
)


df = load_data()

st.title("📊 Seasonal Indicators")

st.subheader("Indicators by type")
st.bar_chart(df["Indicator_type"].value_counts())

st.subheader("Indicators by season")
st.bar_chart(df["Season_Name"].value_counts())

st.subheader("Dataset")
st.dataframe(df, use_container_width=True)