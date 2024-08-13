#!/bin/bash

# Collect static files
python manage.py collectstatic --no-input

# Run server with TLS/HTTPS enabled
# python manage.py runserver_plus 0.0.0.0:443 --cert-file /backend/ssl/django.crt --key-file /backend/ssl/django.key
uvicorn backend.asgi:application --host 0.0.0.0 --port 8000