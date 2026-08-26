import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency is listed in requirements.txt
    load_dotenv = None


if load_dotenv:
    load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"{name} is required. Copy .env.example to .env and set your deployment values."
        )
    return value


@dataclass(frozen=True)
class Settings:
    database_url: str = _require_env("ASYNC_DATABASE_URL")
    database_schema: str = os.getenv("DATABASE_SCHEMA", "public")
    sqlalchemy_echo: bool = _get_bool("SQLALCHEMY_ECHO", False)

    redis_url: str | None = os.getenv("REDIS_URL")
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    redis_password: str | None = os.getenv("REDIS_PASSWORD")
    redis_socket_timeout: float = float(os.getenv("REDIS_SOCKET_TIMEOUT", "5"))


settings = Settings()
