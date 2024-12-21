# pylint: disable=import-error
"business agent"
import os
import sys
from base_agent import BaseAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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
            "healthcare_facilities",
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

    def ask_llm(self):
        """Ask the LLM for information.

        Args:
            llm (object, optional): The LLM instance to handle text processing.
                               Not used as we're using Claude directly.
        Returns:
            str: An infrastructure assessment
            or questions about missing information.
        """
        # if not self.collected_data:
        #   return "Please provide infrastructure-related information."

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
        """Construct the prompt for the LLM with
          neighborhood visualization capabilities.
        
        Returns:
            str: The constructed prompt
        """
        return f"""Role: You are an expert urban planner specializing
          in smart neighborhood design and sustainable community development.

    Context: You are tasked with creating a detailed intelligent neighborhood
      plan that includes both a visual layout and comprehensive infrastructure assessment.

    Task: Analyze the provided data and respond in ONE of these two formats:

    1. If ANY required information is missing:
    - List ONLY the specific missing items as questions
    - Format: "- What are the [missing item] planned for this neighborhood?"
    - Consider both physical infrastructure and smart technology requirements
    - Do not include any other text or explanations

    2. If ALL required information is available, provide a TWO-PART response:

    PART 1 - NEIGHBORHOOD LAYOUT:
    Title: "Smart Neighborhood Visual Layout"

    a) Legend:
    List all components with symbols (R: Residential, C: Commercial, etc.)

    b) Grid Specifications:
    - Total dimensions
    - Zone sizes
    - Street widths
    - Building footprints

    c) ASCII Layout Plan:
    Create a visual grid using ASCII characters showing:
    - Building placements
    - Street layouts
    - Green spaces
    - Community facilities
    Format:
    +------------------------+
    |  R  |  G  |  R  |  C  |
    |  S  |  S  |  S  |  S  |
    |  R  |  T  |  R  |  G  |
    +------------------------+
    (You can choose the most efficient area to represent the layout of the nerighborhood)
    PART 2 - INFRASTRUCTURE ASSESSMENT:
    Title: "Infrastructure Assessment Summary:"

    a) Smart Infrastructure Layout:
    - Strategic positioning of buildings and facilities
    - Integration of smart systems and IoT infrastructure
    - Transportation network optimization
    - Green spaces and community areas distribution

    b) Quality of Life Considerations:
    - Walking distances to essential services
    - Noise and pollution reduction measures
    - Community interaction spaces
    - Safety and security features

    c) Sustainability Features:
    - Energy efficiency solutions
    - Waste management systems
    - Water conservation methods
    - Environmental impact reduction

    d) Smart Technology Integration:
    - IoT sensor networks
    - Smart grid implementation
    - Digital services infrastructure
    - Data collection and analysis systems

    e) Specific Recommendations:
    - Infrastructure optimization opportunities
    - Technology enhancement suggestions
    - Community engagement improvements
    - Future expansion possibilities

    Required information: {self.required_info}
    Provided data: {self.collected_data}

    Note: Ensure the layout and assessment work together to create an optimized living environment that balances technology integration with human-centric design principles."""
