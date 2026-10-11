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
    "Rain": {
        "question": "What current rainfall patterns are you experiencing?",
        "options": [
            "Little or no rain",
            "Decreased rainfall",
            "Some days are rainy",
            "Wettest time of year",
            "Rain replenishes water supplies",
            "Rain is decreasing",
        ],
    },
    "Temperature": {
        "question": "How do the temperatures feel right now?",
        "options": [
            "Warm temperatures",
            "Cool temperatures",
            "Cold temperatures",
            "Transitional temperatures",
        ],
    },
    "Plants": {
        "question": "What native plants do you see around you?",
        "options": [
            "Moodjar (Christmas tree)",
            "Paperbark tree",
            "Banksia",
            "Acacias",
            "Grass trees",
            "Flowers",
            "Orchids",
        ],
    },
    "Animals": {
        "question": "Which animals have been more active lately?",
        "options": [
            "Frogs",
            "Reptiles",
            "Kangaroos",
            "Young animals",
            "Birds breeding",
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