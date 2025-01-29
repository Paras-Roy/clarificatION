import streamlit as st
from data import database
from searchbar import *
from company_card import company_card
from ml_model import *


APP_TITLE = "clarificatION - ESG bond explorer"
BODY_TITLE = "clarificatION"

st.set_page_config(page_title=APP_TITLE, page_icon=":chart_with_upwards_trend:", layout="wide")
companies = database.get_companies_names()

if "model" not in st.session_state:
    st.session_state["model"] = ModelInterface("ml-model/model.pkl")
    print("DEBUG: ML model loaded")

def get_card_data(selected_companies):
    result = []
    data_set = database.companies_data()

    for _, row in data_set.iterrows():
        if row["Company_Name"] in selected_companies:
            result.append(row)
    return result


st.markdown(
    """
    <style>
    .stMain {
        background-color: #22222E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"<h1 style='text-align: center; color: white; padding: 0'>{BODY_TITLE}</h1>",
unsafe_allow_html=True
)
selected_companies = render_searchbar(companies)

if selected_companies:
    card_data = get_card_data(selected_companies)
    for company in card_data:
        company_card(company)


