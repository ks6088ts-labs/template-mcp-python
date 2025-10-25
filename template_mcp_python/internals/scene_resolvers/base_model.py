from abc import ABC, abstractmethod

from template_mcp_python.internals.scene_resolvers.results import SceneResolverResult


class SceneResolverBaseModel(ABC):
    @abstractmethod
    def solve(
        self,
        base64_image: str,
    ) -> SceneResolverResult:
        raise NotImplementedError
