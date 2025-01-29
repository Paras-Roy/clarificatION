import streamlit as st

def render_searchbar(companies):
    """
    Renders a multiselect dropdown for companies with dynamic selection.
    """
    selected_companies = st.multiselect(
        "",
        options=companies,
        default=[],
        help="You can type to filter and select companies.",
        label_visibility="hidden",
        placeholder="Search a company...",
        key="search_bar"
    )

    return selected_companies
