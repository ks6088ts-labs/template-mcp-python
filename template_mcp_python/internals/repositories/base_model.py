from abc import ABC, abstractmethod

from template_mcp_python.internals.repositories.types import (
    CreateImageRequest,
    CreateImageResponse,
    ReadImageRequest,
    ReadImageResponse,
)


class RepositoryBaseModel(ABC):
    @abstractmethod
    def create_image(
        self,
        request: CreateImageRequest,
    ) -> CreateImageResponse:
        raise NotImplementedError

    @abstractmethod
    def read_image(
        self,
        request: ReadImageRequest,
    ) -> ReadImageResponse:
        raise NotImplementedError
