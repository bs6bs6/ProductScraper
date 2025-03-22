import secrets
from typing import Union, List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
import os


class Config(BaseSettings):
    PROJECT_VERSION: Union[int, str] = 1.0
    PROJECT_ROOT_PATH: str = os.path.abspath('./')
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8000"

    API_PREFIX: str = "/api"
    STATIC_DIR: str = 'static'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[str] = ["*"]

    DATABASE_URI: str = "mysql+pymysql://root:123456@localhost/scraper_db"
    # DATABASE_URI: str = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
    #     user=os.getenv("MYSQL_USER", "root"),
    #     password=os.getenv("MYSQL_PASSWORD", "root"),
    #     host=os.getenv("MYSQL_HOST", "localhost"),
    #     port=os.getenv("MYSQL_PORT", "3306"),
    #     database=os.getenv("MYSQL_DATABASE", "scraper_db")
    # )
    DATABASE_ECHO: bool = False

    LOGGER_DIR: str = "logs"
    LOGGER_NAME: str = '{time:YYYY-MM-DD_HH-mm-ss}.log'
    LOGGER_LEVEL: str = 'DEBUG'

    class Config:
        case_sensitive = True


config = Config()