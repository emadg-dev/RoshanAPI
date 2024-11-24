#!/bin/bash

echo "make database migrations"
python manage.py makemigrations

echo "apply database migrations"
python manage.py migrate

echo "Starting server"
exec python manage.py runserver 0.0.0.0:8000

exec "$@"