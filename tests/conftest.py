import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_url():
    return f"{BASE_URL}/auth"

@pytest.fixture(scope="session")
def booking_url():
    return f"{BASE_URL}/booking"

@pytest.fixture(scope="session")
def token(auth_url):
    creds = {"username": "admin", "password": "password123"}
    response = requests.post(auth_url, json=creds)
    assert response.status_code == 200, f"Auth failed: {response.status_code}"
    data = response.json()
    assert "token" in data and data["token"], "No token found"
    return data["token"]
