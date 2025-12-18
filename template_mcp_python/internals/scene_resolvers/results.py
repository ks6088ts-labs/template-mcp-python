from pydantic import BaseModel, Field


class SceneResolverResult(BaseModel):
    """
    Model representing the result of a scene resolver.
    """

    caption: str = Field(description="Caption of the image")
    confidence: float = Field(description="Confidence score of the caption")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)


class PointingResult(BaseModel):
    """
    Model representing the result of a pointing detection in an image.
    """

    horizontal_position: float = Field(description="Horizontal position of the pointing")
    vertical_position: float = Field(description="Vertical position of the pointing")
    confidence: float = Field(description="Confidence score of the pointing")
    description: str = Field(description="Description of the pointing")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)
