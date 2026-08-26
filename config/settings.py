import os
from dataclasses import dataclass, field

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


def _get_list(name: str, default: list[str]) -> list[str]:
    value = os.getenv(name)
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_debug: bool = _get_bool("APP_DEBUG", False)
    cors_origins: list[str] = field(
        default_factory=lambda: _get_list(
            "CORS_ORIGINS",
            ["http://127.0.0.1:5173", "http://localhost:5173"],
        )
    )
    cors_allow_credentials: bool = _get_bool("CORS_ALLOW_CREDENTIALS", False)

    database_url: str = _require_env("ASYNC_DATABASE_URL")
    database_schema: str = os.getenv("DATABASE_SCHEMA", "public")
    sqlalchemy_echo: bool = _get_bool("SQLALCHEMY_ECHO", False)

    redis_url: str | None = os.getenv("REDIS_URL")
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    redis_password: str | None = os.getenv("REDIS_PASSWORD")
    redis_socket_timeout: float = float(os.getenv("REDIS_SOCKET_TIMEOUT", "5"))

    ai_api_endpoint: str = os.getenv(
        "AI_API_ENDPOINT",
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    )
    ai_api_key: str | None = os.getenv("AI_API_KEY")
    ai_model: str = os.getenv("AI_MODEL", "qwen3-max-preview")
    ai_request_timeout: float = float(os.getenv("AI_REQUEST_TIMEOUT", "60"))


settings = Settings()
