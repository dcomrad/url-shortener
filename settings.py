from pydantic import BaseSettings, Field


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Field(env='DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool
    SECRET_KEY: str
    SQLALCHEMY_ECHO: bool


config = Config()
