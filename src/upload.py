"""
File upload, validation, and queue management for AI Financial Reviewer.
"""

# Placeholder imports
# import streamlit, etc.

ALLOWED_EXTENSIONS = {'.csv', '.pdf', '.png', '.jpg', '.jpeg'}
MAX_FILE_SIZE_MB = 10


def validate_file(file):
    """Validate file size and type. Return (is_valid, error_message)."""
    pass

def add_to_upload_queue(file, user_id):
    """Add a validated file to the user's upload queue."""
    pass

def get_upload_queue(user_id):
    """Return the current upload queue for the user."""
    pass 