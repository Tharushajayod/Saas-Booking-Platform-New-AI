# Quick Start - Local Setup

## Prerequisites (Install if Missing)

### Windows Setup

#### 1. Install Docker Desktop
- Download: https://www.docker.com/products/docker-desktop
- Install and restart your computer
- Open PowerShell and verify: `docker --version`

#### 2. OR: Install PostgreSQL Locally
- Download: https://www.postgresql.org/download/windows/
- Install with default settings (password: postgres)
- Verify: `psql --version`

#### 3. Install Node.js
- Download: https://nodejs.org/ (LTS version)
- Verify: `node --version` and `npm --version`

---

## Option A: Run with Docker (Recommended)

### 1. Start Docker Desktop
- Click the Docker Desktop icon on your taskbar
- Wait 30 seconds for it to fully start
- Verify: Open PowerShell and run `docker ps`

### 2. Build and Start Services
```powershell
cd "c:\Users\Tharusha Jayod\OneDrive\Documents\New project\Test 1"

# Build all images
docker-compose build

# Start all services
docker-compose up
```

### 3. In a New PowerShell Terminal, Run Migrations
```powershell
cd "c:\Users\Tharusha Jayod\OneDrive\Documents\New project\Test 1"

# Run migrations
npm run backend:migrate

# Create superuser (follow prompts)
npm run backend:createsuperuser
```

### Services Available:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Database**: localhost:5432
- **Redis**: localhost:6379

---

## Option B: Run Backend & Frontend Separately (Without Docker)

### Backend Setup

#### 1. Create Virtual Environment
```powershell
cd "c:\Users\Tharusha Jayod\OneDrive\Documents\New project\Test 1\backend"

# Create venv
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1
```

#### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

#### 3. Run Migrations
```powershell
# Update .env with local database credentials if needed
python manage.py migrate
```

#### 4. Create Superuser
```powershell
python manage.py createsuperuser
```

#### 5. Start Backend Server
```powershell
python manage.py runserver
```

Backend will be at: http://localhost:8000

---

### Frontend Setup

#### 1. Install Dependencies
```powershell
cd "c:\Users\Tharusha Jayod\OneDrive\Documents\New project\Test 1\frontend"
npm install
```

#### 2. Start Frontend Server
```powershell
npm run dev
```

Frontend will be at: http://localhost:3000

---

## Database Setup Options

### Option 1: Use Supabase (Cloud - Recommended for Testing)
1. Go to https://supabase.com
2. Sign up and create a project
3. Copy the PostgreSQL connection string
4. Update `.env` file with the connection string
5. Run migrations

### Option 2: Install PostgreSQL Locally
1. Download & install PostgreSQL
2. Create a database: `createdb saas_booking`
3. Update `.env` with connection details
4. Run migrations

### Option 3: Use Docker Just for Database
```powershell
# Run only PostgreSQL in Docker
docker run --name postgres_saas \
  -e POSTGRES_DB=saas_booking \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15-alpine
```

---

## Troubleshooting

### Docker Daemon Not Running
```powershell
# Check Docker status
docker ps

# If error, ensure Docker Desktop is running from taskbar
```

### Port Already in Use
```powershell
# Find process using port
netstat -ano | findstr :3000

# Kill process by PID
taskkill /PID [PID] /F
```

### Database Connection Error
- Ensure PostgreSQL is running
- Check `.env` database credentials
- Test connection: `psql -U postgres -d saas_booking`

### Module Not Found
```powershell
# Reinstall dependencies
pip install -r backend/requirements.txt

# Or with frontend
npm install --prefix frontend
```

---

## Helpful Commands

```powershell
# View all services
docker-compose ps

# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Reset everything (WARNING: deletes database)
docker-compose down -v

# Access backend shell
npm run backend:shell

# Run backend tests
docker-compose exec backend python manage.py test
```

---

## Next Steps

1. ✅ Complete the setup above
2. 📝 Visit http://localhost:3000 (or :8000/admin with credentials)
3. 📚 Read DEVELOPMENT.md for architecture details
4. 🚀 Start building Phase 3-6 of the roadmap

For questions, refer to:
- `DEVELOPMENT.md` - Development guide
- `DEPLOYMENT.md` - Production setup
- `docs/ARCHITECTURE.md` - System design
- `docs/API.md` - API documentation
