import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

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
    .full-height {
        height: 100%;
    }
</style>
"""

# Inject the CSS style
st.markdown(card_style, unsafe_allow_html=True)

predictions_dict = {6: 'AAA', 5: 'AA', 4: 'A', 3: 'BBB', 2: 'BB', 1: 'B', 0: 'CCC'}

# Mapping of alphabetical scores to numeric values for visualization
score_mapping = {
    "AAA": 10,
    "AA": 9,
    "A": 8,
    "BBB": 7,
    "BB": 6,
    "B": 5,
    "CCC": 4,
    "CC": 3,
    "C": 2,
}

def update_model(company_name):
    input_values = [
        st.session_state[f"slide1_{company_name}"],
        st.session_state[f"slide2_{company_name}"],
        st.session_state[f"slide3_{company_name}"],
        st.session_state[f"slide4_{company_name}"],
        st.session_state[f"slide5_{company_name}"],
        st.session_state[f"slide6_{company_name}"],
        st.session_state[f"slide7_{company_name}"],
        st.session_state[f"slide8_{company_name}"],
        st.session_state[f"slide9_{company_name}"],
        st.session_state[f"slide10_{company_name}"],
        st.session_state[f"slide11_{company_name}"]
    ]
    # print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG inputs: {input_values}")
    model = st.session_state['model']
    # print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: model type {type(model)}")
    prediction = model.predict([input_values])
    # print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: prediction {prediction}")
    st.session_state[f"prediction_{company_name}"] = prediction

def map_score_to_numeric(score):
    """
    Convert alphabetical score to numeric value using the score mapping.
    :param score: Alphabetical score (e.g., "AAA", "AA", etc.).
    :return: Numeric value corresponding to the score.
    """
    return score_mapping.get(score, 5)  # Default to 5 if score is missing or invalid

def company_card(company):
    """
    Generates a detailed card for the company using the data from the provided company dictionary.
    :param company: Dictionary with company data.
    """
    # Create a container for the card
    with st.container():
        company_name = company['Company_Name']
        # print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: company_name {company_name}")
        prediction = None
        prediction_key = f"prediction_{company_name}"
        if prediction_key in st.session_state:
            # print(f"DEBUG: found prediction for {company_name}")
            prediction = st.session_state[prediction_key]
            prediction = predictions_dict[prediction[0]]
            st.session_state.pop(prediction_key, None)

        # Row 1: Company Name and Industry Info
        col1, col2 = st.columns([3, 2])  # Adjust the column widths as necessary
        esg_value_alpha = company.get("IVA_COMPANY_RATING", "B")
        esg_value_numeric = map_score_to_numeric(esg_value_alpha)

        prev_rating_alpha = company.get("IVA_PREVIOUS_RATING", "B")
        prev_rating_numeric = map_score_to_numeric(prev_rating_alpha)

        delta = esg_value_numeric - prev_rating_numeric
        delta_arrow = ""
        delta_text = ""

        if delta > 0:
            delta_arrow = "\u25B2"  # Up arrow
            delta_color = "green"
            delta_text = f"{delta_arrow} {delta}"
        elif delta < 0:
            delta_arrow = "\u25BC"  # Down arrow
            delta_color = "red"
            delta_text = f"{delta_arrow} {delta}"
        else:
            delta_arrow = "\u003D"  # Equal sign
            delta_color = ""
            delta_text = f"{delta_arrow}"

        # Displaying ESG Rating with color

        if prediction == None:
            st.markdown(f"### {company['Company_Name']}: <span style='font-size:28px;'>{esg_value_alpha}<sup style='font-size:24px; color:{delta_color};'> ({delta_text})</sup></span>", unsafe_allow_html=True)
        else:
            score_col, pred_score_col = st.columns([3,2])
            with score_col:
                st.markdown(
                    f"### {company['Company_Name']}: <span style='font-size:28px;'>{esg_value_alpha}<sup style='font-size:24px; color:{delta_color};'> ({delta_text})</sup></span>",
                    unsafe_allow_html=True
                )

            with pred_score_col:
                st.markdown(
                    f"### Score Prediction: {prediction}",
                    unsafe_allow_html=True
                )

        st.markdown(f"**Industry:** {company['IVA_INDUSTRY']} | **GICS Sub-Industry:** {company['GICS_SUB_IND']}")

        # Barcharts and sliders
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            esg_values = [
                company.get("ENVIRONMENTAL_PILLAR_SCORE", 5),
                company.get("SOCIAL_PILLAR_SCORE", 5),
                company.get("GOVERNANCE_PILLAR_SCORE", 5),
            ]
            categories = ['Environmental', 'Social', 'Governance']

            fig_bars = go.Figure(data=[
                go.Bar(
                    y=esg_values,
                    x=categories,
                    orientation='v',
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                    text=esg_values,
                    textposition='outside',
                    textfont=dict(size=18),  # Increase font size of the values inside the bars
                )
            ])

            fig_bars.update_layout(
                xaxis_title="Score (out of 10)",
                yaxis=dict(range=[0, 10.5]),  # Extend Y-axis slightly for better spacing
                xaxis=dict(
                    title=dict(
                        text="Pillar Categories",  # X-axis label
                        font=dict(size=18)  # Font size for the X-axis label
                    ),
                    tickfont=dict(size=16),  # Increase font size for the X-axis tick labels
                ),
                template="plotly_white",
                height=400,
                paper_bgcolor="#22222E",
                plot_bgcolor="#22222E",
                margin=dict(l=0, r=0, t=0, b=0),  # Set the margins to zero for better layout
            )

            st.plotly_chart(fig_bars, use_container_width=True, key=f"bars_{company['Company_Name']}")  # Unique key for each chart
        # Column 2: ESG Analysis Summary (Expandable below chart)
        hide_sliders_limits = """
                <style>
                    div[data-testid="stSliderTickBarMin"],
                    div[data-testid="stSliderTickBarMax"] {
                        display: none;
                    }
                </style>
        """

        st.markdown(hide_sliders_limits, unsafe_allow_html=True)
        with col2:
            # model_features = [
            #         company['ENVIRONMENTAL_PILLAR_SCORE'],
            #         company['GOVERNANCE_PILLAR_SCORE'],
            #         company['SOCIAL_PILLAR_SCORE'],
            #         company['CLIMATE_CHANGE_THEME_SCORE'],
            #         company['BUSINESS_ETHICS_THEME_SCORE'],
            #         company['HUMAN_CAPITAL_THEME_SCORE'],
            #         company['HUMAN_CAPITAL_DEV_SCORE'],
            #         company['ACCOUNTING_SCORE'],
            #         company['BOARD_SCORE'],
            #         company['OWNERSHIP_AND_CONTROL_SCORE'],
            #         company['PAY_SCORE']
            # ]

            st.slider('Environmental Pillar Score', 0.0, 10.0, company['ENVIRONMENTAL_PILLAR_SCORE'], 0.1, key=f"slide1_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Governance Pillar Score", 0.0, 10.0, company['GOVERNANCE_PILLAR_SCORE'], 0.1, key=f"slide2_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Social Pillar Score", 0.0, 10.0, company['SOCIAL_PILLAR_SCORE'], 0.1, key=f"slide3_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Climate Change Theme Score", 0.0, 10.0, company['CLIMATE_CHANGE_THEME_SCORE'], 0.1, key=f"slide4_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Business Ethics Theme Score", 0.0, 10.0, company['BUSINESS_ETHICS_THEME_SCORE'], 0.1, key=f"slide5_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Human Capital Theme Score", 0.0, 10.0, company['HUMAN_CAPITAL_THEME_SCORE'], 0.1, key=f"slide6_{company['Company_Name']}", on_change=update_model, args=(company_name,))

        with col3:
            st.slider("Human Capital Dev Score", 0.0, 10.0, company['HUMAN_CAPITAL_DEV_SCORE'], 0.1, key=f"slide7_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Accounting Score", 0.0, 10.0, company['ACCOUNTING_SCORE'], 0.1, key=f"slide8_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Board Score", 0.0, 10.0, company['BOARD_SCORE'], 0.1, key=f"slide9_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Ownership and Control Score", 0.0, 10.0, company['OWNERSHIP_AND_CONTROL_SCORE'], 0.1, key=f"slide10_{company['Company_Name']}", on_change=update_model, args=(company_name,))
            st.slider("Pay Score", 0.0, 10.0, company['PAY_SCORE'], 0.1, key=f"slide11_{company['Company_Name']}", on_change=update_model, args=(company_name,))

            if st.button("Reset", type="primary"):
                st.session_state[f"slide1_{company['Company_Name']}"] = company['ENVIRONMENTAL_PILLAR_SCORE']
                st.session_state[f"slide2_{company['Company_Name']}"] = company['GOVERNANCE_PILLAR_SCORE']
                st.session_state[f"slide3_{company['Company_Name']}"] = company['SOCIAL_PILLAR_SCORE']
                st.session_state[f"slide4_{company['Company_Name']}"] = company['CLIMATE_CHANGE_THEME_SCORE']
                st.session_state[f"slide5_{company['Company_Name']}"] = company['BUSINESS_ETHICS_THEME_SCORE']
                st.session_state[f"slide6_{company['Company_Name']}"] = company['HUMAN_CAPITAL_THEME_SCORE']
                st.session_state[f"slide7_{company['Company_Name']}"] = company['HUMAN_CAPITAL_DEV_SCORE']
                st.session_state[f"slide8_{company['Company_Name']}"] = company['ACCOUNTING_SCORE']
                st.session_state[f"slide9_{company['Company_Name']}"] = company['BOARD_SCORE']
                st.session_state[f"slide10_{company['Company_Name']}"] = company['OWNERSHIP_AND_CONTROL_SCORE']
                st.session_state[f"slide11_{company['Company_Name']}"] = company['PAY_SCORE']


        with st.expander("Analysis Summary"):
            st.write(
                company.get("IVA_RATING_ANALYSIS", "No analysis available.")
            )

        st.divider()

        st.markdown('</div>', unsafe_allow_html=True)
