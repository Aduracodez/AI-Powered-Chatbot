#!/usr/bin/env python3
"""
Python wrapper to fix WEB_CONCURRENCY issue before importing gunicorn
"""
import os
import sys

# Fix WEB_CONCURRENCY if it's set to empty string BEFORE importing gunicorn
if os.environ.get("WEB_CONCURRENCY") == "":
    del os.environ["WEB_CONCURRENCY"]

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

