# Development Guide

Complete guide for running API Looter in **development mode** on your local machine.

## Recommended Development Workflow

**Development = Local (fastest iteration, instant hot reload)**
- No Docker needed
- Instant file change detection
- Memory-based rate limiting (no Redis)

**Staging Test = Docker Compose** (production-like environment for final testing before deploy)

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment File Management](#environment-file-management)
- [Quick Start](#quick-start)
- [Initial Setup](#initial-setup)
- [Daily Development Workflow](#daily-development-workflow)
- [Testing with Docker (Staging)](#testing-with-docker-staging)
- [Common Development Tasks](#common-development-tasks)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Python 3.11+** installed
- **Docker** (only for staging tests)
- **Git** for version control

**Note:** No database needed! This app uses static Python data structures.

---

## Environment File Management

**IMPORTANT:** This project uses environment-specific `.env` files that you copy into the standard `.env` before running.

### How It Works

The application **ALWAYS reads the standard `.env` file**.

The other files are **templates** you maintain and copy from:
- `.env.development` - Development settings (memory-based rate limiting)
- `.env.staging` - Staging settings (Docker + Redis)
- `.env.production` - Production settings (Docker + Redis + Cloudflare)

### Switching Environments

**Development (Local):**
```bash
cp .env.development .env
python run.py
```

**Staging (Docker):**
```bash
cp .env.staging .env
# Fill in: SECRET_KEY, REDIS_PASSWORD, CLOUDFLARE_TUNNEL_TOKEN
docker-compose -f docker-compose.staging.yml up -d
```

**Production (Docker):**
```bash
cp .env.production .env
# Fill in: SECRET_KEY, REDIS_PASSWORD, CLOUDFLARE_TUNNEL_TOKEN
docker-compose -f docker-compose.prod.yml up -d
```

### Why This Approach?

✅ **One source of truth** - Application always reads `.env`
✅ **Easy switching** - Just copy the environment you need
✅ **Safe** - Original templates stay unchanged
✅ **Clear** - Know exactly which environment you're using

**Remember:** The standard `.env` file is in `.gitignore` and never committed.

---

## Quick Start

**TL;DR - Get coding in 5 minutes:**

```bash
# STEP 1: Clone repository
git clone <your-repo-url>
cd api_looter

# STEP 2: Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# STEP 3: Install dependencies
pip install -r requirements.txt

# STEP 4: Set up environment
cp .env.development .env

# STEP 5: Run the app!
python run.py
```

**App:** http://localhost:8000

**That's it!** No database setup, no migrations, no Redis container for development.

---

## Initial Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd api_looter
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate it
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy development template
cp .env.development .env

# (Optional) Edit if you want to change SECRET_KEY
nano .env  # or code .env
```

**Default `.env.development` contents:**

```bash
# Development Environment
SECRET_KEY=19eb1b96290552d1dc675c84843f85f7da52543e172ae559b5964a6bf1b2f3ff
REDIS_URL=memory://
FLASK_ENV=development
FLASK_APP=run.py
```

**Key points:**
- `REDIS_URL=memory://` - No Redis container needed, rate limiting uses in-memory storage
- `FLASK_ENV=development` - Enables debug mode and hot reload
- `SECRET_KEY` - Default dev key (change for staging/production)

### 4. Run the Application

```bash
python run.py
```

You should see:

```
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.x.x:8000
 * Restarting with stat
 * Debugger is active!
```

**Visit:** http://localhost:8000

**File changes auto-reload instantly!**

---

## Daily Development Workflow

This is what you'll do every day when coding:

```bash
# 1. Navigate to project
cd /path/to/api_looter

# 2. Activate virtualenv
source venv/bin/activate

# 3. Ensure you're using dev environment
cp .env.development .env

# 4. Run the app
python run.py
```

**That's it!** Just one terminal, instant hot reload.

### Making Changes

**To add a new API:**

1. Edit `app/data.py`
2. Add your API to the `APIS` list
3. Save the file
4. Flask auto-reloads instantly!
5. Refresh browser to see changes

**Example:**

```python
# In app/data.py
APIS = [
    # ... existing APIs ...
    {
        "id": 15,
        "name": "My New API",
        "description": "Description of the API",
        "endpoint": "https://api.example.com/endpoint",
        "parameters": [],
        "why_use": "Why developers use this API",
        "how_use": "How developers use this API",
        "category": "Fun"
    }
]
```

**Domain whitelist updates automatically** - no manual changes needed!

---

## Testing with Docker (Staging)

Before deploying to production, test in a production-like environment.

**Staging uses:**
- Docker containers (backend + Redis)
- Real Redis for rate limiting
- Production-like network segmentation
- Cloudflare Tunnel (optional)

### Start Staging

```bash
# Copy staging environment
cp .env.staging .env

# Edit .env and fill in:
# - SECRET_KEY (generate: python -c "import secrets; print(secrets.token_hex(32))")
# - REDIS_PASSWORD (use strong password)
# - CLOUDFLARE_TUNNEL_TOKEN (optional for local staging)

# Start all services
docker-compose -f docker-compose.staging.yml up --build
```

**App:** http://localhost:5000 (or via Cloudflare Tunnel if configured)

### View Logs

```bash
# All services
docker-compose -f docker-compose.staging.yml logs -f

# Specific service
docker-compose -f docker-compose.staging.yml logs -f backend
docker-compose -f docker-compose.staging.yml logs -f redis
```

### Stop Staging

```bash
docker-compose -f docker-compose.staging.yml down
```

### Switch Back to Development

```bash
# Stop Docker
docker-compose -f docker-compose.staging.yml down

# Copy dev environment
cp .env.development .env

# Run locally
python run.py
```

---

## Common Development Tasks

### Update Dependencies

```bash
# Activate venv
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade Flask
```

### Check Security Headers (Local)

```bash
# Run the app
python run.py

# In another terminal, check headers
curl -I http://localhost:8000

# Should see:
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# X-XSS-Protection: 1; mode=block
# Referrer-Policy: strict-origin-when-cross-origin
```

### Test Rate Limiting (Local)

```bash
# Run the app
python run.py

# In another terminal, spam requests
for i in {1..35}; do curl -X POST http://localhost:8000/api/1 -d "{}"; done

# After 30 requests, you should see:
# {"error": "Too many requests. Please try again later.", "retry_after": 60}
```

### Validate APIs

```bash
# Run validation script
python validate_apis.py

# Should output:
# ✅ Validation passed!
# Total APIs: 14
# All APIs meet security requirements
```

### View Allowed Domains

```bash
# Run Python shell
python

>>> from app import create_app
>>> app = create_app()
>>> print(app.config['ALLOWED_API_DOMAINS'])
# Should show all auto-extracted domains
```

### Clean Cache Files

```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

---

## Code Quality

### Python Linting

This project follows PEP 8 style guidelines.

```bash
# Install flake8 (optional)
pip install flake8

# Check for issues
flake8 app/

# Auto-format with black (optional)
pip install black
black app/
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
FLASK_RUN_PORT=9000 python run.py
```

### "ModuleNotFoundError"

```bash
# Make sure virtualenv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# If still failing, recreate venv
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Changes Not Reflecting

```bash
# Make sure FLASK_ENV=development in .env
cat .env | grep FLASK_ENV

# Should show: FLASK_ENV=development

# If not, copy dev template again
cp .env.development .env

# Restart the app
# Ctrl+C to stop, then:
python run.py
```

### Template Not Updating

```bash
# Flask caches templates. Hard reload browser:
# - Chrome/Firefox: Ctrl + Shift + R
# - Mac: Cmd + Shift + R

# Or disable caching in .env (not recommended):
# TEMPLATES_AUTO_RELOAD=True
```

### Rate Limiting Not Working

```bash
# Check REDIS_URL in .env
cat .env | grep REDIS_URL

# For development, should be: memory://
# If you see redis:// URL, you need Redis running

# Option 1: Switch to memory-based (no Redis needed)
cp .env.development .env
python run.py

# Option 2: Start Redis with Docker
docker-compose -f docker-compose.staging.yml up redis -d
```

### Docker Issues (Staging)

```bash
# Rebuild containers
docker-compose -f docker-compose.staging.yml build --no-cache

# Remove all containers and volumes
docker-compose -f docker-compose.staging.yml down -v

# Start fresh
docker-compose -f docker-compose.staging.yml up --build
```

### Check if APIs Still Work

```bash
# Test a specific API (Dog CEO)
curl https://dog.ceo/api/breeds/image/random

# Should return JSON with image URL

# Test all APIs via the app
python run.py
# Visit http://localhost:8000
# Click on each API and test
```

---

## Environment Files Summary

**Your active config:**
- `.env` - Current active environment (gitignored)

**Template files (copy to .env as needed):**
- `.env.development` - Local development template
- `.env.staging` - Staging deployment template
- `.env.production` - Production deployment template

**Copy workflow:**
```bash
# For dev
cp .env.development .env
python run.py

# For staging test
cp .env.staging .env
docker-compose -f docker-compose.staging.yml up -d

# For production deploy
cp .env.production .env
docker-compose -f docker-compose.prod.yml up -d
```

---

## Project Structure Explained

```
api_looter/
├── app/
│   ├── __init__.py            # Flask app factory
│   │                          # - Security headers
│   │                          # - Rate limiting setup
│   │                          # - CSRF configuration
│   │                          # - Auto-domain extraction
│   │
│   ├── data.py                # ⭐ EDIT THIS TO ADD APIs!
│   │                          # - Static API list
│   │                          # - handler functions
│   │
│   ├── routes.py              # API endpoints
│   │                          # - Homepage (GET /)
│   │                          # - API detail (GET/POST /api/<id>)
│   │
│   ├── api_handlers.py         # API call handlers
│   │                          # - SSRF protection
│   │                          # - Request handling
│   │                          # - Response parsing
│   │
│   ├── static/                # CSS, JS, images
│   │   ├── style.css          # Main stylesheet
│   │   ├── script.js          # JSON syntax highlighting
│   │   └── images/            # Favicons, etc.
│   │
│   └── templates/             # HTML templates
│       ├── layout.html        # Base template
│       ├── index.html         # Homepage (API list)
│       └── api_detail.html    # API detail page
│
├── docs/                      # Documentation
├── .github/workflows/         # CI/CD automation
├── validate_apis.py           # Security validation
├── requirements.txt           # Python dependencies
├── run.py                     # App entry point
└── .env                       # Active environment (gitignored)
```

---

## Next Steps

- Make your changes
- Test locally: `python run.py`
- Test in staging: `docker-compose -f docker-compose.staging.yml up`
- Before deploying: See [PRODUCTION.md](./PRODUCTION.md)

Happy coding! 🚀
