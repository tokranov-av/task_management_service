from logging.config import dictConfig

from fastapi import FastAPI

from api import router as api_router
from core.config import settings

dictConfig(settings.logging.dict_config)

app = FastAPI(
    title="API Сервиса управления задачами",
)
app.include_router(api_router)
