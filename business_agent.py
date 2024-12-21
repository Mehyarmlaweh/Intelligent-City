"business agent"
from base_agent import BaseAgent


class BusinessAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.required_info = [
            "budget",
            "expected_roi",
            "target_demographics",
            "commercial_zones",
            "economic_factors"
        ]
        self.collected_data = {}

    def process_information(self, data):
        self.collected_data.update(data)
        
    def generate_questions(self):
        questions = []
        for info in self.required_info:
            if info not in self.collected_data:
                prompt = f"Generate relevant questions about {info} for neighborhood planning"
                questions.extend(self.ask_claude(prompt).split("\n"))
        return questions
    
    def create_summary(self):
        prompt = f"""Create a business summary for neighborhood development based on:
        Collected data: {self.collected_data}
        Include: budget allocation, ROI projections, and economic impact."""
        
        return self.ask_gpt4(prompt)
