# Import Streamlit to build the interactive season-finder page.
import streamlit as st

# Import the shared dataset loader and the season-scoring function.
from data_processing.data_loader import load_data
from data_processing.season_matcher import calculate_season_scores


# Configure the page's browser title, icon, and wide layout.
st.set_page_config(
    page_title="Season Finder",
    page_icon="🔎",
    layout="wide",
)


# Load the cleaned seasonal dataset once for this page run.
df = load_data()

# Group selectable signs by category; each category has a question and options.
# These labels are passed to the scorer, which maps them to dataset matching rules.
SECTION_CONFIG = {
    # Signs about birds, paired with the question shown above their choices.
    "Birds": {
        "question": "What birds are you noticing?",
        "options": [
            "fledglings",
            "magpies",
            "bronzewing pigeons",
            "emus",
            "ravens",
            "black swans",
            "crows",
            "wedge-tailed shearwaters",
            "bird eggs",
            "willie wagtails swooping",
            "wattle birds swooping",
            "magpies swooping",
            "rainbow bee-eaters",
        ],
    },
    # Signs about reptiles and amphibians.
    "Reptiles": {
        "question": "What reptile activity are you noticing?",
        "options": [
            "dugites",
            "king skinks",
            "snakes",
            "reptile skins",
            "tadpoles becoming frogs",
            "goannas",
            "frogs",
            "tortoises",
            "moaning frogs",
            "turtles",
            "motorbike frogs"
        ],
    },
    # Signs about mammals.
    "Mammals": {
        "question": "What mammals are you noticing?",
        "options": [
            "kangaroos",
            "possums",
            "whales migrating",
            "quendas",
        ],
    },
    # Signs about fish, shellfish, and other marine life.
    "Marine": {
        "question": "What marine life are you noticing?",
        "options": [
            "mullet",
            "bream",
            "marron",
            "crabs",
            "mussels",
            "abalone",
            "salmon",
            "herring",
            "gilgies",
            "freshwater fish",
            "whales migrating",
        ],
    },
    # Signs about insects and their activity.
    "Insects": {
        "question": "What insect activity are you noticing?",
        "options": [
            "insects abundants with flowers",
            "fly ants",
        ],
    },
    # Signs about native trees and other woody plants.
    "Trees": {
        "question": "What native trees can you see?",
        "options": [
            "moodjar (Christmas tree)",
            "paperbark tree",
            "jarrah",
            "marri",
            "ghost gums",
            "red flowering gums",
            "banksia",
            "eucalypts",
            "weeping peppermint trees",
            "bull banksia",
            "sheoaks trees",
            "golden acacia",
            "grass trees",
            "quandong trees",
            "rottnest island tea tree",
        ],
    },
    # Signs about flowering plants and fruit.
    "Flowers and Fruits": {
        "question": "What flowers and fruits are you seeing?",
        "options": [
            "yams",
            "rottnest island daisy",
            "kangaroo paw",
            "orchids",
            "berries",
            "lillies",
            "djilba flowers",
            "purple flags",
            "bluberry lilies",
            "summer flame",
            "white flowers",
            "red flowers",
            "samphire",
            "zamia",
        ],
    },
    # Signs about winds and storms.
    "Winds / Storms": {
        "question": "What wind or storm conditions are you noticing?",
        "options": [
            "afternoon sea breeze (south-west)",
            "morning easterly winds",
            "hot easterly winds",
            "light southerly breeze (south east-south west)",
            "winds west and south",
            "frequent gales",
            "frequent storms",
            "harsh costal winds",
            "windy days",
        ],
    },
    # Signs describing current or seasonal rainfall.
    "Rain": {
        "question": "What current rainfall patterns are you experiencing?",
        "options": [
            "decreased rainfall",
            "little to no rainfall",
            "some days are cool and rainy",
            "inland water supplies replenished",
            "wettest time of the year",
            "snow on peaks of ranges",
            "waterways swelled",
            "catchments start to fill",
            "second rains",
        ],
    },
    # Signs describing temperatures and seasonal changes in warmth or cold.
    "Temperature": {
        "question": "How do the temperatures feel right now?",
        "options": [
            "warm temperatures",
            "cool temperatures",
            "cold temperatures",
            "transitional temperatures",
            "days are very dry",
            "fire danger is high",
            "hottest time of the year",
            "nights are cool",
            "mornings are dewy",
            "coldest time of the year",
            "cold days and nights",
            "warm sunny days",
            "warming trend",
            "less cold fronts",
            "longer dry periods"
        ],
    },
    # Signs describing visible cloud or sky conditions.
    "Sky": {
        "question": "What sky conditions are you noticing?",
        "options": [
            "clear skies",
            "clustered clouds",
        ],
    },
}


# Introduce the page and explain what the user should select.
st.title("What season are you in?")
st.write("Pick indicators that you are noticing around you.")

# Store each category's selections under that category name.
selected_by_section = {}
# Create one heading and multi-select widget for every configured category.
for section_name, config in SECTION_CONFIG.items():
    # Label the current category.
    st.subheader(section_name)
    # Save the selected option values for this category.
    selected_by_section[section_name] = st.multiselect(
        config["question"],
        config["options"],
    )


# Run the matching workflow only when the user presses the button.
if st.button("Find Season"):
    # Flatten all category selections into one list of signs to match.
    selected_observations = [
        item
        for values in selected_by_section.values()
        for item in values
    ]

    # Require at least one selection before asking the scorer for results.
    if not selected_observations:
        st.warning("Select at least one sign before finding a season.")
    else:
        # Count matching selected signs for each season in the dataset.
        scores = calculate_season_scores(df, selected_observations)
        # Find the largest score, using zero if the result mapping is empty.
        highest_score = max(scores.values(), default=0)

        # A zero high score means none of the selected signs matched any season.
        if highest_score == 0:
            st.warning(
                "None of those signs matched the dataset. Try a different selection."
            )
        else:
            # Collect every season tied for the greatest matching-sign score.
            leading_seasons = [
                season for season, score in scores.items() if score == highest_score
            ]

            # Give a single-season result a distinct message from a tie.
            if len(leading_seasons) == 1:
                st.success(
                    f"Most likely season: **{leading_seasons[0]}** "
                    f"({highest_score} matching signs)"
                )
            else:
                st.success(
                    f"Your signs match multiple seasons: "
                    f"**{', '.join(leading_seasons)}** "
                    f"({highest_score} matching signs each)"
                )

            # Sort scores highest-first, then alphabetically to break ties consistently.
            ranking = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
            # Add a heading and show every season's score in a compact table.
            st.subheader("Season matching scores")
            st.dataframe(
                {
                    "Season": [season for season, _ in ranking],
                    "Matching signs": [score for _, score in ranking],
                },
                use_container_width=True,
                hide_index=True,
            )