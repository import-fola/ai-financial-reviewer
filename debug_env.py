
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print the environment variables
print("GOOGLE_CLIENT_ID:", os.environ.get("GOOGLE_CLIENT_ID"))
print("GOOGLE_CLIENT_SECRET:", os.environ.get("GOOGLE_CLIENT_SECRET"))
print("GOOGLE_REDIRECT_URI:", os.environ.get("GOOGLE_REDIRECT_URI"))
