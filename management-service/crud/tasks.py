from sqlalchemy import (
    Result,
    and_,
    or_,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskUpdatePartial,
)
from core.schemas.task import (
    TaskFilterParams,
    TaskPaginationParams,
)


async def get_tasks(
    session: AsyncSession,
    filter_params: TaskFilterParams | None = None,
    pagination: TaskPaginationParams | None = None,
) -> list[Task]:
    stmt = select(Task)

    if filter_params:
        conditions = []

        if filter_params.status:
            conditions.append(Task.status == filter_params.status)
        if filter_params.priority:
            conditions.append(Task.priority == filter_params.priority)
        if filter_params.search:
            conditions.append(
                or_(
                    Task.title.ilike(f"%{filter_params.search}%"),
                    Task.description.ilike(f"%{filter_params.search}%"),
                ),
            )

        if conditions:
            stmt = stmt.where(and_(*conditions))

    stmt = stmt.order_by(Task.id)

    if pagination:
        stmt = stmt.limit(pagination.limit).offset(pagination.offset)

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
) -> Task:
    """Выполняет обновление задачи."""
    for field_name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, field_name, value)
    await session.commit()

    return task


async def delete_task(
    session: AsyncSession,
    task: Task,
) -> None:
    """Удаляет задачу."""
    await session.delete(task)
    await session.commit()
