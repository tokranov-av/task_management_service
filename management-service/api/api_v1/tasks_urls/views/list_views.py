from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas import (
    TaskCreate,
    TaskRead,
)
from crud import tasks as crud_tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get(
    path="/",
)
async def get_list_of_tasks(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
) -> list[TaskRead]:
    tasks = await crud_tasks.get_all_tasks(
        session=session,
    )

    return [TaskRead.model_validate(task) for task in tasks]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
    task_create: TaskCreate,
) -> TaskRead:
    task = await crud_tasks.create_task(
        session=session,
        task_create=task_create,
    )

    return TaskRead.model_validate(task)
