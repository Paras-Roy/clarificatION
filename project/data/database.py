import streamlit as st
import pandas as pd
from typing import List

@st.cache_data
def companies_data():
    return pd.read_csv("data/df_demo.csv")

@st.cache_data
def get_companies_names() -> List[str]:
    print(companies_data().columns)
    return sorted(companies_data()["Company_Name"].tolist())
