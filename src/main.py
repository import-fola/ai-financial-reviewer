from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.auth import get_google_auth_url, exchange_code_for_tokens, verify_id_token

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/auth/url")
def auth_url():
    """Return the Google OAuth URL for user sign-in."""
    try:
        url = get_google_auth_url()
        print(f"Generated auth URL: {url}")
        return {"auth_url": url}
    except Exception as e:
        print(f"Error generating auth URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/callback")
async def auth_callback(request: Request):
    """Handle OAuth callback, exchange code for tokens, return user info."""
    data = await request.json()
    auth_code = data.get("code")
    if not auth_code:
        raise HTTPException(status_code=400, detail="Missing auth code")
    user_info = exchange_code_for_tokens(auth_code)
    return JSONResponse(content=user_info)

# Dependency for authentication
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1]
    try:
        user = verify_id_token(token)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

# Example protected endpoint
@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    """A protected endpoint that requires a valid ID token."""
    return {"message": "Authenticated!", "user": user} 