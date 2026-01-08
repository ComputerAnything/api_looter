# Environment Setup Guide

## Quick Start

api_looter uses a **single `.env` file** that you copy from environment-specific templates.

### Switching Environments

```bash
# For local development (no Docker, hot reload):
cp .env.development .env
python run.py

# For staging deployment:
cp .env.staging .env
# Fill in: SECRET_KEY, REDIS_PASSWORD, CLOUDFLARE_TUNNEL_TOKEN
docker-compose -f docker-compose.staging.yml up -d

# For production deployment:
cp .env.production .env
# Fill in: SECRET_KEY, REDIS_PASSWORD, CLOUDFLARE_TUNNEL_TOKEN
docker-compose -f docker-compose.prod.yml up -d
```

---

## Environment Details

### Development (Local, No Docker)
**File:** `.env.development`
**Use Case:** Local development with instant hot reload

**Features:**
- ✅ No Docker containers needed
- ✅ Hot reload on file changes
- ✅ Memory-based rate limiting (no Redis)
- ✅ Debug mode enabled

**Run:**
```bash
cp .env.development .env
python run.py
# Visit: http://localhost:8000
```

---

### Staging (Docker + Redis)
**File:** `.env.staging`
**Use Case:** Testing before production

**Features:**
- 🐳 Docker containers (backend + Redis + Cloudflare Tunnel)
- 🔒 Real Redis for rate limiting
- 🌐 Cloudflare Tunnel (staging subdomain)

**Setup:**
```bash
cp .env.staging .env
# Edit .env and fill in:
# - SECRET_KEY (generate: python -c "import secrets; print(secrets.token_hex(32))")
# - REDIS_PASSWORD (use strong password)
# - CLOUDFLARE_TUNNEL_TOKEN (from Cloudflare dashboard)

docker-compose -f docker-compose.staging.yml up -d
```

---

### Production (Docker + Redis)
**File:** `.env.production`
**Use Case:** Live production deployment

**Domain:** Your production domain

**Features:**
- 🐳 Docker containers with health checks
- 🔒 Redis with persistence
- 🌐 Cloudflare Tunnel
- 🛡️ Security hardening (read-only filesystem, capability dropping)

**Setup:**
```bash
cp .env.production .env
# Edit .env and fill in:
# - SECRET_KEY (NEW random key, different from staging)
# - REDIS_PASSWORD (strong password)
# - CLOUDFLARE_TUNNEL_TOKEN (production tunnel)

docker-compose -f docker-compose.prod.yml up -d
```

---

## Environment Variables

| Variable | Development | Staging | Production |
|----------|-------------|---------|------------|
| `SECRET_KEY` | Any value | Random 64-char hex | Random 64-char hex (different from staging) |
| `REDIS_URL` | `memory://` | `redis://:password@redis:6379/0` | `redis://:password@redis:6379/0` |
| `REDIS_PASSWORD` | N/A | Strong password | Strong password |
| `CLOUDFLARE_TUNNEL_TOKEN` | N/A | Staging tunnel token | Production tunnel token |
| `FLASK_ENV` | `development` | `staging` | `production` |

---

## Important Notes

- **Never commit `.env` to git** - it's in `.gitignore`
- Use **different SECRET_KEY values** for each environment
- Use **different REDIS_PASSWORD values** for each environment
- Keep production credentials **completely separate** from staging
- The `.env.*` template files are gitignored - fill them in locally

---

## Deployment Workflow

**Development → Staging → Production**

1. **Develop locally:**
   ```bash
   cp .env.development .env
   python run.py
   ```

2. **Test in staging:**
   ```bash
   cp .env.staging .env
   # Fill in staging credentials
   docker-compose -f docker-compose.staging.yml up -d
   ```

3. **Deploy to production:**
   ```bash
   cp .env.production .env
   # Fill in production credentials
   docker-compose -f docker-compose.prod.yml up -d
   ```

---

## Stopping Services

```bash
# Stop development server:
# Press Ctrl+C in terminal

# Stop staging:
docker-compose -f docker-compose.staging.yml down

# Stop production:
docker-compose -f docker-compose.prod.yml down
```
