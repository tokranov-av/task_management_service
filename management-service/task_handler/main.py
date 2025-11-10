import asyncio
import logging
from logging.config import dictConfig

from core.config import settings

from .worker import worker

dictConfig(settings.logging.dict_config)

logger = logging.getLogger(__name__)


async def main() -> None:
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
