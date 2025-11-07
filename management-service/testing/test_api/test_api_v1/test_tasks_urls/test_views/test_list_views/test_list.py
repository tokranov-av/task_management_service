import pytest
from fastapi import status
from httpx import AsyncClient

from core.enums import TaskStatus
from main import app
from testing.consts import (
    NUMBER_OF_TASKS_IN_DB,
    TASK_ONE_ID,
)


@pytest.mark.apitest
async def test_get_tasks(client: AsyncClient) -> None:
    url = app.url_path_for("get_tasks")

    response = await client.get(url=url)

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert len(data) >= NUMBER_OF_TASKS_IN_DB
    task1 = data[0]
    assert task1["id"] == TASK_ONE_ID
    assert task1["title"] == "Задача 1"
    assert task1["description"] == "Описание задачи 1"
    assert task1["priority"] == "MEDIUM"
    assert task1["status"] == TaskStatus.COMPLETED.value
    assert task1["started_at"] == "2025-11-07T03:30:30"
    assert task1["completed_at"] == "2025-11-07T03:35:30"
    assert task1["result"] == "Успешно выполнена"
    assert task1["error_info"] is None
