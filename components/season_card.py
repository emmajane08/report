import streamlit as st


def display_season_information(season, information):
    """Display the information page for a selected season."""

    if st.button("← Back"):
        st.session_state.selected_season = None
        st.session_state.season_pie_version += 1
        st.rerun()

    st.title(information["title"])

    st.markdown("---")

    st.write(information["text"])

    st.markdown("---")

    st.caption(
        f"Source: {information['source']}"
    )