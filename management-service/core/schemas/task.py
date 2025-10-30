from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict

from core.enums import (
    TaskPriority,
    TaskStatus,
)


class TaskBase(BaseModel):
    """Базовая схема задачи."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    title: Annotated[str, MaxLen(255)]
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.NEW
    result: str | None = None
    error_info: str | None = None


class TaskCreate(TaskBase):
    """Схема для создания задачи."""


class TaskUpdate(TaskBase):
    """Схема для обновления задачи."""


class TaskUpdatePartial(BaseModel):
    """Схема частичного обновления задачи."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    title: Annotated[str, MaxLen(255)] | None = None
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.NEW
    result: str | None = None
    error_info: str | None = None


class TaskRead(TaskBase):
    """Схема для чтения задачи."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
