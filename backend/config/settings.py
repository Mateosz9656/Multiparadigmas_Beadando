from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WEATHER_API_KEY: str
    DATABASE_URL: str = "sqlite:///./weather.db"
    WEATHER_API_BASE_URL: str = "http://api.weatherapi.com/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
