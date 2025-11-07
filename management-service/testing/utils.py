__all__ = (
    "create_task_in_db",
    "get_random_string",
    "get_task_by_id",
)

import random
import string

from core.enums import TaskPriority
from core.models import Task, db_helper
from core.schemas import TaskCreate


def get_random_string(length: int = 8) -> str:
    """Возвращает случайную строку из букв ascii_letters заданной длины."""
    return "".join(
        random.choices(
            string.ascii_letters,
            k=length,
        ),
    )


async def create_task_in_db(
    title: str | None = None,
    description: str | None = None,
    priority: TaskPriority | None = None,
) -> Task:
    actual_priority = TaskPriority.MEDIUM if priority is None else priority
    task_create = TaskCreate(
        title=title or get_random_string(),
        description=description or get_random_string(),
        priority=actual_priority,
    )
    async with db_helper.session_factory() as session:
        task = Task(**task_create.model_dump())
        session.add(task)
        await session.commit()

        return task


async def get_task_by_id(
    task_id: int,
) -> Task | None:
    async with db_helper.session_factory() as session:
        return await session.get(Task, task_id)
