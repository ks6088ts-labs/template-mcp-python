from langchain_core.messages import HumanMessage, SystemMessage

from template_mcp_python.internals.llms.azure_openai import AzureOpenAiWrapper
from template_mcp_python.internals.scene_resolvers.base_model import SceneResolverBaseModel
from template_mcp_python.internals.scene_resolvers.results import SceneResolverResult

llm = AzureOpenAiWrapper().llm.with_structured_output(SceneResolverResult)


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
