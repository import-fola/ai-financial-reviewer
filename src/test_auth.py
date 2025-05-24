import pytest
from src import auth
import os
import json
from unittest.mock import patch

@pytest.fixture
def fake_tokens():
    return {
        "access_token": "test_access",
        "refresh_token": "test_refresh",
        "id_token": "test_id",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "scopes": ["openid", "email"]
    }

def test_store_and_get_tokens(fake_tokens):
    user_id = "user@example.com"
    auth.store_tokens_securely(user_id, fake_tokens)
    retrieved = auth.get_tokens(user_id)
    assert retrieved == fake_tokens

def test_verify_id_token_valid():
    with patch("src.auth.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = {"email": "user@example.com", "name": "Test User", "picture": "pic.png", "sub": "123"}
        info = auth.verify_id_token("valid_token")
        assert info["email"] == "user@example.com"
        assert info["name"] == "Test User"
        assert info["picture"] == "pic.png"
        assert info["sub"] == "123"

def test_verify_id_token_invalid():
    with patch("src.auth.id_token.verify_oauth2_token", side_effect=Exception("bad token")):
        with pytest.raises(ValueError):
            auth.verify_id_token("invalid_token")

def test_refresh_access_token():
    with patch("src.auth.Credentials") as mock_creds:
        instance = mock_creds.return_value
        instance.token = "new_access"
        instance.refresh_token = "new_refresh"
        instance.id_token = "new_id"
        instance.token_uri = "uri"
        instance.client_id = "cid"
        instance.client_secret = "csecret"
        instance.scopes = ["openid"]
        with patch.object(instance, "refresh") as mock_refresh:
            result = auth.refresh_access_token("refresh_token")
            assert result["access_token"] == "new_access"
            assert result["refresh_token"] == "new_refresh"
            assert result["id_token"] == "new_id" 