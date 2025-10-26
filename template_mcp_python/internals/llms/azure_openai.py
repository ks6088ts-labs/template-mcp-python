from langchain_openai import AzureChatOpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_endpoint: str = "https://<YOUR_AOAI_NAME>.openai.azure.com/"
    azure_openai_api_key: str = "<YOUR_API_KEY>"
    azure_openai_api_version: str = "2025-04-01-preview"
    azure_openai_model_chat: str = "gpt-5"
    azure_openai_model_embedding: str = "text-embedding-3-small"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )


class AzureOpenAiWrapper:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()

    @property
    def llm(self):
        return AzureChatOpenAI(
            api_key=self.settings.azure_openai_api_key,
            azure_endpoint=self.settings.azure_openai_endpoint,
            api_version=self.settings.azure_openai_api_version,
            azure_deployment=self.settings.azure_openai_model_chat,
        )
