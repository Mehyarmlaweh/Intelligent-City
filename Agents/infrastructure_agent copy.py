# pylint: disable=import-error
"business agent"
import os
import sys
from base_agent import BaseAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Settings


class InfrastructureAgent(BaseAgent):
    """InfrastructureAgent class for handling 
        infrastructure planning and analysis"""
    
    def __init__(self, settings: Settings):
        """Initialize the InfrastructureAgent with configuration settings.
        
        Args:
            settings (Settings): Configuration settings instance
        """
        super().__init__(settings)
        
        self.claude_api_key = settings.CLAUDE_API_KEY
        self.required_info = [
            "building_types",
            "transportation",
            "public_spaces",
            "educational_facilities",
            "healthcare_facilities"
        ]
        self.collected_data = None
        self.environment = settings.ENVIRONMENT

    def collect_data(self, data: dict):
        """Collect data from the input dictionary.
        
        Args:
            data (dict): A dictionary containing 
            infrastructure-related information.
        
        Raises:
            ValueError: If the input is not a dictionary.
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")
        
        infrastructure_data = data.get("infrastructure")
        if infrastructure_data:
            self.collected_data = infrastructure_data

    def ask_llm(self, llm=None):
        """Ask the LLM for information.
        
        Args:
            llm (object, optional): The LLM instance to handle text processing.
                               Not used as we're using Claude directly.
        Returns:
            str: An infrastructure assessment 
            or questions about missing information.
        """
        if not self.collected_data:
            return "Please provide infrastructure-related information."
        
        # Construct a prompt for the LLM
        prompt = self._construct_prompt()
        
        try:
            response = self.claude.invoke(prompt)
            return response
        except Exception as e:
            if self.environment == "local":
                print(f"Error invoking Claude: {str(e)}")
            return "An error occurred while processing your request."

    def _construct_prompt(self) -> str:
        """Construct the prompt for the LLM.
        
        Returns:
            str: The constructed prompt
        """
        return f"""Role: You are an urban infrastructure planning expert.

Task: Compare the provided data against required information and respond in ONE of two ways:

1. If ANY required information is missing:
   - List ONLY the specific missing items as questions
   - Format: "- What are the [missing item]?"
   - Do not include any other text or explanations

2. If ALL required information is available:
   - Provide ONLY the infrastructure assessment report, you can add more details if needed and recommendations to optimi
   - Start directly with "Infrastructure Assessment Summary:"
   - Do not include any prefacing text or statements about data availability

Required information: {self.required_info}
Provided data: {self.collected_data}"""