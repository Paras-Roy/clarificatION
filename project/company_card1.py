import streamlit as st
import plotly.graph_objects as go
from expander import *

# CSS for card styling
card_style = """
<style>
    .company-card {
        background-color: 'white';
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
</style>
"""

# Inject the CSS style
st.markdown(card_style, unsafe_allow_html=True)

# Mapping of alphabetical scores to numeric values for visualization
score_mapping = {
    "AAA": 100,
    "AA": 90,
    "A": 80,
    "BBB": 70,
    "BB": 60,
    "B": 50,
    "CCC": 40,
    "CC": 30,
    "C": 20,
}

def map_score_to_numeric(score):
    """
    Convert alphabetical score to numeric value using the score mapping.
    :param score: Alphabetical score (e.g., "AAA", "AA", etc.).
    :return: Numeric value corresponding to the score.
    """
    return score_mapping.get(score, 50)  # Default to 50 if score is missing or invalid

def company_card(company):
    """
    Generates a detailed card for the company using the data from the provided company dictionary.
    :param company: Dictionary with company data.
    """
    # Create a container for the card
    with st.container():
        # Wrap the entire card content in a div with the class 'company-card'
        st.markdown('<div class="company-card">', unsafe_allow_html=True)

        # Row 1: Company info
        st.markdown(f"### {company['Company_Name']}")
        st.markdown(f"**Industry:** {company['IVA_INDUSTRY']} | **GICS Sub-Industry:** {company['GICS_SUB_IND']}")

        # Row 2: ESG Score Meter, Individual Bar Charts, and Analysis Summary
        col1, spacer1, col2, spacer2, col3 = st.columns([2, 0.3, 2, 0.3, 2])

        # ESG Score Meter in the first column
        with col1:
            st.subheader("ESG Score Meter")
            esg_value_alpha = company.get("IVA_COMPANY_RATING", "B")  # Default to "B" if value is missing
            esg_value_numeric = map_score_to_numeric(esg_value_alpha)

            fig_meter = go.Figure(go.Indicator(
                mode="gauge+number",  # Show gauge and number
                value=esg_value_numeric,
                number={'valueformat': '', 'suffix': ''},  # No numeric display
                title={'text': esg_value_alpha, 'font': {'size': 24}},  # Display the alphabetical score
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1f77b4"},
                    'steps': [
                        {'range': [0, 30], 'color': '#d9534f'},  # Red for low scores
                        {'range': [30, 60], 'color': '#f0ad4e'},  # Orange for medium scores
                        {'range': [60, 100], 'color': '#5cb85c'},  # Green for high scores
                    ]
                }
            ))
            fig_meter.update_layout(margin={'t': 0, 'b': 0, 'l': 0, 'r': 0})
            st.plotly_chart(fig_meter, use_container_width=True, key=f"meter_{company['Company_Name']}")  # Unique key for each chart

        # ESG Individual Bar Charts in the second column
        with col2:
            st.subheader("Pillar Scores")
            esg_values = [
                company.get("ENVIRONMENTAL_PILLAR_SCORE", "B"),
                company.get("SOCIAL_PILLAR_SCORE", "B"),
                company.get("GOVERNANCE_PILLAR_SCORE", "B"),
            ]
            categories = ['Environmental', 'Social', 'Governance']

            fig_bars = go.Figure(data=[
                go.Bar(
                    x=categories,
                    y=esg_values,
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                    text=esg_values,
                    textposition='outside',
                )
            ])

            fig_bars.update_layout(
                yaxis_title="Score (out of 100)",
                template="plotly_white",
                height = 400,
            )
            st.plotly_chart(fig_bars, use_container_width=True, key=f"bars_{company['Company_Name']}")  # Unique key for each chart

        # Analysis Summary in the third column
        with col3:
            st.subheader("Features")
            # st.text_area(
            #     label=f"Insights for {company['Company_Name']}",
            #     value=company.get("IVA_RATING_ANALYSIS", "No analysis available."),
            #     height=300,
            # )
            # slider_7 = st.slider("Feat 7", 0, 100, 50, 1, key="slider_7")
            # render_expander()
            hide_elements = """
                    <style>
                        div[data-testid="stSliderTickBarMin"],
                        div[data-testid="stSliderTickBarMax"] {
                            display: none;
                        }
                    </style>
            """
            predictors_dict.get("ENVIRONMENTAL_PILLAR_SCORE")

            st.markdown(hide_elements, unsafe_allow_html=True)
            slider_1 = st.slider('Environmental pillar score', 0, 100, 50, 1, key="slider_1")
            slider_2 = st.slider("Governance pillar score", 0, 100, 50, 1, key="slider_2")
            slider_3 = st.slider("Climate change theme score", 0, 100, 50, 1, key="slider_3")
            slider_4 = st.slider("Business ethics theme score", 0, 100, 50, 1, key="slider_4")
            slider_5 = st.slider("Human capital theme score", 0, 100, 50, 1, key="slider_5")
            slider_6 = st.slider("Human capital dev score", 0, 100, 50, 1, key="slider_6")
            slider_7 = st.slider("Accounting score", 0, 100, 50, 1, key="slider_7")
            slider_8 = st.slider("Board score", 0, 100, 50, 1, key="slider_7")
            slider_9 = st.slider("Ownership and control score", 0, 100, 50, 1, key="slider_7")
            slider_10 = st.slider("Pay score", 0, 100, 50, 1, key="slider_7")
            slider_10 = st.slider("Pay score", 0, 100, 50, 1, key="slider_7")
            slider_10 = st.slider("Tax transp pctl global", 0, 100, 50, 1, key="slider_7")

        # render_expander()
        st.divider()

        # Close the div tag for the card content
        st.markdown('</div>', unsafe_allow_html=True)
