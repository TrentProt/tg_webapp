from pathlib import Path

from pydantic import BaseModel, Field

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / 'logs'
ENV_FILE = BASE_DIR / '.env'


class LoggingConfig(BaseModel):
    debug_mode: bool = False


class TelegramBotConfig(BaseSettings):
    api_key: str
    web_url: str


class TelegramUserConfig(BaseSettings):
    api_hash: str
    api_id: str


class FastAPIConfig(BaseSettings):
    host: str = Field(default='localhost')
    port: int = Field(default=8000)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding='utf-8',
        env_nested_delimiter='_',
        env_nested_max_split=1,
        extra='ignore',
        frozen=True,
    )

    logging: LoggingConfig
    fastapi: FastAPIConfig
    tgbot: TelegramBotConfig
    tguser: TelegramUserConfig
    LOG_DIR: Path = LOG_DIR


def _get_config() -> Config:
    """Возвращает объект конфигурации.

    Это решение, рекомендованное разработчиком pydantic_settings, подробнее:
    https://github.com/pydantic/pydantic/issues/3753#issuecomment-1087417884
    """
    return Config.model_validate({})


CONFIG: Config = _get_config()
