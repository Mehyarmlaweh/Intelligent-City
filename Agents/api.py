from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import sys 
import os 

from business_agent import BusinessAgent
from energy_agent import EnergyAgent
from infrastructure_agent import InfrastructureAgent
from vision_agent import VisionAgent
from coordinator_agent import CoordinatorAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_settings

app = FastAPI(
    title="Neighborhood Analysis API",
    description="API for analyzing neighborhoods using multiple specialized agents",
    version="1.0.0"
)
# Initialize settings
settings = get_settings()

# Initialize agents (move to a function to avoid global state)
def initialize_agents():
    return {
        'coordinator': CoordinatorAgent(settings),
        'business': BusinessAgent(settings),
        'infrastructure': InfrastructureAgent(settings),
        'energy': EnergyAgent(settings),
        'vision': VisionAgent(settings)
    }

agents = initialize_agents()

@app.post("/analyze")
async def analyze_neighborhood(query: str):
    """
    Analyzes a neighborhood based on the provided prompt using multiple specialized agents.
    
    Args:
        request: AnalysisRequest containing the analysis prompt
        
    Returns:
        AnalysisResponse containing the analysis report and generated images
        
    Raises:
        HTTPException: If there's an error during analysis
    """
    try:
        # Process the input using the coordinator agent
        global_output, images = agents['coordinator'].format_report(query)

        return global_output,images

        
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}"
        )

# CHECKING health  endpoint
@app.get("/health")
async def health_check():
    """
    Simple health check endpoint to verify the API is running
    """
    return {"status": "OK"}