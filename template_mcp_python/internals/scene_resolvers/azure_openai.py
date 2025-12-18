from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from template_mcp_python.internals.llms.azure_openai import AzureOpenAiWrapper
from template_mcp_python.internals.scene_resolvers.base_model import SceneResolverBaseModel
from template_mcp_python.internals.scene_resolvers.results import SceneResolverResult


class AzureOpenAiSceneResolver(SceneResolverBaseModel):
    def __init__(
        self,
        model: BaseModel = SceneResolverResult,
        system_prompt: str = "You are a helpful assistant that performs image analysis tasks. You will be provided with an image in base64 format. Analyze the image and provide the required information based on the user's request.",  # noqa: E501
        human_prompt: str = "Analyze the following image and provide the required information.",
    ):
        super().__init__()
        self.llm = AzureOpenAiWrapper().llm.with_structured_output(model)
        self.system_prompt = system_prompt
        self.human_prompt = human_prompt

    def solve(
        self,
        base64_image: str,
    ) -> BaseModel:
        return self.llm.invoke(
            input=[
                SystemMessage(content=self.system_prompt),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": self.human_prompt,
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
