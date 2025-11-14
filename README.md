# Сервис управления задачами

[![Python checks 🐍](https://img.shields.io/github/actions/workflow/status/tokranov-av/fastapi-film-catalog/python-checks.yaml?branch=master&label=Python%20checks%20%F0%9F%90%8D&logo=github&style=for-the-badge)](https://github.com/tokranov-av/fastapi-film-catalog/actions/workflows/python-checks.yaml)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&style=for-the-badge)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&style=for-the-badge)](https://github.com/psf/black)
[![Lint: Ruff](https://img.shields.io/badge/lint-ruff-%23efc000?logo=ruff&logoColor=white&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Type Checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blueviolet?logo=python&style=for-the-badge)](https://github.com/python/mypy)
[![Dependency: uv](https://img.shields.io/badge/dependencies-uv-4B8BBE?logo=python&style=for-the-badge)](https://github.com/astral-sh/uv)

## Установка

1. Установите зависимости:

```shell
uv sync
```

2. Создайте файлы для чувствительных данных:

```shell
cd management-service && cp env.template .env && cp config.default.yaml config.local.yaml
```

3. Заполните (замените значения по умолчанию) данные в файлах `.env` и `config.local.yaml`

4. Запустите сервис базы данных и очередь сообщений в docker контейнерах:

В директории `task_management_service` выполните команду:

```shell
docker compose up
```
5. Выполните миграции в базу данных в директории `management-service`:

```shell
alembic upgrade head
```

6. Запустите API:

В отдельном окне терминала в директории `management-service` выполните команду:

```shell
uv run uvicorn main:app --reload
```

7. Запустите обработчик сообщений (имитация сервиса, получающего данные из очереди сообщений и обрабатывающая задачи)

Команду необходимо запустить в отдельном окне терминала в директории `management-service`:

```shell
uv run python -m task_handler.main
```


## Тестирование

1. Для тестирования необходимо установить dev зависимости:

```shell
uv sync --dev
```

2. Запустите сервис тестовой базы данных в директории `task_management_service`:

```shell
docker compose -f docker-compose.test.yaml up
```

3. Запустите тесты:

```shell
uv run env TESTING=TRUE pytest -v
```
