from fastapi import APIRouter

from core import settings

from .tasks_urls.views import router as tasks_urls

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(tasks_urls)
