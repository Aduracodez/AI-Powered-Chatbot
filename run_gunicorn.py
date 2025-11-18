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
    Wrapper that converts empty strings to None/default for ANY variable.
    This prevents Gunicorn from trying to convert empty strings to integers.
    If default is numeric (int or numeric string), empty strings become None.
    """
    value = _original_environ_get(key, default)
    
    # If value is empty string, handle it intelligently
    if value == "":
        # If default is provided and looks numeric, return None (so default is used)
        # This handles cases like int(os.environ.get('VAR', 0)) where default is numeric
        if default is not None:
            # Check if default is numeric (int, or string that looks like a number)
            try:
                int(default)
                # Default is numeric, so return None to use the default
                return None
            except (ValueError, TypeError):
                # Default is not numeric, return empty string
                return ""
        
        # Known problematic variables that Gunicorn converts to int without defaults
        problematic_vars = ["WEB_CONCURRENCY", "GUNICORN_PID", "LISTEN_FDS", "WORKERS", "THREADS"]
        if key in problematic_vars:
            # For GUNICORN_PID, always return None (Gunicorn sets it itself)
            if key == "GUNICORN_PID":
                return None
            # For others, return None so Gunicorn uses its internal defaults
            return None
        
        # For unknown vars with no default, return empty string
        return ""
    
    return value

# AGGRESSIVE FIX: Remove ALL empty string environment variables
# Railway sets many empty strings which cause Gunicorn to crash
# Better to remove them all than try to handle each one
empty_vars = [key for key, value in os.environ.items() if value == ""]
for var in empty_vars:
    os.environ.pop(var, None)
if empty_vars:
    print(f"Removed {len(empty_vars)} empty environment variables: {', '.join(empty_vars[:10])}...")

# Patch os.environ.get BEFORE importing gunicorn
# This ensures Gunicorn never sees empty strings for numeric vars
# (as a backup in case Railway sets new ones after cleanup)
os.environ.get = safe_environ_get

# Now import and run gunicorn - it will use our patched environ.get
from gunicorn.app.wsgiapp import run

if __name__ == "__main__":
    sys.argv = [
        "gunicorn",
        "--bind", f"0.0.0.0:{os.environ.get('PORT', '5050')}",
        "--workers", "2",
        "--threads", "2",
        "--timeout", "120",
        "wsgi:app"
    ]
    sys.exit(run())

