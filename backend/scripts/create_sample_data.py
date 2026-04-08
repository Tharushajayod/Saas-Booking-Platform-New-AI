import os
import sys
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from apps.tenants.models import Tenant, Owner
from apps.properties.models import Property, Room

User = get_user_model()

def run():
    # Use existing admin user as owner
    admin_email = 'admin@example.com'
    try:
        user = User.objects.get(email=admin_email)
    except User.DoesNotExist:
        print('Admin user not found, aborting')
        return

    tenant, _ = Tenant.objects.get_or_create(subdomain='demo', defaults={'name': 'Demo Tenant'})
    owner, _ = Owner.objects.get_or_create(tenant=tenant, user=user)

    prop, created = Property.objects.get_or_create(
        tenant=tenant,
        owner=owner,
        name='Seaside Villa',
        defaults={
            'description': 'Lovely villa by the sea',
            'short_description': 'Seaside villa',
            'property_type': 'villa',
            'address': 'Beach Road',
            'city': 'Galle',
            'country': 'Sri Lanka',
            'is_published': True,
            'cover_image_url': '',
        }
    )

    room, _ = Room.objects.get_or_create(
        tenant=tenant,
        property=prop,
        name='Ocean View Suite',
        defaults={
            'description': 'Spacious suite with ocean view',
            'capacity': 4,
            'beds': 2,
            'bathrooms': 1.0,
            'base_price_lkr': 15000.00,
            'is_available': True,
        }
    )

    print('Sample data created: tenant=%s property=%s room=%s' % (tenant.subdomain, prop.name, room.name))

if __name__ == '__main__':
    run()
