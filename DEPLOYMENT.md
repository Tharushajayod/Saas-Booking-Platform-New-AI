# Deployment Guide

Complete instructions for deploying the SaaS Booking Platform to production.

## Architecture Overview

```
┌─────────────┐
│  Users      │
└──────┬──────┘
       │ HTTPS
┌──────▼──────────────────────┐
│  Cloudflare CDN             │
│  *.yoursaas.lk (wildcard)   │
└──────┬──────────┬───────────┘
       │          │
   ┌───▼──┐   ┌───▼──┐
   │ Next.js   │Django│
   │(Vercel)   │(Koyeb)
   └───┬──┘   └───┬──┘
       │          │
       └────┬─────┘
            │
       ┌────▼─────┐
       │PostgreSQL │
       │(Supabase) │
       └───────────┘
```

## Prerequisites

1. **Vercel Account** - For frontend hosting
2. **Koyeb Account** - For backend hosting
3. **Supabase Account** - For PostgreSQL database
4. **Cloudflare Account** - For DNS & CDN
5. **PayHere Account** - For payment processing
6. **SendGrid Account** - For email
7. **Notify.lk Account** - For SMS

## Step 1: Database Setup (Supabase)

### Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up and create a new project
3. Choose **Singapore** region (best latency from Sri Lanka)
4. Wait for project to be created

### Deploy Database

```bash
# Get connection string from Supabase
# Settings > Database > URI

# Connect with psql
psql postgresql://user:password@db.supabase.co:5432/postgres

# Or use Supabase SQL Editor in dashboard
```

### Run Migrations

In Supabase SQL Editor, paste and run:

```sql
-- Phase 2 & 3 migrations (to be created)
-- Start with tenants, owners, properties, rooms
```

## Step 2: Backend Deployment (Koyeb)

### Create Koyeb Service

1. Sign up at [koyeb.com](https://koyeb.com)
2. Click **Create Service**
3. Choose **Docker**
4. Enter Docker image: `ghcr.io/your-username/saas-booking-platform/backend:latest`

### Configure Environment Variables

In Koyeb service settings, add:

```
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=api.yoursaas.lk,yoursaas.koyeb.app
JWT_SECRET=your-jwt-secret-key
SENDGRID_API_KEY=your-sendgrid-key
PAYHERE_MERCHANT_ID=your-merchant-id
PAYHERE_MERCHANT_SECRET=your-merchant-secret
PAYHERE_SANDBOX_MODE=False
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
NOTIFY_LK_USER_ID=your-notify-id
NOTIFY_LK_API_KEY=your-notify-key
```

### Configure Domain

In Koyeb Domains:
- Add custom domain: `api.yoursaas.lk`
- SSL is automatic

### Deploy Webhook URL

Get the deployment webhook URL from Koyeb settings (for GitHub Actions).

## Step 3: Frontend Deployment (Vercel)

### Connect GitHub

1. Sign up at [vercel.com](https://vercel.com)
2. Click **Add New Project**
3. Import GitHub repository
4. Set **Root Directory** to `frontend`

### Configure Environment Variables

In Vercel project settings:

```
NEXT_PUBLIC_API_URL=https://api.yoursaas.lk
NEXT_PUBLIC_APP_URL=https://yoursaas.lk
```

### Add Wildcard Domain

In Vercel **Domains** settings:
1. Add `*.yoursaas.lk`
2. Follow DNS configuration instructions
3. SSL certificate auto-provisioned

## Step 4: DNS Configuration (Cloudflare)

### Transfer Domain to Cloudflare

1. Sign up at [cloudflare.com](https://cloudflare.com)
2. Add your domain
3. Update nameservers at your registrar

### Configure Records

Create these DNS records in Cloudflare:

```
Name         Type    Value                    Proxy
@            CNAME   cname.vercel-dns.com     Proxied (Orange ☁️)
www          CNAME   cname.vercel-dns.com     Proxied
*            CNAME   cname.vercel-dns.com     Proxied
api          CNAME   your-koyeb-app.koyeb.app DNS only
```

### SSL/TLS Settings

1. Go to SSL/TLS settings
2. Set to **Full (strict)**
3. Enable **Always Use HTTPS**
4. Add Page Rule to always redirect HTTP to HTTPS

## Step 5: CI/CD Setup (GitHub Actions)

### Create Secrets

In GitHub repository **Settings > Secrets and variables > Actions**, add:

```
KOYEB_WEBHOOK_URL=https://api.koyeb.io/v1/webhooks/...
DOCKER_USERNAME=your-github-username
DOCKER_PASSWORD=your-github-token
VERCEL_TOKEN=your-vercel-token
```

### Deploy Workflow

The `.github/workflows/deploy.yml` will:
1. Run tests on push to main
2. Build Docker image
3. Push to GitHub Container Registry
4. Trigger Koyeb redeployment
5. Deploy to Vercel

## Step 6: PayHere Live Mode

### Switch from Sandbox

1. In PayHere Merchant Portal, submit for live mode
2. Provide: NIC, bank account, business details
3. Approval takes 5-7 business days

### Update Environment

Once approved, in production:

```
PAYHERE_MERCHANT_ID=live-merchant-id
PAYHERE_MERCHANT_SECRET=live-merchant-secret
PAYHERE_SANDBOX_MODE=False
```

## Monitoring & Maintenance

### Database Backups

Supabase provides automatic daily backups. For additional security:

1. Enable point-in-time recovery (Pro plan)
2. Download backups regularly
3. Test restore procedures

### Logs & Monitoring

**Backend (Koyeb):**
- View logs in Koyeb dashboard
- Set up error alerts

**Frontend (Vercel):**
- View logs in Vercel dashboard
- Monitor analytics

**Database (Supabase):**
- View query performance
- Monitor connections

### Update Procedures

```bash
# Update dependencies
npm install
git push  # Triggers CI/CD

# Manual redeployment
# Koyeb: Trigger webhook
# Vercel: Auto-redeploys on push
# Database: Run migrations in Supabase SQL
```

## Troubleshooting

### Frontend Not Loading

- Check Cloudflare DNS settings
- Verify custom domain in Vercel
- Check Cloudflare SSL/TLS settings

### API Connection Errors

- Verify `NEXT_PUBLIC_API_URL` in Vercel settings
- Check CORS settings in Django
- Verify Koyeb service is running

### Database Connection Issues

- Check `DATABASE_URL` format
- Verify IP not blocked by Supabase
- Check PostgreSQL connection limits

### Payment Gateway Errors

- Verify PayHere credentials
- Check webhook URL accessibility
- Review PayHere logs for errors

## Production Checklist

- [ ] Database backups configured
- [ ] SSL certificates installed
- [ ] Environment variables set correctly
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] Monitoring alerts set up
- [ ] Email templates configured
- [ ] SMS gateway tested
- [ ] PayHere live mode enabled
- [ ] Cloudinary images configured
- [ ] Database migrations applied
- [ ] Superuser created
- [ ] Smoke tests passed
- [ ] 5-10 test bookings completed
- [ ] Payment webhook tested

## Cost Estimates (Monthly)

| Service | Plan | Cost |
|---------|------|------|
| Supabase | Pro | $25 |
| Koyeb | Pro | $20 |
| Vercel | Pro | $20 |
| Cloudflare | Pro | $20 |
| SendGrid | Free | $0 |
| PayHere | Free | $0 |
| **Total** | | **$85** |

*Note: Costs vary based on traffic and storage*

## Support

For deployment issues, check:
- Vercel documentation: https://vercel.com/docs
- Koyeb documentation: https://koye.com/docs
- Supabase documentation: https://supabase.com/docs
- Cloudflare documentation: https://developers.cloudflare.com
