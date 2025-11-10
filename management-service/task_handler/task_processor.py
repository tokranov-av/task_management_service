import asyncio
import logging
import random

logger = logging.getLogger(__name__)


class TaskExecutingError(Exception):
    """Ошибка при выполнении задачи."""


async def process_task(task_data: dict[str, str]) -> str:
    """Обработка задачи с имитацией работы."""

    task_id = int(task_data["id"])
    priority = task_data["priority"]

    logger.info("Processing task %s with priority %s", task_id, priority)

    # Время обработки в зависимости от приоритета
    processing_times = {
        "LOW": random.uniform(20, 55),  # noqa: S311
        "MEDIUM": random.uniform(30, 50),  # noqa: S311
        "HIGH": random.uniform(25, 30),  # noqa: S311
    }

    processing_time = processing_times.get(priority, 5)

    # Имитация обработки
    logger.info("Task %s will take %.2f seconds", task_id, processing_time)
    await asyncio.sleep(processing_time)

    # Имитация возможной ошибки (5% вероятность)
    if random.random() < (5 / 100):  # noqa: S311
        error_msg = f"Simulated error processing task {task_id}"
        logger.error(error_msg)
        raise TaskExecutingError(error_msg)

    result = f"Task processed successfully in {processing_time:.2f} seconds"
    logger.info("Task %s completed: %s", task_id, result)

    return result
