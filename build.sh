#!/usr/bin/env bash
set -o errexit

# Install whatever is in the text file
pip install -r requirements.txt

# FORCE install the Render production dependencies
pip install dj-database-url whitenoise "uvicorn[standard]"

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput || true