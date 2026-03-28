import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Корень проекта (папка с run.py), чтобы токен находился при запуске из любой cwd
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")
load_dotenv()  # опционально: переопределение из текущей директории


@dataclass(frozen=True)
class Config:
    bot_token: str
    telegram_proxy: str | None  # TELEGRAM_PROXY, если нет прямого доступа к api.telegram.org
    request_timeout: float  # TELEGRAM_REQUEST_TIMEOUT, сек


def load_config() -> Config:
    token = (os.getenv("BOT_TOKEN") or "").strip()
    if not token:
        env_file = _PROJECT_ROOT / ".env"
        msg = (
            "Не задан BOT_TOKEN.\n"
            f"Создайте файл {env_file} (скопируйте из .env.example) и строку:\n"
            "BOT_TOKEN=токен_от_BotFather"
        )
        raise ValueError(msg)

    proxy_raw = (os.getenv("TELEGRAM_PROXY") or "").strip()
    telegram_proxy = proxy_raw or None

    timeout_raw = (os.getenv("TELEGRAM_REQUEST_TIMEOUT") or "120").strip()
    try:
        request_timeout = float(timeout_raw)
    except ValueError:
        request_timeout = 120.0
    if request_timeout < 10:
        request_timeout = 10.0

    return Config(
        bot_token=token,
        telegram_proxy=telegram_proxy,
        request_timeout=request_timeout,
    )
