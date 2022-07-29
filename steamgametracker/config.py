from pydantic import BaseSettings


class Settings(BaseSettings):
    STEAM_API_KEY: str
    DEBUG = False
    PORT = 3030

    class Config:
        env_file = ".env"


settings = Settings()
