import requests
from sqlalchemy.orm import Session
from ..config.settings import settings
from ..models.weather_model import Weather
from ..schemas.weather_schema import WeatherCreate


class WeatherService:

    def __init__(self, db: Session):
        self.db = db
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_BASE_URL

    def fetch_weather_data(self, city: str):

        url = f"{self.base_url}/current.json"
        params = {"key": self.api_key, "q": city}
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            raw_data = response.json()
            if "error" in raw_data:
                return None
            return raw_data
        except requests.exceptions.RequestException as e:
            print(f"API Hiba: {e}")
            return None

    def save_weather_data(self, data: dict, city: str):

        current = data.get("current", {})
        weather_data = WeatherCreate(
            city=city,
            temperature_c=current.get("temp_c"),
            description=current.get("condition", {}).get("text"),
            humidity=current.get("humidity"),
            wind_kph=current.get("wind_kph"),
        )
        db_weather = Weather(**weather_data.model_dump())
        self.db.add(db_weather)
        self.db.commit()
        self.db.refresh(db_weather)
        return db_weather
