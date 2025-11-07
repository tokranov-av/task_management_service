import pytest
from fastapi import status
from httpx import AsyncClient

from core.enums import (
    TaskPriority,
    TaskStatus,
)
from main import app
from testing.consts import (
    TASK_ONE_ID,
    TASK_TWO_ID,
)


@pytest.mark.apitest
async def test_read_task(client: AsyncClient) -> None:
    url = app.url_path_for("read_task", task_id=TASK_TWO_ID)

    response = await client.get(url=url)

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["id"] == TASK_TWO_ID
    assert data["title"] == "Задача 2"
    assert data["description"] == "Описание задачи 2"
    assert data["priority"] == TaskPriority.LOW.value
    assert data["status"] == TaskStatus.IN_PROGRESS.value
    assert data["started_at"] == "2025-11-07T05:50:50"
    assert data["completed_at"] is None
    assert data["result"] is None
    assert data["error_info"] is None


@pytest.mark.apitest
async def test_get_task_status(client: AsyncClient) -> None:
    url = app.url_path_for("get_task_status", task_id=TASK_ONE_ID)

    response = await client.get(url=url)

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["id"] == TASK_ONE_ID
    assert data["status"] == TaskStatus.COMPLETED.value
