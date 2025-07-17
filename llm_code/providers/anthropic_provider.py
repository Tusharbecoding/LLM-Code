from typing import List, Dict
from anthropic import Anthropic, APIError
from .base import BaseProvider

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = Anthropic(api_key=api_key)
    
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.6) -> str:
        try:
            # Convert messages to Anthropic format
            system_message = None
            formatted_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=temperature,
                system=system_message,
                messages=formatted_messages
            )
            
            return response.content[0].text
            
        except APIError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def validate_connection(self) -> bool:
        try:
            # Try a minimal API call
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except:
            return False