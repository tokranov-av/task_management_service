__all__ = ("rabbitmq_service",)

import json
import logging
from typing import TYPE_CHECKING

import aio_pika

from core import settings

if TYPE_CHECKING:
    from aio_pika.abc import (
        AbstractChannel,
        AbstractExchange,
        AbstractRobustConnection,
    )


logger = logging.getLogger(__name__)


class RabbitMQService:
    """Управление подключением и публикацией задач в RabbitMQ."""

    def __init__(self) -> None:
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None
        self.exchange: AbstractExchange | None = None

    async def connect(self) -> None:
        """Установка соединения с RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(settings.rabbitmq.url)
            self.channel = await self.connection.channel()

            # Объявляем Direct Exchange
            self.exchange = await self.channel.declare_exchange(
                settings.rabbitmq.exchange_name,
                aio_pika.ExchangeType.DIRECT,
                durable=True,
            )

            # Объявляем очередь с поддержкой приоритетов
            queue = await self.channel.declare_queue(
                settings.rabbitmq.queue_name,
                durable=True,
            )

            await queue.bind(self.exchange, settings.rabbitmq.queue_name)
            logger.info("RabbitMQ connected successfully")

        except Exception:
            error_msg = "Exchange is not initialized"
            logger.exception(error_msg)
            raise

    async def close(self) -> None:
        """Закрытие соединения"""
        if self.connection:
            await self.connection.close()

    async def publish_task(self, task_data: dict[str, str]) -> None:
        """Публикация задачи в очередь."""
        if not self.channel:
            await self.connect()

        priority_map = {"LOW": 1, "MEDIUM": 5, "HIGH": 10}
        priority = priority_map.get(task_data.get("priority", "MEDIUM"), 5)

        message = aio_pika.Message(
            body=json.dumps(task_data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            priority=priority,
        )

        if self.exchange is None:
            error_msg = "Exchange is not initialized"
            raise RuntimeError(error_msg)

        await self.exchange.publish(message, routing_key=settings.rabbitmq.queue_name)

        logger.info("Task %s published to RabbitMQ", task_data.get("id"))


rabbitmq_service = RabbitMQService()
