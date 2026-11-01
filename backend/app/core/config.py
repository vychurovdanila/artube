from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-in-production-please-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    TELEGRAM_BOT_TOKEN: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
