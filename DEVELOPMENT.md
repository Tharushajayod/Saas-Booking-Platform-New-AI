# Development Setup Guide

## Quick Start with Docker

### Prerequisites
- Docker & Docker Compose installed
- Git
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Start Development Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd saas-booking-platform

# Create environment file
cp .env.example .env

# Start all services (PostgreSQL, Redis, Backend, Frontend)
npm run dev

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - Admin: http://localhost:8000/admin
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

## Running Migrations

```bash
# Run database migrations
npm run backend:migrate

# Create superuser
npm run backend:createsuperuser
```

## Project Structure

```
saas-booking-platform/
├── backend/                 # Django REST API
│   ├── apps/
│   │   ├── core/           # Authentication & common utilities
│   │   ├── tenants/        # Tenant management
│   │   ├── properties/     # Property management
│   │   └── bookings/       # Booking logic
│   ├── config/             # Django configuration
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # Next.js React App
│   ├── app/               # App directory structure
│   ├── components/        # React components
│   ├── lib/              # Utilities and API clients
│   ├── store/            # Zustand state management
│   ├── hooks/            # React hooks
│   ├── utils/            # Helper functions
│   └── Dockerfile
│
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD pipelines
├── docker-compose.yml     # Local development setup
└── package.json          # Root monorepo config

```

## Backend Development

### Create a new Django App
```bash
cd backend
python manage.py startapp <app_name>
```

### Run Django Shell
```bash
npm run backend:shell
```

### View Backend Logs
```bash
docker-compose logs -f backend
```

## Frontend Development

### Install dependencies
```bash
cd frontend
npm install
```

### Run local Next.js development server
```bash
npm run dev
```

### Build for production
```bash
npm run build
npm start
```

## Environment Variables

See `.env.example` for all required environment variables. Key variables:

- `DEBUG`: Django debug mode
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `SENDGRID_API_KEY`: Email service
- `PAYHERE_MERCHANT_ID`: Payment gateway
- `CLOUDINARY_*`: Image storage

## API Documentation

API endpoints are documented with Swagger at:
`http://localhost:8000/api/schema/swagger/`

## Testing

### Backend Tests
```bash
docker-compose exec backend python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

See `DEPLOYMENT.md` for deployment instructions to Vercel, Koyeb, and Supabase.

## Common Commands

```bash
# View all services
npm run dev:logs

# Stop services
npm run down

# Rebuild containers
npm run dev:build

# Reset database
docker-compose down -v
npm run dev
npm run backend:migrate
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port 8000
lsof -ti :8000 | xargs kill -9

# Find and kill process using port 3000
lsof -ti :3000 | xargs kill -9
```

### Database Connection Error
```bash
# Restart PostgreSQL container
docker-compose restart postgres

# Check database status
docker-compose exec postgres pg_isready
```

### Redis Connection Error
```bash
# Restart Redis container
docker-compose restart redis

# Check Redis status
docker-compose exec redis redis-cli ping
```

## Contributing

1. Create a feature branch: `git checkout -b feature/description`
2. Commit changes: `git commit -m "Add feature description"`
3. Push to branch: `git push origin feature/description`
4. Open a Pull Request

## Next Steps

1. **Phase 2**: Complete database models and authentication
2. **Phase 3**: Implement core API endpoints
3. **Phase 4**: Build frontend pages and components
4. **Phase 5**: Integrate PayHere, SendGrid, and Notify.lk
5. **Phase 6**: Deploy to production
