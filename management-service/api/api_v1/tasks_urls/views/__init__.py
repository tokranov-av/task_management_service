__all__ = ("router",)

from .detail_views import router as details_router
from .list_views import router

router.include_router(details_router)
