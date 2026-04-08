import os
import sys
from pathlib import Path

# Ensure project root on sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, PROJECT_ROOT)

from django import setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
setup()
from django.contrib.auth import get_user_model
from apps.tenants.models import Owner, Tenant
User = get_user_model()
print('Users:', User.objects.count())
print('Owners:', Owner.objects.count())
if Owner.objects.exists():
    owner = Owner.objects.first()
    print('First owner user:', owner.user.email)
    print('Owner tenant:', owner.tenant.name, owner.tenant.id)
else:
    print('No owner entries')
