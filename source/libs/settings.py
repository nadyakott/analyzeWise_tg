from pydantic import BaseSettings

class Settings(BaseSettings):
    """Общие настройки из env."""

    BOT_TOKEN: str

    class Config:
        case_sensitive = True
        env_file = '../.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

settings = Settings()