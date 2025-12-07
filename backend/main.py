import asyncio
from fastapi import FastAPI
from .db.database import Base, engine
from .api.weather_routes import router
from .tasks.scheduler import update_weather_periodically

app = FastAPI(title="Weather App Backend")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_weather_periodically())


Base.metadata.create_all(bind=engine)
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Weather Backend is running!"}
