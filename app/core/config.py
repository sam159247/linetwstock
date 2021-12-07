"""Read .env file to set token if it's in DEVELPOMENT environment, otherwise
read AWS Systems Manager Parameter Store to set token."""
import os
from functools import cache

from pydantic import BaseSettings

from app.core.utils import get_ssm_parameters

# TODO: refactor
ENVIRONMENT: str = os.getenv("ENV", "DEVELPOMENT")


class Settings(BaseSettings):
    PROJECT_NAME: str = "linetwstock"
    ENV: str = ENVIRONMENT
    FINMIND_BASE_URL: str = "https://api.finmindtrade.com/api/v4/data"
    FINMIND_TOKEN: str
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str


class Development(Settings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Staging_1(Settings):
    if ENVIRONMENT == "STAGING_1":
        result_params = get_ssm_parameters(
            [
                "/stg1/lambda/linetwstock/finmind_token",
                "/stg1/lambda/linetwstock/line_channel_secret",
                "/stg1/lambda/linetwstock/line_channel_access_token",
            ]
        )

        FINMIND_TOKEN = result_params["/stg1/lambda/linetwstock/finmind_token"]
        LINE_CHANNEL_SECRET = result_params["/stg1/lambda/linetwstock/line_channel_secret"]
        LINE_CHANNEL_ACCESS_TOKEN = result_params["/stg1/lambda/linetwstock/line_channel_access_token"]


class Production(Settings):
    if ENVIRONMENT == "PRODUCTION":
        result_params = get_ssm_parameters(
            [
                "/prod/lambda/linetwstock/finmind_token",
                "/prod/lambda/linetwstock/line_channel_secret",
                "/prod/lambda/linetwstock/line_channel_access_token",
            ]
        )

        FINMIND_TOKEN = result_params["/prod/lambda/linetwstock/finmind_token"]
        LINE_CHANNEL_SECRET = result_params["/prod/lambda/linetwstock/line_channel_secret"]
        LINE_CHANNEL_ACCESS_TOKEN = result_params["/prod/lambda/linetwstock/line_channel_access_token"]


@cache
def get_settings() -> Settings:
    if ENVIRONMENT == "STAGING_1":
        return Staging_1()
    if ENVIRONMENT == "PRODUCTION":
        return Production()
    return Development()


settings = get_settings()
