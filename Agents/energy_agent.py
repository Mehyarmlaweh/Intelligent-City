# pylint: disable=import-error
import os
import sys
from base_agent import BaseAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import Settings


class EnergyAgent(BaseAgent):
    """EnergyAgent class for handling energy analysis and planning"""

    def __init__(self, settings: Settings):
        """Initialize the EnergyAgent with configuration settings.

        Args:
            settings (Settings): Configuration settings instance
        """
        super().__init__(settings)

        self.claude_api_key = settings.CLAUDE_API_KEY
        self.required_info = [
            "energy_requirements",
            "renewable_preferences",
            "climate_data",
            "sustainability_goals",
        ]
        self.collected_data = None
        self.environment = settings.ENVIRONMENT

    def collect_data(self, data: dict):
        """Collect energy-related data from the input dictionary.

        Args:
            data (dict): A dictionary containing energy-related information.

        Raises:
            ValueError: If the input is not a dictionary.
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        energy_data = data.get("energy")
        if energy_data:
            self.collected_data = energy_data

    def ask_llm(self):
        """Ask the LLM for energy analysis and recommendations.

        Returns:
            str: An energy analysis plan or questions about missing information.
        """
        if not self.collected_data:
            return """No data provided.
            Please provide energy consumption and facility information."""

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
        """Construct the prompt for energy analysis.

        Returns:
            str: The constructed prompt
        """
        return f"""Role: You are an energy efficiency and sustainability expert.       
        Task: Compare the provided data against required information and
        respond in ONE of two ways:
        1. If ANY required information is missing:
        - List ONLY the specific missing items as questions
        - Format: "- What is the [missing item]?"
        - Do not include any other text or explanations

        2. If ALL required information is available:
        - Provide ONLY the energy analysis and optimization plan
        - Start directly with "Energy Assessment Summary:"
        - Include sections for:
          * Current Energy Profile
          * Efficiency Opportunities
          * Renewable Integration
          * Cost-Benefit Analysis
          * Implementation Timeline
        - Do not include any prefacing text or statements about data 
        availability

        Required information: {self.required_info}
        Provided data: {self.collected_data}"""
