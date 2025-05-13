import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def token():
    auth_resp = requests.post(
        f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"}
    )
    return auth_resp.json().get("token")

@pytest.fixture(scope="session")
def booking_url():
    return f"{BASE_URL}/booking"

def create_booking(token):
    payload = {
        "firstname": "ToDelete",
        "lastname": "Me",
        "totalprice": 75,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-07-10", "checkout": "2025-07-15"},
        "additionalneeds": "None"
    }
    headers = {"Cookie": f"token={token}"}
    resp = requests.post(f"{BASE_URL}/booking", json=payload, headers=headers)
    return resp.json()["bookingid"]

def test_delete_existing_booking(booking_url, token):
    booking_id = create_booking(token)

    headers = {"Cookie": f"token={token}"}  #BUG: Authorization header does not work, only Cookie is accepted
    resp = requests.delete(f"{booking_url}/{booking_id}", headers=headers)

    #BUG: API returns 201 Created on successful delete — should return 200 OK or 204 No Content
    assert resp.status_code in [201, 204]

    resp_check = requests.get(f"{booking_url}/{booking_id}")
    assert resp_check.status_code == 404

def test_delete_invalid_id(booking_url, token):
    headers = {"Cookie": f"token={token}"}
    resp = requests.delete(f"{booking_url}/999999", headers=headers)

    #BUG: Deleting non-existent booking returns 405 Method Not Allowed — should be 404 Not Found
    assert resp.status_code in [404, 405]
