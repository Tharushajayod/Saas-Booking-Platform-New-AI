import os
import sys
from pathlib import Path

# Ensure project root on sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
from django import setup
setup()

from apps.properties.models import Room
from apps.bookings.models import Guest, Booking
import uuid
from datetime import date

room = Room.objects.first()
if not room:
    print('No room found')
else:
    tenant = room.tenant
    guest = Guest.objects.create(
        tenant=tenant,
        full_name='Alice Guest',
        email='alice@example.com',
        phone='+94771234567'
    )
    booking = Booking.objects.create(
        tenant=tenant,
        room=room,
        guest=guest,
        check_in=date(2026,5,1),
        check_out=date(2026,5,4),
        nights=3,
        guests_count=2,
        room_price_per_night_lkr=room.base_price_lkr,
        total_price_lkr=room.base_price_lkr * 3,
        status='pending',
        payment_status='unpaid',
        booking_ref=f'BKG-{uuid.uuid4().hex[:8].upper()}',
        special_requests='Late arrival'
    )
    print('Booking created', booking.id)
