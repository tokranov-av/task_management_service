from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from ..enums import (
    TaskPriority,
    TaskStatus,
)
from .base import Base
from .mixins import (
    CreatedAtMixin,
    IntIdPkMixin,
)


class Task(IntIdPkMixin, CreatedAtMixin, Base):
    """Модель задачи."""

    title: Mapped[str] = mapped_column(
        String(255),
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.NEW,
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
