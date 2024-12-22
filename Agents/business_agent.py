# pylint: disable=import-error
"business agent"
from base_agent import BaseAgent
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Settings


class BusinessAgent(BaseAgent):
    """BusinessAgent class for handling business-related queries and plans"""

    def __init__(self, settings: Settings):
        """Initialize the BusinessAgent with configuration settings.

        Args:
            settings (Settings): Configuration settings instance
        """
        super().__init__(settings)

        self.claude_api_key = settings.CLAUDE_API_KEY
        self.required_info = [
            "budget",
            "expected_roi",
            "target_demographics",
            "commercial_zones",
            "economic_factors",
            "Competition Analysis",
        ]
        self.collected_data = None
        self.environment = settings.ENVIRONMENT

    def collect_data(self, data: dict):
        """Collect data from the input dictionary.

        Args:
            data (dict): A dictionary containing business-related information.

        Raises:
            ValueError: If the input is not a dictionary.
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        business_data = data.get("business")
        if business_data:
            self.collected_data = business_data

    def ask_llm(self):
        """Ask the LLM for information.

        Args:
                            

        Returns:
            str: A business plan or questions about missing information.
        """
        # if not self.collected_data:
        #    return """No data provided.
        #    Please provide business-related information."""

        # Construct a prompt for the LLM
        prompt = self._construct_prompt()

        try:
            response = self.claude.invoke(prompt)
            return response.content
        except Exception as e:
            if self.environment == "local":
                print(f"Error invoking Claude: {str(e)}")
            return "An error occurred while processing your request."

    def _construct_prompt(self) -> str:
        """Construct the prompt for the LLM.

        Returns:
            str: The constructed prompt
        """
        return f"""Role: You are a business planning expert.     
        Task: Compare the provided data against required information and
        respond in ONE of two ways:
        1. If ANY required information is missing:
        - List ONLY the specific missing items as questions
        - Format: "- What is the [missing item]?"
        - Do not include any other text or explanations

        2. If ALL required information is available:
        - Provide ONLY the business plan
        - Start directly with "Executive Summary:"
        - Do not include any prefacing text or statements about data
          availability

        Required information: {self.required_info}
        Provided data: {self.collected_data}"""
