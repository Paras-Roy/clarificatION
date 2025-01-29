import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from streamlit.runtime.state import session_state

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

def update_model(company_row):
    """
    Updates the model prediction for a given company based on user input.

    This function retrieves user-modified input values from Streamlit session state
    (stored as slider values), passes them to the prediction model, and updates
    the session state with the predicted values.

    Args:
        company_row (pd.Series): A row containing company-specific data.

    Workflow:
        1. Extracts the company name from the provided row.
        2. Retrieves input values from Streamlit session state using company-specific keys.
        3. Uses the stored model in session state to generate a prediction.
        4. Converts the prediction into integer values.
        5. Stores the prediction result in session state.
        6. Marks the company analysis as updated.
        7. Removes any previous analysis data from the session state.

    Returns:
        None

    Debugging:
        - Prints input values for verification.
        - Logs the model type and prediction output for debugging.

    Example:
        >>> update_model(company_row)
        # Updates session state with new predictions based on slider inputs.
    """
    company_name = company_row['Company_Name']
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
    predictions_int = [int(prediction[0, 0]), int(prediction[0, 1])]
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: prediction {prediction}")
    st.session_state[f"prediction_{company_name}"] = predictions_int

    st.session_state[f"analysis_{company_name}"] = True
    if f"analysis_data_{company_name}" in st.session_state:
        st.session_state.pop(f"analysis_data_{company_name}", None)

@st.dialog("Analysis summary")
def analysis(company, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11):
    """
    Displays and updates the AI-generated analysis for a given company.

    This function retrieves or generates an analysis based on the company's scores.
    If an analysis already exists in the Streamlit session state, it is displayed.
    Otherwise, the function updates the company's scores and processes the analysis
    using an AI model.

    Args:
        company (pd.Series): The company's data.
        s1 - s11 (float): Updated scores for various performance metrics.

    Workflow:
        1. Retrieves the company name and session state keys for the analysis.
        2. Checks if a previous analysis exists in the session state:
            - If found, it displays the stored analysis.
            - If not found, updates the company’s scores and runs the AI analysis.
        3. Shows a loading spinner while AI processes the analysis.
        4. Saves the generated analysis in the session state.
        5. Displays the analysis result.
        6. If no analysis is available, displays a default message.
        7. Provides a "Close" button to refresh the page.

    Returns:
        None

    Example:
        >>> analysis(company, 5.2, 7.8, 6.1, 4.3, 6.9, 5.0, 7.2, 8.5, 7.0, 6.8, 5.5)
        # Displays or generates an analysis based on updated scores.
    """
    company_name = company['Company_Name']
    analysis_data_name = f"analysis_{company_name}"
    analysis_data = f"analysis_data_{company_name}"

    if analysis_data_name in st.session_state:

        if analysis_data in st.session_state:
            st.write(
                st.session_state[analysis_data]
            )
        else:
            llama = st.session_state['llama']
            s_copy = company.copy(deep=True)
            company['ENVIRONMENTAL_PILLAR_SCORE'] = s1
            company['GOVERNANCE_PILLAR_SCORE'] = s2
            company['SOCIAL_PILLAR_SCORE'] = s3
            company['CLIMATE_CHANGE_THEME_SCORE'] = s4
            company['BUSINESS_ETHICS_THEME_SCORE'] = s5
            company['HUMAN_CAPITAL_THEME_SCORE'] = s6
            company['HUMAN_CAPITAL_DEV_SCORE'] = s7
            company['ACCOUNTING_SCORE'] = s8
            company['BOARD_SCORE'] = s9
            company['OWNERSHIP_AND_CONTROL_SCORE'] = s10
            company['PAY_SCORE'] = s11

            with st.spinner("Our AI is writing the analysis..."):
                result = llama.analyze(s_copy)
                st.session_state[f"analysis_data_{company_name}"] = result

            st.write(
                result
            )
    else:
        st.write(
            company.get("IVA_RATING_ANALYSIS", "No analysis available.")
        )

    if st.button("Close"):
        st.rerun()


def reset_card(company):
    """
    Resets the session state values for a given company's scores and removes related analysis data.

    This function restores the original scores of a company in the Streamlit session state
    and clears previously generated analysis and predictions.

    Args:
        company (pd.Series): A pandas Series representing the company's data.

    Workflow:
        1. Extracts the company name from the given data.
        2. Resets all score-related session state variables to their original values.
        3. Removes any existing analysis and predictions related to the company.
        4. Clears the reset flag from the session state.

    Returns:
        None

    Example:
        >>> reset_card(company)
        # Restores original company scores and clears previous analysis.
    """
    company_name = company['Company_Name']
    st.session_state[f"slide1_{company_name}"] = company['ENVIRONMENTAL_PILLAR_SCORE']
    st.session_state[f"slide2_{company_name}"] = company['GOVERNANCE_PILLAR_SCORE']
    st.session_state[f"slide3_{company_name}"] = company['SOCIAL_PILLAR_SCORE']
    st.session_state[f"slide4_{company_name}"] = company['CLIMATE_CHANGE_THEME_SCORE']
    st.session_state[f"slide5_{company_name}"] = company['BUSINESS_ETHICS_THEME_SCORE']
    st.session_state[f"slide6_{company_name}"] = company['HUMAN_CAPITAL_THEME_SCORE']
    st.session_state[f"slide7_{company_name}"] = company['HUMAN_CAPITAL_DEV_SCORE']
    st.session_state[f"slide8_{company_name}"] = company['ACCOUNTING_SCORE']
    st.session_state[f"slide9_{company_name}"] = company['BOARD_SCORE']
    st.session_state[f"slide10_{company_name}"] = company['OWNERSHIP_AND_CONTROL_SCORE']
    st.session_state[f"slide11_{company_name}"] = company['PAY_SCORE']

    st.session_state.pop(f"analysis_{company_name}", None)
    st.session_state.pop(f"prediction_{company_name}", None)
    st.session_state.pop(f"reset_{company_name}", None)


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
    :param company: pd.Series with company data.
    """
    # Create a container for the card
    with st.container():
        company_name = company['Company_Name']
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: building container for company: {company_name}")
        prediction = None
        prediction_key = f"prediction_{company_name}"
        reset_key = f"reset_{company_name}"

        if reset_key in st.session_state:
            print(f"DEBUG: reset found for {company_name}")
            reset_card(company)
            st.session_state.pop(reset_key, None)

        elif prediction_key in st.session_state:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: found prediction for {company_name}")
            prediction = st.session_state[prediction_key]
            prediction = [predictions_dict[prediction[0]], predictions_dict[prediction[1]]]


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
                    f"### Score Prediction: {prediction[0]}/{prediction[1]}",
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
                    marker_color=['#2ca02c', '#1f77b4', '#ff7f0e'],
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
            s1 = st.slider('Environmental Pillar Score', 0.0, 10.0, company['ENVIRONMENTAL_PILLAR_SCORE'], 0.1, key=f"slide1_{company_name}", on_change=update_model, args=(company,))
            s2 = st.slider("Governance Pillar Score", 0.0, 10.0, company['GOVERNANCE_PILLAR_SCORE'], 0.1, key=f"slide2_{company_name}", on_change=update_model, args=(company,))
            s3 = st.slider("Social Pillar Score", 0.0, 10.0, company['SOCIAL_PILLAR_SCORE'], 0.1, key=f"slide3_{company_name}", on_change=update_model, args=(company,))
            s4 = st.slider("Climate Change Theme Score", 0.0, 10.0, company['CLIMATE_CHANGE_THEME_SCORE'], 0.1, key=f"slide4_{company_name}", on_change=update_model, args=(company,))
            s5 = st.slider("Business Ethics Theme Score", 0.0, 10.0, company['BUSINESS_ETHICS_THEME_SCORE'], 0.1, key=f"slide5_{company_name}", on_change=update_model, args=(company,))
            s6 = st.slider("Human Capital Theme Score", 0.0, 10.0, company['HUMAN_CAPITAL_THEME_SCORE'], 0.1, key=f"slide6_{company_name}", on_change=update_model, args=(company,))

        with col3:
            s7 = st.slider("Human Capital Dev Score", 0.0, 10.0, company['HUMAN_CAPITAL_DEV_SCORE'], 0.1, key=f"slide7_{company_name}", on_change=update_model, args=(company,))
            s8 = st.slider("Accounting Score", 0.0, 10.0, company['ACCOUNTING_SCORE'], 0.1, key=f"slide8_{company_name}", on_change=update_model, args=(company,))
            s9 = st.slider("Board Score", 0.0, 10.0, company['BOARD_SCORE'], 0.1, key=f"slide9_{company_name}", on_change=update_model, args=(company,))
            s10 = st.slider("Ownership and Control Score", 0.0, 10.0, company['OWNERSHIP_AND_CONTROL_SCORE'], 0.1, key=f"slide10_{company_name}", on_change=update_model, args=(company,))
            s11 = st.slider("Pay Score", 0.0, 10.0, company['PAY_SCORE'], 0.1, key=f"slide11_{company_name}", on_change=update_model, args=(company,))
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("Read analysis", type="primary", key=f"analysis_button_{company_name}", use_container_width=True):
                    analysis(company, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11)

            with btn2:
                if st.button("Reset", type="secondary", key=f"reset_button_{company_name}", use_container_width=True):
                    st.session_state[f"reset_{company_name}"] = True
                    st.rerun()

        st.divider()

        st.markdown('</div>', unsafe_allow_html=True)
