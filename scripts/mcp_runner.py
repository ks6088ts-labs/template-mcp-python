import asyncio
import logging
from typing import Annotated

import typer
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_core.runnables.config import RunnableConfig

from template_mcp_python.internals.agents.multi_server_mcp import make_graph
from template_mcp_python.loggers import get_logger
from template_mcp_python.mcp_servers.image_analyzer import mcp as image_analyzer_mcp
from template_mcp_python.mcp_servers.image_transfer import mcp as image_transfer_mcp
from template_mcp_python.mcp_servers.quick_example import mcp as quick_example_mcp
from template_mcp_python.settings import Settings

app = typer.Typer(
    add_completion=False,
    help="MCP Runner CLI",
)

logger = get_logger(__name__)


def set_verbose_logging(
    verbose: bool,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)


@app.command(
    help="Run a quick example MCP server",
)
def quick_example(
    name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help="Name of the person to greet",
        ),
    ] = "World",
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)

    logger.debug(f"This is a debug message with name: {name}")
    logger.info(f"Settings from .env: {Settings().model_dump_json(indent=2)}")

    quick_example_mcp.run()


@app.command(
    help="Run the Image Transfer MCP server",
)
def image_transfer(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)
    image_transfer_mcp.run()


@app.command(
    help="Run the Image Analyzer MCP server",
)
def image_analyzer(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)
    image_analyzer_mcp.run()


@app.command(
    help="Run the multi-server MCP agent",
)
def multi_server_mcp(
    prompt: Annotated[
        str,
        typer.Option(
            "--prompt",
            "-p",
            help="Prompt to send to the agent",
        ),
    ] = "Yahoo ニュースの最新記事を教えて",
    recursion_limit: int = typer.Option(
        10,
        "--recursion-limit",
        "-r",
        help="Recursion limit for the agent",
    ),
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)

    logger.info("Creating agent graph")
    graph = asyncio.run(make_graph())

    logger.info("Invoking agent with prompt")
    response = asyncio.run(
        graph.ainvoke(
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
            config=RunnableConfig(
                recursion_limit=recursion_limit,
                callbacks=[
                    # You can add custom callbacks here
                ],
            ),
        )
    )
    logger.info(f"response: {response}")

    try:
        message: BaseMessage = response["messages"][-1]
        print(f"Agent response: {message.content}")
    except Exception as e:
        print(f"Failed to parse agent response: {e}")


if __name__ == "__main__":
    assert load_dotenv(
        override=True,
        verbose=True,
    ), "Failed to load environment variables"
    app()
