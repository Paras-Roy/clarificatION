import streamlit as st
from data import database
from searchbar import *
from company_card import company_card
from companies_comparator import *
from ml_model import *
from llama_wrapper import *


APP_TITLE = "ClarificatION - ESG bond explorer"
BODY_TITLE = "ClarificatION"

st.set_page_config(page_title=APP_TITLE, page_icon=":chart_with_upwards_trend:", layout="wide")
companies = database.get_companies_names()

if "model" not in st.session_state:
    st.session_state["model"] = ModelInterface("ml-model/model.pkl")
    print("DEBUG: ML model loaded")

if "llama" not in st.session_state:
    st.session_state["llama"] = CompanyAnalyzer(
        api_url="http://localhost:11434/api/chat",
        model_name="qwen2.5:0.5b",
        csv_path="data/df_demo.csv"
    )
    print("DEBUG: LLama model loaded")

def get_card_data(selected_companies):
    """
    Retrieves data for the specified companies from the database.

    This function filters the company dataset and returns the rows
    corresponding to the selected companies.

    Args:
        selected_companies (list): A list of company names to retrieve data for.

    Returns:
        list: A list of rows (as pandas Series) representing the data of the selected companies.

    Example:
        >>> selected = ["Company A", "Company B"]
        >>> data = get_card_data(selected)
        >>> print(data)  # List of matching rows

    Notes:
        - The function accesses the dataset through `database.companies_data()`.
        - It iterates through the dataset and selects rows where the "Company_Name"
          column matches one of the names in `selected_companies`.
    """
    result = []
    if selected_companies == None or len(selected_companies) == 0:
        return result

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

card_data = get_card_data(selected_companies)
companies_comparator(card_data)

if selected_companies:
    card_data = get_card_data(selected_companies)
    for company in card_data:
        company_card(company)


