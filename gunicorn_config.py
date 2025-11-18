"""
Gunicorn configuration file that fixes WEB_CONCURRENCY issue
"""
import os

# Fix WEB_CONCURRENCY if it's set to empty string
if os.environ.get("WEB_CONCURRENCY") == "":
    os.environ.pop("WEB_CONCURRENCY", None)

# Gunicorn config
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
workers = 2
threads = 2
timeout = 120
worker_class = "sync"

