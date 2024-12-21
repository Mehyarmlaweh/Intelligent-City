# pylint: disable=import-error
import os
import sys
from business_agent import BusinessAgent
from energy_agent import EnergyAgent
from infrastructure_agent import InfrastructureAgent
from vision_agent import VisionAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_settings
import base64


def main():
    # Get settings instance
    settings = get_settings()

    # Initialize the agent with settings
    agent = BusinessAgent(settings)
    agent1 = InfrastructureAgent(settings)

    agent2 = EnergyAgent(settings)

    agent3 = VisionAgent(settings)

    # Example data
    test_data = {
        "business": {
            "budget": 100000,
            "expected_roi": "25% within 2 years",
            "target_demographics": "Young professionals, age 25-35",
            "commercial_zones": ["Downtown", "Shopping Mall"],
            "economic_factors": {
                "market_growth": "5% annually",
                "inflation_rate": "2.5%",
                "local_economy": "Strong"
            },
            "Competition Analysis": {
                "direct_competitors": 3,
                "market_share": "15%",
                "competitive_advantage": "Unique product offering"
            }
        },
        "energy": {
            "energy_requirements": {
                "electricity": "1000 kWh",
                "natural_gas": "500 therms"
            },
            "renewable_preferences": {
                "solar": "High",
                "wind": "Low"
            },
            "climate_data": {
                "temperature": "25 C",
                "humidity": "60%"
            },
        },
        "infrastructure":{
            """The neighborhood is being planned with a mix of different building types, including residential, commercial, and mixed-use buildings. The transportation system will include options such as buses, bike lanes, and electric vehicles to promote sustainable mobility.

                For public spaces, the plan includes parks, community centers, and public squares, ensuring areas for recreation and social interaction. The neighborhood will be equipped with educational facilities, including a primary school, high school, and university, to cater to the educational needs of residents.

                Healthcare services are a priority, with plans for a hospital, clinic, and pharmacy to provide essential medical care.

                This data will help inform the planning and analysis of the infrastructure to ensure it meets the needs of the community while integrating smart technologies and sustainable solutions.
"""
        }
    }
    # Test the agent

    globalOutput = {}

    agent.collect_data(test_data)
    agent1.collect_data(test_data)

    agent2.collect_data(test_data)

    globalOutput["Infrastructure"] = agent1.ask_llm()
    globalOutput["Business"] = agent.ask_llm()

    globalOutput["Energy"] = agent2.ask_llm()
    agent3.collect_data(globalOutput)
    print(agent3.ask_llm())


if __name__ == "__main__":
    main()
