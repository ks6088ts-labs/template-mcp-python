from abc import ABC, abstractmethod

from pydantic import BaseModel


class SceneResolverBaseModel(ABC):
    @abstractmethod
    def solve(
        self,
        base64_image: str,
    ) -> BaseModel:
        raise NotImplementedError
