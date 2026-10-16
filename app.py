# Import Streamlit so this file can configure and run the web application.
import streamlit as st

# Set the browser-tab title, icon, and wide layout for the entire app.
st.set_page_config(
    page_title="Noongar Seasonal Calendar",
    page_icon="🐞",
    layout="wide",
)

# Define the three pages and their navigation labels, icons, and default page.
pages = [
    st.Page("pages/1_six_seasons.py", title="Six Seasons", icon="🪷", default=True),
    st.Page("pages/2_season_finder.py", title="Seasonal Match", icon="🔎"),
    st.Page("pages/3_data_analysis.py", title="Data & Visualisations", icon="📊"),
]

# Display the navigation menu and run the page the user selects.
st.navigation(pages).run()