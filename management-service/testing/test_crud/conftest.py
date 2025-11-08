from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession]:
    async with db_helper.session_factory() as session:
        yield session
