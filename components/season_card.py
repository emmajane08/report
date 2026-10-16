# Import Streamlit to render the season details and navigation controls.
import streamlit as st


# Define a reusable component for displaying one season's information.
def display_season_information(season, information):
    """Display the information page for a selected season."""

    # When Back is clicked, clear the selection and reset the pie-chart key.
    if st.button("← Back"):
        st.session_state.selected_season = None
        st.session_state.season_pie_version += 1
        st.rerun()

    # Show the selected season's title.
    st.title(information["title"])

    # Separate the title from the season description.
    st.markdown("---")

    # Display the season's descriptive text.
    st.write(information["text"])

    # Separate the description from its sources.
    st.markdown("---")

    # Label the references, then display each semicolon-separated source.
    st.caption("Sources:")
    for source in information["source"].split(";"):
        st.caption(source.strip())