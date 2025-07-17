import os 
from dataclasses import dataclass
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ProviderConfig:
    api_key: str
    model: str

class Config:
    def __init__(self):
        self.default_provider = "gemini"
        self.providers: Dict[str, ProviderConfig] = {
            "anthropic": ProviderConfig(
                api_key = os.getenv("ANTHROPIC_API_KEY", ""),
                model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"),
            ),
            "openai": ProviderConfig(
                api_key = os.getenv("OPENAI_API_KEY", ""),
                model = os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            ),
            "gemini": ProviderConfig(
                api_key = os.getenv("GEMINI_API_KEY", ""),
                model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            ),
        }

    def get_provider_config(self, provider_name:str) -> Optional[ProviderConfig]:
        return self.providers.get(provider_name)
    
    def validate_provider(self, provider_name: str) -> bool:
        config = self.get_provider_config(provider_name)
        return config is not None and bool(config.api_key)
    