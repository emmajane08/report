import streamlit as st

st.set_page_config(
    page_title="Noongar Seasonal Calendar",
    page_icon="🐞",
    layout="wide",
)

pages = [
    st.Page("pages/1_six_seasons.py", title="Six Seasons", icon="🪷", default=True),
    st.Page("pages/2_season_finder.py", title="Seasonal Match", icon="🔎"),
    st.Page("pages/3_data_analysis.py", title="Data & Visualisations", icon="📊"),
]

st.navigation(pages).run()