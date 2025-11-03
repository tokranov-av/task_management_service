# ruff: noqa: UP047
__all__ = ("handle_errors",)

import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def handle_errors(
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            log.exception("Database error in %s", func.__name__)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred",
            ) from e
        except Exception as e:
            log.exception("Unexpected error in %s", func.__name__)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from e

    return wrapper
