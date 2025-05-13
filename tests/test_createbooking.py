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

def test_create_booking_valid(booking_url, token):
    payload = {
        "firstname": "Salih",
        "lastname": "Buro",
        "totalprice": 250,  #BUG: Floating point values in 'totalprice' lose precision when saved
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-06-01", "checkout": "2025-06-07"},
        "additionalneeds": "Breakfast"
    }
    headers = {"Cookie": f"token={token}"}
    resp = requests.post(booking_url, json=payload, headers=headers)

    #BUG: Invalid checkin/checkout dates are not accepted, but response is 200 OK instead of 400 Bad Request
    assert resp.status_code == 200
    data = resp.json()
    assert "bookingid" in data

@pytest.mark.parametrize("missing_field", ["firstname", "lastname", "totalprice"])
def test_create_booking_missing_required_field(booking_url, missing_field):
    base_payload = {
        "firstname": "Name",
        "lastname": "Smith",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-06-01", "checkout": "2025-06-07"},
        "additionalneeds": "Wi-Fi"
    }
    del base_payload[missing_field]
    resp = requests.post(booking_url, json=base_payload)
    assert resp.status_code == 500
