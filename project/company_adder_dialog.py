import streamlit as st

@st.dialog("Cast your vote")
def show_add_company_dialog():
    """Function to display the company form and return the data as a dictionary."""

    st.subheader("Add a new company")

    company_name = st.text_input("Company Name")
    company_description = st.text_area("Company Description")
    company_industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Retail", "Other"])
    company_location = st.text_input("Location")

    if st.button("Submit"):
        company_data = {
            "name": company_name,
            "description": company_description,
            "industry": company_industry,
            "location": company_location
        }

        # Access session_state.new_company from main to get data
        st.session_state.new_company = company_data
        st.rerun()

