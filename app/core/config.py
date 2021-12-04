"""Read .env file to set token if it's in DEVELPOMENT environment, otherwise
read AWS Systems Manager Parameter Store to set token."""
import os

from pydantic import BaseSettings

# iru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "linetwstock"
    ENV: str
    FINMIND_BASE_URL: str = "https://api.finmindtrade.com/api/v4/data"
    FINMIND_TOKEN: str


class Development(Settings):
    ENV = "DEVELPOMENT"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    env = os.getenv("ENV", "DEVELPOMENT")
    print(f"ENV={env}")
    return Development()


settings = get_settings()
