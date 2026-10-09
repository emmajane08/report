from pathlib import Path

import pandas as pd
import streamlit as st

data_file = Path(__file__).parent / "Data.csv"
data = pd.read_csv(data_file)
seasons = data["Season_Name"].dropna().unique().tolist()

st.set_page_config(page_title="Noongar Seasonal Calendar")

st.title("Noongar Seasonal Calendar")
st.write(
	"Explore the six Noongar seasons and discover seasonal observations about "
	"the weather, plants, animals, and activities recorded in this dataset."
)

st.divider()
st.subheader("Explore the seasons")

selected_season = st.selectbox("Choose a season", seasons)
season_data = data[data["Season_Name"] == selected_season]
season_info = season_data.iloc[0]

st.header(selected_season)
st.write(season_info["English_Equivalent"].capitalize())
st.caption(f"{season_info['Start_of_month']} to {season_info['End_of_month']}")
st.write(f"{len(season_data)} seasonal observations in this dataset.")

topics = season_data["Indicator_type"].dropna().unique().tolist()
selected_topic = st.selectbox("Filter by topic", ["All topics", *topics])

if selected_topic != "All topics":
	season_data = season_data[season_data["Indicator_type"] == selected_topic]

st.dataframe(
	season_data[["Indicator_type", "Indicator_Name", "Description"]],
	hide_index=True,
	width="stretch",
)
