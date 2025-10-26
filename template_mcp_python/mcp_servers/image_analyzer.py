import os

from mcp.server.fastmcp import FastMCP

from template_mcp_python.internals.repositories.sqlite_repository import SqliteRepository
from template_mcp_python.internals.repositories.types import ReadImageRequest, ResultStatus
from template_mcp_python.internals.scene_resolvers.azure_openai import AzureOpenAiSceneResolver
from template_mcp_python.internals.scene_resolvers.base_model import SceneResolverBaseModel
from template_mcp_python.internals.scene_resolvers.results import SceneResolverResult
from template_mcp_python.loggers import get_logger
from template_mcp_python.settings import ImageTransferSettings as Settings

logger = get_logger(__name__)
logger.setLevel("INFO")
mcp = FastMCP("Image Analyzer Server")
settings = Settings()
db_path = os.getenv("IMAGE_TRANSFER_DB_PATH", settings.image_transfer_sqlite_db_path)
repository = SqliteRepository(db_path)
model: SceneResolverBaseModel = AzureOpenAiSceneResolver()


@mcp.tool()
def analyze_repository_image(image_id: str) -> str:
    """Read an image from the repository and return its analysis as JSON."""
    logger.info("Retrieving image %s from repository...", image_id)
    response = repository.read_image(ReadImageRequest(image_id=image_id))

    if response.status is ResultStatus.FAILURE:
        logger.error("Failed to retrieve image %s from repository.", image_id)
        raise RuntimeError(f"Failed to retrieve image with id {image_id}.")

    logger.info("Image retrieved; analyzing.")
    result: SceneResolverResult = model.solve(response.base64_image)
    logger.info("Image analysis complete for id %s.", image_id)
    return result.model_dump_json(indent=2)
