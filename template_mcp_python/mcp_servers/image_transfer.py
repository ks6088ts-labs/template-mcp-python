from mcp.server.fastmcp import FastMCP

from template_mcp_python.internals.helpers import load_image_to_base64
from template_mcp_python.loggers import get_logger
from template_mcp_python.settings import ImageTransferSettings as Settings

logger = get_logger(__name__)
logger.setLevel("INFO")
mcp = FastMCP("Image Transfer Server")
settings = Settings()

logger.info("Loading image for transfer...")
image_data_base64 = load_image_to_base64(settings.image_transfer_image_path)
logger.info("Image loaded and encoded to base64")


@mcp.tool()
def image() -> str:
    """Transfer an image and return its base64-encoded string."""
    logger.info("Transferring image as base64-encoded string.")
    return image_data_base64
