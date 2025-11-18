#!/bin/bash
# Production startup script for Railway/Heroku
# Fixes WEB_CONCURRENCY empty string issue

# Unset WEB_CONCURRENCY if it's empty or not set
if [ -z "$WEB_CONCURRENCY" ] || [ "$WEB_CONCURRENCY" = "" ]; then
    unset WEB_CONCURRENCY
fi

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 wsgi:app

