import streamlit as st

from data_processing.data_loader import load_data


st.set_page_config(
    page_title="Season Finder",
    page_icon="🔎",
    layout="wide"
)


df = load_data()


st.title("🔎 Find the Most Likely Season")

st.write(
    "Select the environmental signs you are observing."
)


# Your friendly indicator questions go here.
# Keep the actual CSV indicator names/descriptions
# as the values used by the algorithm.


st.subheader("Rain")

rain_options = [
    "Little or no rain",
    "Decreased rainfall",
    "Some days are rainy",
    "Wettest time of year",
    "Rain replenishes water supplies",
    "Rain is decreasing"
]

selected_rain = st.multiselect(
    "What are you noticing about rainfall?",
    rain_options
)


st.subheader("Temperature")

temperature_options = [
    "Warm temperatures",
    "Cool temperatures",
    "Cold temperatures",
    "Transitional temperatures"
]

selected_temperature = st.multiselect(
    "What are you noticing about temperature?",
    temperature_options
)


st.subheader("Plants")

plant_options = [
    "Moodjar (Christmas tree)",
    "Paperbark tree",
    "Banksia",
    "Acacias",
    "Grass trees",
    "Flowers",
    "Orchids"
]

selected_plants = st.multiselect(
    "What plants or flowers are you noticing?",
    plant_options
)


st.subheader("Animals")

animal_options = [
    "Frogs",
    "Reptiles",
    "Kangaroos",
    "Young animals",
    "Birds breeding"
]

selected_animals = st.multiselect(
    "What animals are you noticing?",
    animal_options
)


if st.button("Find Season"):

    st.info(
        "Your season-matching algorithm will go here."
    )