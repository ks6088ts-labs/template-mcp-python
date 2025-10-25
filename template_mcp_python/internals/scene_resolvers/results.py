from pydantic import BaseModel, Field


class SceneResolverResult(BaseModel):
    """
    Model representing the result of a scene resolver.
    """

    caption: str = Field(description="Caption of the image")
    confidence: float = Field(description="Confidence score of the caption")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)
