#!/bin/sh

# Ensure that the password is set
if [ -z "$REDIS_PASSWORD" ]; then
  echo "Error: REDIS_PASSWORD environment variable is not set."
  exit 1
fi

# Start Redis with SSL/TLS configuration
exec redis-server --requirepass "$REDIS_PASSWORD" \
                  --tls-port "$REDIS_PORT"
                #   --tls-cert-file /etc/ssl/shared.crt \
                #   --tls-key-file /etc/ssl/shared.key \
                #   --tls-ca-cert-file /etc/ssl/shared.crt
