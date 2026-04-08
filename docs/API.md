# API Documentation

Complete reference for all SaaS Booking Platform API endpoints.

## Base URL

```
https://api.yoursaas.lk/api/
```

## Authentication

All endpoints (except public ones) require JWT token in header:

```
Authorization: Bearer <access_token>
```

## Error Responses

Standard error format:

```json
{
  "detail": "Error message",
  "code": "ERROR_CODE"
}
```

Common status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - No permission
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Authentication Endpoints

### Register Owner

```
POST /auth/register
Content-Type: application/json

{
  "email": "owner@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "phone": "+94771234567"
}

Response: 201
{
  "id": "uuid",
  "email": "owner@example.com",
  "full_name": "John Doe",
  "tenant_id": "uuid"
}
```

### Login

```
POST /auth/login
Content-Type: application/json

{
  "email": "owner@example.com",
  "password": "password123"
}

Response: 200
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": "uuid",
    "email": "owner@example.com"
  }
}
```

### Refresh Token

```
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}

Response: 200
{
  "access_token": "eyJ..."
}
```

### Password Reset

```
POST /auth/password-reset
Content-Type: application/json

{
  "email": "owner@example.com"
}

Response: 200
{ "detail": "Password reset link sent to email" }
```

## Tenant Endpoints

### Get Current Tenant

```
GET /tenants/me
Authorization: Bearer <token>

Response: 200
{
  "id": "uuid",
  "name": "Palm Grove Villa",
  "subdomain": "palmgrove",
  "plan": "starter",
  "is_active": true
}
```

### Update Tenant

```
PATCH /tenants/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Name",
  "custom_domain": "www.palmgrovevilla.lk"
}

Response: 200
{ ... updated tenant ... }
```

## Property Endpoints

### List Properties

```
GET /properties/
Authorization: Bearer <token>
Query: ?page=1&page_size=20

Response: 200
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "name": "Palm Grove Beach Villa",
      "property_type": "villa",
      "city": "Unawatuna",
      "rooms_count": 4,
      "is_published": true
    }
  ]
}
```

### Create Property

```
POST /properties/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Property",
  "description": "Description here",
  "property_type": "villa",
  "city": "Mirissa",
  "address": "123 Beach Road, Mirissa",
  "amenities": ["WiFi", "Pool", "Breakfast"]
}

Response: 201
{ ... created property ... }
```

### Get Property

```
GET /properties/{id}/
Authorization: Bearer <token>

Response: 200
{ ... property details ... }
```

### Update Property

```
PATCH /properties/{id}/
Authorization: Bearer <token>

Response: 200
{ ... updated property ... }
```

### Delete Property

```
DELETE /properties/{id}/
Authorization: Bearer <token>

Response: 204 No Content
```

## Room Endpoints

### List Rooms

```
GET /properties/{property_id}/rooms/
Authorization: Bearer <token>

Response: 200
{
  "results": [
    {
      "id": "uuid",
      "name": "Ocean View Deluxe",
      "capacity": 2,
      "base_price_lkr": 15000,
      "is_available": true
    }
  ]
}
```

### Create Room

```
POST /properties/{property_id}/rooms/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Ocean View Deluxe",
  "description": "Room with ocean view",
  "capacity": 2,
  "base_price_lkr": 15000
}

Response: 201
{ ... created room ... }
```

## Booking Endpoints

### Create Booking (Public)

```
POST /bookings/create
Content-Type: application/json

{
  "room_id": "uuid",
  "check_in": "2024-01-15",
  "check_out": "2024-01-20",
  "guest_email": "guest@example.com",
  "guest_full_name": "Jane Doe",
  "guest_phone": "+94771234567",
  "special_requests": "Late checkout if possible"
}

Response: 201
{
  "id": "uuid",
  "booking_ref": "BKG-00123",
  "status": "pending",
  "payment_status": "unpaid",
  "total_price_lkr": 75000
}
```

### Get Booking

```
GET /bookings/{id}/
Authorization: Bearer <token>

Response: 200
{ ... booking details ... }
```

### List Owner's Bookings

```
GET /bookings/
Authorization: Bearer <token>
Query: ?status=confirmed&date_from=2024-01-01

Response: 200
{
  "count": 12,
  "results": [ ... bookings ... ]
}
```

### Update Booking Status

```
PATCH /bookings/{id}/
Authorization: Bearer <token>

{
  "status": "completed"
}

Response: 200
{ ... updated booking ... }
```

## Payment Endpoints

### Initiate Payment (PayHere)

```
POST /payments/payhere-init
Content-Type: application/json

{
  "booking_id": "uuid"
}

Response: 200
{
  "merchant_id": "12345",
  "order_id": "ORDER123",
  "amount": "75000.00",
  "currency": "LKR",
  "md5sig": "hash...",
  "return_url": "https://yoursaas.lk/booking/success",
  "cancel_url": "https://yoursaas.lk/booking/cancel"
}
```

### PayHere Webhook (Internal)

```
POST /payments/payhere-notify
Content-Type: application/x-www-form-urlencoded

merchant_id=12345&order_id=ORDER123&status_code=2&md5sig=hash...
```

## Availability Endpoints

### Search Available Rooms

```
GET /properties/search-availability
Query: ?check_in=2024-01-15&check_out=2024-01-20&capacity=2

Response: 200
{
  "results": [
    {
      "room_id": "uuid",
      "property_name": "Palm Grove",
      "room_name": "Deluxe",
      "price_per_night_lkr": 15000,
      "nights": 5,
      "total_price_lkr": 75000
    }
  ]
}
```

### Get Room Availability Calendar

```
GET /properties/{property_id}/rooms/{room_id}/availability/
Authorization: Bearer <token>
Query: ?month=2024-01

Response: 200
{
  "month": "2024-01",
  "availability": {
    "2024-01-15": "available",
    "2024-01-16": "booked",
    "2024-01-17": "maintenance"
  }
}
```

### Block Dates

```
POST /properties/{property_id}/rooms/{room_id}/block-dates/
Authorization: Bearer <token>

{
  "dates": ["2024-01-15", "2024-01-16"],
  "reason": "maintenance"
}

Response: 201
{ "detail": "Dates blocked successfully" }
```

## Pagination

All list endpoints support pagination:

```
?page=1&page_size=20

Response includes:
{
  "count": 100,
  "next": "...?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering & Sorting

Common query parameters:

```
?status=confirmed
?date_from=2024-01-01
?date_to=2024-12-31
?ordering=-created_at
?search=villa
```

## Rate Limiting

API rate limits:
- Public endpoints: 100 requests/hour
- Authenticated endpoints: 1000 requests/hour

Response headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

## Testing with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Get properties with token
curl -X GET http://localhost:8000/api/properties/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Interactive Documentation

Available at:
- Swagger UI: http://localhost:8000/api/schema/swagger/
- ReDoc: http://localhost:8000/api/schema/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/
