# Production Deployment Guide

Guide for deploying API Looter to production.

---

## Production Architecture

- **Backend:** Flask + Gunicorn (WSGI server)
- **Data Storage:** Static Python data structure (no database!)
- **Redis:** Docker container for rate limiting
- **CDN/Proxy:** Cloudflare Tunnel (HTTPS, DDoS protection)
- **Web Server:** Gunicorn inside Docker container

---

## Prerequisites

- VPS server (Ubuntu 20.04+ recommended)
- Domain name configured in Cloudflare
- Docker and Docker Compose installed
- Cloudflare Tunnel created

---

## Quick Start

### 1. Clone Repository on Server

```bash
ssh user@your-server
cd /opt
sudo git clone https://github.com/ComputerAnything/api_looter.git
cd api_looter
```

### 2. Configure Environment

```bash
# Copy production template
cp .env.production .env

# Edit with your production values
nano .env
```

**Edit `.env` with production credentials:**

```bash
# Flask Configuration
SECRET_KEY=<generate-random-64-char-hex>
FLASK_ENV=production

# Redis Configuration (for rate limiting)
REDIS_PASSWORD=<generate-strong-password>
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0

# Cloudflare Tunnel
CLOUDFLARE_TUNNEL_TOKEN=<your-tunnel-token>
```

**Generate strong SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Deploy with Docker Compose

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. Verify Deployment

```bash
# Check containers are running
docker-compose -f docker-compose.prod.yml ps

# Should show:
# - backend (healthy)
# - redis (healthy)
# - cloudflared (running)
```

---

## Cloudflare Tunnel Setup

### Create Tunnel (One-Time Setup)

1. **Go to Cloudflare Zero Trust Dashboard**
   - Navigate to Access > Tunnels
   - Click "Create a tunnel"
   - Name it: `api-looter-production`

2. **Install Connector** - We use Docker, so:
   - Click "Docker" as connector type
   - Copy the tunnel token

3. **Configure Public Hostname**
   - Hostname: `apilooter.yourdom ain.com`
   - Service: `http://backend:8000`
   - Save tunnel

4. **Add Token to `.env`**
   ```bash
   CLOUDFLARE_TUNNEL_TOKEN=eyJh...your-token-here
   ```

5. **Restart Services**
   ```bash
   docker-compose -f docker-compose.prod.yml restart cloudflared
   ```

### DNS Configuration

In Cloudflare DNS:
- The tunnel automatically creates a CNAME record
- Verify it points to `<tunnel-id>.cfargotunnel.com`

---

## Production Configuration

### docker-compose.prod.yml

The production compose file includes:

**Security Features:**
- Read-only root filesystem
- Non-root user
- Capability dropping
- Network isolation
- Resource limits

**Services:**
- `backend` - Flask app (Gunicorn, 4 workers)
- `redis` - Rate limit storage (persisted)
- `cloudflared` - Cloudflare Tunnel

### Gunicorn Configuration

Production runs with Gunicorn (configured in `Dockerfile`):

```bash
gunicorn -b 0.0.0.0:8000 -w 4 --timeout 120 run:app
```

- **Workers:** 4 (adjust based on CPU cores: `2 * cores + 1`)
- **Timeout:** 120 seconds
- **Bind:** Port 8000 (internal, exposed via Cloudflare Tunnel)

---

## Security Checklist

Before going live, verify:

- [ ] `.env` has strong `SECRET_KEY` (64+ random hex characters)
- [ ] `REDIS_PASSWORD` is strong and unique
- [ ] `CLOUDFLARE_TUNNEL_TOKEN` is set correctly
- [ ] Cloudflare tunnel is active and routing traffic
- [ ] HSTS header enabled (automatic in production)
- [ ] CSP header configured (automatic)
- [ ] Rate limiting working with real Redis
- [ ] All containers have health checks passing

### Test Production Security

From your local machine:

```bash
# Test security headers
curl -I https://apilooter.yourdomain.com

# Should see:
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# Strict-Transport-Security: max-age=31536000
# Content-Security-Policy: ...

# Test rate limiting
for i in {1..12}; do curl -X POST https://apilooter.yourdomain.com/api/1 -d "{}"; done

# After 10 requests, should see:
# <h1>⏱️ Rate Limited</h1>
```

---

## Monitoring

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f redis
docker-compose -f docker-compose.prod.yml logs -f cloudflared
```

### Health Checks

```bash
# Check backend health
curl https://apilooter.yourdomain.com

# Check Redis connection
docker-compose -f docker-compose.prod.yml exec redis redis-cli -a $REDIS_PASSWORD ping
# Should return: PONG

# Check container health
docker-compose -f docker-compose.prod.yml ps
# All should show "healthy" or "running"
```

### Resource Usage

```bash
# Check resource usage
docker stats

# Check disk usage
docker system df

# Check Redis memory
docker-compose -f docker-compose.prod.yml exec redis redis-cli -a $REDIS_PASSWORD INFO memory
```

---

## Maintenance

### Updating the Application

```bash
# Pull latest code
cd /opt/api_looter
sudo git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up --build -d

# Check logs for any errors
docker-compose -f docker-compose.prod.yml logs -f
```

### Backup Redis Data (Rate Limits)

Redis data is persisted in Docker volume `redis_data`:

```bash
# Backup Redis data
docker run --rm -v api_looter_redis_data:/data -v $(pwd):/backup ubuntu tar czf /backup/redis-backup-$(date +%Y%m%d).tar.gz /data

# Restore Redis data (if needed)
docker run --rm -v api_looter_redis_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/redis-backup-YYYYMMDD.tar.gz -C /
```

**Note:** Rate limit data is ephemeral - backups aren't critical.

### Clean Up Old Images

```bash
# Remove unused Docker images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove all stopped containers
docker container prune
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Common issues:
# - Missing .env file → cp .env.production .env
# - Invalid SECRET_KEY → regenerate with: python -c "import secrets; print(secrets.token_hex(32))"
# - Port conflict → check if port 8000 is in use
```

### Cloudflare Tunnel Not Working

```bash
# Check cloudflared logs
docker-compose -f docker-compose.prod.yml logs cloudflared

# Common issues:
# - Invalid CLOUDFLARE_TUNNEL_TOKEN → regenerate in Cloudflare dashboard
# - Tunnel not active → activate in Cloudflare dashboard
# - DNS not propagated → wait 5-10 minutes
```

### Redis Connection Failed

```bash
# Check Redis is running
docker-compose -f docker-compose.prod.yml ps redis

# Check Redis password
docker-compose -f docker-compose.prod.yml exec redis redis-cli -a $REDIS_PASSWORD ping

# If password wrong:
# 1. Update REDIS_PASSWORD in .env
# 2. Restart: docker-compose -f docker-compose.prod.yml restart redis backend
```

### Rate Limiting Not Working

```bash
# Check Redis connection
docker-compose -f docker-compose.prod.yml logs backend | grep -i redis

# Check REDIS_URL in .env
cat .env | grep REDIS_URL
# Should be: redis://:password@redis:6379/0

# Test Redis from backend
docker-compose -f docker-compose.prod.yml exec backend python -c "import redis; r=redis.from_url('redis://:password@redis:6379/0'); print(r.ping())"
# Should return: True
```

### 502 Bad Gateway

```bash
# Check backend health
docker-compose -f docker-compose.prod.yml exec backend curl localhost:8000
# Should return HTML

# Check Gunicorn workers
docker-compose -f docker-compose.prod.yml logs backend | grep "Booting worker"
# Should see 4 workers starting

# Restart backend
docker-compose -f docker-compose.prod.yml restart backend
```

---

## Scaling

### Horizontal Scaling

To handle more traffic, increase Gunicorn workers:

**Edit `Dockerfile`:**
```dockerfile
# Change from -w 4 to -w 8
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "8", "--timeout", "120", "run:app"]
```

Rebuild:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

**Rule of thumb:** `workers = (2 * CPU_cores) + 1`

### Redis Optimization

For high-traffic sites, adjust Redis memory:

**Edit `docker-compose.prod.yml`:**
```yaml
redis:
  command: >
    redis-server
    --maxmemory 256mb  # Increase from 128mb
    --maxmemory-policy allkeys-lru
```

---

## Rollback

If deployment has issues, rollback to previous version:

```bash
# Stop current version
docker-compose -f docker-compose.prod.yml down

# Checkout previous version
git log --oneline  # Find commit hash
git checkout <previous-commit-hash>

# Redeploy
docker-compose -f docker-compose.prod.yml up --build -d
```

---

## Production vs Staging vs Development

| Feature | Development | Staging | Production |
|---------|-------------|---------|------------|
| **Environment** | Local (no Docker) | Docker Compose | Docker Compose |
| **Redis** | Memory (`memory://`) | Redis container | Redis container (persisted) |
| **Rate Limiting** | In-memory | Real Redis | Real Redis |
| **Hot Reload** | ✅ Yes (Flask debug) | ❌ No | ❌ No |
| **HTTPS** | ❌ No (localhost) | ✅ Yes (Cloudflare) | ✅ Yes (Cloudflare) |
| **Security Headers** | ⚠️ Partial (no HSTS) | ✅ Full | ✅ Full |
| **Gunicorn Workers** | N/A | 2-4 | 4-8 |
| **Domain** | localhost:8000 | staging.domain.com | domain.com |

---

## Security Best Practices

### Secrets Management

- ❌ **NEVER commit `.env` to git**
- ✅ Use strong random secrets (64+ hex characters)
- ✅ Different secrets for staging vs production
- ✅ Rotate secrets regularly (quarterly)

### Server Hardening

```bash
# Enable UFW firewall
sudo ufw enable
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP (Cloudflare)
sudo ufw allow 443/tcp # HTTPS (Cloudflare)

# Keep system updated
sudo apt update && sudo apt upgrade -y

# Enable automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Docker Security

```bash
# Run Docker daemon in rootless mode (optional, advanced)
dockerd-rootless-setuptool.sh install

# Limit container resources in docker-compose.prod.yml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

---

## Next Steps

After deployment:

1. ✅ Test all APIs work via your production domain
2. ✅ Verify rate limiting (try 12 POST requests)
3. ✅ Check security headers (`curl -I https://yourdomain.com`)
4. ✅ Monitor logs for 24 hours for errors
5. ✅ Set up monitoring/alerts (optional: UptimeRobot, Better Uptime)
6. ✅ Document your specific domain/credentials in a private wiki

---

*Last Updated: January 2026*
