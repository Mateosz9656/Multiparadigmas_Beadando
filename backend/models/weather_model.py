from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..db.database import Base


class Weather(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    city = Column(String, index=True)
    temperature_c = Column(Float)
    description = Column(String)
    humidity = Column(Integer)
    wind_kph = Column(Float)
