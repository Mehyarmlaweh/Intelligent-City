"InfraStructure Agent"    
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import SystemMessage, HumanMessage
from base_agent import BaseAgent


class InfrastructureAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.required_info = [
            "building_types",
            "transportation",
            "public_spaces",
            "educational_facilities",
            "healthcare_facilities",
            "green_spaces"
        ]
        self.collected_data = {}
        self.claude = ChatAnthropic(api_key=config.ANTHROPIC_API_KEY)
        self.gpt4 = ChatOpenAI(api_key=config.OPENAI_API_KEY, model_name=config.GPT4_MODEL)

    def process_information(self, data):
        self.collected_data.update(data)
        missing_info = self.check_missing_info()
        if missing_info:
            return self.generate_questions(missing_info)
        return None

    def check_missing_info(self):
        return [info for info in self.required_info if info not in self.collected_data]

    def generate_questions(self, missing_info):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an infrastructure planning expert. Generate specific questions to gather information about the following aspects of a neighborhood:"),
            HumanMessage(content=f"Generate questions for: {', '.join(missing_info)}")
        ])
        chain = LLMChain(llm=self.claude, prompt=prompt)
        response = chain.run(missing_info)
        return response.split('\n')

    def analyze_infrastructure_needs(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an urban planning expert. Analyze the infrastructure needs and provide recommendations based on the following information:"),
            HumanMessage(content=f"""
            Demographics: {self.collected_data.get('demographics', 'N/A')}
            Area: {self.collected_data.get('area', 'N/A')}
            Building Types: {self.collected_data.get('building_types', 'N/A')}
            Transportation: {self.collected_data.get('transportation', 'N/A')}
            Public Spaces: {self.collected_data.get('public_spaces', 'N/A')}
            Educational Facilities: {self.collected_data.get('educational_facilities', 'N/A')}
            Healthcare Facilities: {self.collected_data.get('healthcare_facilities', 'N/A')}
            Green Spaces: {self.collected_data.get('green_spaces', 'N/A')}

            Provide a detailed analysis and recommendations for optimal facility placement, transportation routes, and overall infrastructure design.
            """)
        ])
        chain = LLMChain(llm=self.gpt4, prompt=prompt)
        return chain.run()

    def create_summary(self):
        if not all(info in self.collected_data for info in self.required_info):
            return "Insufficient information to create a summary. Please provide all required information."
        return self.analyze_infrastructure_needs()

    def communicate_with_master_agent(self, message_from_master):
        if isinstance(message_from_master, dict):
            questions = self.process_information(message_from_master)
            if questions:
                return {"status": "need_more_info", "questions": questions}
            else:
                return {"status": "ready", "summary": self.create_summary()}
        else:
            return {"status": "error", "message": "Invalid input format from master agent"}
