---
name: dev-server
description: Manage development servers for vacay-photo-map. Use when starting, stopping, or checking status of postgres, frontend (Vite), or API (Bun) servers.
allowed-tools: Bash
---

# Dev Server Manager

Manages the three dev services: PostgreSQL, Frontend (Vite), and API (Bun/Hono).

## Quick Commands

### Check Status
```bash
.claude/hooks/check-dev-status.sh
```

### Start All Services
```bash
# Start postgres first (use the hook for proper wait)
.claude/hooks/start-dev.sh

# Or manually:
docker compose -p vacay-dev up -d postgres
# Wait for ready: docker compose -p vacay-dev exec -T postgres pg_isready -U vacay

# Start frontend and API (run in background)
pnpm dev &
pnpm dev:api &
```

### Start Individual Services
```bash
# Postgres only
docker compose -p vacay-dev up -d postgres

# Frontend only (localhost:5173)
pnpm dev

# API only (localhost:4000)
pnpm dev:api
```

### Stop All Services
```bash
.claude/hooks/cleanup-dev.sh
```

### Stop Individual Services
```bash
# Stop frontend/API (matches the pnpm commands)
pkill -f "pnpm dev"
pkill -f "pnpm dev:api"

# Stop postgres
docker compose -p vacay-dev down
```

## Service Details

| Service | Port | Command | Health Check |
|---------|------|---------|--------------|
| PostgreSQL | 5433 | `docker compose -p vacay-dev up -d postgres` | `docker compose -p vacay-dev ps` |
| Frontend | 5173 | `pnpm dev` | `curl -s localhost:5173` |
| API | 4000 | `pnpm dev:api` | `curl -s localhost:4000` |

## Dev Tunnel Mode

For mobile/WebAuthn testing via Cloudflare Tunnel:
- Frontend: https://photos-dev.joeczar.com
- API: https://photos-dev-api.joeczar.com

Same commands - tunnel is configured on server side.

## Troubleshooting

### Port already in use
```bash
# Find what's using the port
lsof -i :5173
lsof -i :4000

# Kill it
kill -9 <PID>
```

### Orphaned processes
```bash
# Run cleanup script
.claude/hooks/cleanup-dev.sh

# Or manually
pkill -f "pnpm dev"
pkill -f "pnpm dev:api"
```

### Database connection issues
```bash
# Check postgres logs
docker compose -p vacay-dev logs postgres

# Restart postgres
docker compose -p vacay-dev restart postgres
```
