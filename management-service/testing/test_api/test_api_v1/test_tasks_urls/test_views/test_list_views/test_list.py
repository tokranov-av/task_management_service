import pytest
from fastapi import status
from httpx import AsyncClient

from core.enums import (
    TaskPriority,
    TaskStatus,
)
from main import app
from testing.consts import (
    NUMBER_OF_TASKS_IN_DB,
    TASK_ONE_ID,
    TASK_THREE_ID,
    TASK_TWO_ID,
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
    assert task1["priority"] == TaskPriority.MEDIUM.value
    assert task1["status"] == TaskStatus.COMPLETED.value
    assert task1["started_at"] == "2025-11-07T03:30:30"
    assert task1["completed_at"] == "2025-11-07T03:35:30"
    assert task1["result"] == "Успешно выполнена"
    assert task1["error_info"] is None


@pytest.mark.apitest
@pytest.mark.parametrize(
    "query_params, expected_data",
    [
        pytest.param(
            {"status": TaskStatus.COMPLETED.value},
            {
                "id": TASK_ONE_ID,
                "title": "Задача 1",
                "status": TaskStatus.COMPLETED.value,
            },
            id="filter-by-status-completed",
        ),
        pytest.param(
            {"status": TaskStatus.IN_PROGRESS.value},
            {
                "id": TASK_TWO_ID,
                "title": "Задача 2",
                "status": TaskStatus.IN_PROGRESS.value,
            },
            id="filter-by-status-in-progress",
        ),
        pytest.param(
            {"priority": TaskPriority.LOW.value},
            {
                "id": TASK_TWO_ID,
                "title": "Задача 2",
                "priority": TaskPriority.LOW.value,
            },
            id="filter-by-priority-low",
        ),
        pytest.param(
            {"priority": TaskPriority.HIGH.value},
            {
                "id": TASK_THREE_ID,
                "title": "Задача 3",
                "priority": TaskPriority.HIGH.value,
            },
            id="filter-by-priority-high",
        ),
    ],
)
async def test_filters(
    client: AsyncClient,
    query_params: dict[str, str],
    expected_data: dict[str, str],
) -> None:
    url = app.url_path_for("get_tasks")

    response = await client.get(url=url, params=query_params)

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert len(data) == 1
    task = data[0]
    for key, value in expected_data.items():
        assert task[key] == value
