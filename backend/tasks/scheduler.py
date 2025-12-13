import asyncio
import logging
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..services.weather_service import WeatherService

HUNGARIAN_CITIES = [
    "Budapest",
    "Békéscsaba",
    "Debrecen",
    "Eger",
    "Győr",
    "Kaposvár",
    "Kecskemét",
    "Miskolc",
    "Nyíregyháza",
    "Pécs",
    "Salgótarján",
    "Szeged",
    "Szekszárd",
    "Székesfehérvár",
    "Szolnok",
    "Szombathely",
    "Tatabánya",
    "Veszprém",
    "Zalaegerszeg",
]
logger = logging.getLogger("uvicorn")


async def update_weather_periodically():

    logger.info("Background Scheduler Initialized.")
    while True:
        logger.info("--- Starting Scheduled Weather Update (Hourly) ---")
        db: Session = SessionLocal()
        service = WeatherService(db)
        try:
            for city in HUNGARIAN_CITIES:
                try:
                    # Run blocking synchronous code in a thread to verify the main loop isn't blocked
                    raw_data = await asyncio.to_thread(service.fetch_weather_data, city)
                    if raw_data:
                        await asyncio.to_thread(service.save_weather_data, raw_data, city)
                        logger.info(f"Auto-saved: {city}")
                    else:
                        logger.warning(f"Failed to fetch: {city}")
                except Exception as inner_e:
                    logger.error(f"Error processing {city}: {inner_e}")
                
                # Short pause between cities
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Critical Scheduler Error: {e}")
        finally:
            db.close()
        
        logger.info("--- Update Cycle Finished. Next run in 5 minutes. ---")
        await asyncio.sleep(300)
