from base64 import b64encode

from template_mcp_python.loggers import get_logger

logger = get_logger(__name__)


def load_image_to_base64(image_path: str) -> str:
    """Load an image from the given path and return its base64-encoded string."""
    logger.info(f"Loading image from path: {image_path}")
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode("utf-8")
