import streamlit as st

def render_expander():
    # with st.expander("Apri per visualizzare i 7 slider"):
    slider_1 = st.slider("Feat 1", 0, 100, 50, 1, key="slider_1")
    slider_2 = st.slider("Feat 2", 0, 100, 50, 1, key="slider_2")
    slider_3 = st.slider("Feat 3", 0, 100, 50, 1, key="slider_3")
    slider_4 = st.slider("Feat 4", 0, 100, 50, 1, key="slider_4")
    slider_5 = st.slider("Feat 5", 0, 100, 50, 1, key="slider_5")
    slider_6 = st.slider("Feat 6", 0, 100, 50, 1, key="slider_6")
    slider_7 = st.slider("Feat 7", 0, 100, 50, 1, key="slider_7")

    return [slider_1, slider_2, slider_3, slider_4, slider_5, slider_6, slider_7]
