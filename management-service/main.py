import logging

from fastapi import (
    FastAPI,
)

from api import router as api_router
from core.config import (
    settings,
)

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)

app = FastAPI(
    title="API Сервиса управления задачами ",
)
app.include_router(api_router)
