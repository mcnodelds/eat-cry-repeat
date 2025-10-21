from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="EAT_CRY_REPEAT",
        env_file=".env",
    )

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:password@localhost:5432/eatcryrepeat"
    )
    SECRET_KEY: str = "change_me_to_strong_random"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"


settings = Settings()
