import pytest
from fastapi import status
from httpx import AsyncClient

from core.enums import TaskPriority
from core.schemas import TaskCreate
from main import app
from testing.utils import get_random_string


@pytest.mark.apitest
async def test_create_task(client: AsyncClient) -> None:
    url = app.url_path_for("create_task")
    task_create = TaskCreate(
        title=get_random_string(),
        description=get_random_string(),
        priority=TaskPriority.MEDIUM,
    ).model_dump(mode="json")

    response = await client.post(url=url, json=task_create)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert "id" in response_data
    assert response_data["title"] == task_create["title"]
    assert response_data["description"] == task_create["description"]
    assert response_data["priority"] == task_create["priority"]
