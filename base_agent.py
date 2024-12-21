"BaseAgent"
from abc import ABC, abstractmethod
from anthropic import Anthropic
import openai

class BaseAgent(ABC):
    def __init__(self, config):
        self.config = config
        self.anthropic = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.openai_client = openai.Client(api_key=config.OPENAI_API_KEY)
        
    @abstractmethod
    def process_information(self, data):
        pass
    
    @abstractmethod
    def generate_questions(self):
        pass
    
    @abstractmethod
    def create_summary(self):
        pass
    
    def ask_claude(self, prompt):
        response = self.anthropic.messages.create(
            model=self.config.CLAUDE_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content

    def ask_gpt4(self, prompt):
        response = self.openai_client.chat.completions.create(
            model=self.config.GPT4_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
