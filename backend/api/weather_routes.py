from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..services.weather_service import WeatherService
from ..models.weather_model import Weather
from ..schemas.weather_schema import WeatherResponse

router = APIRouter(prefix="/weather", tags=["Weather"])


def get_weather_service(db: Session = Depends(get_db)):
    return WeatherService(db)


@router.post("/fetch/{city}", response_model=WeatherResponse)
def fetch_and_save_weather(
    city: str, service: WeatherService = Depends(get_weather_service)
):

    raw_data = service.fetch_weather_data(city)
    if raw_data is None:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch valid weather data for {city}. Reason: Invalid city name or API error.",
        )
    db_data = service.save_weather_data(raw_data, city)
    return db_data


@router.get("/history", response_model=List[WeatherResponse])
def get_all_weather_history(db: Session = Depends(get_db)):

    return db.query(Weather).all()


@router.get("/list/{city}", response_model=List[WeatherResponse])
def get_weather_history(city: str, db: Session = Depends(get_db)):

    history = db.query(Weather).filter(Weather.city == city).all()
    if not history:
        raise HTTPException(
            status_code=404, detail=f"No weather history found for {city}"
        )
    return history


@router.get("/{data_id}", response_model=WeatherResponse)
def get_weather_detail(data_id: int, db: Session = Depends(get_db)):

    data = db.query(Weather).filter(Weather.id == data_id).first()
    if data is None:
        raise HTTPException(
            status_code=404, detail=f"Weather data with ID {data_id} not found"
        )
    return data
