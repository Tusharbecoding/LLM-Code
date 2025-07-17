from typing import List, Dict
from google import genai
from google.genai import types
from .base import BaseProvider

class GeminiProvider(BaseProvider):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = genai.Client(api_key=api_key)

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.6) -> str:
        try:
            contents = []
            system_instruction = None

            for msg in messages:
                if msg["role"] == "system":
                    system_instruction = msg["content"]
                elif msg["role"] == "user":
                    contents.append(types.Content(
                        role="user",
                        parts=[types.Part(text=msg["content"])]
                    ))
                elif msg["role"] == "assistant":
                    contents.append(types.Content(
                        role="model",
                        parts=[types.Part(text=msg["content"])]
                    ))

            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=1024,
                system_instruction=system_instruction,
            )

            response = self.client.models.generate_content(
                model = f"models/{self.model}",
                contents = contents,
                config = config
            )

            return response.text

        except Exception as e:
            return f"Error generating response: {str(e)}"
        
    def validate_connection(self) -> bool:
        try: 
            self.client.models.list()
            return True
        except:
            return False