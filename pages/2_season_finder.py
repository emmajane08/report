import streamlit as st

from data_processing.data_loader import load_data
from data_processing.season_matcher import calculate_season_scores


st.set_page_config(
    page_title="Season Finder",
    page_icon="🔎",
    layout="wide",
)


df = load_data()

SECTION_CONFIG = {
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
    "Mammals": {
        "question": "What mammals are you noticing?",
        "options": [
            "kangaroos",
            "possums",
            "whales migrating",
            "quendas",
        ],
    },
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
    "Insects": {
        "question": "What insect activity are you noticing?",
        "options": [
            "insects abundants with flowers",
            "fly ants",
        ],
    },
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
    "Sky": {
        "question": "What sky conditions are you noticing?",
        "options": [
            "clear skies",
            "clustered clouds",
        ],
    },
}


st.title("What season are you in?")
st.write("Pick indicators that you are noticing around you.")

selected_by_section = {}
for section_name, config in SECTION_CONFIG.items():
    st.subheader(section_name)
    selected_by_section[section_name] = st.multiselect(
        config["question"],
        config["options"],
    )


if st.button("Find Season"):
    selected_observations = [
        item
        for values in selected_by_section.values()
        for item in values
    ]

    if not selected_observations:
        st.warning("Select at least one sign before finding a season.")
    else:
        scores = calculate_season_scores(df, selected_observations)
        highest_score = max(scores.values(), default=0)

        if highest_score == 0:
            st.warning(
                "None of those signs matched the dataset. Try a different selection."
            )
        else:
            leading_seasons = [
                season for season, score in scores.items() if score == highest_score
            ]

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

            ranking = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
            st.subheader("Season matching scores")
            st.dataframe(
                {
                    "Season": [season for season, _ in ranking],
                    "Matching signs": [score for _, score in ranking],
                },
                use_container_width=True,
                hide_index=True,
            )