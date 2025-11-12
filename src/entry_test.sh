#!/bin/bash
set -e

# configuration from env vars
PROJECT_NAME=${DJANGO_PROJECT_NAME:-project}
WORKERS=${WORKERS:-1}
PORT=${PORT:-8080}

echo "Waiting for PostgreSQL to be ready ..."
while ! nc -z django_db_test 5432; do
  sleep 0.1
done

if [ ! -f "$PROJECT_NAME/settings.py" ]; then
  echo "No Django project found, exiting."
  exit 1
fi

echo "Running Migrations ..."
python manage.py migrate --noinput

echo "Running tests ..."
pytest -v
