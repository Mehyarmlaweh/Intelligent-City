"coordinator agent"
import ast
import os
import sys
from base_agent import BaseAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import Settings
from business_agent import BusinessAgent
from energy_agent import EnergyAgent
from infrastructure_agent import InfrastructureAgent
from vision_agent import VisionAgent


class CoordinatorAgent(BaseAgent):
    """Coordinator Agent to handle data collection and distribution."""

    def __init__(self, settings: Settings):
        """Initialize the CoordinatorAgent with configuration settings.

        Args:
            settings (Settings): Configuration settings instance.
        """
        super().__init__(settings)
        self.settings = settings
        self.business_agent = BusinessAgent(settings)
        self.energy_agent = EnergyAgent(settings)
        self.infrastructure_agent = InfrastructureAgent(settings)
        self.vision_agent = VisionAgent(settings)

    def process_input(self, user_input) -> dict:
        """Process user input into a structured dictionary.

        Args:
            user_input: Raw user input.

        Returns:
            dict: Structured data with keys for business, energy, and infrastructure.
        """
        # Construct a prompt to organize the input
        prompt = f"""
        Role: You are an expert assistant specializing in organizing and categorizing information.
        Task: Based on the provided input, structure the data into a dictionary with exactly three keys:
        - Provide ONLY the dictionary.
        - "business": Data related to budgets, market analysis, ROI, etc.
        - "energy": Data related to energy requirements, sustainability goals, renewables, etc.
        - "infrastructure": Data related to transportation, buildings, public spaces, and facilities.
        - Do not include any other text or explanations
        Input: {user_input}
        
        Output Format (as Python dictionary):
        {{
            "business": {{...}},
            "energy": {{...}},
            "infrastructure": {{...}}
        }}
        """

        # Use the base agent's LLM to generate the structured dictionary
        try:
            response = self.claude.invoke(prompt)
            try:
                response = ast.literal_eval(response.content)
                return response  # Safely parse the LLM's response
            except (SyntaxError, ValueError) as e:
                print(f"Error converting string to dictionary: {e}")
        except Exception as e:
            if self.settings.ENVIRONMENT == "local":
                print(f"Error processing input: {str(e)}")
            return "An error occurred while processing your request."

    def format_report(self, data):
        structured_input = self.process_input(data)
        self.business_agent.collect_data(structured_input)
        self.infrastructure_agent.collect_data(structured_input)
        self.energy_agent.collect_data(structured_input)
        globalOutput = {}
        globalOutput["Infrastructure"] = self.infrastructure_agent.ask_llm()
        globalOutput["Business"] = self.business_agent.ask_llm()
        globalOutput["Energy"] = self.energy_agent.ask_llm()
        self.vision_agent.collect_data(globalOutput)
        images = self.vision_agent.ask_llm()
        #print(images)
        # globalOutput["SVG_Image"] = images["image2_Claude"]
        # globalOutput["DallE_Image"] = images["image1_DallE"]
        return globalOutput, images
