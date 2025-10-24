from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from template_mcp_python.loggers import get_logger
from template_mcp_python.settings import ImageTransferSettings as Settings

logger = get_logger(__name__)
logger.setLevel("INFO")
mcp = FastMCP("Image Analyzer Server")
settings = Settings()


class ImageAnalyzeResult(BaseModel):
    """
    Image Analyze Result Model
    """

    caption: str = Field(description="Caption of the image")
    confidence: float = Field(description="Confidence score of the caption")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)


@mcp.tool()
def analyze(base64_encoded_str: str) -> str:
    """Analyze an image and return ImageAnalyzeResult as JSON string."""
    logger.info("Analyzing image...")
    # Dummy analysis logic for illustration purposes
    result = ImageAnalyzeResult(caption="A sample caption for the provided image.", confidence=0.95)
    logger.info("Image analysis complete.")
    return result.model_dump_json(indent=2)
