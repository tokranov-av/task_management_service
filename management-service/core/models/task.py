import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import func

from ..enums import (
    TaskPriority,
    TaskStatus,
)
from .base import Base
from .mixins import CreatedAtMixin


class Task(CreatedAtMixin, Base):
    """Модель задачи."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority),
        nullable=False,
        default=TaskPriority.MEDIUM,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.NEW,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    error_info: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, title={self.title}, status='{self.status.value}')>"

    def __repr__(self) -> str:
        return str(self)
