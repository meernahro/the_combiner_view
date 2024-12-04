#!/bin/bash

# Create data directory if it doesn't exist
mkdir -p /app/data

# Wait for a few seconds to ensure the container is fully started
sleep 2

# Check if database exists
if [ ! -f "data/db.sqlite3" ]; then
    echo "Database does not exist, creating..."
    
    # Run migrations
    python manage.py makemigrations
    python manage.py makemigrations trading
    python manage.py migrate

    # Create superuser
    python manage.py shell << END
from django.contrib.auth.models import User
from django.db import IntegrityError
import os

try:
    username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    
    if not username or not password:
        print('Superuser environment variables not set')
        exit(1)
        
    User.objects.create_superuser(username=username, 
                                password=password,
                                email=email)
    print('Superuser created successfully')
except IntegrityError:
    print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {str(e)}')
END
fi

# Start Daphne
exec daphne -b 0.0.0.0 -p 7999 the_combiner_view.asgi:application 