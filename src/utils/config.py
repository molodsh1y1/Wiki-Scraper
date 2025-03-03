import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Logger:
    """Class for setting up logging."""
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)


class EnvLoader:
    """Class for loading environment variables."""
    
    @staticmethod
    def load_env_file(env_file: str = ".env") -> None:
        """Loads environment variables from .env file."""
        env_path = Path(__file__).resolve().parent.parent / env_file
        load_dotenv(env_path)


class EnvVariableManager:
    """Class for getting environment variables."""

    logger = Logger.get_logger(__name__)

    @staticmethod
    def get_env_variable(variable_name: str) -> str:
        """
        Get the value of an environment variable.
        """
        try:
            value = os.environ[variable_name]
            EnvVariableManager.logger.info(f"Retrieved variable {variable_name}")
            return value
        except KeyError:
            error_msg = f"Please set the environment variable {variable_name}"
            EnvVariableManager.logger.error(error_msg)
            raise KeyError({"error": error_msg})


class Settings(BaseSettings):
    """
    Settings class for loading environment variables and database URLs.
    """

    EnvLoader.load_env_file()

    POSTGRES_USER: str = EnvVariableManager.get_env_variable("POSTGRES_USER")
    POSTGRES_PASSWORD: str = EnvVariableManager.get_env_variable("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = EnvVariableManager.get_env_variable("POSTGRES_HOST")
    POSTGRES_PORT: str = EnvVariableManager.get_env_variable("POSTGRES_PORT")
    POSTGRES_DB: str = EnvVariableManager.get_env_variable("POSTGRES_DB")
    WIKI_URL: str = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
logger = Logger.get_logger(__name__)
