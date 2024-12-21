from base_agent import BaseAgent

class EnergyAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.required_info = [
            "energy_requirements",
            "renewable_preferences",
            "climate_data",
            "sustainability_goals"
        ]
        self.collected_data = {}

    def process_information(self, data):
        self.collected_data.update(data)
        
    def recommend_energy_solutions(self):
        prompt = f"""Recommend optimal energy solutions based on:
        Area: {self.collected_data.get('area')}
        Climate: {self.collected_data.get('climate_data')}
        Goals: {self.collected_data.get('sustainability_goals')}
        Consider renewable energy integration and carbon emission reduction."""
        
        return self.ask_claude(prompt)
    
    def create_summary(self):
        return self.recommend_energy_solutions()
