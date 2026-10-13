import plotly.graph_objects as go
import streamlit as st
from streamlit_plotly_events import plotly_events

from components.season_card import display_season_information
from content.season_information import SEASON_INFORMATION


st.title("The Six Seasons")

st.session_state.setdefault("selected_season", None)
st.session_state.setdefault("season_pie_version", 0)


# ------------------------------------------------
# SEASON INFORMATION
# ------------------------------------------------

if st.session_state.selected_season:
    season = st.session_state.selected_season
    display_season_information(season, SEASON_INFORMATION[season])
    st.stop()


# ------------------------------------------------
# SEASON PIE
# ------------------------------------------------

st.write("Click on a season displayed in the circle to learn more about it.")

SEASON_COLORS = [
    "#FF6355",
    "#FBA949",
    "#8BD448",
    "#2AA8F2",
    "#FF93BE",
    "#FAE442",
]

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
            "colors": SEASON_COLORS,
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