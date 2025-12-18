import logging
from typing import Annotated

import typer
from dotenv import load_dotenv

from template_mcp_python.internals.processors.images import ImageProcessor
from template_mcp_python.loggers import get_logger

app = typer.Typer(
    add_completion=False,
    help="Image Processor Operator CLI",
)

logger = get_logger(__name__)


def set_verbose_logging(
    verbose: bool,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)


@app.command(
    help="Add grid overlay to an image",
)
def add_grid_overlay(
    image_path: Annotated[
        str,
        typer.Option(
            "--image-path",
            "-i",
            help="Path to the image file",
        ),
    ] = "data/windows-kitchen.jpg",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-o",
            help="Path to save the processed image",
        ),
    ] = "data/windows-kitchen.grid.jpg",
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    set_verbose_logging(verbose)

    try:
        processor = ImageProcessor(image_path=image_path)
        processor.read_image()
        processor.overlay_grid(
            interval=50,
            bgr_color=(0, 0, 255),
            enable_ticks=True,
        )
        processor.save_image(output_path=output_path)
        logger.info(f"Processed image saved to {output_path}")
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
