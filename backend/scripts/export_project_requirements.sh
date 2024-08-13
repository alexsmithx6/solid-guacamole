#!/bin/bash

# File path for exported requirements file
EXPORT_FILE="/backend/requirements.exported.txt"

# Export the project requirements to text file
python -m pip freeze > $EXPORT_FILE

# Apply all permissions for file to be exported
chmod 777 $EXPORT_FILE

# Notification of completion
echo "Project Python requirements have been written to $EXPORT_FILE"
