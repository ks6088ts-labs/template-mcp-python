from __future__ import annotations

import importlib
import json
import sys
from base64 import b64encode
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from mcp.client.session import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
from mcp.types import CallToolResult

from template_mcp_python.internals.repositories.types import CreateImageRequest, ResultStatus
from template_mcp_python.internals.scene_resolvers.results import SceneResolverResult

_MODULE_PATH = "template_mcp_python.mcp_servers.image_analyzer"


class StubSceneResolver:
    """Stub scene resolver capturing inputs for assertions."""

    def __init__(self, result: SceneResolverResult) -> None:
        self._result = result
        self.calls: list[str] = []

    def solve(self, base64_image: str) -> SceneResolverResult:
        self.calls.append(base64_image)
        return self._result


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def image_analyzer_setup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    image_bytes = b"test analyzer image"
    base64_image = b64encode(image_bytes).decode("utf-8")
    db_path = tmp_path / "test_images.db"

    monkeypatch.setenv("IMAGE_TRANSFER_DB_PATH", str(db_path))

    if _MODULE_PATH in sys.modules:
        del sys.modules[_MODULE_PATH]

    module = importlib.import_module(_MODULE_PATH)

    stub_result = SceneResolverResult(caption="stub caption", confidence=0.87)
    stub_model = StubSceneResolver(result=stub_result)
    module.model = stub_model

    try:
        yield module, base64_image, stub_model, stub_result
    finally:
        sys.modules.pop(_MODULE_PATH, None)


@pytest.fixture
async def client_session(image_analyzer_setup) -> AsyncGenerator[ClientSession, None]:
    module, *_ = image_analyzer_setup
    async with create_connected_server_and_client_session(module.mcp, raise_exceptions=True) as session:
        yield session


@pytest.mark.anyio
async def test_analyze_tool_returns_model_result(
    client_session: ClientSession,
    image_analyzer_setup,
):
    _, base64_image, stub_model, stub_result = image_analyzer_setup

    result: CallToolResult = await client_session.call_tool(
        "analyze",
        {"base64_encoded_str": base64_image},
    )

    assert result.isError is False
    assert result.structuredContent is not None, "Expected structuredContent in result"
    payload = result.structuredContent["result"]
    assert json.loads(payload) == stub_result.model_dump()
    assert stub_model.calls == [base64_image]


@pytest.mark.anyio
async def test_analyze_repository_image_reads_and_analyzes(
    client_session: ClientSession,
    image_analyzer_setup,
):
    module, base64_image, stub_model, stub_result = image_analyzer_setup

    create_response = module.repository.create_image(CreateImageRequest(base64_image=base64_image))
    assert create_response.status is ResultStatus.SUCCESS

    result: CallToolResult = await client_session.call_tool(
        "analyze_repository_image",
        {"image_id": create_response.image_id},
    )

    assert result.isError is False
    assert result.structuredContent is not None, "Expected structuredContent in result"
    payload = result.structuredContent["result"]
    assert json.loads(payload) == stub_result.model_dump()
    assert stub_model.calls == [base64_image]
