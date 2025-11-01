from fastapi import APIRouter

from .tasks_urls.views import router as tasks_urls

router = APIRouter(
    prefix="/v1",
)

router.include_router(tasks_urls)
