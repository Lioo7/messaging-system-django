#!/bin/bash

# Apply database migrations
python manage.py migrate

# Load environment variables
set -a
. /code/.env
set +a

# Create superuser if not already exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
      User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
      User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell

# Start Django server
exec "$@"
