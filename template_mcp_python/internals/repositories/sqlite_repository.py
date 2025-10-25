"""SQLite-backed repository implementation."""

from __future__ import annotations

import sqlite3
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from template_mcp_python.internals.repositories.base_model import RepositoryBaseModel
from template_mcp_python.internals.repositories.types import (
    CreateImageRequest,
    CreateImageResponse,
    ReadImageRequest,
    ReadImageResponse,
    ResultStatus,
)


class SqliteRepository(RepositoryBaseModel):
    """Repository implementation storing images in a SQLite database."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _initialize(self) -> None:
        # Create the images table if it does not already exist.
        with self._connect() as conn:
            conn.execute(
                """
				CREATE TABLE IF NOT EXISTS images (
					id TEXT PRIMARY KEY,
					base64_image TEXT NOT NULL,
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				)
				"""
            )

    def create_image(self, request: CreateImageRequest) -> CreateImageResponse:
        image_id = uuid.uuid4().hex
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO images (id, base64_image) VALUES (?, ?)",
                    (image_id, request.base64_image),
                )
        except sqlite3.Error:  # pragma: no cover - defensive branch
            # Surface a failure status while keeping the generated identifier.
            return CreateImageResponse(image_id=image_id, status=ResultStatus.FAILURE)
        return CreateImageResponse(image_id=image_id, status=ResultStatus.SUCCESS)

    def read_image(self, request: ReadImageRequest) -> ReadImageResponse:
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT base64_image FROM images WHERE id = ?",
                    (request.image_id,),
                )
                row = cursor.fetchone()
        except sqlite3.Error:  # pragma: no cover - defensive branch
            return ReadImageResponse(base64_image="", status=ResultStatus.FAILURE)

        if row is None:
            return ReadImageResponse(base64_image="", status=ResultStatus.FAILURE)

        return ReadImageResponse(base64_image=row[0], status=ResultStatus.SUCCESS)
