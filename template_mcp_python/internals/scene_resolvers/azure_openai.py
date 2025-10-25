from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict

from template_mcp_python.internals.scene_resolvers.base_model import SceneResolverBaseModel
from template_mcp_python.internals.scene_resolvers.results import SceneResolverResult


class Settings(BaseSettings):
    scene_resolver_azure_openai_endpoint: str = "https://<YOUR_AOAI_NAME>.openai.azure.com/"
    scene_resolver_azure_openai_api_key: str = "<YOUR_API_KEY>"
    scene_resolver_azure_openai_api_version: str = "2025-04-01-preview"
    scene_resolver_azure_openai_model_chat: str = "gpt-5"
    scene_resolver_azure_openai_model_embedding: str = "text-embedding-3-small"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()
llm = AzureChatOpenAI(
    api_key=settings.scene_resolver_azure_openai_api_key,
    azure_endpoint=settings.scene_resolver_azure_openai_endpoint,
    api_version=settings.scene_resolver_azure_openai_api_version,
    azure_deployment=settings.scene_resolver_azure_openai_model_chat,
).with_structured_output(SceneResolverResult)


class AzureOpenAiSceneResolver(SceneResolverBaseModel):
    def solve(
        self,
        base64_image: str,
    ) -> SceneResolverResult:
        return llm.invoke(
            input=[
                SystemMessage(
                    content="You are a helpful assistant that performs image analysis tasks. "
                    "You will be provided with an image in base64 format. "
                    "Analyze the image and provide the required information based on the user's request."
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": "Analyze the following image and provide the required information.",
                        },
                        {
                            "type": "image",
                            "source_type": "base64",
                            "data": base64_image,
                            "mime_type": "image/png",
                        },
                    ]
                ),
            ],
        )
