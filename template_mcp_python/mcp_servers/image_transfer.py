import os

from mcp.server.fastmcp import FastMCP

from template_mcp_python.internals.helpers import load_image_to_base64
from template_mcp_python.internals.repositories.sqlite_repository import SqliteRepository
from template_mcp_python.internals.repositories.types import CreateImageRequest, ResultStatus
from template_mcp_python.loggers import get_logger
from template_mcp_python.settings import ImageTransferSettings as Settings

logger = get_logger(__name__)
logger.setLevel("INFO")
mcp = FastMCP("Image Transfer Server")
settings = Settings()
db_path = os.getenv("IMAGE_TRANSFER_DB_PATH", settings.image_transfer_sqlite_db_path)
repository = SqliteRepository(db_path)

logger.info("Loading image for transfer...")
image_data_base64 = load_image_to_base64(settings.image_transfer_image_path)
logger.info("Image loaded and encoded to base64")


@mcp.tool()
def store_image() -> str:
    """Persist the base64-encoded image in a SQLite database and return its identifier."""
    logger.info("Persisting image to SQLite database.")
    response = repository.create_image(CreateImageRequest(base64_image=image_data_base64))

    if response.status is ResultStatus.FAILURE:
        logger.error("Failed to persist image to SQLite database.")
        raise RuntimeError("Failed to persist image to SQLite database.")

    logger.info("Image stored in SQLite with id %s", response.image_id)
    return response.image_id
