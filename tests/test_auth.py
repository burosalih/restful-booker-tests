import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_url():
    return f"{BASE_URL}/auth"

def test_auth_valid_credentials(auth_url):
    payload = {"username": "admin", "password": "password123"}
    resp = requests.post(auth_url, json=payload)
    assert resp.status_code == 200
    assert "token" in resp.json()

@pytest.mark.parametrize("payload", [
    {"username": "wrong", "password": "password123"},
    {"username": "admin", "password": "wrongpass"},
    {"username": "", "password": ""},
    {},
])
def test_auth_invalid_credentials(auth_url, payload):
    resp = requests.post(auth_url, json=payload)
    assert resp.status_code == 200  # API still returns 200 for bad creds
    assert resp.json().get("reason") == "Bad credentials"