import base64
import logging
from typing import Annotated

import typer
from dotenv import load_dotenv

from template_mcp_python.internals.scene_resolvers.azure_openai import AzureOpenAiSceneResolver
from template_mcp_python.internals.scene_resolvers.results import PointingResult
from template_mcp_python.loggers import get_logger

app = typer.Typer(
    add_completion=False,
    help="Scene Resolvers Operator CLI",
)

logger = get_logger(__name__)


def set_verbose_logging(
    verbose: bool,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)


@app.command(
    help="Resolve scene from an image using Azure OpenAI",
)
def resolve_scene(
    image_path: Annotated[
        str,
        typer.Option(
            "--image-path",
            "-i",
            help="Path to the image file",
        ),
    ] = "data/windows-kitchen.jpg",
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)

    try:
        # Load image file
        with open(image_path, "rb") as f:
            image_data = f.read()
        # Convert to base64
        base64_image = base64.b64encode(image_data).decode("utf-8")
        resolver = AzureOpenAiSceneResolver()
        result = resolver.solve(
            base64_image=base64_image,
        )
        print(f"Processed image saved to {result.model_dump_json(indent=2)}")
    except Exception as e:
        logger.error(f"Error processing image: {e}")


@app.command(
    help="Pointing detection from an image using Azure OpenAI",
)
def pointing(
    image_path: Annotated[
        str,
        typer.Option(
            "--image-path",
            "-i",
            help="Path to the image file",
        ),
    ] = "data/windows-kitchen.grid.jpg",
    system_prompt: Annotated[
        str,
        typer.Option(
            "--system-prompt",
            "-s",
            help="System prompt for the LLM",
        ),
    ] = "あなたは入力画像を参照し、ユーザーが指し示すオブジェクトの情報を提供する有能なアシスタントです。",  # noqa: E501
    human_prompt: Annotated[
        str,
        typer.Option(
            "--human-prompt",
            "-u",
            help="Human prompt for the LLM",
        ),
    ] = "スマホはどこにありますか？",  # noqa: E501
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)

    try:
        # Load image file
        with open(image_path, "rb") as f:
            image_data = f.read()
        # Convert to base64
        base64_image = base64.b64encode(image_data).decode("utf-8")
        resolver = AzureOpenAiSceneResolver(
            model=PointingResult,
            system_prompt=system_prompt,
            human_prompt=human_prompt,
        )
        result = resolver.solve(
            base64_image=base64_image,
        )
        print(f"Processed image saved to {result.model_dump_json(indent=2)}")
    except Exception as e:
        logger.error(f"Error processing image: {e}")


if __name__ == "__main__":
    result = load_dotenv(
        override=True,
        verbose=True,
    )
    if not result:
        logger.warning("Failed to load .env file")
        # pass through even if .env loading fails
    app()
