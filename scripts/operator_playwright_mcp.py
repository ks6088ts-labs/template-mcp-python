import asyncio
import logging
from os import getenv
from typing import Annotated

import typer
from dotenv import load_dotenv
from fastmcp.client import Client

from template_mcp_python.loggers import get_logger

app = typer.Typer(
    add_completion=False,
    help="Playwright MCP Operator CLI",
)

logger = get_logger(__name__)


def set_verbose_logging(
    verbose: bool,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)


def get_mcp_server_url() -> str:
    return f"http://{getenv('MCP_HOST', 'localhost')}:{getenv('MCP_PORT', '8000')}/mcp"


@app.command(
    help="List available Playwright MCP Tools",
)
def list_tools(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)

    async def list_playwright_tools():
        # クライアントを初期化し、サーバーに接続
        async with Client(get_mcp_server_url()) as client:
            # 利用可能なツールをリスト
            tools = await client.list_tools()
            for tool in tools:
                print(f"{tool.name}: {tool.description}")
                # print(tool.model_dump_json(indent=2))

    asyncio.run(list_playwright_tools())


@app.command(
    help="Navigate to a URL in the browser",
)
def browser_navigate(
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-u",
            help="The URL to navigate to in the browser",
        ),
    ] = "https://www.example.com",
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)

    async def playwright_browser_navigate():
        # クライアントを初期化し、サーバーに接続
        async with Client(get_mcp_server_url()) as client:
            # 利用可能なツールをリスト
            result = await client.call_tool(
                name="browser_navigate",
                arguments={
                    "url": url,
                },
            )
            print(f"Result from {url}:")
            print(result)

            # keep the browser open until user presses Enter
            input("Press Enter to close the browser...")

    asyncio.run(playwright_browser_navigate())


if __name__ == "__main__":
    result = load_dotenv(
        override=True,
        verbose=True,
    )
    if not result:
        logger.warning("Failed to load .env file")
        # pass through even if .env loading fails
    app()
