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


def test_resistance_series(client):
    response = client.post("/resistance", json={"resistances": [10, 20, 30], "mode": "series"})
    assert response.status_code == 200
    assert response.get_json() == {"result": 60, "error": None}


def test_resistance_parallel(client):
    response = client.post("/resistance", json={"resistances": [10, 10], "mode": "parallel"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["error"] is None
    assert data["result"] == pytest.approx(5)


def test_resistance_parallel_with_zero(client):
    response = client.post("/resistance", json={"resistances": [0, 10, 20], "mode": "parallel"})
    assert response.status_code == 200
    assert response.get_json() == {"result": 0, "error": None}


def test_resistance_empty_list_shows_error(client):
    response = client.post("/resistance", json={"resistances": [], "mode": "series"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] is None
    assert data["error"] is not None


def test_resistance_negative_value_shows_error(client):
    response = client.post("/resistance", json={"resistances": [10, -5], "mode": "series"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] is None
    assert "negative" in data["error"].lower()


def test_resistance_non_numeric_value_shows_error(client):
    response = client.post("/resistance", json={"resistances": [10, "abc"], "mode": "parallel"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] is None
    assert data["error"] is not None


def test_resistance_unknown_mode_shows_error(client):
    response = client.post("/resistance", json={"resistances": [10, 20], "mode": "bogus"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] is None
    assert data["error"] is not None
