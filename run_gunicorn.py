#!/usr/bin/env python3
"""
Permanent fix for Railway environment variable issues with Gunicorn.
Railway sets empty strings for env vars which cause Gunicorn's int() conversions to fail.
This wrapper patches os.environ.get() to return None for empty strings BEFORE Gunicorn imports.
"""
import os
import sys

# Store original os.environ.get
_original_environ_get = os.environ.get

def safe_environ_get(key, default=None):
    """
    Wrapper that converts empty strings to None for numeric environment variables.
    This prevents Gunicorn from trying to convert empty strings to integers.
    """
    value = _original_environ_get(key, default)
    
    # If value is empty string and default is None, return None
    # This allows Gunicorn's int() conversions to work properly
    if value == "":
        # For known numeric variables, return None so Gunicorn uses its defaults
        numeric_vars = ["WEB_CONCURRENCY", "GUNICORN_PID", "WORKERS", "THREADS"]
        if key in numeric_vars:
            return None
        # For other vars, return empty string as-is
        return ""
    
    return value

# Also clean up any existing empty string values in known problematic vars
# Do this BEFORE patching, using original environ.get
for var in ["WEB_CONCURRENCY", "GUNICORN_PID"]:
    if _original_environ_get(var) == "":
        os.environ.pop(var, None)

# Patch os.environ.get BEFORE importing gunicorn
# This ensures Gunicorn never sees empty strings for numeric vars
os.environ.get = safe_environ_get

# Now import and run gunicorn - it will use our patched environ.get
from gunicorn.app.wsgiapp import run

if __name__ == "__main__":
    sys.argv = [
        "gunicorn",
        "--bind", f"0.0.0.0:{os.environ.get('PORT', '5000')}",
        "--workers", "2",
        "--threads", "2",
        "--timeout", "120",
        "wsgi:app"
    ]
    sys.exit(run())

