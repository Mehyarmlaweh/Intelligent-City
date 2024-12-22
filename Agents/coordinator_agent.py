import ast
import os
import sys
from typing import Dict, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph

# Update import for settings and agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import Settings
from base_agent import BaseAgent
from business_agent import BusinessAgent
from energy_agent import EnergyAgent
from infrastructure_agent import InfrastructureAgent
from vision_agent import VisionAgent
import json

class AgentState(TypedDict):
    messages: List[BaseMessage]  
    business_data: Dict
    energy_data: Dict
    infrastructure_data: Dict
    all_data_collected: bool
    final_report: str

class CoordinatorAgent(BaseAgent):
    """Coordinator Agent to handle data collection and distribution using LangGraph."""

    def __init__(self, settings: Settings):
        """Initialize the CoordinatorAgent with configuration settings."""
        super().__init__(settings)
        self.settings = settings
        self.business_agent = BusinessAgent(settings)
        self.energy_agent = EnergyAgent(settings)
        self.infrastructure_agent = InfrastructureAgent(settings)
        self.vision_agent = VisionAgent(settings)
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow for agent communication."""
        workflow = StateGraph(AgentState)

        # Add nodes for each agent
        def process_business(state: AgentState) -> AgentState:
            try:
                response = self.business_agent.ask_llm()
                if isinstance(response, list):
                    state["messages"].extend([HumanMessage(content=msg) for msg in response])
                else:
                    state["business_data"] = response
            except Exception as e:
                if self.settings.ENVIRONMENT == "local":
                    print(f"Error in business processing: {str(e)}")
                state["business_data"] = {}
            return state

        def process_energy(state: AgentState) -> AgentState:
            try:
                response = self.energy_agent.ask_llm()
                if isinstance(response, list):
                    state["messages"].extend([HumanMessage(content=msg) for msg in response])
                else:
                    state["energy_data"] = response
            except Exception as e:
                if self.settings.ENVIRONMENT == "local":
                    print(f"Error in energy processing: {str(e)}")
                state["energy_data"] = {}
            return state

        def process_infrastructure(state: AgentState) -> AgentState:
            try:
                response = self.infrastructure_agent.ask_llm()
                if isinstance(response, list):
                    state["messages"].extend([HumanMessage(content=msg) for msg in response])
                else:
                    state["infrastructure_data"] = response
            except Exception as e:
                if self.settings.ENVIRONMENT == "local":
                    print(f"Error in infrastructure processing: {str(e)}")
                state["infrastructure_data"] = {}
            return state

        def generate_final_report(state: AgentState) -> AgentState:
            try:
                prompt = f"""
                Create a comprehensive neighborhood development report using the following data:
                Business Analysis: {state['business_data']}
                Energy Assessment: {state['energy_data']}
                Infrastructure Plan: {state['infrastructure_data']}

                Format the report with clear sections and recommendations.
                """
                response = self.claude.invoke(prompt)

                state["final_report"] = response.content 
                
            except Exception as e:
                if self.settings.ENVIRONMENT == "local":
                    print(f"Error generating report: {str(e)}")
                state["final_report"] = "Error generating report"
            return state

        def process_vision(state: AgentState) -> AgentState:
            try:  
                self.vision_agent.collect_data(state["final_report"])
                response = self.vision_agent.ask_llm()
                state["vision"] = response
            except Exception as e:
                if self.settings.ENVIRONMENT == "local":
                    print(f"Error in vision processing: {str(e)}")
                state["vision"] = {}
            return state

        # Add nodes to the graph
        workflow.add_node("business", process_business)
        workflow.add_node("energy", process_energy)
        workflow.add_node("infrastructure", process_infrastructure)
        workflow.add_node("generate_report", generate_final_report)
        workflow.add_node("vision", process_vision)

        # Add edges
        workflow.add_edge("business", "energy")
        workflow.add_edge("energy", "infrastructure")
        workflow.add_edge("infrastructure", "generate_report")
        workflow.add_edge("generate_report", "vision")

        # Set the entry point
        workflow.set_entry_point("business")

        return workflow.compile()

    async def process_input(self, user_input: str) -> dict:
        """Process user input through the agent workflow."""
        try:
            # Initial state setup
            initial_state = AgentState(
                messages=[HumanMessage(content=user_input)],
                business_data={},
                energy_data={},
                infrastructure_data={},
                all_data_collected=False,
                final_report="",
                vision={},
            )

            # Structure the input data
            structured_data = self._structure_input(user_input)

            # Distribute data to agents
            self.business_agent.collect_data(structured_data)
            self.energy_agent.collect_data(structured_data)
            self.infrastructure_agent.collect_data(structured_data)

            # Execute the workflow
            final_state = await self.workflow.ainvoke(initial_state)

            return {
                "report": final_state["final_report"],
                "images": final_state["vision"],
                "questions": [
                    msg.content
                    for msg in final_state["messages"]
                    if isinstance(msg, HumanMessage)
                ]
            }

        except Exception as e:
            if self.settings.ENVIRONMENT == "local":
                print(f"Error in workflow execution: {str(e)}")
            return {"error": "An error occurred during processing"}

    def _structure_input(self, user_input: str) -> dict:
        """Structure the user input into categorized data."""
        try:
            prompt = f"""
            Analyze the following input and organize it into three categories:
              business, energy, and infrastructure.
            Return the result as a JSON object with these three keys.
            If a category has no relevant data, use an empty object {{}} 
            for that key.
            Input: {user_input}
            """

            response = self.claude.invoke(prompt)
            return json.loads(response.content)
        except Exception as e:
            if self.settings.ENVIRONMENT == "local":
                print(f"Error structuring input: {str(e)}")
            return {"business": {}, "energy": {}, "infrastructure": {}}