# pylint: disable=import-error
import os
import sys
from business_agent import BusinessAgent
from energy_agent import EnergyAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import get_settings


def main():
    # Get settings instance
    settings = get_settings()

    # Initialize the agent with settings
    agent = EnergyAgent(settings)

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
                "local_economy": "Strong",
            },
            "competition_analysis": {
                "direct_competitors": 3,
                "market_share": "15%",
                "competitive_advantage": "Unique product offering",
            },
        },
        "energy": {"energy": """The energy requirements of the facility show an average daily consumption of 2500 kWh, with peak demand reaching 500 kW. Seasonal variations include a 30% increase in summer, 15% in winter, a 10% decrease in spring, and a 5% decrease in fall. Critical loads comprise the Data Center, HVAC systems, and Manufacturing Line operations.

The organization has a primary interest in integrating solar and wind energy. To support this, energy storage solutions are also required. The facility offers 25,000 square feet of rooftop space for renewable energy installations, with a budget cap of $2 million for the initial investment.

The facility is located at 34.0522°N, -118.2437°W, within a Mediterranean climate zone. This location experiences an average solar irradiance of 5.5 kWh/m²/day and an average wind speed of 12 mph. Seasonal temperatures range from 75-95°F in summer to 45-65°F in winter, with approximately 285 sunny days annually.

In terms of sustainability goals, the organization aims to achieve a 50% carbon reduction by 2030 and transition to an 80% renewable energy mix by 2025. Energy efficiency targets include:
    • A 30 percent reduction in energy intensity compared to the baseline.
    • A 25% reduction in peak demand.
    • A 40% reduction in water usage.

The organization is pursuing LEED Gold certification and aims to be Net Zero Ready. Additionally, tracking of greenhouse gas (GHG) emissions and Environmental, Social, and Governance (ESG) metrics is required to support these goals."""},
    }

    # Test the agent
    agent.collect_data(test_data["energy"])
    response = agent.ask_llm()
    print(response)


if __name__ == "__main__":
    main()
