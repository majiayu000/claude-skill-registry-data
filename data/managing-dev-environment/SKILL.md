---
name: managing-dev-environment
description: Use this skill when starting, stopping, or troubleshooting the development environment including managing backend/frontend services, handling port conflicts, setting up Docker vs SQLite modes, configuring Cloudflare tunnels, managing environment variables, regenerating TypeScript types, clearing caches, or diagnosing startup failures. Supports multiple modes (local, tunnel, SQLite, PostgreSQL).
---

You are an expert at managing the UFC Pokedex development environment, which supports multiple configurations and deployment modes.

# Environment Overview

The UFC Pokedex supports multiple development modes:

1. **Local Mode** (Default) - Backend + Frontend on localhost
2. **Tunnel Mode** - Backend + Frontend exposed via Cloudflare tunnels
3. **SQLite Mode** - Lightweight database (no Docker required)
4. **PostgreSQL Mode** - Production-like database (requires Docker)

# When to Use This Skill

Invoke this skill when the user wants to:
- Start/stop development servers
- Switch between environment modes
- Troubleshoot startup failures
- Resolve port conflicts
- Configure Cloudflare tunnels
- Manage environment variables
- Clear build caches
- Regenerate TypeScript types
- Check service health
- Reset development environment

# Quick Start Commands

## Start Development Environment

### Option 1: Local Development (Recommended)
Backend + Frontend on localhost (no tunnels, no env file changes).

**Command:**
```bash
make dev-local
```

**Ports:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Database: PostgreSQL on localhost:5432 (via Docker)

**Best for:**
- Daily development
- No need for public URLs
- Fastest startup

### Option 2: With Cloudflare Tunnels
Backend + Frontend exposed via public URLs.

**Command:**
```bash
make dev
```

**URLs:**
- Backend: https://api.ufc.wolfgangschoenberger.com
- Frontend: https://ufc.wolfgangschoenberger.com

**Best for:**
- Testing on mobile devices
- Sharing work with others
- Testing webhooks or external services

**Note:** Auto-configures environment variables in `.env` and `frontend/.env.local`

### Option 3: SQLite Mode (No Docker)
Lightweight development without PostgreSQL.

**Command:**
```bash
make api:dev
```

**What it does:**
- Uses SQLite database at `data/app.db`
- No Docker required
- Auto-creates tables on startup
- Perfect for quick testing

**Best for:**
- Quick prototyping
- When Docker isn't available
- Testing with small datasets

**Limitations:**
- Single-writer (no concurrency)
- Full dataset blocked (10K+ fighters)
- Alembic migrations not supported

### Option 4: Frontend Only
Start just the frontend (backend must be running separately).

**Command:**
```bash
make frontend
```

**Port:** http://localhost:3000

## Stop Development Environment

**Command:**
```bash
make stop
```

**What it stops:**
- Backend (port 8000)
- Frontend (port 3000)
- Cloudflare tunnels
- Background processes

## Clean and Restart

If you encounter webpack cache issues, module not found errors, or chunk 404s:

**Command:**
```bash
make dev-clean
```

**What it does:**
- Stops all services
- Removes `frontend/.next` directory
- Removes `frontend/node_modules/.cache`
- Clears npm cache
- Reinstalls dependencies
- Restarts dev servers

**Use when:**
- Webpack cache corruption
- MODULE_NOT_FOUND errors
- Chunk loading failures (404s)
- Strange build behavior

# Environment Modes Explained

## Docker vs SQLite

### PostgreSQL (Docker) Mode
**Pros:**
- Production-like environment
- Supports full dataset (10K+ fighters)
- Alembic migrations work
- Better concurrency

**Setup:**
```bash
# Start PostgreSQL
docker-compose up -d

# Run migrations
make db-upgrade

# Start backend
make api
```

**Environment variables:**
```bash
DATABASE_URL=postgresql+psycopg://ufc_pokedex:ufc_pokedex@localhost:5432/ufc_pokedex
```

### SQLite Mode
**Pros:**
- No Docker required
- Faster startup
- Simpler setup
- Great for quick testing

**Setup:**
```bash
# Just start the backend (SQLite auto-configured if DATABASE_URL not set)
make api:dev

# Or force SQLite mode even if DATABASE_URL is set
make api:sqlite
```

**Environment variables:**
```bash
# Option 1: Unset DATABASE_URL (auto-detects SQLite)
# No environment variable needed

# Option 2: Force SQLite
USE_SQLITE=1

# SQLite database location
# DATABASE_URL=sqlite+aiosqlite:///./data/app.db
```

**Auto-detects:** If `DATABASE_URL` is not set, automatically uses `sqlite+aiosqlite:///./data/app.db`

## Localhost vs Tunnel Mode

### Localhost Mode (dev-local)
**Pros:**
- Faster (no tunnel overhead)
- Private (not exposed to internet)
- No environment file changes
- Simpler

**Cons:**
- Can't test on external devices
- Can't share with others

**Use case:** Daily development

### Tunnel Mode (dev)
**Pros:**
- Public URLs for testing
- Works on mobile devices
- Can share with others
- Tests production-like setup

**Cons:**
- Slower (tunnel overhead)
- Modifies environment files
- Requires Cloudflare authentication

**Use case:** Cross-device testing, demos

# Service Management

## Start Individual Services

### Backend Only (PostgreSQL)
```bash
make api
```

### Backend Only (SQLite)
```bash
make api:dev    # Auto-detects SQLite if DATABASE_URL not set
make api:sqlite # Forces SQLite even if DATABASE_URL set
```

### Frontend Only
```bash
make frontend
```

### Cloudflare Tunnels Only
```bash
# Frontend tunnel (port 3000)
make tunnel-frontend

# Backend tunnel (port 8000)
make tunnel-api

# Stop all tunnels
make tunnel-stop
```

## Check Service Status

### Check if services are running:
```bash
# Backend (port 8000)
lsof -ti :8000

# Frontend (port 3000)
lsof -ti :3000

# Cloudflare tunnels
ps aux | grep cloudflared

# Docker (PostgreSQL)
docker ps

# Redis
redis-cli ping
```

### Test endpoints:
```bash
# Backend health check
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000

# Database connection
PGPASSWORD=ufc_pokedex psql -h localhost -U ufc_pokedex -d ufc_pokedex -c "SELECT 1;"

# Redis
redis-cli ping
```

# Environment Variables

## Backend (.env)

**Required for PostgreSQL mode:**
```bash
DATABASE_URL=postgresql+psycopg://ufc_pokedex:ufc_pokedex@localhost:5432/ufc_pokedex
```

**Optional:**
```bash
# Force SQLite mode
USE_SQLITE=1

# Redis cache (optional - gracefully degrades if unavailable)
REDIS_URL=redis://localhost:6379/0

# API server
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# CORS (auto-configured by make dev)
CORS_ALLOW_ORIGINS=http://localhost:3000

# Scraper settings
SCRAPER_USER_AGENT=UFC-Pokedex-Scraper/0.1
SCRAPER_DELAY_SECONDS=1.5
SCRAPER_CONCURRENT_REQUESTS=4
```

## Frontend (frontend/.env.local)

**Required:**
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**For tunnel mode (auto-configured by make dev):**
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.ufc.wolfgangschoenberger.com
```

## Check Environment Variables

```bash
# Backend
cat .env

# Frontend
cat frontend/.env.local

# Check if set in environment
echo $DATABASE_URL
echo $NEXT_PUBLIC_API_BASE_URL
```

# Cloudflare Tunnel Setup

## One-Time Setup

**Command:**
```bash
bash scripts/setup_tunnel.sh
```

**What it does:**
1. Authenticates with Cloudflare (opens browser)
2. Creates tunnel named `ufc-pokedex`
3. Sets up DNS routes for subdomains
4. Generates config file at `~/.cloudflared/config.yml`

**You only need to run this once!**

## Check Tunnel Status

```bash
# List all tunnels
cloudflared tunnel list

# Get tunnel details
cloudflared tunnel info ufc-pokedex

# Check DNS routes
cloudflared tunnel route dns list

# Check tunnel logs
tail -f /tmp/tunnel.log

# Test connectivity
curl https://api.ufc.wolfgangschoenberger.com/health
curl https://ufc.wolfgangschoenberger.com

# Verify DNS propagation
nslookup ufc.wolfgangschoenberger.com
nslookup api.ufc.wolfgangschoenberger.com
```

## Troubleshooting Tunnels

### Issue: Tunnel not starting
**Solutions:**
```bash
# Check if cloudflared is installed
which cloudflared

# Reinstall if needed
brew install cloudflare/cloudflare/cloudflared

# Check authentication
cloudflared tunnel list

# Re-run setup
bash scripts/setup_tunnel.sh
```

### Issue: DNS not resolving
**Solutions:**
```bash
# Check DNS propagation
nslookup ufc.wolfgangschoenberger.com

# Wait 5-10 minutes for DNS propagation
# Or flush DNS cache
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

### Issue: Tunnel connects but can't reach service
**Solutions:**
```bash
# Verify backend is running on port 8000
lsof -ti :8000

# Verify frontend is running on port 3000
lsof -ti :3000

# Check tunnel configuration
cat ~/.cloudflared/config.yml
```

# TypeScript Type Generation

The project uses OpenAPI → TypeScript code generation for type safety.

## Regenerate Types

**Command:**
```bash
make types-generate
```

**Prerequisite:** Backend must be running (needs `/openapi.json` endpoint)

**What it does:**
1. Fetches OpenAPI schema from `http://localhost:8000/openapi.json`
2. Generates TypeScript types using `openapi-typescript`
3. Outputs to `frontend/src/lib/generated/api-schema.ts`

**Auto-generates:** Types are automatically generated when you run `make dev` or `make dev-local`

## Check if Types are Stale

```bash
# Check when types were last generated
ls -lh frontend/src/lib/generated/api-schema.ts

# Check for TypeScript errors
cd frontend && npx tsc --noEmit
```

# Port Conflict Resolution

## Check What's Using Ports

```bash
# Check port 8000 (backend)
lsof -ti :8000

# Check port 3000 (frontend)
lsof -ti :3000

# Kill process on port 8000
lsof -ti :8000 | xargs kill -9

# Kill process on port 3000
lsof -ti :3000 | xargs kill -9
```

**Note:** `make dev`, `make api`, and `make frontend` automatically kill existing processes on their ports.

# Database Management

## Start PostgreSQL (Docker)

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Check if running
docker ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## SQLite (No Docker)

```bash
# Just start the backend - SQLite auto-configured
make api:dev

# Check SQLite database
ls -lh data/app.db

# Query SQLite
sqlite3 data/app.db "SELECT COUNT(*) FROM fighters;"
```

## Run Migrations (PostgreSQL only)

```bash
# Apply pending migrations
make db-upgrade

# Rollback last migration
make db-downgrade

# Reset database (⚠️ destroys data!)
make db-reset
```

**Note:** Alembic migrations do NOT work with SQLite mode. SQLite uses `create_all()` instead.

## Seed Database

```bash
# Seed with 8 sample fighters (works on SQLite)
make api:seed

# Seed with all fighters (PostgreSQL recommended)
make load-data

# Seed with all fighters (SQLite - requires override)
ALLOW_SQLITE_PROD_SEED=1 make api:seed-full
```

# Troubleshooting

## Issue: "Port already in use"

**Solution:**
```bash
# Stop all services
make stop

# Or kill specific ports
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9

# Restart
make dev-local
```

## Issue: "Module not found" or webpack cache errors

**Solution:**
```bash
make dev-clean
```

## Issue: "Database connection failed"

**Solutions:**
```bash
# Check if PostgreSQL is running
docker ps

# Start PostgreSQL
docker-compose up -d

# Check connection
PGPASSWORD=ufc_pokedex psql -h localhost -U ufc_pokedex -d ufc_pokedex -c "SELECT 1;"

# Or switch to SQLite
make api:sqlite
```

## Issue: "TypeScript errors about API types"

**Solution:**
```bash
# Make sure backend is running
make api

# Regenerate types
make types-generate

# Check for errors
cd frontend && npx tsc --noEmit
```

## Issue: "Redis connection failed"

**Note:** Redis is optional! Backend gracefully degrades.

**Solution (if you want Redis):**
```bash
# Start Redis
docker-compose up -d redis

# Check connection
redis-cli ping

# If Redis not available, backend will log warning and continue without cache
```

## Issue: "Frontend shows old data after API changes"

**Solutions:**
```bash
# 1. Clear Redis cache (if using Redis)
redis-cli FLUSHDB

# 2. Regenerate types
make types-generate

# 3. Restart frontend
make frontend
```

## Issue: "Cloudflare tunnel not connecting"

**Solutions:**
```bash
# Check tunnel status
cloudflared tunnel list

# Check logs
tail -f /tmp/tunnel.log

# Restart tunnel
make tunnel-stop
make dev
```

## Issue: Environment variable mismatch

**Symptoms:**
- Frontend can't reach backend
- CORS errors
- 404 on API calls

**Solution:**
```bash
# Check current settings
cat .env
cat frontend/.env.local

# For local development
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > frontend/.env.local
echo "CORS_ALLOW_ORIGINS=http://localhost:3000" > .env

# For tunnel mode
make dev  # Auto-configures both files
```

# Complete Diagnostic Workflow

When something isn't working, run through this checklist:

```bash
# 1. Check if services are running
lsof -ti :8000  # Backend
lsof -ti :3000  # Frontend
docker ps       # PostgreSQL

# 2. Test endpoints
curl http://localhost:8000/health
curl http://localhost:3000

# 3. Check environment variables
cat .env
cat frontend/.env.local

# 4. Check database connection
PGPASSWORD=ufc_pokedex psql -h localhost -U ufc_pokedex -d ufc_pokedex -c "SELECT 1;"
# OR
sqlite3 data/app.db "SELECT 1;"

# 5. Check logs
tail -f /tmp/backend.log
tail -f /tmp/frontend.log

# 6. If still broken, clean restart
make stop
make dev-clean
```

# Environment Reset Workflow

To completely reset your development environment:

```bash
# 1. Stop everything
make stop
docker-compose down

# 2. Clean caches
make dev-clean

# 3. Reset database (⚠️ destroys data!)
docker-compose down -v
docker-compose up -d
make db-upgrade

# 4. Reseed database
make api:seed  # Sample data
# OR
make load-data  # Full data

# 5. Restart services
make dev-local
```

# Best Practices

1. **Use dev-local for daily work** - Faster, simpler, no tunnel overhead
2. **Use dev for demos/mobile testing** - When you need public URLs
3. **Use SQLite for quick prototyping** - No Docker overhead
4. **Use PostgreSQL for realistic testing** - Production-like environment
5. **Run make stop before switching modes** - Prevents port conflicts
6. **Check environment variables** - Ensure frontend/backend URLs match
7. **Regenerate types after API changes** - Keeps TypeScript in sync
8. **Use dev-clean when webpack acts weird** - Solves 90% of cache issues
9. **Monitor logs during development** - `tail -f /tmp/backend.log`
10. **Test tunnel setup once** - Run `scripts/setup_tunnel.sh` on new machine

# Quick Reference

```bash
# Start development (localhost)
make dev-local

# Start development (with tunnels)
make dev

# Stop everything
make stop

# Clean and restart
make dev-clean

# Individual services
make api          # Backend (PostgreSQL)
make api:dev      # Backend (SQLite auto-detect)
make api:sqlite   # Backend (SQLite forced)
make frontend     # Frontend only

# Database
docker-compose up -d   # Start PostgreSQL
make db-upgrade        # Run migrations
make api:seed          # Seed sample data

# Types
make types-generate    # Regenerate TypeScript types

# Diagnostics
lsof -ti :8000         # Check backend port
lsof -ti :3000         # Check frontend port
curl localhost:8000/health  # Test backend
docker ps              # Check Docker services
```

# Related Skills

- See `scraping-data-pipeline` skill for scraping and loading data
- See `managing-fighter-images` skill for image management
