# pylint: disable=import-error
import os
import sys
from infrastructure_agent import InfrastructureAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_settings

def main():
    # Get settings instance
    settings = get_settings()
    
    # Initialize the agent with settings
    agent = InfrastructureAgent(settings)

    # Example data
    test_data = {
        "infrastructure": {"""
The neighborhood is being planned with a mix of different building types, 
                     including residential, commercial, and mixed-use 
                     buildings. The transportation system will include options such as buses, bike lanes, and electric vehicles to promote sustainable mobility.

For public spaces, the plan includes parks, community centers, and public squares, ensuring areas for recreation and social interaction. The neighborhood will be equipped with educational facilities, including a primary school, high school, and university, to cater to the educational needs of residents.

Healthcare services are a priority, with plans for a hospital, clinic, and pharmacy to provide essential medical care.

This data will help inform the planning and analysis of the infrastructure to ensure it meets the needs of the community while integrating smart technologies and sustainable solutions.












"""
   
                    }
    }
    
    # Test the agent
    agent.collect_data(test_data)
    response = agent.ask_llm()
    print(response)

if __name__ == "__main__":
    main()