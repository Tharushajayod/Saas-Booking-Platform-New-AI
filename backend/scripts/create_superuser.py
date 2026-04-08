import os
import sys
from pathlib import Path

# Ensure the project root (backend) is on sys.path so Django settings import works
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass')
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print('Superuser created:', email)
else:
    print('Superuser already exists:', email)
