from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

# from core.schemas import TaskRead
from main import app

# from testing.utils import create_movie_random_slug


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app=app) as client:
        yield client


# @pytest.fixture
# def task() -> Generator[TaskRead]:
#     movie = create_movie_random_slug()
#     yield movie
#     storage.delete(movie)
