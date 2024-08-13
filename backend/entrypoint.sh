#!/bin/bash

# Export project requirements to text file
/backend/scripts/export_project_requirements.sh
# Export file structure to text file
/backend/scripts/export_project_structure.sh

# Apply database migrations
python manage.py migrate
python manage.py migrate_spotify_history_functions

# Generate admin scripts (for use in admin portal)
python manage.py admin_generator spotify_history > /backend/spotify_history/admin.py
python manage.py admin_generator users > /backend/users/admin.py

# create a superuser if it doesn't already exist
python manage.py create_admin
# Continue with the usual Django entrypoint command
exec "$@"
