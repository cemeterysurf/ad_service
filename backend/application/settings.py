import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import PostgresDsn, SecretStr, RedisDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = True
    LOG_LEVEL: str = 'DEBUG'

    # DATABASE
    DB_HOST: str
    DB_PORT: Optional[int]
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: Optional[int]
    REDIS_USER: str
    REDIS_PASSWORD: SecretStr
    REDIS_NAME: str

    # AUTH
    REFRESH_TOKEN_COOKIE_NAME: str
    REFRESH_TOKEN_DURATION_DAYS: int

    ACCESS_TOKEN_COOKIE_NAME: str
    ACCESS_TOKEN_DURATION_MINUTES: int

    JWT_SECRET: str
    JWT_ALGORITHM: str

    @property
    def DB_URL(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME}"
        )

    @property
    def REDIS_URL(self) -> str:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USER,
            password=self.REDIS_PASSWORD.get_secret_value(),
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_NAME}"
        )


settings = Settings(
    DB_HOST=os.getenv("DB_HOST"),
    DB_PORT=int(os.getenv("DB_PORT")),
    DB_USER=os.getenv("DB_USER"),
    DB_PASSWORD=os.getenv("DB_PASSWORD"),
    DB_NAME=os.getenv("DB_NAME"),
    REDIS_HOST=os.getenv("REDIS_HOST"),
    REDIS_PORT=int(os.getenv("REDIS_PORT")),
    REDIS_USER=os.getenv("REDIS_USER"),
    REDIS_PASSWORD=os.getenv("REDIS_PASSWORD"),
    REDIS_NAME=os.getenv("REDIS_NAME"),
    REFRESH_TOKEN_COOKIE_NAME=os.getenv("REFRESH_TOKEN_COOKIE_NAME",
                                        "refresh_token"),
    REFRESH_TOKEN_DURATION_DAYS=int(
        os.getenv("REFRESH_TOKEN_DURATION_DAYS", "10")),
    ACCESS_TOKEN_COOKIE_NAME=os.getenv("ACCESS_TOKEN_COOKIE_NAME",
                                       "access_token"),
    ACCESS_TOKEN_DURATION_MINUTES=int(
        os.getenv("ACCESS_TOKEN_DURATION_MINUTES", "10")),
    JWT_SECRET=os.getenv("JWT_SECRET", None),
    JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256")
)
