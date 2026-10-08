from content.season_information import SEASON_INFORMATION

from pathlib import Path

import streamlit as st
from PIL import Image
from streamlit_image_coordinates import (
    streamlit_image_coordinates
)

from components.season_map import (
    get_season_from_click
)

from components.season_card import (
    display_season_information
)

from content.season_information import (
    SEASON_INFORMATION
)


st.title("The Six Seasons")


IMAGE_PATH = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "six_seasons_diagram.jpg"
)


# Remember which season the user selected
if "selected_season" not in st.session_state:
    st.session_state.selected_season = None


# ------------------------------------------------
# SHOW SEASON INFORMATION
# ------------------------------------------------

if st.session_state.selected_season:

    season = st.session_state.selected_season

    if st.button("← Back to main page (Six Seasons)"):
        st.session_state.selected_season = None
        st.rerun()

    display_season_information(
        season,
        SEASON_INFORMATION[season]
    )

    st.stop()


# ------------------------------------------------
# SHOW THE DIAGRAM
# ------------------------------------------------

st.write(
    "Click on one of the six seasons in the diagram "
    "to explore it."
)


image = Image.open(IMAGE_PATH)

display_width = 900

display_height = round(
    image.height * display_width / image.width
)


clicked = streamlit_image_coordinates(
    image,
    width=display_width
)


# ------------------------------------------------
# WORK OUT WHAT WAS CLICKED
# ------------------------------------------------

if clicked is not None:

    selected_season = get_season_from_click(
        clicked["x"],
        clicked["y"],
        display_width,
        display_height
    )

    if selected_season:

        st.session_state.selected_season = (
            selected_season
        )

        st.rerun()

    else:

        st.info(
            "Click on one of the six seasonal areas."
        )