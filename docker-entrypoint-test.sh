#!/bin/bash
# docker-entrypoint-test.sh

# Run migrations (to ensure the test database is up-to-date)
echo "Running migrations..."
python manage.py migrate --noinput

# Run tests
echo "Running tests..."
python manage.py test

