import asyncio
import os
from asyncio import AbstractEventLoop
from collections.abc import AsyncGenerator, Generator

import pytest

from core.models import Base, db_helper


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[AbstractEventLoop]:
    """Создает event loop для фикстур."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> AsyncGenerator[None]:
    """Подготовка базы данных для тестов."""
    assert os.getenv("TESTING") == "TRUE"

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield
