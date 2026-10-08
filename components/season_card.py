import streamlit as st


def display_season_information(season, information):
    """Display the information page for a selected season."""

    st.title(information["title"])

    st.markdown("---")

    st.write(information["text"])

    st.markdown("---")

    st.caption(
        f"Source: {information['source']}"
    )