from typing import (
    Annotated,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.tasks_urls import prefetch_task
from core.models import Task, db_helper
from core.schemas import (
    TaskRead,
)
from core.schemas.task import TaskStatusRead
from crud import tasks as crud_tasks

router = APIRouter(
    prefix="/{task_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Task with 'task_id' not found",
                    },
                },
            },
        },
    },
)

TaskById = Annotated[
    Task,
    Depends(prefetch_task),
]


@router.get(
    path="/",
)
async def read_task(
    task: TaskById,
) -> TaskRead:
    return TaskRead.model_validate(task)


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
    task: TaskById,
) -> None:
    await crud_tasks.delete_task(
        session=session,
        task=task,
    )


@router.get(
    path="/status",
)
async def get_task_status(
    task: TaskById,
) -> TaskStatusRead:
    return TaskStatusRead(
        id=task.id,
        status=task.status,
    )
