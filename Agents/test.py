# pylint: disable=import-error
import os
import sys
from business_agent import BusinessAgent
from energy_agent import EnergyAgent
from infrastructure_agent import InfrastructureAgent
from vision_agent import VisionAgent
from coordinator_agent import CoordinatorAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import get_settings
import base64


def main():
    # Get settings instance
    settings = get_settings()

    # Initialize the agent with settings
    businessAgent = BusinessAgent(settings)
    infrastructureAgent = InfrastructureAgent(settings)
    energyAgent = EnergyAgent(settings)

    coordinatorAgent = CoordinatorAgent(settings)

    visionAgent = VisionAgent(settings)

    # Example data
    test_data = """
Business
- Budget: $100,000
- Expected ROI: 25% within 2 years
- Target Demographics: Young professionals, age 25-35
- Commercial Zones: Downtown, Shopping Mall
- Economic Factors:
  - Market Growth: 5% annually
  - Inflation Rate: 2.5%
  - Local Economy: Strong
- Competition Analysis:
  - Direct Competitors: 3
  - Market Share: 15%
  - Competitive Advantage: Unique product offering

Energy
- Energy Requirements:
  - Electricity: 1000 kWh
  - Natural Gas: 500 therms
- Renewable Preferences:
  - Solar: High
  - Wind: Low
- Climate Data:
  - Temperature: 25°C
  - Humidity: 60%

Infrastructure
The neighborhood is being planned with a mix of different building types, including residential, commercial, and mixed-use buildings. The transportation system will include options such as buses, bike lanes, and electric vehicles to promote sustainable mobility.

For public spaces, the plan includes parks, community centers, and public squares, ensuring areas for recreation and social interaction. The neighborhood will be equipped with educational facilities, including a primary school, high school, and university, to cater to the educational needs of residents.

Healthcare services are a priority, with plans for a hospital, clinic, and pharmacy to provide essential medical care.

This data will help inform the planning and analysis of the infrastructure to ensure it meets the needs of the community while integrating smart technologies and sustainable solutions.
"""

    # Test the agent

    globalOutput = {}

    structured_input = coordinatorAgent.process_input(test_data)

    businessAgent.collect_data(structured_input)
    infrastructureAgent.collect_data(structured_input)
    energyAgent.collect_data(structured_input)
    coordinatorAgent.distribute_data(structured_input)

    globalOutput["Infrastructure"] = infrastructureAgent.ask_llm()
    globalOutput["Business"] = businessAgent.ask_llm()

    globalOutput["Energy"] = energyAgent.ask_llm()
    visionAgent.collect_data(globalOutput)
    print(visionAgent.ask_llm())


if __name__ == "__main__":
    main()
