from enum import Enum
from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class CacheType(str, Enum):
    DUMMY = "dummy"
    REDIS = "redis"
    DB = "db"


class ProjectConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '../.env'),
        env_file_encoding='utf-8',
        ignored_types=(cached_property,)
    )

    ENVIRONMENT: Environment
    SECRET_KEY: str
    DEBUG: bool
    ALLOWED_HOSTS: str = []

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NUMBER: int = 0
    PG_EXT_PORT: int = 5432

    CACHE_TYPE: CacheType = CacheType.DUMMY.value
    CACHE_TIMEOUT: str | None = None

    REDIS_HOST: str
    REDIS_EXT_PORT: int = 6379

    CELERY_CACHE_BACKEND: CacheType

    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_HOST_USER: str
    EMAIL_USE_TLS: bool
    EMAIL_USE_SSL: bool
    EMAIL_HOST_PASSWORD: str

    @cached_property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:6379/{self.DB_NUMBER}"

    @cached_property
    def allowed_hosts(self) -> list[str]:
        return self.ALLOWED_HOSTS.split(',')


project_config = ProjectConfig()
