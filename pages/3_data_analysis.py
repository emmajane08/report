# Import Streamlit for page display and pandas for table transformations.
import streamlit as st
import pandas as pd

# Import the shared function that loads the cleaned CSV data.
from data_processing.data_loader import load_data


# Keep chart rows in the cultural season sequence rather than alphabetical order.
SEASON_ORDER = ["Birak", "Bunuru", "Djeran", "Makuru", "Djilba", "Kambarang"]


# Configure this page's title, browser icon, and wide layout.
st.set_page_config(
    page_title="Seasonal Indicators",
    page_icon="📊",
    layout="wide",
)


# Load the dataset into a pandas DataFrame for the charts and table.
df = load_data()

# Add the page's main heading.
st.title("📊 Seasonal Indicators")

# Introduce the maximum- and minimum-temperature chart.
st.subheader("Temperature changes with the seasons")
# Keep only temperature records and make a copy for safe conversion.
temperature_data = df[
    df["Indicator_Name"].isin(["Max Temperature ℃", "Min Temperature ℃"])
# Make the filtered rows independent before changing their values.
].copy()
# Convert the description strings into numeric values for plotting.
temperature_data["Description"] = pd.to_numeric(temperature_data["Description"])

# Reshape temperature rows into one column per indicator and order the seasons.
chart_data = temperature_data.pivot(
    index="Season_Name",
    columns="Indicator_Name",
    values="Description",
).reindex(SEASON_ORDER)

# Draw the maximum- and minimum-temperature lines in the specified colors.
st.line_chart(chart_data, color=["#ff2424", "#5c6fff"])

# Introduce the rainfall chart.
st.subheader("Rainfall Changes with the season")
# Keep only rainfall records and make a copy before converting values.
rainfall_data = df[df["Indicator_Name"] == "Rainfall (mm)"].copy()
# Convert rainfall descriptions into numeric values for plotting.
rainfall_data["Description"] = pd.to_numeric(rainfall_data["Description"])

# Reshape rainfall records into chart form and order the seasons.
chart_data = rainfall_data.pivot(
    index="Season_Name",
    columns="Indicator_Name",
    values="Description",
).reindex(SEASON_ORDER)

# Draw the rainfall line in blue.
st.line_chart(chart_data, color="#4e95c2")

# Add a heading and show the complete dataset in a full-width table.
st.subheader("Dataset")
st.dataframe(df, use_container_width=True)