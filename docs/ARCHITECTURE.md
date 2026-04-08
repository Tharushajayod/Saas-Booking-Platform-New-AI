# System Architecture

Detailed technical architecture of the SaaS Booking Platform.

## High-Level Overview

```
┌────────────────────────────────────────────────────────────────┐
│                        Guests & Property Owners                 │
└────────────────────────────────────────────────────────────────┘
                             │
                             │ HTTPS
                             │
┌────────────────────────────────────────────────────────────────┐
│                    Cloudflare CDN + WAF                         │
│              Wildcard DNS (*yoursaas.lk)                       │
│              SSL Termination, DDoS Protection                   │
└────────┬──────────────────────────────────┬─────────────────────┘
         │                                  │
         │ *.yoursaas.lk                    │ api.yoursaas.lk
         │                                  │
┌────────▼─────────────┐          ┌────────▼──────────────┐
│   Frontend (Vercel)   │          │   Backend (Koyeb)     │
│  - Public Booking    │          │   Django REST API      │
│  - Owner Dashboard   │          │   - Business Logic     │
│  - React/Next.js     │          │   - Authentication     │
│  - Tailwind CSS      │          │   - Data Validation    │
└────────┬─────────────┘          └────────┬──────────────┘
         │                                  │
         └──────────────┬───────────────────┘
                        │ SQL
         ┌──────────────▼─────────────────┐
         │  PostgreSQL Database            │
         │  (Supabase)                     │
         │  - Multi-tenant schema          │
         │  - Row-level security           │
         │  - Automated backups            │
         └──────────────┬──────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    ┌───▼──┐      ┌────▼─────┐   ┌────▼──┐
    │Redis │      │Cloudinary│   │S3 for │
    │Cache │      │for Images│   │Backups│
    └──────┘      └──────────┘   └───────┘
```

## Multi-Tenancy Implementation

### Data Isolation Strategy

**Shared Database, Shared Schema + tenant_id**

Every table containing tenant-specific data has a `tenant_id` UUID column:

```
tenants
├── id (PK)
├── subdomain (unique)
└── custom_domain

owners (tenant_id FK)
properties (tenant_id FK)
rooms (tenant_id FK)
bookings (tenant_id FK)
payments (tenant_id FK)
guests (tenant_id FK)
```

### Subdomain Resolution

Frontend flow:
```
1. User visits palmgrove.yoursaas.lk
2. Cloudflare routes to Vercel
3. Vercel Next.js middleware:
   - Reads Host header
   - Extracts subdomain "palmgrove"
   - Stores in context/header
4. API calls include x-tenant-slug header
5. Backend resolves tenant_id from subdomain
6. All queries filtered by tenant_id
```

### Row-Level Security (RLS)

PostgreSQL policies enforce multi-tenancy at DB level:

```sql
CREATE POLICY tenant_isolation ON properties
  USING (tenant_id = current_setting('app.current_tenant')::UUID);

ALTER TABLE properties ENABLE ROW LEVEL SECURITY;
```

If code forgets to filter, database blocks access.

## Authentication Flow

```
Login Request
    ↓
POST /auth/login
    ↓
Verify Email & Password
    ↓
Generate JWT Tokens:
  - access_token (24h expiry)
  - refresh_token (7d expiry)
    ↓
Return to Frontend
    ↓
Store in localStorage
    ↓
Include in future requests:
Authorization: Bearer <access_token>
```

JWT Payload:
```json
{
  "user_id": "uuid",
  "tenant_id": "uuid",
  "email": "owner@example.com",
  "role": "owner",
  "exp": 1234567890,
  "iat": 1234567800
}
```

## Booking Payment Flow

```
Guest Submits Booking
    ↓
POST /bookings/create
    ↓ Backend validates:
  - Room exists & available
  - Dates not booked
  - Calculate total price
    ↓ Create booking (status: pending)
    ↓
POST /payments/payhere-init
    ↓ Generate secure hash:
  MD5(merchant_id + order_id + amount + 'LKR' + MD5(secret))
    ↓
Return PayHere checkout parameters
    ↓
Frontend redirects guest to PayHere payment page
    ↓
Guest enters card details & pays
    ↓
PayHere POSTs webhook to /payments/payhere-notify
    ↓ Backend:
  1. Verify MD5 hash
  2. Update booking status: confirmed
  3. Update payment_status: paid
  4. Send confirmation email
  5. Send SMS alert
    ↓
PayHere redirects guest to success page
    ↓
Guest receives booking confirmation with reference
```

## API Architecture

### REST Endpoints Structure

```
/api/
├── auth/              # Authentication
│   ├── register       # POST
│   ├── login          # POST
│   ├── refresh        # POST
│   └── password-reset # POST
├── tenants/           # Tenant management
│   └── me             # GET, PATCH
├── properties/        # Properties & rooms
│   ├── {id}/         # GET, PATCH, DELETE
│   ├── {id}/rooms/   # GET, POST
│   └── search-availability/
├── bookings/          # Bookings
│   ├── {id}/         # GET, PATCH
│   └── create        # POST
└── payments/          # Payment handling
    ├── payhere-init   # POST
    └── payhere-notify # POST (webhook)
```

### Versioning

Support multiple API versions:
```
/api/v1/
/api/v2/
```

## Frontend Architecture

### Directory Structure

```
frontend/
├── app/                  # Next.js 14 app directory
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Homepage
│   ├── dashboard/       # Owner dashboard
│   ├── properties/      # Property pages
│   ├── bookings/        # Booking flow
│   └── [tenant]/        # Dynamic routes for subdomains
├── components/          # Reusable components
├── lib/                 # Utilities
│   └── api.ts          # Axios client with auth
├── store/              # Zustand state management
├── hooks/              # Custom React hooks
└── utils/              # Helper functions
```

### State Management

Using Zustand for lightweight state:

```typescript
// Global stores
- useAuthStore      // User, tokens, auth state
- useBookingStore   // Bookings data
- usePropertyStore  // Properties data
```

### Middleware for Subdomains

```typescript
// frontend/middleware.ts
export function middleware(request: NextRequest) {
  const host = request.headers.get('host')
  const subdomain = host?.split('.')[0]
  
  // Store subdomain in request headers
  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-tenant-slug', subdomain)
  
  return NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  })
}
```

## Backend Architecture

### Django App Structure

```
backend/
├── apps/
│   ├── core/          # Authentication & utils
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── tenants/       # Multi-tenancy
│   ├── properties/    # Properties & rooms
│   └── bookings/      # Bookings & payments
├── config/            # Settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

### Custom Middleware

```python
# Tenant resolution middleware
# Reads x-tenant-slug header from frontend
# Resolves to tenant_id
# Sets in request context
# Used for data filtering
```

### Serializers Pattern

```python
# Validation & transformation
PropertySerializer    # Full property details
PropertyListSerializer # Light property list
PropertyCreateSerializer # POST/PATCH validation
```

### QuerySet Filtering

All queries filtered by tenant:

```python
# models.py
class PropertyQuerySet(models.QuerySet):
    def for_tenant(self, tenant_id):
        return self.filter(tenant_id=tenant_id)

# views.py
properties = Property.objects.for_tenant(request.tenant_id)
```

## Database Schema

```
Tenants (master registry)
  ├── Owners (tenant users)
  ├── Properties (guest houses/villas)
  │   ├── Rooms (bookable units)
  │   │   ├── RoomAvailability
  │   │   └── SeasonalPricing
  │   └── Amenities
  ├── Guests (guest profiles)
  └── Bookings (reservations)
      └── Payments (PayHere records)
```

## Deployment Pipeline

```
Developer Push to main
    ↓
GitHub Actions trigger
    ↓
├─ Run tests
├─ Lint code
├─ Build Docker image
├─ Push to GHCR
└─ Trigger Vercel & Koyeb
    ↓
Koyeb pulls & redeploys backend
    ↓
Vercel auto-deploys frontend
    ↓
Database migrations (manual)
    ↓
Smoke tests
    ↓
Live!
```

## Caching Strategy

### Redis Cache

**Use cases:**
- Session storage
- Rate limiting
- Query result caching
- Temporary data (TBD bookings)

```python
CACHE_KEY_PROPERTY = f"property:{property_id}"
cache.set(CACHE_KEY_PROPERTY, property_data, timeout=3600)
```

### CDN Caching

**Vercel:**
- Static files (JS, CSS) - cached globally
- HTML - cache control headers

**Cloudinary:**
- Product images cached with transformation

## Security Layers

```
1. Cloudflare WAF
   - DDoS protection
   - Rate limiting
   - SQL injection prevention

2. SSL/TLS
   - HTTPS everywhere
   - Auto-renewed certificates

3. CORS
   - Whitelisted origins
   - Preflight handling

4. Authentication
   - JWT tokens
   - Refresh token rotation
   - Token expiration

5. Authorization
   - Role-based access (RBAC)
   - Tenant isolation
   - Row-level security

6. Input Validation
   - Serializer validation
   - Type checking
   - Length limits

7. Rate Limiting
   - Per-user limits
   - Per-endpoint limits
   - Exponential backoff
```

## Monitoring & Observability

### Logging

```
Backend logs → CloudWatch / Loggly
Frontend errors → Sentry
Database → Supabase monitoring
```

### Metrics

- API response times
- Error rates
- Database query performance
- Cache hit rates
- Payment success/failure rates

## Performance Optimization

1. **Database**
   - Indexes on common queries
   - Connection pooling
   - Query optimization

2. **Caching**
   - Redis for sessions
   - CDN for static assets
   - Page caching

3. **Frontend**
   - Code splitting
   - Image optimization (Cloudinary)
   - Lazy loading

4. **Backend**
   - Pagination
   - Field selection
   - Async tasks (Celery)

## Disaster Recovery

**RTO (Recovery Time Objective):** < 1 hour
**RPO (Recovery Point Objective):** < 24 hours

1. Database backups - Supabase daily
2. Code backups - GitHub
3. Failover plan - Switch DNS

## Scalability

As traffic grows:

1. **Horizontal scaling** - Multiple Koyeb replicas
2. **Database** - Upgrade Supabase plan
3. **Cache** - Increase Redis capacity
4. **CDN** - Already global with Cloudflare
5. **Async jobs** - Add Celery workers

## Cost Optimization

1. Use free/generous tiers initially
2. Auto-scaling based on demand
3. Optimize database queries
4. Compress images (Cloudinary)
5. Cache aggressively
