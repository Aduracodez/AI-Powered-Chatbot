#!/usr/bin/env python3
"""
Python wrapper to fix Railway environment variable issues before importing gunicorn
Railway sets empty strings for various env vars which cause Gunicorn to crash
"""
import os
import sys

# Fix all problematic environment variables BEFORE importing gunicorn
# Railway sets these to empty strings which cause int() conversion errors

def fix_env_var(name, default_value):
    """Fix an environment variable if it's empty or invalid"""
    value = os.environ.get(name)
    if value == "" or value is None:
        os.environ[name] = default_value
    elif name in ["WEB_CONCURRENCY", "GUNICORN_PID"] and not value.isdigit():
        # For numeric vars, ensure they're valid numbers
        os.environ[name] = default_value

# Fix all known problematic variables
fix_env_var("WEB_CONCURRENCY", "1")
fix_env_var("GUNICORN_PID", "")  # Unset if empty, Gunicorn will set it itself

# Remove GUNICORN_PID if it's empty (Gunicorn will set it when needed)
if os.environ.get("GUNICORN_PID") == "":
    os.environ.pop("GUNICORN_PID", None)

# Now import and run gunicorn
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

