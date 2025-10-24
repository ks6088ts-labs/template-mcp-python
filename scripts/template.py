import logging
from typing import Annotated

import typer
from dotenv import load_dotenv

from template_mcp_python.loggers import get_logger
from template_mcp_python.mcp_servers.image_transfer import mcp as image_transfer_mcp
from template_mcp_python.mcp_servers.quick_example import mcp as quick_example_mcp
from template_mcp_python.settings import Settings

app = typer.Typer(
    add_completion=False,
    help="template-mcp-python CLI",
)

logger = get_logger(__name__)


def set_verbose_logging(
    verbose: bool,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)


@app.command()
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


@app.command()
def image_transfer(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)
    image_transfer_mcp.run()


if __name__ == "__main__":
    assert load_dotenv(
        override=True,
        verbose=True,
    ), "Failed to load environment variables"
    app()
