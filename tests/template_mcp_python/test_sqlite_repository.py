import pytest

from template_mcp_python.internals.repositories.sqlite_repository import SqliteRepository
from template_mcp_python.internals.repositories.types import (
    CreateImageRequest,
    ReadImageRequest,
    ResultStatus,
)


@pytest.fixture()
def sqlite_repo(tmp_path):
    db_path = tmp_path / "images.db"
    return SqliteRepository(db_path)


def test_create_and_read_image(sqlite_repo):
    request = CreateImageRequest(base64_image="ZmFrZV9iYXNlNjQ=")

    create_response = sqlite_repo.create_image(request)
    assert create_response.status is ResultStatus.SUCCESS
    assert create_response.image_id

    read_response = sqlite_repo.read_image(ReadImageRequest(image_id=create_response.image_id))

    assert read_response.status is ResultStatus.SUCCESS
    assert read_response.base64_image == request.base64_image


def test_read_image_missing_returns_failure(sqlite_repo):
    read_response = sqlite_repo.read_image(ReadImageRequest(image_id="missing"))

    assert read_response.status is ResultStatus.FAILURE
    assert read_response.base64_image == ""
