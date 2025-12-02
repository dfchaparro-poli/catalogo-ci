# tests/test_api_endpoints.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_countries_list():
    response = client.get("/countries")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first = data[0]
    assert "id" in first and "name" in first

def test_get_movies_list():
    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        first = data[0]
        assert "id" in first
        assert "title" in first
        assert "year" in first
        assert "country" in first
        country = first["country"]
        assert "id" in country and "name" in country

def test_get_series_list():
    response = client.get("/series")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        s = data[0]
        assert "id" in s
        assert "title" in s
        assert "year" in s
        assert "country" in s
        assert "seasons" in s
        assert isinstance(s["seasons"], list)

def test_get_games_list():
    response = client.get("/games")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        g = data[0]
        assert "id" in g
        assert "title" in g
        assert "year" in g
        assert "country" in g
        assert "publisher" in g

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert json_data["status"] == "ok"
