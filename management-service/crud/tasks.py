from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskUpdatePartial,
)


async def get_tasks(session: AsyncSession) -> list[Task]:
    """Возвращает задачи."""
    stmt = select(Task).order_by(Task.id)
    result: Result[tuple[Task]] = await session.execute(stmt)
    tasks = result.scalars().all()

    return list(tasks)


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    """Возвращает задачу по идентификатору."""
    return await session.get(Task, task_id)


async def create_task(
    session: AsyncSession,
    task_create: TaskCreate,
) -> Task:
    """Создает задачу."""
    task = Task(**task_create.model_dump())
    session.add(task)
    await session.commit()
    # await session.refresh(user)

    return task


async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: TaskUpdate | TaskUpdatePartial,
    partial: bool = False,  # noqa: FBT001, FBT002
) -> Task | None:
    """Выполняет обновление задачи."""
    for field_name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, field_name, value)
    await session.commit()

    return task


async def delete_task(
    task: Task,
    session: AsyncSession,
) -> None:
    """Удаляет задачу."""
    await session.delete(task)
    await session.commit()
