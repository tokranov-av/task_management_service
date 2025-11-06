__all__ = (
    "BASE_DIR",
    "settings",
)

import logging
import os
from pathlib import Path
from typing import (
    Any,
    Literal,
)

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)
from sqlalchemy import NullPool

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]

    @property
    def dict_config(self) -> dict[str, Any]:
        """Возвращает конфигурацию для dictConfig"""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.log_format,
                    "datefmt": self.date_format,
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": self.log_level,
                },
                "uvicorn": {
                    "handlers": ["default"],
                    "level": self.log_level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["default"],
                    "level": self.log_level,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": self.log_level,
                    "propagate": False,
                },
            },
        }


class PostgresConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    db: str = "postgres"
    user: str = "postgres"
    password: str = ""
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def url(self) -> str:
        user = f"{self.user}:{self.password}"
        database = f"{self.host}:{self.port}/{self.db}"

        return f"postgresql+asyncpg://{user}@{database}"

    @property
    def get_database_params(self) -> dict[str, Any]:
        """Возвращает конфигурацию для DatabaseHelper"""
        db_params: dict[str, Any] = {
            "echo": self.echo,
            "echo_pool": self.echo_pool,
        }

        if os.getenv("TESTING") == "TRUE":
            db_params["poolclass"] = NullPool
        else:
            db_params = db_params | {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
            }

        return db_params

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        yaml_file=(
            BASE_DIR / "config.default.yaml",
            (
                BASE_DIR / "config.custom.test.yaml"
                if os.getenv("TESTING") == "TRUE"
                else BASE_DIR / "config.custom.yaml"
            ),
        ),
        yaml_config_section="management-service",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources
            and their order for loading the settings values.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    logging: LoggingConfig = LoggingConfig()
    postgres: PostgresConfig = PostgresConfig()


settings = Settings()
