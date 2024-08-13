# backend/Dockerfile
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /backend

# Install system dependencies for psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file
COPY requirements.txt /backend/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project files
COPY . /backend/

# # Copy SSL certificates
# COPY ssl/django.crt /etc/ssl/certs/django.crt
# COPY ssl/django.key /etc/ssl/private/django.key

# Expose the port for HTTPS
EXPOSE 8000

# Use the custom script as the entrypoint
ENTRYPOINT ["/backend/entrypoint.sh"]

# Run the Django server
CMD ["/backend/start.sh"]
