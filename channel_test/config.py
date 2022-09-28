"""Custom config module for load from .env file."""

from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    ADMIN_TELEGRAM_ID: str
    TELEBOT_TOKEN: str
    SHEET_URL: str
    GOOGLE_TOKEN_FILENAME: str = 'token.json'
    UPDATE_INTERVAL_SECONDS: int = 60
    DEBUG: bool = False


class Database(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


ROOT_PATH = Path(__file__).parent.parent
path_to_env = ROOT_PATH / '.env'

db = Database(
    _env_file=path_to_env,
    _env_file_encoding='utf-8'
)

settings = Settings(
    _env_file=path_to_env,
    _env_file_encoding='utf-8'
)
