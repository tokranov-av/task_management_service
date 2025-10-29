from datetime import (
    UTC,
    datetime,
)

from sqlalchemy import func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


def get_current_dt() -> datetime:
    dt = datetime.now(tz=UTC)
    return dt.replace(microsecond=0, tzinfo=None)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
    )
