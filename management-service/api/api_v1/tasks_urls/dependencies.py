from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    Task,
    db_helper,
)
from crud import tasks as crud_tasks


async def prefetch_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
    task_id: int,
) -> Task:
    task: Task | None = await crud_tasks.get_task(
        session=session,
        task_id=task_id,
    )

    if task:
        return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
