import requests

BASE = 'http://localhost:8000'

print('Health:', requests.get(f'{BASE}/api/auth/health/').json())

# Register
reg = requests.post(f'{BASE}/api/auth/register/', json={
    'email': 'user1@example.com',
    'password': 'testpass123',
    'password2': 'testpass123',
    'first_name': 'User',
    'last_name': 'One'
})
print('Register status:', reg.status_code, reg.text)

# Login
login = requests.post(f'{BASE}/api/auth/login/', json={
    'email': 'user1@example.com',
    'password': 'testpass123'
})
print('Login status:', login.status_code, login.text)
if login.status_code == 200:
    access = login.json().get('access')
    headers = {'Authorization': f'Bearer {access}'}
    profile = requests.get(f'{BASE}/api/auth/profile/', headers=headers)
    print('Profile status:', profile.status_code, profile.text)
else:
    print('Skipping profile check')

# Create Tenant
tenant_payload = {
    'name': 'Demo Tenant',
    'subdomain': 'demo'
}
ten = requests.post(f'{BASE}/api/tenants/', headers=headers, json=tenant_payload)
print('Create tenant:', ten.status_code, ten.text)

# Create Property (owner)
prop_payload = {
    'name': 'Seaside Villa',
    'description': 'Lovely villa by the sea',
    'short_description': 'Seaside villa',
    'property_type': 'villa',
    'address': 'Beach Road',
    'city': 'Galle',
    'country': 'Sri Lanka',
    'is_published': True,
}
prop = requests.post(f'{BASE}/api/properties/create/', headers=headers, json=prop_payload)
print('Create property:', prop.status_code, prop.text)

if prop.status_code == 201:
    room_list = requests.get(f'{BASE}/api/properties/{prop.json().get("id")}/', headers=headers)
    print('Property detail:', room_list.status_code)

    # Create Booking for the first room (if any) - find a room by querying rooms for this property via /api/properties/<id>/
    # For now attempt booking by creating with a known room id if present in the response (rooms not yet exposed via API)
    # Attempt to create a booking by finding any room via DB fallback: assume room id exists after admin created via scripts.
    # We'll try using the property itself to create a simple booking if possible.

    # Try a sample booking (this may fail if room id unknown)
    booking_payload = {
        # placeholder room_id - replace if you have a room UUID
        'room_id': prop.json().get('id'),
        'check_in': '2026-05-01',
        'check_out': '2026-05-04',
        'guest_full_name': 'Alice Guest',
        'guest_email': 'alice@example.com',
        'guest_phone': '+94771234567',
        'guests_count': 2,
        'special_requests': 'Late arrival'
    }
    book = requests.post(f'{BASE}/api/bookings/create/', json=booking_payload)
    print('Create booking:', book.status_code, book.text)
else:
    print('Skipping booking creation since property creation failed')
