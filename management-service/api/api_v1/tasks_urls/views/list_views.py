from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.decorators import handle_errors
from core.models import db_helper
from core.schemas import (
    TaskCreate,
    TaskRead,
)
from core.schemas.task import (
    TaskFilterParams,
    TaskPaginationParams,
)
from crud import tasks as crud_tasks
from services import rabbitmq_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
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
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Database error occurred",
                    },
                },
            },
        },
    },
)


@router.get(
    path="/",
)
@handle_errors
async def get_tasks(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    filter_params: Annotated[TaskFilterParams, Depends()],
    pagination: Annotated[TaskPaginationParams, Depends()],
) -> list[TaskRead]:
    tasks = await crud_tasks.get_tasks(
        session=session,
        filter_params=filter_params,
        pagination=pagination,
    )

    return [TaskRead.model_validate(task) for task in tasks]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
@handle_errors
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

    task_message = {
        "id": str(task.id),
        "title": str(task.title),
        "description": str(task.description),
        "priority": str(task.priority.value),
        "created_at": task.created_at.isoformat() if task.created_at else "",
    }

    await rabbitmq_service.publish_task(task_message)

    return TaskRead.model_validate(task)
