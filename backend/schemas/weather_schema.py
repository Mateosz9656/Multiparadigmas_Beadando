from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WeatherBase(BaseModel):
    city: str
    temperature_c: float
    description: str
    humidity: int
    wind_kph: float


class WeatherCreate(WeatherBase):
    pass


class WeatherResponse(WeatherBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
