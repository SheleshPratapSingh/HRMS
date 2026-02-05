#!/bin/bash
set -e

echo "Starting Django application..."

cd /app/backend

python manage.py makemigrations --noinput
python manage.py migrate --noinput

python manage.py collectstatic --noinput --clear

gunicorn hrms.wsgi:application --bind 0.0.0.0:8001 --workers 3 --timeout 120
