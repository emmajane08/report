from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# LOAD AND PREPARE DATA
# ============================================================

DATA_FILE = Path(__file__).parent / "Data.csv"


data = pd.read_csv(DATA_FILE)

# Clean column names and text values so matching is reliable.
data.columns = data.columns.str.strip()

for column in data.select_dtypes(include="object").columns:
    data[column] = (
        data[column]
        .fillna("")
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Noongar Seasonal Calendar",
    page_icon="🌿",
    layout="wide",
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalise_text(value):
    """Make text easier to compare without changing what is displayed."""
    return " ".join(str(value).lower().split())


def row_matches_rule(row, rule):
    """
    Check whether one dataset row matches one user observation.

    A rule can specify an indicator name and/or words that should
    occur in the description. This lets the app distinguish choices
    such as different rainfall descriptions even when the CSV uses
    the same Indicator_Name (for example, 'Rain').
    """
    indicator = normalise_text(row["Indicator_Name"])
    description = normalise_text(row["Description"])

    allowed_names = [
        normalise_text(name)
        for name in rule.get("indicator_names", [])
    ]

    description_phrases = [
        normalise_text(phrase)
        for phrase in rule.get("description_contains", [])
    ]

    name_matches = (
        not allowed_names
        or indicator in allowed_names
    )

    description_matches = (
        not description_phrases
        or any(
            phrase in description
            for phrase in description_phrases
        )
    )

    return name_matches and description_matches


def calculate_season_scores(dataset, selected_rules):
    """
    Rank seasons by how many of the user's selected observations
    are supported by rows in each season.

    Each selected observation contributes at most one point to a
    season, even if several rows happen to match that observation.
    """
    scores = {}

    for season in sorted(dataset["Season_Name"].unique()):
        season_data = dataset[
            dataset["Season_Name"] == season
        ]

        score = 0

        for rule in selected_rules:
            matched = any(
                row_matches_rule(row, rule)
                for _, row in season_data.iterrows()
            )

            if matched:
                score += 1

        scores[season] = score

    return scores


def get_matching_rows(dataset, season, selected_rules):
    """Return the rows that explain why a season received matches."""
    season_data = dataset[
        dataset["Season_Name"] == season
    ]

    matches = []

    for rule in selected_rules:
        matching_rows = season_data[
            season_data.apply(
                lambda row: row_matches_rule(row, rule),
                axis=1,
            )
        ]

        if not matching_rows.empty:
            matches.append(
                {
                    "Observation": rule["label"],
                    "Indicator": matching_rows.iloc[0]["Indicator_Name"],
                    "Description": matching_rows.iloc[0]["Description"],
                }
            )

    return pd.DataFrame(matches)


def make_rule(label, indicator_names=None, description_contains=None):
    """Create a user-observation rule."""
    return {
        "label": label,
        "indicator_names": indicator_names or [],
        "description_contains": description_contains or [],
    }


# ============================================================
# USER-FRIENDLY OBSERVATIONS
# ============================================================
#
# The labels are designed for the app interface. The matching
# rules underneath them refer back to Indicator_Name and/or
# Description values that occur in the supplied CSV.
# ============================================================

USER_OPTIONS = {
    "🌧️ Rainfall": {
        "Little or no rain": make_rule(
            "Little or no rain",
            ["Rain"],
            ["little to no rainfall"],
        ),
        "Decreased rainfall": make_rule(
            "Decreased rainfall",
            ["Rain"],
            ["decreased rainfall"],
        ),
        "Some days are rainy": make_rule(
            "Some days are rainy",
            ["Rain"],
            ["some days are cool and rainy"],
        ),
        "Wettest time of year": make_rule(
            "Wettest time of year",
            ["Rain"],
            ["wettest time of year"],
        ),
        "Rain replenishes water supplies": make_rule(
            "Rain replenishes water supplies",
            ["Rain"],
            ["replenishes inland water supplies"],
        ),
        "Rain is decreasing": make_rule(
            "Rain is decreasing",
            ["Rain"],
            ["rain decreasing"],
        ),
        "Second rains": make_rule(
            "Second rains",
            ["Rain"],
            ["second rains"],
        ),
    },

    "🌡️ Temperature": {
        "Warm temperatures": make_rule(
            "Warm temperatures",
            ["Warm Temperatures"],
        ),
        "Hottest time of year": make_rule(
            "Hottest time of year",
            ["Warm Temperatures"],
            ["hottest time of the year"],
        ),
        "Warm sunny days": make_rule(
            "Warm sunny days",
            ["Warm Temperatures"],
            ["warm sunny days"],
        ),
        "Cool temperatures": make_rule(
            "Cool temperatures",
            ["Cool Temperatures"],
        ),
        "Cold days and nights": make_rule(
            "Cold days and nights",
            ["Cool Temperatures"],
            ["cold days and nights"],
        ),
        "Coldest time of year": make_rule(
            "Coldest time of year",
            ["Temperature"],
            ["coldest time of the year"],
        ),
        "Transitional temperatures": make_rule(
            "Transitional temperatures",
            ["Temperature"],
            ["transitional time of the year"],
        ),
        "Transformational temperature": make_rule(
            "Transformational temperature",
            ["Temperature"],
            ["transformational time of year"],
        ),
    },

    "💨 Weather conditions": {
        "Dry conditions": make_rule(
            "Dry conditions",
            ["Dry"],
        ),
        "Windy conditions": make_rule(
            "Windy conditions",
            ["Winds"],
        ),
        "Strong winds / gales": make_rule(
            "Strong winds / gales",
            ["Winds"],
            ["frequent gales"],
        ),
        "Storms": make_rule(
            "Storms",
            ["Storms"],
        ),
        "Clouds": make_rule(
            "Clouds",
            ["Clouds"],
        ),
        "Clear skies": make_rule(
            "Clear skies",
            ["Skies"],
            ["clear skies"],
        ),
        "Snow": make_rule(
            "Snow",
            ["Snow"],
        ),
        "Waterways are swelling": make_rule(
            "Waterways are swelling",
            ["Water"],
            ["waterways swelled"],
        ),
        "Fire season": make_rule(
            "Fire season",
            ["Fire season"],
        ),
    },

    "🌱 Plants and flowers": {
        "Moodjar (Christmas tree)": make_rule(
            "Moodjar (Christmas tree)",
            ["Moodjar (Christmas tree)"],
        ),
        "Paperbark tree": make_rule(
            "Paperbark tree",
            ["Paperbark tree"],
        ),
        "Banksia": make_rule(
            "Banksia",
            ["Banksia", "Bull Banksia"],
        ),
        "Eucalypts": make_rule(
            "Eucalypts",
            ["Eucalypts"],
        ),
        "Acacias": make_rule(
            "Acacias",
            ["Acacias", "Golden Acacias"],
        ),
        "Balgas (grass trees)": make_rule(
            "Balgas (grass trees)",
            ["Balgas (grass trees)", "(Balgas) grass trees"],
        ),
        "Flowers": make_rule(
            "Flowers",
            ["Flowers"],
        ),
        "Orchids": make_rule(
            "Orchids",
            ["Orchids"],
        ),
        "Jarrah": make_rule(
            "Jarrah",
            ["Jarrah"],
        ),
        "Marri": make_rule(
            "Marri",
            ["Marri"],
        ),
        "Lilies": make_rule(
            "Lilies",
            ["Lilies"],
        ),
        "Purple Flags": make_rule(
            "Purple Flags",
            ["Purple Flags"],
        ),
        "White flowers": make_rule(
            "White flowers",
            ["White flowers"],
        ),
        "Red flowerings": make_rule(
            "Red flowerings",
            ["Red flowerings"],
        ),
        "Red-flowering Gum": make_rule(
            "Red-flowering Gum",
            ["Red-flowering Gum"],
        ),
        "Quandong trees": make_rule(
            "Quandong trees",
            ["Quandong trees"],
        ),
        "Sheoak trees": make_rule(
            "Sheoak trees",
            ["Sheoak trees", "Sheoaks"],
        ),
        "Wild Carrots": make_rule(
            "Wild Carrots",
            ["Wild Carrots"],
        ),
        "Wild potatoes": make_rule(
            "Wild potatoes",
            ["Wild potatoes"],
        ),
        "Yams": make_rule(
            "Yams",
            ["yams"],
        ),
        "Berries": make_rule(
            "Berries",
            ["berries"],
        ),
        "Jeeriji (zamia)": make_rule(
            "Jeeriji (zamia)",
            ["jeeriji (zamia)", "Female jeeriji (zamia)"],
        ),
        "Yanget (Bullrushes)": make_rule(
            "Yanget (Bullrushes)",
            ["Yanget (Bullrushes)"],
        ),
        "Rottnest Island daisy": make_rule(
            "Rottnest Island daisy",
            ["Rottnest Island daisy"],
        ),
    },

    "🐾 Animals": {
        "Frogs": make_rule(
            "Frogs",
            [
                "Frogs",
                "frogs",
                "frogs (kooyal)",
                "kwooyar (moaning frogs)",
                "kooboolong (motorbike frog)",
            ],
        ),
        "Reptiles": make_rule(
            "Reptiles",
            ["Reptiles", "reptiles"],
        ),
        "Snakes": make_rule(
            "Snakes",
            ["snakes", "snake (Waugal)"],
        ),
        "Kangaroos": make_rule(
            "Kangaroos",
            ["Yonga (Kangaroo)", "Yongar (Kangaroo)"],
        ),
        "Emus": make_rule(
            "Emus",
            ["Emu", "Waitj (emu)", "weitj (emus)"],
        ),
        "Magpies": make_rule(
            "Magpies",
            ["Koolbardi (Magpie)", "Koolbardies (Magpies)", "magpies (Koolbardi)"],
        ),
        "Black swans": make_rule(
            "Black swans",
            ["Mali (Black Swan)"],
        ),
        "Fish": make_rule(
            "Fish",
            ["Fish", "freshwater fish", "Salmon", "Herring", "Mullet", "bream"],
        ),
        "Marron": make_rule(
            "Marron",
            ["Marron", "marron"],
        ),
        "Gilgies / freshwater crayfish": make_rule(
            "Gilgies / freshwater crayfish",
            ["Gilgies", "gilgies (freshwater crayfish)", "freshwater crayfish (gilgies)"],
        ),
        "Tortoises": make_rule(
            "Tortoises",
            ["Tortoises", "tortoises", "tortoises (yaarkin)"],
        ),
        "Whales": make_rule(
            "Whales",
            ["Whales"],
        ),
        "Fledglings / young birds": make_rule(
            "Fledglings / young birds",
            ["Fledgings", "baby birds"],
        ),
        "Breeding animals": make_rule(
            "Breeding animals",
            ["Breeding"],
        ),
        "Bird eggs": make_rule(
            "Bird eggs",
            ["bird eggs", "eggs"],
        ),
        "Insects": make_rule(
            "Insects",
            ["Insects"],
        ),
    },

    "🔥 Activities": {
        "Mosaic Burning": make_rule(
            "Mosaic Burning",
            ["Mosaic Burning"],
        ),
        "Fishing": make_rule(
            "Fishing",
            ["Fishing", "fishing"],
        ),
        "Movement": make_rule(
            "Movement",
            ["Movement", "movement"],
        ),
        "Social gathering": make_rule(
            "Social gathering",
            ["social", "social time"],
        ),
        "Eating / food gathering": make_rule(
            "Eating / food gathering",
            ["eating"],
        ),
        "Young / newborn animals": make_rule(
            "Young / newborn animals",
            ["Young"],
        ),
        "Mia mia (houses or shelter)": make_rule(
            "Mia mia (houses or shelter)",
            ["mia mia (houses or shelter)"],
        ),
    },
}


# ============================================================
# ONLY SHOW OPTIONS THAT EXIST IN THE CSV
# ============================================================

actual_indicators = {
    normalise_text(value)
    for value in data["Indicator_Name"].unique()
}

valid_options = {}

for category, options in USER_OPTIONS.items():
    valid_options[category] = {}

    for label, rule in options.items():
        has_valid_indicator = any(
            normalise_text(name) in actual_indicators
            for name in rule["indicator_names"]
        )

        if has_valid_indicator:
            valid_options[category][label] = rule


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🌿 Noongar Seasonal Calendar")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "Season Finder",
        "Explore Seasons",
        "Data & Visualisations",
    ],
)

st.sidebar.divider()
st.sidebar.caption(f"{len(data)} records loaded")


# ============================================================
# PAGE 1 — SEASON FINDER
# ============================================================

if page == "Season Finder":

    st.title("🌿 Find the Season")

    st.write(
        "Select observations that match what you are seeing in the "
        "environment. The app compares your selections with the "
        "seasonal indicators recorded in the dataset."
    )

    st.info(
        "You can select more than one observation from each category. "
        "The more selected observations that match a season, the higher "
        "that season's score."
    )

    st.divider()

    selected_rules = []

    for category, options in valid_options.items():
        st.subheader(category)

        selected_labels = st.multiselect(
            "Select observations:",
            list(options.keys()),
            key=category,
        )

        for label in selected_labels:
            selected_rules.append(options[label])

    st.divider()

    if st.button("🔎 Find Most Likely Season", type="primary"):

        if not selected_rules:
            st.warning("Please select at least one observation.")

        else:
            scores = calculate_season_scores(
                data,
                selected_rules,
            )

            ranked_seasons = sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )

            best_season, best_score = ranked_seasons[0]

            if best_score == 0:
                st.warning(
                    "None of the selected observations matched the "
                    "seasonal indicators in the dataset. Try selecting "
                    "a different combination."
                )

            else:
                st.success(
                    f"🌿 Most likely season: **{best_season}**"
                )

                st.metric(
                    "Matching observations",
                    best_score,
                )

                season_data = data[
                    data["Season_Name"] == best_season
                ]

                first_row = season_data.iloc[0]

                st.subheader(f"About {best_season}")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "English equivalent",
                    first_row["English_Equivalent"],
                )

                col2.metric(
                    "Start",
                    first_row["Start_of_month"],
                )

                col3.metric(
                    "End",
                    first_row["End_of_month"],
                )

                st.subheader("Why this season matched")

                matching_rows = get_matching_rows(
                    data,
                    best_season,
                    selected_rules,
                )

                if not matching_rows.empty:
                    st.dataframe(
                        matching_rows,
                        use_container_width=True,
                        hide_index=True,
                    )

                st.subheader("Season matching scores")

                ranking = pd.DataFrame(
                    ranked_seasons,
                    columns=[
                        "Season",
                        "Matching observations",
                    ],
                )

                st.dataframe(
                    ranking,
                    use_container_width=True,
                    hide_index=True,
                )


# ============================================================
# PAGE 2 — EXPLORE SEASONS
# ============================================================

elif page == "Explore Seasons":

    st.title("🌿 Explore the Seasons")

    st.write(
        "Choose a season and explore the environmental, plant, "
        "animal and activity indicators recorded for it."
    )

    seasons = sorted(data["Season_Name"].unique())

    selected_season = st.selectbox(
        "Choose a season:",
        seasons,
    )

    season_data = data[
        data["Season_Name"] == selected_season
    ]

    st.divider()

    st.header(selected_season)

    first_row = season_data.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "English equivalent",
        first_row["English_Equivalent"],
    )

    col2.metric(
        "Start",
        first_row["Start_of_month"],
    )

    col3.metric(
        "End",
        first_row["End_of_month"],
    )

    st.divider()

    st.subheader("Seasonal indicators")

    indicator_types = sorted(
        season_data["Indicator_type"].unique()
    )

    selected_type = st.selectbox(
        "Choose an indicator category:",
        ["All"] + indicator_types,
    )

    if selected_type == "All":
        display_data = season_data
    else:
        display_data = season_data[
            season_data["Indicator_type"] == selected_type
        ]

    display_data = (
        display_data[
            [
                "Indicator_type",
                "Indicator_Name",
                "Description",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE 3 — DATA & VISUALISATIONS
# ============================================================

elif page == "Data & Visualisations":

    st.title("📊 Data & Visualisations")

    st.write(
        "Explore the dataset using summary statistics, tables and charts."
    )

    st.divider()

    st.subheader("Dataset summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total records", len(data))
    col2.metric("Seasons", data["Season_Name"].nunique())
    col3.metric("Indicator types", data["Indicator_type"].nunique())

    st.divider()

    st.subheader("Number of records per season")

    season_counts = (
        data["Season_Name"]
        .value_counts()
        .sort_values(ascending=False)
    )

    st.bar_chart(season_counts)

    st.subheader("Number of records by indicator type")

    type_counts = (
        data["Indicator_type"]
        .value_counts()
        .sort_values(ascending=False)
    )

    st.bar_chart(type_counts)

    st.subheader("Most frequently recorded indicators")

    indicator_counts = data["Indicator_Name"].value_counts().head(20)

    st.bar_chart(indicator_counts)

    st.subheader("Explore the dataset")

    selected_type = st.selectbox(
        "Filter by indicator type:",
        ["All"] + sorted(data["Indicator_type"].unique()),
        key="data_filter",
    )

    if selected_type == "All":
        filtered_data = data
    else:
        filtered_data = data[
            data["Indicator_type"] == selected_type
        ]

st.dataframe(
	season_data[["Indicator_type", "Indicator_Name", "Description"]],
	hide_index=True,
	width="stretch",
)