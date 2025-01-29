import streamlit as st
import plotly.graph_objects as go

def companies_comparator(companies):
    """
    companies_comparator Function Documentation
    -------------------------------------------

    Function Name:
        companies_comparator

    Description:
        This function generates an expandable section in a Streamlit app that displays
        a comparison of ESG (Environmental, Social, and Governance) scores for one or more companies.
        It visualizes the data using a grouped bar chart created with Plotly.

    Parameters:
        companies (list of dict):
            A list of dictionaries where each dictionary represents a company.
            Each dictionary should contain the company name and relevant ESG scores.
            If the list is empty or None, the function displays a message prompting the user
            to select at least one company.

    Visualization:
        - The function creates a grouped bar chart using Plotly to compare different companies across
          various ESG-related categories.
        - Categories include Environmental, Social, Governance, Climate Change, Business Ethics,
          Human Capital, Human Capital Development, Accounting, Board, Ownership & Control, and Pay.
        - If multiple companies are provided, their scores are displayed in different colors.

    Layout & Styling:
        - The comparison chart is placed inside a Streamlit `expander` to keep the UI clean.
        - The bar chart uses a dark background (`#22222E`) and white text.
        - A distinct color palette is applied to differentiate companies.
        - The legend is positioned horizontally below the chart for better readability.

    Returns:
        None (The function directly renders the chart in the Streamlit UI).

    Usage Example:
        companies_data = [
            {"Company_Name": "Company A", "ENVIRONMENTAL_PILLAR_SCORE": 7.5, "SOCIAL_PILLAR_SCORE": 6.8},
            {"Company_Name": "Company B", "ENVIRONMENTAL_PILLAR_SCORE": 8.2, "SOCIAL_PILLAR_SCORE": 7.1}
        ]
        companies_comparator(companies_data)

    """
    with st.expander("Show companies comparison", expanded=False):  # Wrapped everything inside an expander
        if companies == None or len(companies) == 0:
            st.write(
                    "Select at least one company to display the information."
                    )
        category_names = [
            'Environmental', 'Social', 'Governance', 'Climate Change', 'Business Ethics',
            'Human Capital', 'Human Capital Dev', 'Accounting', 'Board',
            'Ownership & Control', 'Pay'
        ]
        fig_comparison = go.Figure()

        for i, company in enumerate(companies):
            company_name = company['Company_Name']
            esg_values = [
                company.get("ENVIRONMENTAL_PILLAR_SCORE", 5),
                company.get("SOCIAL_PILLAR_SCORE", 5),
                company.get("GOVERNANCE_PILLAR_SCORE", 5),
                company.get("CLIMATE_CHANGE_THEME_SCORE", 5),
                company.get("BUSINESS_ETHICS_THEME_SCORE", 5),
                company.get("HUMAN_CAPITAL_THEME_SCORE", 5),
                company.get("HUMAN_CAPITAL_DEV_SCORE", 5),
                company.get("ACCOUNTING_SCORE", 5),
                company.get("BOARD_SCORE", 5),
                company.get("OWNERSHIP_AND_CONTROL_SCORE", 5),
                company.get("PAY_SCORE", 5)
            ]

            # Color palette
            colors = [
                'rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                'rgb(148, 103, 189)', 'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                'rgb(188, 189, 34)', 'rgb(23, 190, 207)'
            ]
            color = colors[i % len(colors)]

            fig_comparison.add_trace(go.Bar(
                y=esg_values,
                x=category_names,
                name=company_name,
                text=esg_values,
                textposition='outside',
                textfont=dict(size=14),
                marker_color=color
            ))

        fig_comparison.update_layout(
            xaxis_title="Categories",
            yaxis=dict(range=[0, 10.5], title="Score (out of 10)"),
            template="plotly_white",
            height=600,
            barmode='group',
            paper_bgcolor="#22222E",
            plot_bgcolor="#22222E",
            font=dict(color="white"),
            margin=dict(l=0, r=0, t=50, b=100),
            legend_title="Companies",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig_comparison, use_container_width=True)
