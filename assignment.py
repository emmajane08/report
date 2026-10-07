from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# LOAD DATA
# ============================================================

DATA_FILE = Path(__file__).parent / "Data.csv"

data = pd.read_csv(DATA_FILE)

# Clean column names
data.columns = data.columns.str.strip()

# Clean text values
for column in data.select_dtypes(include="object").columns:
    data[column] = data[column].fillna("").astype(str).str.strip()


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Noongar Seasonal Calendar",
    page_icon="🌿",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_season_scores(dataset, selected_indicators):
    """
    Compare the user's selected environmental indicators
    against the indicators recorded for each season.

    Each matching indicator contributes one point.
    """

    seasons = sorted(dataset["Season_Name"].unique())

    scores = {}

    for season in seasons:

        season_data = dataset[
            dataset["Season_Name"] == season
        ]

        # Use unique indicator names so duplicate descriptions
        # do not give a season extra points.
        season_indicators = set(
            season_data["Indicator_Name"].str.strip()
        )

        matches = season_indicators.intersection(
            selected_indicators
        )

        scores[season] = len(matches)

    return scores


def get_season_information(dataset, season):
    """Return the information associated with a season."""

    return (
        dataset[
            dataset["Season_Name"] == season
        ]
        .drop_duplicates()
    )


# ============================================================
# USER-FRIENDLY OPTIONS
# ============================================================
#
# These are based ONLY on indicators that actually occur
# in the edited CSV.
#
# The text shown to the user is easier to understand, while
# the value in each list is the actual Indicator_Name used
# by the dataset.
# ============================================================

USER_OPTIONS = {

    "🌧️ Rainfall": {
        "Little or no rainfall": ["Rain"],
        "Some rain": ["Rain"],
        "Wettest time of the year": ["Rain"],
        "Rain is increasing/decreasing": ["Rain"],
    },

    "🌡️ Temperature": {
        "Warm temperatures": ["Warm Temperatures"],
        "Cool temperatures": ["Cool Temperatures"],
        "Cold / coldest conditions": ["Temperature"],
        "Changing / transitional temperature": ["Temperature"],
    },

    "💨 Weather conditions": {
        "Dry conditions": ["Dry"],
        "Windy conditions": ["Winds"],
        "Storms": ["Storms"],
        "Cloudy skies": ["Clouds"],
        "Clear skies": ["Skies"],
        "Snow": ["Snow"],
        "Water levels are increasing": ["Water"],
    },

    "🌱 Plants and flowers": {
        "Flowers are appearing": ["Flowers"],
        "Banksia is flowering": ["Banksia"],
        "Eucalypts are present": ["Eucalypts"],
        "Acacias are flowering": ["Acacias", "Golden Acacias"],
        "Grass trees are flowering": [
            "Balgas (grass trees)",
            "(Balgas) grass trees"
        ],
        "Trees are flowering": [
            "Paperbark tree",
            "Moodjar (Christmas tree)",
            "Jarrah",
            "Marri"
        ],
        "Berries or fruits are developing": [
            "berries",
            "Flowering fruits",
            "Quandong trees"
        ],
    },

    "🐾 Animals": {
        "Frogs are active": [
            "Frogs",
            "frogs",
            "frogs (kooyal)",
            "kwooyar (moaning frogs)",
            "kooboolong (motorbike frog)"
        ],
        "Reptiles are active": [
            "Reptiles",
            "reptiles",
            "snakes",
            "snake (Waugal)"
        ],
        "Kangaroos are present": [
            "Yonga (Kangaroo)"
        ],
        "Birds are nesting or breeding": [
            "Breeding",
            "Mali (Black Swan)",
            "Koolbardi (Magpie)",
            "Koolbardies (Magpies)"
        ],
        "Young animals are appearing": [
            "Fledgings",
            "baby birds",
            "adolescent animals"
        ],
        "Fish are abundant": [
            "Fish",
            "freshwater fish",
            "Salmon",
            "Herring",
            "Mullet",
            "bream"
        ],
    },

    "🔥 Activities": {
        "Mosaic burning": ["Mosaic Burning"],
        "Fishing": ["Fishing", "fishing"],
        "Movement between areas": ["Movement", "movement"],
        "People gathering socially": [
            "social",
            "social time"
        ],
        "Eating / food gathering": ["eating"],
        "Young/newborn animals": ["Young"],
    }
}


# ============================================================
# CHECK THAT MAPPED VALUES EXIST IN THE DATA
# ============================================================

actual_indicators = set(
    data["Indicator_Name"]
    .dropna()
    .str.strip()
    .unique()
)

valid_options = {}

for category, options in USER_OPTIONS.items():

    valid_options[category] = {}

    for friendly_name, csv_indicators in options.items():

        valid_indicators = [
            indicator
            for indicator in csv_indicators
            if indicator in actual_indicators
        ]

        if valid_indicators:
            valid_options[category][friendly_name] = (
                valid_indicators
            )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌿 Noongar Seasonal Calendar")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "Season Finder",
        "Explore Seasons",
        "Data & Visualisations"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    f"{len(data)} records loaded"
)


# ============================================================
# PAGE 1 — SEASON FINDER
# ============================================================

if page == "Season Finder":

    st.title("🌿 Find the Season")

    st.write(
        "Select the environmental conditions you are observing. "
        "The app will compare your observations with the seasonal "
        "indicators in the dataset."
    )

    st.info(
        "You can select multiple observations from each category."
    )

    st.divider()

    selected_indicators = set()

    # --------------------------------------------------------
    # DISPLAY USER OPTIONS
    # --------------------------------------------------------

    for category, options in valid_options.items():

        st.subheader(category)

        choices = list(options.keys())

        selected = st.multiselect(
            f"Select observations:",
            choices,
            key=category
        )

        for choice in selected:

            for indicator in options[choice]:

                selected_indicators.add(indicator)

    st.divider()

    # --------------------------------------------------------
    # FIND SEASON
    # --------------------------------------------------------

    if st.button(
        "🔎 Find Most Likely Season",
        type="primary"
    ):

        if len(selected_indicators) == 0:

            st.warning(
                "Please select at least one observation."
            )

        else:

            scores = calculate_season_scores(
                data,
                selected_indicators
            )

            ranked_seasons = sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True
            )

            best_season = ranked_seasons[0][0]
            best_score = ranked_seasons[0][1]

            # ------------------------------------------------
            # NO MATCHES
            # ------------------------------------------------

            if best_score == 0:

                st.warning(
                    "There were no direct matches between "
                    "your observations and the dataset."
                )

            else:

                st.success(
                    f"🌿 Most likely season: **{best_season}**"
                )

                st.metric(
                    "Matching indicators",
                    best_score
                )

                # ------------------------------------------------
                # SEASON INFORMATION
                # ------------------------------------------------

                season_data = get_season_information(
                    data,
                    best_season
                )

                st.subheader(
                    f"About {best_season}"
                )

                first_row = season_data.iloc[0]

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "English equivalent",
                    first_row["English_Equivalent"]
                )

                col2.metric(
                    "Start",
                    first_row["Start_of_month"]
                )

                col3.metric(
                    "End",
                    first_row["End_of_month"]
                )

                # ------------------------------------------------
                # MATCHING INDICATORS
                # ------------------------------------------------

                matching_indicators = []

                for indicator in selected_indicators:

                    if indicator in set(
                        season_data["Indicator_Name"]
                    ):
                        matching_indicators.append(
                            indicator
                        )

                if matching_indicators:

                    st.subheader(
                        "Why this season matched"
                    )

                    for indicator in sorted(
                        matching_indicators
                    ):
                        st.write(
                            f"✓ {indicator}"
                        )

                # ------------------------------------------------
                # SEASON RANKING
                # ------------------------------------------------

                st.subheader(
                    "Season matching scores"
                )

                ranking = pd.DataFrame(
                    ranked_seasons,
                    columns=[
                        "Season",
                        "Matching indicators"
                    ]
                )

                st.dataframe(
                    ranking,
                    use_container_width=True,
                    hide_index=True
                )


# ============================================================
# PAGE 2 — EXPLORE SEASONS
# ============================================================

elif page == "Explore Seasons":

    st.title("🌿 Explore the Seasons")

    st.write(
        "Explore the environmental, plant, animal and activity "
        "indicators recorded for each season."
    )

    seasons = sorted(
        data["Season_Name"].unique()
    )

    selected_season = st.selectbox(
        "Choose a season:",
        seasons
    )

    season_data = data[
        data["Season_Name"] == selected_season
    ]

    st.divider()

    # --------------------------------------------------------
    # SEASON INFORMATION
    # --------------------------------------------------------

    st.header(selected_season)

    first_row = season_data.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "English equivalent",
        first_row["English_Equivalent"]
    )

    col2.metric(
        "Start",
        first_row["Start_of_month"]
    )

    col3.metric(
        "End",
        first_row["End_of_month"]
    )

    st.divider()

    # --------------------------------------------------------
    # FILTER BY INDICATOR TYPE
    # --------------------------------------------------------

    st.subheader("Seasonal indicators")

    indicator_types = sorted(
        season_data["Indicator_type"].unique()
    )

    selected_type = st.selectbox(
        "Choose an indicator category:",
        ["All"] + indicator_types
    )

    if selected_type == "All":

        display_data = season_data

    else:

        display_data = season_data[
            season_data["Indicator_type"]
            == selected_type
        ]

    display_data = (
        display_data[
            [
                "Indicator_type",
                "Indicator_Name",
                "Description"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 3 — DATA & VISUALISATIONS
# ============================================================

elif page == "Data & Visualisations":

    st.title("📊 Data & Visualisations")

    st.write(
        "Explore the dataset using summary statistics, "
        "tables and charts."
    )

    st.divider()

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.subheader("Dataset summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total records",
        len(data)
    )

    col2.metric(
        "Seasons",
        data["Season_Name"].nunique()
    )

    col3.metric(
        "Indicator types",
        data["Indicator_type"].nunique()
    )

    st.divider()

    # --------------------------------------------------------
    # RECORDS PER SEASON
    # --------------------------------------------------------

    st.subheader(
        "Number of records per season"
    )

    season_counts = (
        data["Season_Name"]
        .value_counts()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        season_counts
    )

    # --------------------------------------------------------
    # INDICATORS BY TYPE
    # --------------------------------------------------------

    st.subheader(
        "Number of records by indicator type"
    )

    type_counts = (
        data["Indicator_type"]
        .value_counts()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        type_counts
    )

    # --------------------------------------------------------
    # UNIQUE INDICATORS
    # --------------------------------------------------------

    st.subheader(
        "Most frequently recorded indicators"
    )

    indicator_counts = (
        data["Indicator_Name"]
        .value_counts()
        .head(20)
    )

    st.bar_chart(
        indicator_counts
    )

    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    st.subheader(
        "Explore the dataset"
    )

    selected_type = st.selectbox(
        "Filter by indicator type:",
        ["All"] +
        sorted(data["Indicator_type"].unique())
    )

    if selected_type == "All":

        filtered_data = data

    else:

        filtered_data = data[
            data["Indicator_type"] == selected_type
        ]

    st.dataframe(
        filtered_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# END
# ============================================================