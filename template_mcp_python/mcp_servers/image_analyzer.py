from mcp.server.fastmcp import FastMCP

from template_mcp_python.internals.scene_resolvers.azure_openai import AzureOpenAiSceneResolver
from template_mcp_python.internals.scene_resolvers.base_model import SceneResolverBaseModel
from template_mcp_python.internals.scene_resolvers.results import SceneResolverResult
from template_mcp_python.loggers import get_logger
from template_mcp_python.settings import ImageTransferSettings as Settings

logger = get_logger(__name__)
logger.setLevel("INFO")
mcp = FastMCP("Image Analyzer Server")
settings = Settings()
model: SceneResolverBaseModel = AzureOpenAiSceneResolver()


@mcp.tool()
def analyze(base64_encoded_str: str) -> str:
    """Analyze an image and return as JSON string."""
    logger.info("Analyzing image...")
    result: SceneResolverResult = model.solve(base64_encoded_str)
    logger.info("Image analysis complete.")
    return result.model_dump_json(indent=2)
