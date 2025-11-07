import pytest
from fastapi import status
from httpx import AsyncClient

from main import app
from testing.utils import (
    create_task_in_db,
    get_task_by_id,
)


@pytest.mark.apitest
async def test_delete_task(client: AsyncClient) -> None:
    task = await create_task_in_db()
    assert task.id is not None
    url = app.url_path_for("delete_task", task_id=task.id)

    response = await client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    deleted_task = await get_task_by_id(task_id=task.id)
    assert deleted_task is None
