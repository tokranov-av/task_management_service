# Сервис управления задачами

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
