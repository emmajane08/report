from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# DATA LOADING
# ============================================================

DATA_FILE = Path(__file__).parent / "Data.csv"

data = pd.read_csv(DATA_FILE)

# Remove accidental spaces from column names and text values
data.columns = data.columns.str.strip()

for column in data.select_dtypes(include="object").columns:
    data[column] = data[column].str.strip()


# ============================================================
# USER-FRIENDLY INDICATOR MAPPING
# ============================================================
# These choices are the words the user sees in the app.
# Each choice is mapped to indicator names that already exist
# in the CSV file.
#
# IMPORTANT:
# Only use mappings that match the actual Indicator_Name
# values in your Data.csv.
# ============================================================

USER_INDICATORS = {
    "Rainfall": {
        "Very little or no rain": [
            "Decreased rainfall",
            "Little to no rainfall",
            "Decreased rain"
        ],
        "Some rain": [
            "Some days are cool and rainy",
            "Some rainfall"
        ],
        "Frequent or heavy rain": [
            "Wettest time of the year",
            "Heavy rainfall",
            "Frequent rainfall"
        ],
    },

    "Temperature": {
        "Very hot": [
            "Hot weather",
            "Very hot"
        ],
        "Warm": [
            "Warm weather",
            "Warm"
        ],
        "Mild or changing temperatures": [
            "Mild weather",
            "Changing temperatures"
        ],
        "Cool": [
            "Cool weather",
            "Cool"
        ],
        "Very cold": [
            "Cold weather",
            "Very cold"
        ],
    },

    "Weather": {
        "Sunny or clear": [
            "Sunny",
            "Clear skies",
            "Clear weather"
        ],
        "Cloudy": [
            "Cloudy",
            "Clouds"
        ],
        "Strong winds": [
            "Strong winds",
            "Windy"
        ],
        "Storms": [
            "Storms",
            "Stormy weather"
        ],
    },

    "Plants": {
        "Flowers are blooming": [
            "Flowers blooming",
            "Flowering"
        ],
        "Banksias are flowering": [
            "Banksias flowering",
            "Banksia flowering"
        ],
        "Eucalypts are flowering": [
            "Eucalypts flowering",
            "Eucalyptus flowering"
        ],
        "Trees are flowering or changing": [
            "Trees changing",
            "Trees flowering"
        ],
        "Fruits or seeds are developing": [
            "Fruits developing",
            "Seeds developing",
            "Fruits and seeds"
        ],
    },

    "Animals": {
        "Frogs are active": [
            "Frogs active",
            "Frog activity"
        ],
        "Reptiles are active": [
            "Reptiles active",
            "Reptile activity"
        ],
        "Kangaroos are active": [
            "Kangaroos active",
            "Kangaroo activity"
        ],
        "Birds are nesting or breeding": [
            "Birds nesting",
            "Birds breeding"
        ],
        "Young animals are appearing": [
            "Young animals",
            "Young animals appearing"
        ],
    },

    "Activities": {
        "Fire or burning is occurring": [
            "Fire",
            "Burning",
            "Fire/burning"
        ],
        "Fishing is important": [
            "Fishing"
        ],
        "Animals are moving": [
            "Animals moving"
        ],
        "People are gathering": [
            "People gathering"
        ],
    }
}


# ============================================================
# CLEAN THE MAPPING
# ============================================================
# Only keep mapped indicator names that actually occur in the
# CSV. This prevents the program from accidentally using
# invented indicators that are not present in the dataset.
# ============================================================

actual_indicators = set(
    data["Indicator_Name"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

valid_user_indicators = {}

for category, choices in USER_INDICATORS.items():
    valid_user_indicators[category] = {}

    for friendly_name, csv_names in choices.items():
        matching_names = [
            name for name in csv_names
            if name in actual_indicators
        ]

        if matching_names:
            valid_user_indicators[category][friendly_name] = matching_names


# ============================================================
# SEASON SCORING ALGORITHM
# ============================================================

def calculate_season_scores(dataset, selected_indicators):
    """
    Calculate how strongly each season matches the user's
    environmental observations.

    Each unique Season_Name + Indicator_Name combination
    counts as one possible match.

    Returns a dictionary containing the score for each season.
    """

    seasons = sorted(
        dataset["Season_Name"]
        .dropna()
        .unique()
    )

    scores = {}

    unique_data = dataset[
        ["Season_Name", "Indicator_Name"]
    ].drop_duplicates()

    selected_indicators = set(selected_indicators)

    for season in seasons:

        season_data = unique_data[
            unique_data["Season_Name"] == season
        ]

        season_indicators = set(
            season_data["Indicator_Name"]
            .dropna()
        )

        matches = season_indicators.intersection(
            selected_indicators
        )

        scores[season] = len(matches)

    return scores


# ============================================================
# FIND MATCHED INDICATORS
# ============================================================

def get_season_matches(dataset, season, selected_indicators):
    """
    Return the indicators selected by the user that occur
    in the chosen season.
    """

    season_data = dataset[
        dataset["Season_Name"] == season
    ]

    season_indicators = set(
        season_data["Indicator_Name"]
        .dropna()
    )

    return sorted(
        season_indicators.intersection(
            set(selected_indicators)
        )
    )


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Noongar Seasonal Calendar",
    page_icon="🌿",
    layout="wide"
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🌿 Navigation")

page = st.sidebar.radio(
    "Choose a page:",
    [
        "Season Finder",
        "Explore Seasons",
        "Data & Visualisations"
    ]
)


# ============================================================
# PAGE 1 — SEASON FINDER
# ============================================================

if page == "Season Finder":

    st.title("🌿 Noongar Seasonal Calendar")

    st.write(
        "Select the environmental conditions you are observing "
        "to find the season that best matches the available data."
    )

    st.info(
        "Select as many observations as apply. "
        "The app compares your selections with the indicators "
        "recorded for each season."
    )

    st.divider()

    # Store all selected CSV indicators here
    selected_indicators = []

    # --------------------------------------------------------
    # RAINFALL
    # --------------------------------------------------------

    st.subheader("🌧️ Rainfall")

    rainfall_options = list(
        valid_user_indicators.get("Rainfall", {}).keys()
    )

    if rainfall_options:
        rainfall = st.multiselect(
            "What is the rainfall like?",
            rainfall_options
        )

        for choice in rainfall:
            selected_indicators.extend(
                valid_user_indicators["Rainfall"][choice]
            )

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    st.subheader("🌡️ Temperature")

    temperature_options = list(
        valid_user_indicators.get("Temperature", {}).keys()
    )

    if temperature_options:
        temperature = st.multiselect(
            "What is the temperature like?",
            temperature_options
        )

        for choice in temperature:
            selected_indicators.extend(
                valid_user_indicators["Temperature"][choice]
            )

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    st.subheader("☁️ Weather")

    weather_options = list(
        valid_user_indicators.get("Weather", {}).keys()
    )

    if weather_options:
        weather = st.multiselect(
            "What weather conditions are you observing?",
            weather_options
        )

        for choice in weather:
            selected_indicators.extend(
                valid_user_indicators["Weather"][choice]
            )

    # --------------------------------------------------------
    # PLANTS
    # --------------------------------------------------------

    st.subheader("🌱 Plants")

    plant_options = list(
        valid_user_indicators.get("Plants", {}).keys()
    )

    if plant_options:
        plants = st.multiselect(
            "What are you observing in plants?",
            plant_options
        )

        for choice in plants:
            selected_indicators.extend(
                valid_user_indicators["Plants"][choice]
            )

    # --------------------------------------------------------
    # ANIMALS
    # --------------------------------------------------------

    st.subheader("🦘 Animals")

    animal_options = list(
        valid_user_indicators.get("Animals", {}).keys()
    )

    if animal_options:
        animals = st.multiselect(
            "What are you observing in animals?",
            animal_options
        )

        for choice in animals:
            selected_indicators.extend(
                valid_user_indicators["Animals"][choice]
            )

    # --------------------------------------------------------
    # ACTIVITIES
    # --------------------------------------------------------

    st.subheader("🔥 Activities")

    activity_options = list(
        valid_user_indicators.get("Activities", {}).keys()
    )

    if activity_options:
        activities = st.multiselect(
            "What activities or seasonal events are occurring?",
            activity_options
        )

        for choice in activities:
            selected_indicators.extend(
                valid_user_indicators["Activities"][choice]
            )

    # Remove duplicate indicators
    selected_indicators = list(
        set(selected_indicators)
    )

    st.divider()

    # --------------------------------------------------------
    # FIND SEASON BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔎 Find Most Likely Season",
        type="primary"
    ):

        if not selected_indicators:

            st.warning(
                "Please select at least one environmental "
                "observation before finding a season."
            )

        else:

            scores = calculate_season_scores(
                data,
                selected_indicators
            )

            # Sort seasons from highest score to lowest score
            ranked_seasons = sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True
            )

            best_season = ranked_seasons[0][0]
            best_score = ranked_seasons[0][1]

            # Check whether there were any matches
            if best_score == 0:

                st.warning(
                    "No season in the dataset matched the "
                    "selected observations."
                )

                st.write(
                    "Try selecting different observations."
                )

            else:

                st.success(
                    f"🌿 Most likely season: **{best_season}**"
                )

                st.metric(
                    "Number of matching indicators",
                    best_score
                )

                # ------------------------------------------------
                # SHOW SEASON INFORMATION
                # ------------------------------------------------

                season_rows = data[
                    data["Season_Name"] == best_season
                ]

                if not season_rows.empty:

                    st.subheader(
                        f"About {best_season}"
                    )

                    info_columns = []

                    for column in [
                        "English_Equivalent",
                        "Start_Month",
                        "End_Month"
                    ]:
                        if column in season_rows.columns:
                            info_columns.append(column)

                    if info_columns:

                        info = (
                            season_rows[
                                info_columns
                            ]
                            .drop_duplicates()
                            .reset_index(drop=True)
                        )

                        st.dataframe(
                            info,
                            use_container_width=True,
                            hide_index=True
                        )

                # ------------------------------------------------
                # SHOW MATCHED INDICATORS
                # ------------------------------------------------

                matches = get_season_matches(
                    data,
                    best_season,
                    selected_indicators
                )

                if matches:

                    st.subheader(
                        "Matching indicators"
                    )

                    for indicator in matches:
                        st.write(f"✓ {indicator}")

                # ------------------------------------------------
                # SHOW RANKING
                # ------------------------------------------------

                st.subheader(
                    "Season matching scores"
                )

                ranking_data = pd.DataFrame(
                    ranked_seasons,
                    columns=[
                        "Season",
                        "Matches"
                    ]
                )

                st.dataframe(
                    ranking_data,
                    use_container_width=True,
                    hide_index=True
                )


# ============================================================
# PAGE 2 — EXPLORE SEASONS
# ============================================================

elif page == "Explore Seasons":

    st.title("🌿 Explore the Seasons")

    st.write(
        "Choose a season to explore the environmental indicators "
        "recorded in the dataset."
    )

    seasons = sorted(
        data["Season_Name"]
        .dropna()
        .unique()
    )

    selected_season = st.selectbox(
        "Select a season:",
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

    if "English_Equivalent" in season_data.columns:

        english_names = (
            season_data["English_Equivalent"]
            .dropna()
            .unique()
        )

        if len(english_names) > 0:

            st.write(
                f"**English equivalent:** "
                f"{english_names[0]}"
            )

    if "Start_Month" in season_data.columns:

        start_months = (
            season_data["Start_Month"]
            .dropna()
            .unique()
        )

        if len(start_months) > 0:

            st.write(
                f"**Start month:** "
                f"{start_months[0]}"
            )

    if "End_Month" in season_data.columns:

        end_months = (
            season_data["End_Month"]
            .dropna()
            .unique()
        )

        if len(end_months) > 0:

            st.write(
                f"**End month:** "
                f"{end_months[0]}"
            )

    st.divider()

    # --------------------------------------------------------
    # INDICATORS BY TYPE
    # --------------------------------------------------------

    st.subheader("Seasonal indicators")

    if "Indicator_type" in season_data.columns:

        indicator_types = sorted(
            season_data["Indicator_type"]
            .dropna()
            .unique()
        )

        selected_type = st.selectbox(
            "Choose an indicator type:",
            indicator_types
        )

        filtered_data = season_data[
            season_data["Indicator_type"]
            == selected_type
        ]

    else:

        filtered_data = season_data

    display_columns = [
        column
        for column in [
            "Indicator_type",
            "Indicator_Name",
            "Description"
        ]
        if column in filtered_data.columns
    ]

    if display_columns:

        st.dataframe(
            filtered_data[display_columns]
            .drop_duplicates()
            .reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "The expected indicator columns were not found "
            "in the CSV file."
        )


# ============================================================
# PAGE 3 — DATA & VISUALISATIONS
# ============================================================

elif page == "Data & Visualisations":

    st.title("📊 Data & Visualisations")

    st.write(
        "Explore the number and types of seasonal indicators "
        "contained in the dataset."
    )

    st.divider()

    # --------------------------------------------------------
    # DATASET SUMMARY
    # --------------------------------------------------------

    st.subheader("Dataset summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total records",
        len(data)
    )

    col2.metric(
        "Number of seasons",
        data["Season_Name"].nunique()
    )

    col3.metric(
        "Indicator types",
        data["Indicator_type"].nunique()
        if "Indicator_type" in data.columns
        else 0
    )

    st.divider()

    # --------------------------------------------------------
    # INDICATORS PER SEASON
    # --------------------------------------------------------

    st.subheader(
        "Number of indicators recorded for each season"
    )

    season_counts = (
        data.groupby("Season_Name")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        season_counts
    )

    # --------------------------------------------------------
    # INDICATOR TYPE COUNTS
    # --------------------------------------------------------

    if "Indicator_type" in data.columns:

        st.subheader(
            "Indicators by type"
        )

        type_counts = (
            data["Indicator_type"]
            .value_counts()
        )

        st.bar_chart(
            type_counts
        )

    # --------------------------------------------------------
    # UNIQUE INDICATORS
    # --------------------------------------------------------

    st.subheader(
        "Unique indicators"
    )

    unique_indicators = (
        data["Indicator_Name"]
        .value_counts()
        .reset_index()
    )

    unique_indicators.columns = [
        "Indicator",
        "Number of records"
    ]

    st.dataframe(
        unique_indicators,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # RAW DATA OPTION
    # --------------------------------------------------------

    st.divider()

    with st.expander("View dataset"):

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "CITS 1501 Introduction to Programming with Python"
)

st.sidebar.caption(
    f"{len(data)} records loaded from Data.csv"
)