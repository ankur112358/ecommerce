#!/bin/bash

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files (optional, for production setups)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start the Gunicorn server
echo "Starting Gunicorn..."
exec gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
