import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Voltage Calculator" in response.data


def test_post_valid_values(client):
    response = client.post("/", data={"current": "2", "resistance": "10"})
    assert response.status_code == 200
    assert b"Voltage: 20 V" in response.data
    assert b"voltageChart" in response.data


def test_post_negative_resistance_shows_error(client):
    response = client.post("/", data={"current": "2", "resistance": "-10"})
    assert response.status_code == 200
    assert b"Error:" in response.data
    assert b"Resistance cannot be negative" in response.data


def test_post_non_numeric_shows_error(client):
    response = client.post("/", data={"current": "abc", "resistance": "10"})
    assert response.status_code == 200
    assert b"Error:" in response.data


def test_post_negative_current_allowed(client):
    response = client.post("/", data={"current": "-2", "resistance": "10"})
    assert response.status_code == 200
    assert b"Voltage: -20 V" in response.data
