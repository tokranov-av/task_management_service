__all__ = ("db_helper",)

import logging
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import (
    NullPool,
    Pool,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core import settings

log = logging.getLogger(__name__)


class DatabaseHelper:
    def __init__(  # noqa: PLR0913
        self,
        url: str,
        echo: bool = False,  # noqa: FBT001, FBT002
        echo_pool: bool = False,  # noqa: FBT001, FBT002
        pool_size: int | None = None,
        max_overflow: int | None = None,
        poolclass: type[Pool] | None = None,
    ) -> None:
        engine_kwargs: dict[str, Any] = {
            "url": url,
            "echo": echo,
            "echo_pool": echo_pool,
        }

        if poolclass is not None:
            engine_kwargs["poolclass"] = poolclass

        if poolclass is None or not issubclass(poolclass, NullPool):
            if pool_size is not None:
                engine_kwargs["pool_size"] = pool_size
            if max_overflow is not None:
                engine_kwargs["max_overflow"] = max_overflow

        self.engine: AsyncEngine = create_async_engine(**engine_kwargs)

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def dispose(self) -> None:
        await self.engine.dispose()
        log.info("Database engine disposed")


db_helper = DatabaseHelper(
    url=settings.postgres.url,
    **settings.postgres.get_database_params,
)
