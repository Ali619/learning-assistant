from enum import Enum

from openai import OpenAI

from config.settings import ANTHROPIC_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY


class ClientProvider(Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    OLLAMA = "ollama"
    anthropic = "anthropic"


class ClientConfig:
    def __init__(self, client_provider: ClientProvider, api_key: str, model_name: str):
        self.client_provider = client_provider
        self.api_key = api_key
        self.model_name = model_name

    def get_client(self):
        if self.client_provider == ClientProvider.GOOGLE:
            return OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=self.api_key)
        if self.client_provider == ClientProvider.OPENAI:
            return OpenAI(api_key=self.api_key)
        elif self.client_provider == ClientProvider.OLLAMA:
            return OpenAI(base_url="XXXXXXXXXXXXXXXXXXXXXXXXX", api_key="ollama")
        elif self.client_provider == ClientProvider.anthropic:
            return OpenAI(base_url="XXXXXXXXXXXXXXXXXXXXXXXXXXXX", api_key=self.api_key)
        else:
            raise ValueError("Invalid client provider")
