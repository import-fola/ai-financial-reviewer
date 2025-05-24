"""
Observability: structured logging and Sentry integration for AI Financial Reviewer.
"""

# Placeholder imports
# import sentry_sdk, logging, etc.

def init_logging():
    """Initialize structured JSON logging."""
    pass

def log_event(stage, file_id, duration_ms, status, level="INFO", extra=None):
    """Log a structured event for a pipeline step."""
    pass

def init_sentry(dsn, environment):
    """Initialize Sentry error tracking."""
    pass

def capture_exception(exc):
    """Capture an exception and send to Sentry."""
    pass 