import os
import sys
from pathlib import Path

# Ensure project root on sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
from django import setup
setup()

from apps.properties.models import Property, Room

prop = Property.objects.first()
if not prop:
    print('No property found')
else:
    room, created = Room.objects.get_or_create(
        property=prop,
        tenant=prop.tenant,
        name='Room 1',
        defaults={
            'description': 'First room',
            'room_type': 'double',
            'capacity': 2,
            'beds': 1,
            'bathrooms': 1,
            'base_price_lkr': 15000.00,
            'is_available': True
        }
    )
    print('Room created' if created else 'Room exists', room.id)
