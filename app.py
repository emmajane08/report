import streamlit as st

st.set_page_config(
    page_title="Noongar Seasonal Calendar",
    page_icon="🌿",
    layout="wide"
)

home = st.Page(
    "pages/1_six_seasons.py",
    title="Six Seasons",
    icon="🌿",
    default=True
)

finder = st.Page(
    "pages/2_season_finder.py",
    title="Season Finder",
    icon="🔎"
)

analysis = st.Page(
    "pages/3_data_analysis.py",
    title="Data & Visualisations",
    icon="📊"
)

pg = st.navigation([
    home,
    finder,
    analysis
])

pg.run()