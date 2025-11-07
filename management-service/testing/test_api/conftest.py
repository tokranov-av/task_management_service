from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import (
    ASGITransport,
    AsyncClient,
)

from main import app as fastapi_app


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test",
    ) as ac:
        yield ac
