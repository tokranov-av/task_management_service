from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from core import settings


class Base(DeclarativeBase):
    """Базовая модель."""

    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.postgres.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return f"{cls.__name__.lower()}s"
