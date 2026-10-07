from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

data_file = Path(__file__).parent / "Data.csv"
data = pd.read_csv(data_file)

# Remove rows that don't have a season or indicator
data = data.dropna(subset=["Season_Name", "Indicator_Name"])

# List of seasons
seasons = data["Season_Name"].dropna().unique().tolist()


# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Noongar Seasonal Calendar",
    page_icon="🌿",
    layout="wide"
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_unique_indicators(data):
    """
    Get a list of unique indicator names.
    """
    return sorted(
        data["Indicator_Name"]
        .dropna()
        .unique()
        .tolist()
    )


def calculate_season_scores(data, selected_indicators):
    """
    Calculate how many of the selected indicators
    are associated with each season.

    Each indicator is only counted once per season.
    """

    scores = {}

    # Remove duplicate season/indicator combinations
    unique_data = data[
        ["Season_Name", "Indicator_Name"]
    ].drop_duplicates()

    for season in seasons:

        season_data = unique_data[
            unique_data["Season_Name"] == season
        ]

        season_indicators = set(
            season_data["Indicator_Name"]
        )

        matches = 0

        for indicator in selected_indicators:
            if indicator in season_indicators:
                matches += 1

        scores[season] = matches

    return scores


def get_season_information(data, season):
    """
    Get the first row containing information
    about a particular season.
    """

    season_data = data[
        data["Season_Name"] == season
    ]

    if season_data.empty:
        return None

    return season_data.iloc[0]


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

st.sidebar.title("🌿 Noongar Seasons")

page = st.sidebar.radio(
    "Choose a page",
    [
        "🏠 Season Finder",
        "🌿 Explore Seasons",
        "📊 Data & Visualisations"
    ]
)


# =========================================================
# PAGE 1 — SEASON FINDER
# =========================================================

if page == "🏠 Season Finder":

    st.title("🌿 Noongar Season Finder")

    st.write(
        "Select the environmental indicators you are currently "
        "observing. The application will compare your observations "
        "with the indicators recorded for each season."
    )

    st.divider()

    # Get all possible indicators
    indicators = get_unique_indicators(data)

    st.subheader("What are you observing?")

    st.write(
        "Select one or more indicators from the list below."
    )

    selected_indicators = st.multiselect(
        "Observed indicators",
        indicators
    )

    st.divider()

    # Only calculate if the user has selected something
    if selected_indicators:

        scores = calculate_season_scores(
            data,
            selected_indicators
        )

        # Convert scores to a DataFrame
        score_data = pd.DataFrame(
            scores.items(),
            columns=["Season", "Matches"]
        )

        # Calculate percentage
        score_data["Match_Percentage"] = (
            score_data["Matches"]
            / len(selected_indicators)
            * 100
        )

        # Sort from highest to lowest
        score_data = score_data.sort_values(
            "Matches",
            ascending=False
        )

        # Get the highest-scoring season
        best_season = score_data.iloc[0]["Season"]

        best_score = score_data.iloc[0]["Matches"]

        best_percentage = score_data.iloc[0][
            "Match_Percentage"
        ]

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        st.subheader("Most likely season")

        st.success(
            f"🌿 {best_season}"
        )

        st.write(
            f"Your observations matched "
            f"**{int(best_score)} of {len(selected_indicators)} "
            f"selected indicators** associated with {best_season}."
        )

        st.metric(
            "Match percentage",
            f"{best_percentage:.0f}%"
        )

        # -------------------------------------------------
        # SHOW WHY
        # -------------------------------------------------

        st.subheader("Why this season?")

        best_season_data = data[
            data["Season_Name"] == best_season
        ]

        best_indicators = set(
            best_season_data["Indicator_Name"]
        )

        matching_indicators = [
            indicator
            for indicator in selected_indicators
            if indicator in best_indicators
        ]

        for indicator in matching_indicators:
            st.write(f"✓ {indicator}")

        # -------------------------------------------------
        # SHOW ALL SCORES
        # -------------------------------------------------

        st.subheader("Season comparison")

        display_scores = score_data[
            ["Season", "Matches", "Match_Percentage"]
        ].copy()

        display_scores["Match_Percentage"] = (
            display_scores["Match_Percentage"]
            .round(0)
            .astype(int)
            .astype(str)
            + "%"
        )

        st.dataframe(
            display_scores,
            hide_index=True,
            width="stretch"
        )

    else:

        st.info(
            "Select one or more indicators to find the "
            "most likely season."
        )


# =========================================================
# PAGE 2 — EXPLORE SEASONS
# =========================================================

elif page == "🌿 Explore Seasons":

    st.title("🌿 Explore the Noongar Seasons")

    st.write(
        "Choose a season to explore the environmental "
        "indicators recorded in the dataset."
    )

    st.divider()

    selected_season = st.selectbox(
        "Choose a season",
        seasons
    )

    season_data = data[
        data["Season_Name"] == selected_season
    ]

    season_info = get_season_information(
        data,
        selected_season
    )

    # -------------------------------------------------
    # SEASON INFORMATION
    # -------------------------------------------------

    st.header(selected_season)

    if season_info is not None:

        st.write(
            str(
                season_info["English_Equivalent"]
            ).capitalize()
        )

        st.caption(
            f"{season_info['Start_of_month']} "
            f"to {season_info['End_of_month']}"
        )

    st.write(
        f"**{len(season_data)} observations** "
        "are recorded for this season."
    )

    st.divider()

    # -------------------------------------------------
    # CATEGORY FILTER
    # -------------------------------------------------

    topics = (
        season_data["Indicator_type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_topic = st.selectbox(
        "Filter by indicator type",
        ["All types"] + sorted(topics)
    )

    if selected_topic != "All types":

        filtered_data = season_data[
            season_data["Indicator_type"]
            == selected_topic
        ]

    else:

        filtered_data = season_data

    # -------------------------------------------------
    # DISPLAY INDICATORS
    # -------------------------------------------------

    st.subheader("Seasonal indicators")

    st.dataframe(
        filtered_data[
            [
                "Indicator_type",
                "Indicator_Name",
                "Description"
            ]
        ],
        hide_index=True,
        width="stretch"
    )


# =========================================================
# PAGE 3 — DATA & VISUALISATIONS
# =========================================================

elif page == "📊 Data & Visualisations":

    st.title("📊 Data & Visualisations")

    st.write(
        "Explore patterns in the seasonal indicators "
        "contained in the dataset."
    )

    st.divider()

    # -------------------------------------------------
    # BASIC DATASET INFORMATION
    # -------------------------------------------------

    st.subheader("Dataset overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total observations",
        len(data)
    )

    col2.metric(
        "Number of seasons",
        data["Season_Name"].nunique()
    )

    col3.metric(
        "Indicator types",
        data["Indicator_type"].nunique()
    )

    st.divider()

    # -------------------------------------------------
    # INDICATORS BY SEASON
    # -------------------------------------------------

    st.subheader("Number of indicators by season")

    season_counts = (
        data.groupby("Season_Name")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(season_counts)

    st.write(
        "This shows how many observations are recorded "
        "for each season."
    )

    st.divider()

    # -------------------------------------------------
    # INDICATOR TYPES
    # -------------------------------------------------

    st.subheader("Indicators by type")

    type_counts = (
        data["Indicator_type"]
        .value_counts()
    )

    st.bar_chart(type_counts)

    st.divider()

    # -------------------------------------------------
    # SEASON × INDICATOR TYPE TABLE
    # -------------------------------------------------

    st.subheader(
        "Indicator types across the seasons"
    )

    season_type_table = pd.crosstab(
        data["Season_Name"],
        data["Indicator_type"]
    )

    st.dataframe(
        season_type_table,
        width="stretch"
    )

    st.divider()

    # -------------------------------------------------
    # UNIQUE INDICATORS
    # -------------------------------------------------

    st.subheader("Number of unique indicators")

    unique_indicator_counts = (
        data.groupby("Season_Name")[
            "Indicator_Name"
        ]
        .nunique()
        .sort_values(ascending=False)
    )

    st.bar_chart(unique_indicator_counts)

    st.write(
        "Unlike the previous graph, this graph counts "
        "each indicator only once within a season."
    )

    st.divider()

    # -------------------------------------------------
    # RAW DATA
    # -------------------------------------------------

    with st.expander("View complete dataset"):

        st.dataframe(
            data,
            hide_index=True,
            width="stretch"
        )