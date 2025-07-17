from typing import List, Dict
from openai import OpenAI, OpenAIError
from .base import BaseProvider

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.6) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=4096
            )
            
            return response.choices[0].message.content
            
        except OpenAIError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def validate_connection(self) -> bool:
        try:
            self.client.models.list()
            return True
        except:
            return False