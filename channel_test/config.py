from pydantic import BaseSettings


class Settings(BaseSettings):
    ADMIN_TELEGRAM_ID: str
    TELEBOT_TOKEN: str
    SHEET_URL: str
    GOOGLE_TOKEN_FILEPATH: str = 'token.json'
    UPDATE_INTERVAL_SECONDS: int = 60
    DEBUG: bool = False


class Database(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


db = Database(
    _env_file='../env',
    _env_file_encoding='utf-8'
)

settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8'
)
