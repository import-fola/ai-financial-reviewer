"""
Authentication and Google OAuth utilities for AI Financial Reviewer.
"""

import os
from urllib.parse import urlencode
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import base64
import json
from cryptography.fernet import Fernet
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "openid", "email", "profile"]

# In-memory token store for demonstration (replace with DB in production)
_token_store = {}
# AES-256 key for Fernet (should be in env var in production)
FERNET_KEY = os.environ.get("FERNET_KEY") or Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

def get_google_auth_url():
    """Return the Google OAuth URL for user sign-in."""
    print(f"DEBUG - REDIRECT_URI: {REDIRECT_URI}")
    print(f"DEBUG - CLIENT_ID: {CLIENT_ID}")
    print(f"DEBUG - CLIENT_SECRET: {CLIENT_SECRET and 'SET' or 'NOT SET'}")
    
    if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        raise ValueError("Missing OAuth credentials. Check your .env file.")
        
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    return auth_url

def exchange_code_for_tokens(auth_code):
    """Exchange auth code for access and refresh tokens."""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    flow.fetch_token(code=auth_code)
    credentials = flow.credentials
    # Verify ID token
    idinfo = id_token.verify_oauth2_token(
        credentials.id_token, google_requests.Request(), CLIENT_ID
    )
    user_info = {
        "email": idinfo.get("email"),
        "name": idinfo.get("name"),
        "picture": idinfo.get("picture"),
        "tokens": {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "id_token": credentials.id_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        },
    }
    # TODO: store_tokens_securely(user_info["email"], user_info["tokens"])
    return user_info

def verify_id_token(id_token_str):
    """Verify the Google ID token and return user info if valid, else raise ValueError."""
    try:
        idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), CLIENT_ID)
        return {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "picture": idinfo.get("picture"),
            "sub": idinfo.get("sub"),
        }
    except Exception as e:
        raise ValueError(f"Invalid or expired ID token: {e}")

def store_tokens_securely(user_id, tokens):
    """Encrypt and store tokens securely (AES-256)."""
    data = json.dumps(tokens).encode()
    encrypted = fernet.encrypt(data)
    _token_store[user_id] = encrypted

def get_tokens(user_id):
    """Retrieve and decrypt tokens for a user."""
    encrypted = _token_store.get(user_id)
    if not encrypted:
        return None
    data = fernet.decrypt(encrypted)
    return json.loads(data)

def refresh_access_token(refresh_token):
    """Refresh the access token using the refresh token."""
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES,
    )
    creds.refresh(GoogleRequest())
    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "id_token": creds.id_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    } 