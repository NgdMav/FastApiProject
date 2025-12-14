import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_USER: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()