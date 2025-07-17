from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseProvider(ABC):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.6) -> str:
        "Generate a response from LLM"
        pass

    @abstractmethod
    def validate_connection(self) -> bool:
        pass

    def format_context_message(self, file_content: str, filename: Optional[str] = None) -> str:
        if filename:
            return f"File: {filename}\n\n{file_content}"
        return f"```\n{file_content}\n```"