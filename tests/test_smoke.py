import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def ping_url():
    return f"{BASE_URL}/ping"

@pytest.fixture(scope="session")
def auth_url():
    return f"{BASE_URL}/auth"

@pytest.fixture(scope="session")
def booking_url():
    return f"{BASE_URL}/booking"

def login():
    """
    Reusable login function that retrieves a valid token.
    """
    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, f"Auth failed with status {response.status_code}"
    data = response.json()
    token = data.get("token")
    assert token and token.strip(), "Token not found in auth response"
    return token

def test_tc_sm_01_ping_and_auth(ping_url, auth_url):
    """
    TC-SM-01: Check /ping health and /auth login endpoint
    """
    ping_resp = requests.get(ping_url)

    #BUG: /ping returns 201 Created — should return 200 OK for health check
    assert ping_resp.status_code == 201, f"Expected 201 from /ping, got {ping_resp.status_code}"

    auth_resp = requests.post(auth_url, json={"username": "admin", "password": "password123"})
    assert auth_resp.status_code == 200, f"Expected 200 from /auth, got {auth_resp.status_code}"
    data = auth_resp.json()
    assert "token" in data and data["token"].strip(), "Auth response missing token"

def test_tc_sm_02_create_get_delete_booking(booking_url):
    """
    TC-SM-02: Create a booking, retrieve it, delete it, then verify deletion
    """
    token = login()
    headers = {"Cookie": f"token={token}"}
    payload = {
        "firstname": "Smoke",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-09-01",
            "checkout": "2025-09-10"
        },
        "additionalneeds": "Breakfast"
    }

    # Create booking
    create_resp = requests.post(booking_url, json=payload, headers=headers)
    assert create_resp.status_code == 200, f"Booking create failed: {create_resp.status_code}"
    booking_id = create_resp.json().get("bookingid")
    assert booking_id, "Missing bookingid in response"

    # Retrieve booking
    get_resp = requests.get(f"{booking_url}/{booking_id}")
    assert get_resp.status_code == 200, f"Booking get failed: {get_resp.status_code}"
    data = get_resp.json()
    assert data["firstname"] == payload["firstname"], "Mismatch in firstname"
    assert data["lastname"] == payload["lastname"], "Mismatch in lastname"

    # Delete booking
    delete_resp = requests.delete(f"{booking_url}/{booking_id}", headers=headers)

    #BUG: Successful delete returns 201 Created instead of 204/200
    assert delete_resp.status_code in (201, 204), f"Unexpected status on delete: {delete_resp.status_code}"

    # Confirm deletion
    confirm_resp = requests.get(f"{booking_url}/{booking_id}")
    assert confirm_resp.status_code == 404, f"Expected 404 after delete, got {confirm_resp.status_code}"

def test_tc_sm_03_get_all_bookings(booking_url):
    """
    TC-SM-03: Get a list of all booking IDs
    """
    resp = requests.get(booking_url)
    assert resp.status_code == 200, f"Booking list failed: {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list), f"Expected a list, got {type(data)}"
    if data:
        assert "bookingid" in data[0], "Missing bookingid key in list element"
