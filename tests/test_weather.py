import pytest
import requests
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.db.database import Base, get_db
from backend.models.weather_model import Weather

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False)


@pytest.fixture(scope="session")
def engine():

    return create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )


@pytest.fixture(scope="session")
def setup_db(engine):

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(engine, setup_db):

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):

    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_read_main(client):

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Weather Backend is running!"}


@pytest.mark.parametrize("invalid_id", [9999, 10000, 10001])
def test_get_detail_not_found(client, invalid_id: int):

    response = client.get(f"/weather/{invalid_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Weather data with ID {invalid_id} not found"}


def test_fetch_invalid_city(client, monkeypatch):

    def mock_requests_get(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "error": {"code": 1006, "message": "No matching location found."}
                }

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_requests_get)
    response = client.post("/weather/fetch/invalid-city-name-123")
    assert response.status_code == 400
    assert "Failed to fetch valid weather data" in response.json()["detail"]


def test_successful_fetch_and_list(client, monkeypatch):

    test_city = "Eger"

    def mock_requests_get_success(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "location": {"name": test_city},
                    "current": {
                        "temp_c": 15.0,
                        "condition": {"text": "Sunny"},
                        "humidity": 60,
                        "wind_kph": 10.0,
                    },
                }

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_requests_get_success)
    post_response = client.post(f"/weather/fetch/{test_city}")
    assert post_response.status_code == 200
    get_response = client.get(f"/weather/list/{test_city}")
    assert get_response.status_code == 200
    assert len(get_response.json()) >= 1
    assert get_response.json()[0]["city"] == test_city


def test_create_and_read_data(client):

    test_city = "Debrecen"
    initial_response = client.get(f"/weather/list/{test_city}")
    assert initial_response.status_code == 404
