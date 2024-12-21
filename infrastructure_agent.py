    from base_agent import BaseAgent

class InfrastructureAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.required_info = [
            "building_types",
            "transportation",
            "public_spaces",
            "educational_facilities",
            "healthcare_facilities"
        ]
        self.collected_data = {}

    def process_information(self, data):
        self.collected_data.update(data)
        
    def analyze_infrastructure_needs(self):
        prompt = f"""Analyze infrastructure needs based on:
        Demographics: {self.collected_data.get('demographics')}
        Area: {self.collected_data.get('area')}
        Recommend optimal facility placement and transportation routes."""
        
        return self.ask_claude(prompt)
    
    def create_summary(self):
        return self.analyze_infrastructure_needs()
