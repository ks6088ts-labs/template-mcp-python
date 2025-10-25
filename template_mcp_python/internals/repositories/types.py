from enum import Enum

from pydantic import BaseModel, Field


class ResultStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class CreateImageRequest(BaseModel):
    """
    Model representing the request to create an image.
    """

    base64_image: str = Field(description="Base64 encoded image string")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)


class CreateImageResponse(BaseModel):
    """
    Model representing the response after creating an image.
    """

    image_id: str = Field(description="Unique identifier for the created image")
    status: ResultStatus = Field(description="Status of the create operation")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)


class ReadImageRequest(BaseModel):
    """
    Model representing the request to read an image.
    """

    image_id: str = Field(description="Unique identifier for the image to be read")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)


class ReadImageResponse(BaseModel):
    """
    Model representing the response after reading an image.
    """

    base64_image: str = Field(description="Base64 encoded image string")
    status: ResultStatus = Field(description="Status of the read operation")

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)
