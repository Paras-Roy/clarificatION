import requests
import pandas as pd
import json

class CompanyAnalyzer:
    """
    A class for analyzing company financial and governance data using an AI model.

    This class loads company data from a CSV file, extracts relevant metrics,
    and sends them to an external AI API for financial analysis.

    Attributes:
        api_url (str): The API endpoint for AI analysis.
        model_name (str): The name of the AI model used for analysis.
        required_columns (list): A list of required company data fields.
        df (pd.DataFrame): The loaded dataset containing company information.

    Methods:
        _get_row_data(row: pd.Series) -> dict:
            Extracts required columns from a given row, ensuring safe access.

        analyze(row_data: pd.Series) -> str:
            Sends company data to the AI API and returns a structured analysis.
    """
    def __init__(self, api_url: str, model_name: str, csv_path: str):
        """
        Initializes the CompanyAnalyzer class.

        Args:
            api_url (str): The endpoint URL of the AI API.
            model_name (str): The name of the AI model to use.
            csv_path (str): Path to the CSV file containing company data.

        Raises:
            FileNotFoundError: If the CSV file cannot be found.
            pd.errors.ParserError: If the CSV file cannot be parsed properly.
        """
        self.api_url = api_url
        self.model_name = model_name
        self.required_columns = [
            'Company_Name', 'IVA_COMPANY_RATING', 'IVA_RATING_ANALYSIS',
            'ENVIRONMENTAL_PILLAR_SCORE', 'GOVERNANCE_PILLAR_SCORE',
            'SOCIAL_PILLAR_SCORE', 'CLIMATE_CHANGE_THEME_SCORE',
            'BUSINESS_ETHICS_THEME_SCORE', 'HUMAN_CAPITAL_THEME_SCORE',
            'HUMAN_CAPITAL_DEV_SCORE', 'ACCOUNTING_SCORE', 'BOARD_SCORE',
            'OWNERSHIP_AND_CONTROL_SCORE', 'PAY_SCORE'
        ]
        self.df = pd.read_csv(csv_path)
    def _get_row_data(self, row: pd.Series) -> dict:
        """
        Safely extracts all required data from a row.

        Args:
            row (pd.Series): A row from the company dataset.

        Returns:
            dict: A dictionary containing the required company data fields.
        """
        return {col: row[col] if col in row else "N/A" for col in self.required_columns}

    def analyze(self, row_data: pd.Series) -> str:
        """
        Analyzes a company's financial and governance data using an AI model.

        This function constructs a prompt using the company's scores and
        sends it to the AI API for analysis. The response is processed
        as a bullet list of strengths and weaknesses.

        Args:
            row_data (pd.Series): A row containing company-specific data.

        Returns:
            str: A text-based AI-generated analysis of the company.

        Raises:
            requests.exceptions.RequestException: If the API call fails.
            json.JSONDecodeError: If the API response is not valid JSON.

        Example:
            >>> company_analyzer = CompanyAnalyzer("https://api.example.com", "llama-model", "data.csv")
            >>> row = company_analyzer.df.iloc[0]
            >>> analysis = company_analyzer.analyze(row)
            >>> print(analysis)
        """
        try:

            # Build prompt
            prompt = f"""Analyze {row_data['Company_Name']} with rating {row_data['IVA_COMPANY_RATING']}.

            Scores: {json.dumps({k:v for k,v in row_data.items() if 'SCORE' in k})}
            Write in no more than 100 words a bullet list of strenghts and weaknesses regarding the scores.
"""

            # API request with streaming
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a financial analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": True
                },
                stream=True
            )

            # Process streamed response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        full_response += chunk.get("message", {}).get("content", "")
                    except json.JSONDecodeError:
                        continue

            return full_response or "No analysis generated"

        except Exception as e:
            return f"Analysis failed: {str(e)}"
