import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def booking_url():
    return f"{BASE_URL}/booking"

@pytest.fixture(scope="session")
def token():
    auth_resp = requests.post(
        f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"}
    )
    return auth_resp.json().get("token")

def create_booking():
    payload = {
        "firstname": "Retrieve",
        "lastname": "Test",
        "totalprice": 99,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-05-01", "checkout": "2025-05-05"},
        "additionalneeds": "None"
    }
    resp = requests.post(f"{BASE_URL}/booking", json=payload)
    return resp.json()["bookingid"], payload

def test_retrieve_existing_booking(booking_url):
    booking_id, payload = create_booking()
    resp = requests.get(f"{booking_url}/{booking_id}")
    assert resp.status_code == 200
    for key in payload:
        assert key in resp.json()

def test_retrieve_nonexistent_booking(booking_url):
    resp = requests.get(f"{booking_url}/999999")
    assert resp.status_code == 404