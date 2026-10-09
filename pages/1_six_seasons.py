import plotly.graph_objects as go
import streamlit as st
from streamlit_plotly_events import plotly_events

from components.season_card import display_season_information
from content.season_information import SEASON_INFORMATION


st.title("The Six Seasons")

# Remember which season the user selected
if "selected_season" not in st.session_state:
    st.session_state.selected_season = None

if "season_pie_version" not in st.session_state:
    st.session_state.season_pie_version = 0


# ------------------------------------------------
# SHOW SEASON INFORMATION
# ------------------------------------------------

if st.session_state.selected_season:

    season = st.session_state.selected_season

    display_season_information(
        season,
        SEASON_INFORMATION[season]
    )

    st.stop()


# ------------------------------------------------
# SHOW THE SEASON PIE
# ------------------------------------------------

st.write("Select a slice to explore that season.")

seasons = list(SEASON_INFORMATION)
season_pie = go.Figure(
    go.Pie(
        labels=seasons,
        values=[1] * len(seasons),
        hole=0.25,
        sort=False,
        direction="clockwise",
        rotation=270,
        textinfo="label",
        textposition="inside",
        insidetextorientation="radial",
        marker={
            "colors": [
                "#D9822B",
                "#F2B544",
                "#B86B4B",
                "#3D6B82",
                "#91A85A",
                "#D6A84F",
            ],
            "line": {"color": "white", "width": 3},
        },
        hovertemplate="%{label}<extra></extra>",
    )
)

season_pie.update_layout(
    showlegend=False,
    height=520,
    margin={"t": 20, "b": 20, "l": 20, "r": 20},
    uniformtext={"minsize": 13, "mode": "hide"},
)

clicked_points = plotly_events(
    season_pie,
    key=f"season-pie-{st.session_state.season_pie_version}",
    click_event=True,
    select_event=False,
    hover_event=False,
    override_height=520,
)

if clicked_points:
    clicked_point = clicked_points[0]
    selected_season = clicked_point.get("label")
    if selected_season is None:
        point_index = clicked_point.get(
            "pointNumber",
            clicked_point.get("pointIndex"),
        )
        if isinstance(point_index, int) and 0 <= point_index < len(seasons):
            selected_season = seasons[point_index]

    if selected_season in SEASON_INFORMATION:
        st.session_state.selected_season = selected_season
        st.rerun()