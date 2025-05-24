import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)

@patch("src.main.verify_id_token")
def test_protected_route_valid_token(mock_verify):
    mock_verify.return_value = {"email": "user@example.com", "name": "Test User"}
    headers = {"Authorization": "Bearer valid_token"}
    resp = client.get("/protected", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["user"]["email"] == "user@example.com"
    assert data["message"] == "Authenticated!"

@patch("src.main.verify_id_token")
def test_protected_route_missing_token(mock_verify):
    resp = client.get("/protected")
    assert resp.status_code == 401
    assert "Missing or invalid Authorization header" in resp.text

@patch("src.main.verify_id_token", side_effect=ValueError("expired"))
def test_protected_route_expired_token(mock_verify):
    headers = {"Authorization": "Bearer expired_token"}
    resp = client.get("/protected", headers=headers)
    assert resp.status_code == 401
    assert "expired" in resp.text 