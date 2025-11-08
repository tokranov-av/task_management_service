import asyncio
import json
from asyncio import AbstractEventLoop
from collections.abc import Generator
from datetime import datetime

import pytest
from sqlalchemy import insert

from core.config import (
    BASE_DIR,
    IS_TESTING,
)
from core.models import (
    Base,
    Task,
    db_helper,
)

if not IS_TESTING:
    pytest.exit("Environment is not ready for testing.")


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[AbstractEventLoop]:
    """Создает event loop для фикстур."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    """Подготовка базы данных для тестов."""
    assert IS_TESTING

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    fixture_path = BASE_DIR / "testing" / "fixtures" / "tasks.json"

    with fixture_path.open(encoding="utf-8") as file:
        tasks = json.load(file)

    for task in tasks:
        if task["started_at"] is not None:
            task["started_at"] = datetime.strptime(  # noqa: DTZ007
                task["started_at"],
                "%Y-%m-%d %H:%M:%S",
            )
        if task["completed_at"] is not None:
            task["completed_at"] = datetime.strptime(  # noqa: DTZ007
                task["completed_at"],
                "%Y-%m-%d %H:%M:%S",
            )

    async with db_helper.session_factory() as session:
        add_tasks = insert(Task).values(tasks)
        await session.execute(add_tasks)
        await session.commit()
