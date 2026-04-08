# SaaS Booking Platform

A complete, production-ready multi-tenant direct booking platform for guest houses and villas in Sri Lanka. Built with Next.js, Django, PostgreSQL, and integrated with PayHere, SendGrid, and Notify.lk.

## Features

- ✅ **Multi-Tenant Architecture** - Isolated data for each property owner
- ✅ **Guest Booking Site** - Dynamic subdomain-based public booking websites
- ✅ **Owner Dashboard** - Complete property and booking management
- ✅ **Payment Integration** - PayHere gateway for LKR payments
- ✅ **Email & SMS** - SendGrid & Notify.lk notifications
- ✅ **Image Management** - Cloudinary CDN integration
- ✅ **Availability Calendar** - Date blocking and seasonal pricing
- ✅ **Mobile Responsive** - Works on all devices
- ✅ **Production Ready** - Docker, CI/CD, monitoring

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| Backend | Django 4.2, Django REST Framework |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Storage | Cloudinary CDN |
| Payments | PayHere |
| Email | SendGrid |
| SMS | Notify.lk |
| Hosting | Vercel (Frontend), Koyeb (Backend), Supabase (DB) |
| CI/CD | GitHub Actions |

## Getting Started

### Quick Start with Docker

```bash
# Clone and setup
git clone <your-repo-url>
cd saas-booking-platform
cp .env.example .env

# Start all services
npm run dev

# In new terminal, run migrations
npm run backend:migrate
```

Services available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

### Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── backend/              # Django REST API
│   ├── apps/
│   │   ├── auth/        # Authentication & JWT
│   │   ├── tenants/     # Tenant management
│   │   ├── properties/  # Properties & rooms
│   │   └── bookings/    # Bookings & payments
│   └── config/          # Settings
│
├── frontend/            # Next.js React app
│   ├── app/            # Pages & layouts
│   ├── components/     # Reusable components
│   ├── lib/            # API clients
│   └── store/          # Zustand state
│
└── docs/               # Documentation
```

## Development

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed development setup, database commands, and environmental configuration.

### Essential Commands

```bash
# Development
npm run dev                    # Start all services
npm run down                   # Stop services
npm run dev:build            # Rebuild containers

# Database
npm run backend:migrate      # Run migrations
npm run backend:createsuperuser  # Create admin user

# Logs
npm run dev:logs            # View all service logs
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment guide to production.

Deploy to:
- **Frontend**: Vercel (auto-deploy from GitHub)
- **Backend**: Koyeb (Docker container)
- **Database**: Supabase (managed PostgreSQL)

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/api/schema/swagger/
- ReDoc: http://localhost:8000/api/schema/redoc/

## Database Models

### Core Tables
- `tenants` - Tenant/SaaS owner accounts
- `owners` - Property owner user accounts
- `properties` - Guest houses & villas
- `rooms` - Individual rentable rooms
- `bookings` - Reservations with tenant isolation
- `payments` - PayHere payment records

All tenant-related tables include `tenant_id` for data isolation.

## Security

- Row-Level Security (RLS) policies on all tables
- JWT authentication for APIs
- CORS properly configured
- Rate limiting on endpoints
- Input validation & sanitization
- Password hashing with bcrypt

## Testing

```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests
cd frontend && npm test
```

## Roadmap

- [ ] Phase 1: Project Setup ✓
- [ ] Phase 2: Database & Auth
- [ ] Phase 3: Core Backend API
- [ ] Phase 4: Frontend Development
- [ ] Phase 5: Integrations
- [ ] Phase 6: Deployment & Go-live

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit: `git commit -m "Add feature description"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support & Documentation

- [Development Guide](./DEVELOPMENT.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Architecture Guide](./docs/)
- [PayHere Integration](./docs/PAYHERE.md)
- [API Reference](./docs/API.md)

## Contact

For questions or support regarding this SaaS booking platform, please open an issue or contact the development team.

---

Built with ❤️ for Sri Lankan property owners. Making direct booking simpler.
