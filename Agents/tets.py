# pylint: disable=import-error
import os
import sys
from business_agent import BusinessAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_settings


def main():
    # Get settings instance
    settings = get_settings()

    # Initialize the agent with settings
    agent = BusinessAgent(settings)

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
        }
    }

    # Test the agent
    agent.collect_data(test_data["energy"])
    response = agent.ask_llm()
    print(response)


if __name__ == "__main__":
    main()
