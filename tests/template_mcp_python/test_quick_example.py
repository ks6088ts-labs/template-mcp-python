from collections.abc import AsyncGenerator

import pytest
from mcp.client.session import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
from mcp.types import CallToolResult

from template_mcp_python.mcp_servers.quick_example import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client_session() -> AsyncGenerator[ClientSession]:
    async with create_connected_server_and_client_session(mcp, raise_exceptions=True) as _session:
        yield _session


@pytest.mark.anyio
async def test_call_add_tool(client_session: ClientSession):
    result: CallToolResult = await client_session.call_tool(
        "add",
        {
            "a": 1,
            "b": 2,
        },
    )
    print(result.model_dump_json(indent=2))
    assert result.structuredContent is not None, f"Expected structuredContent, got None: {result}"
    assert result.structuredContent["result"] == 3, f"Unexpected result: {result}"
    assert result.isError is False, f"Unexpected error: {result}"
