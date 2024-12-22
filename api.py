from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

from Agents.business_agent import BusinessAgent
from Agents.energy_agent import EnergyAgent
from Agents.infrastructure_agent import InfrastructureAgent
from Agents.vision_agent import VisionAgent
from Agents.coordinator_agent import CoordinatorAgent
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

class AnalysisRequest(BaseModel):
    """
    Request model for neighborhood analysis
    """
    prompt: str
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "Analyze the downtown area of Springfield"
            }
        }

class AnalysisResponse(BaseModel):
    """
    Response model for neighborhood analysis
    """
    report: str
    images: Dict[str, str]
    
    class Config:
        schema_extra = {
            "example": {
                "report": "Detailed analysis of the neighborhood...",
                "images": {
                    "map": "base64_encoded_image_string",
                    "chart": "base64_encoded_image_string"
                }
            }
        }

@app.post("/analyze", 
         response_model=AnalysisResponse,
         summary="Analyze a neighborhood",
         response_description="Returns a detailed analysis report and related images")
async def analyze_neighborhood(request: AnalysisRequest):
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
        global_output, images = agents['coordinator'].format_report(request.prompt)
        
        return AnalysisResponse(
            report=global_output,
            images=images
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}"
        )

# Add health check endpoint
@app.get("/health",
         summary="Check API health",
         response_description="Returns OK if the API is healthy")
async def health_check():
    """
    Simple health check endpoint to verify the API is running
    """
    return {"status": "OK"}