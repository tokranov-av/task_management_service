from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import (
    TaskPriority,
    TaskStatus,
)
from core.schemas.task import (
    TaskCreate,
    TaskFilterParams,
    TaskUpdate,
)
from crud import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)
from testing.consts import (
    NUMBER_OF_TASKS_IN_DB,
    TASK_ONE_ID,
    TASK_THREE_ID,
)
from testing.utils import (
    create_task_in_db,
    get_random_string,
    get_task_by_id,
)


async def test_get_tasks(db_session: AsyncSession) -> None:
    tasks = await get_tasks(session=db_session)

    assert len(tasks) >= NUMBER_OF_TASKS_IN_DB


@pytest.mark.parametrize(
    "filter_params, expected_data",
    [
        pytest.param(
            {"status": TaskStatus.COMPLETED.value},
            {
                "id": TASK_ONE_ID,
                "title": "Задача 1",
                "status": TaskStatus.COMPLETED,
            },
            id="filter-by-status-completed",
        ),
        pytest.param(
            {"priority": TaskPriority.HIGH.value},
            {
                "id": TASK_THREE_ID,
                "title": "Задача 3",
                "priority": TaskPriority.HIGH,
            },
            id="filter-by-priority-high",
        ),
    ],
)
async def test_get_tasks_filters(
    db_session: AsyncSession,
    filter_params: dict[str, str],
    expected_data: dict[str, str],
) -> None:
    params = TaskFilterParams(
        **filter_params,
    )

    tasks = await get_tasks(
        session=db_session,
        filter_params=params,
    )

    assert len(tasks) == 1
    task = tasks[0]
    for key, value in expected_data.items():
        assert getattr(task, key) == value


async def test_get_task(db_session: AsyncSession) -> None:
    task = await get_task(session=db_session, task_id=TASK_ONE_ID)

    assert task is not None, "Задача не найдена"
    assert task.id == TASK_ONE_ID
    assert task.title == "Задача 1"
    assert task.description == "Описание задачи 1"
    assert task.priority == TaskPriority.MEDIUM
    assert task.status == TaskStatus.COMPLETED
    assert task.started_at == datetime(2025, 11, 7, 3, 30, 30)
    assert task.completed_at == datetime(2025, 11, 7, 3, 35, 30)
    assert task.result == "Успешно выполнена"
    assert task.error_info is None


async def test_create_task(db_session: AsyncSession) -> None:
    task_create = TaskCreate(
        title=get_random_string(),
        description=get_random_string(),
        priority=TaskPriority.HIGH,
    )
    task = await create_task(session=db_session, task_create=task_create)

    task_in_db = await get_task_by_id(task_id=task.id)
    assert task_in_db is not None
    assert task_in_db.id is not None
    assert task_in_db.title == task_create.title
    assert task_in_db.description == task_create.description
    assert task_in_db.priority == task_create.priority


async def test_update_task(db_session: AsyncSession) -> None:
    task_create = TaskCreate(
        title=get_random_string(),
        description=get_random_string(),
        priority=TaskPriority.HIGH,
    )
    task = await create_task(session=db_session, task_create=task_create)
    task_in_db = await get_task_by_id(task_id=task.id)
    assert task_in_db is not None
    assert task_in_db.id is not None
    task_update = TaskUpdate(
        title="Обновленное название",
        description=None,
    )

    task_update_db = await update_task(
        session=db_session,
        task=task_in_db,
        task_update=task_update,
    )

    assert task_update_db.title == task_update.title
    assert task_update_db.description is None


async def test_delete_task(db_session: AsyncSession) -> None:
    task = await create_task_in_db()
    assert task is not None, "Задача не найдена"

    await delete_task(session=db_session, task=task)

    task_in_db = await get_task_by_id(task_id=task.id)
    assert task_in_db is None
