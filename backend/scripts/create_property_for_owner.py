import os
import sys
from pathlib import Path

# Ensure project root on sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
from django import setup
setup()

from apps.tenants.models import Owner
from apps.properties.models import Property

owner = Owner.objects.first()
if owner is None:
    print('No owner found')
else:
    prop, created = Property.objects.get_or_create(
        name='Auto Property',
        tenant=owner.tenant,
        owner=owner,
        defaults={
            'description': 'Auto-created property',
            'short_description': 'Auto prop',
            'property_type': 'villa',
            'address': 'Auto Address',
            'city': 'Colombo',
            'country': 'Sri Lanka',
            'is_published': True,
        }
    )
    print('Property created' if created else 'Property exists', prop.id)
