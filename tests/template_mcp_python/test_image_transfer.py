from __future__ import annotations

import importlib
import sys
from base64 import b64encode
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from mcp.client.session import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
from mcp.types import CallToolResult

from template_mcp_python.internals.repositories.sqlite_repository import SqliteRepository
from template_mcp_python.internals.repositories.types import ReadImageRequest, ResultStatus

_MODULE_PATH = "template_mcp_python.mcp_servers.image_transfer"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def image_transfer_setup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    image_bytes = b"test image bytes"
    expected_base64 = b64encode(image_bytes).decode("utf-8")
    image_path = tmp_path / "test_image.bin"
    image_path.write_bytes(image_bytes)
    db_path = tmp_path / "test_images.db"

    monkeypatch.setenv("IMAGE_TRANSFER_IMAGE_PATH", str(image_path))
    monkeypatch.setenv("IMAGE_TRANSFER_DB_PATH", str(db_path))

    if _MODULE_PATH in sys.modules:
        del sys.modules[_MODULE_PATH]

    module = importlib.import_module(_MODULE_PATH)

    try:
        yield module, expected_base64, db_path
    finally:
        sys.modules.pop(_MODULE_PATH, None)


@pytest.fixture
async def client_session(image_transfer_setup) -> AsyncGenerator[ClientSession, None]:
    module, *_ = image_transfer_setup
    async with create_connected_server_and_client_session(module.mcp, raise_exceptions=True) as session:
        yield session


@pytest.mark.anyio
async def test_store_image_tool_persists_data(
    client_session: ClientSession,
    image_transfer_setup,
):
    _, expected_base64, db_path = image_transfer_setup

    result: CallToolResult = await client_session.call_tool("store_image", {})

    assert result.isError is False
    assert result.structuredContent is not None, "Expected structuredContent in result"
    image_id = result.structuredContent["result"]
    assert image_id, "Expected a non-empty image identifier"

    repository = SqliteRepository(db_path)
    read_response = repository.read_image(ReadImageRequest(image_id=image_id))

    assert read_response.status is ResultStatus.SUCCESS
    assert read_response.base64_image == expected_base64
