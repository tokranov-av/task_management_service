__all__ = ("worker",)

import asyncio
import json
import logging
from datetime import datetime

import aio_pika

from core import settings
from core.enums import TaskStatus
from core.models import db_helper
from core.schemas import TaskUpdatePartial
from crud.tasks import (
    get_task,
    update_task,
)

from .task_processor import process_task

logger = logging.getLogger(__name__)


class TaskWorker:
    """Воркер обработки задач."""

    async def update_task_status(
        self,
        task_id: int,
        status: TaskStatus,
        **kwargs: str | float | bool | None,
    ) -> None:
        """Обновление статуса задачи в БД."""
        async with db_helper.session_factory() as session:
            task = await get_task(session, task_id)
            if task:
                task_update = TaskUpdatePartial(status=status, **kwargs)

                if status == TaskStatus.IN_PROGRESS:
                    task_update.started_at = datetime.now()
                elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    task_update.completed_at = datetime.now()

                await update_task(
                    session=session,
                    task=task,
                    task_update=task_update,
                    partial=True,
                )
                logger.info("Task %s status updated to %s", task_id, status.value)

    async def process_message(self, message: aio_pika.IncomingMessage) -> None:
        """Обработка сообщения из очереди."""
        async with message.process():
            try:
                task_data = json.loads(message.body.decode())
                task_id = int(task_data["id"])
                logger.info("Started processing task: %s", task_id)

                await self.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.IN_PROGRESS,
                )

                result = await process_task(task_data)

                await self.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.COMPLETED,
                    result=result,
                )
                logger.info("Task %s completed successfully", task_id)
            except Exception as e:
                logger.exception("Error processing task %s", task_data.get("id"))
                await self.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.FAILED,
                    error_info=str(e),
                )

    async def start(self) -> None:
        """Запуск воркера."""
        try:
            connection = await aio_pika.connect_robust(settings.rabbitmq.url)
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            queue = await channel.declare_queue(
                settings.rabbitmq.queue_name,
                durable=True,
            )

            logger.info("Task worker started. Waiting for messages...")

            await queue.consume(self.process_message)  # type: ignore[arg-type]
            await asyncio.Future()
        except Exception:
            logger.exception("Worker failed to start")
            raise


worker = TaskWorker()
