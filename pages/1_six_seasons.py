# Import Plotly for the pie chart, Streamlit for the page, and the Plotly click bridge.
import plotly.graph_objects as go
import streamlit as st
from streamlit_plotly_events import plotly_events

# Import the reusable season-detail display and the data for all six seasons.
from components.season_card import display_season_information
from content.season_information import SEASON_INFORMATION


# Add the page heading.
st.title("The Six Seasons")

# Initialize the selected season only if it has not already been stored.
st.session_state.setdefault("selected_season", None)
# Track chart instances so returning from a detail view can reset the chart.
st.session_state.setdefault("season_pie_version", 0)


# ------------------------------------------------
# SEASON INFORMATION
# ------------------------------------------------

# If the user previously selected a season, show its details instead of the chart.
if st.session_state.selected_season:
    # Read the selected season name from Streamlit's persistent session state.
    season = st.session_state.selected_season
    # Render the selected season's title, description, and source references.
    display_season_information(season, SEASON_INFORMATION[season])
    # Stop rendering this run once the detail view has been displayed.
    st.stop()


# ------------------------------------------------
# SEASON PIE
# ------------------------------------------------

# Explain how to interact with the pie chart.
st.write("Click on a season displayed in the circle to learn more about it.")

# Define one display color for each season slice, in season order.
SEASON_COLORS = [
    "#FF6355",
    "#FBA949",
    "#8BD448",
    "#2AA8F2",
    "#FF93BE",
    "#FAE442",
]

# Use the season dictionary's keys as the slice labels and their order.
seasons = list(SEASON_INFORMATION)
# Build an equal-sized, labeled, clickable pie chart with a hole in its center.
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

# Set the chart's legend, dimensions, margins, and text sizing behavior.
season_pie.update_layout(
    showlegend=False,
    height=520,
    margin={"t": 20, "b": 20, "l": 20, "r": 20},
    uniformtext={"minsize": 13, "mode": "hide"},
)

# Render the chart and collect click events from the selected pie slice.
clicked_points = plotly_events(
    season_pie,
    key=f"season-pie-{st.session_state.season_pie_version}",
    click_event=True,
    select_event=False,
    hover_event=False,
    override_height=520,
)

# Continue only if the chart reported at least one clicked point.
if clicked_points:
    # Use the first click event returned by the chart component.
    clicked_point = clicked_points[0]
    # Prefer the event's season label when it is available.
    selected_season = clicked_point.get("label")
    # Fall back to the point's position if the event did not contain a label.
    if selected_season is None:
        point_index = clicked_point.get(
            "pointNumber",
            clicked_point.get("pointIndex"),
        )
        # Accept only a valid integer index within the season list.
        if isinstance(point_index, int) and 0 <= point_index < len(seasons):
            selected_season = seasons[point_index]

    # Save only known season names and rerun to display the selected detail view.
    if selected_season in SEASON_INFORMATION:
        st.session_state.selected_season = selected_season
        st.rerun()