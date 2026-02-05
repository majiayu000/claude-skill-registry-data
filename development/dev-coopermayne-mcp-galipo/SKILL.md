---
name: dev
description: Start/restart all development servers (backend, frontend, postgres) and verify they're working
---

# Development Server Startup

Start or restart all development services and verify each is working correctly.

## Services Overview

| Service | Port | Health Check |
|---------|------|--------------|
| PostgreSQL | 5432 | `psql` connection test |
| Backend (FastAPI) | 8000 | `GET /api/v1/chat/debug` |
| Frontend (Vite) | 5173 | HTTP 200 response |

## Startup Procedure

### Step 1: Check/Start PostgreSQL

```bash
# Check if postgres is running
pg_isready -h localhost -p 5432
```

If not running:
```bash
brew services start postgresql@14
# Or: brew services start postgresql
```

Wait 2 seconds, then verify:
```bash
pg_isready -h localhost -p 5432
```

### Step 2: Stop Existing Processes

```bash
# Kill any existing backend/frontend processes
kill -9 $(lsof -ti:8000) 2>/dev/null || true
kill -9 $(lsof -ti:5173) 2>/dev/null || true
sleep 1
```

### Step 3: Start Backend

**IMPORTANT:** Must source `.env` file for DATABASE_URL and other config.

```bash
cd /Users/coopermayne/Code/mcp-galipo
source .venv/bin/activate
set -a && source .env && set +a
uvicorn main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
```

Wait 3 seconds for startup, then verify:
```bash
curl -s http://localhost:8000/api/v1/chat/debug
```

Expected response: `{"status":"ok","message":"Chat routes are registered!"}`

If it fails, check logs:
```bash
tail -30 /tmp/backend.log
```

Common issues:
- **Address already in use**: Port 8000 not properly killed, retry kill command
- **Database connection error**: PostgreSQL not running or .env not sourced
- **Module not found**: Virtual environment not activated

### Step 4: Start Frontend

```bash
cd /Users/coopermayne/Code/mcp-galipo/frontend
npm run dev > /tmp/frontend.log 2>&1 &
```

Wait 2 seconds for startup, then verify:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173
```

Expected response: `200`

If it fails, check logs:
```bash
tail -20 /tmp/frontend.log
```

### Step 5: Final Verification Summary

Run all checks and report status:

```bash
echo "=== Dev Server Status ==="
echo ""

# PostgreSQL
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "PostgreSQL: OK (port 5432)"
else
    echo "PostgreSQL: FAILED"
fi

# Backend
BACKEND=$(curl -s http://localhost:8000/api/v1/chat/debug 2>/dev/null)
if [[ "$BACKEND" == *"ok"* ]]; then
    echo "Backend:    OK (port 8000)"
else
    echo "Backend:    FAILED - check /tmp/backend.log"
fi

# Frontend
FRONTEND=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null)
if [[ "$FRONTEND" == "200" ]]; then
    echo "Frontend:   OK (port 5173)"
else
    echo "Frontend:   FAILED - check /tmp/frontend.log"
fi

echo ""
echo "Frontend URL: http://localhost:5173"
```

## Quick Reference

### View Logs
```bash
tail -f /tmp/backend.log   # Backend logs
tail -f /tmp/frontend.log  # Frontend logs
```

### Stop All Services
```bash
kill -9 $(lsof -ti:8000) 2>/dev/null  # Stop backend
kill -9 $(lsof -ti:5173) 2>/dev/null  # Stop frontend
```

### Restart Just Backend
```bash
kill -9 $(lsof -ti:8000) 2>/dev/null
cd /Users/coopermayne/Code/mcp-galipo
source .venv/bin/activate && set -a && source .env && set +a
uvicorn main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
```

### Restart Just Frontend
```bash
kill -9 $(lsof -ti:5173) 2>/dev/null
cd /Users/coopermayne/Code/mcp-galipo/frontend
npm run dev > /tmp/frontend.log 2>&1 &
```

## Troubleshooting

### Backend won't start
1. Check if port is in use: `lsof -i:8000`
2. Check database: `pg_isready -h localhost -p 5432`
3. Verify .env exists: `cat /Users/coopermayne/Code/mcp-galipo/.env`
4. Check logs: `tail -50 /tmp/backend.log`

### Frontend won't start
1. Check if port is in use: `lsof -i:5173`
2. Check node_modules: `ls frontend/node_modules`
3. If missing: `cd frontend && npm install`
4. Check logs: `tail -50 /tmp/frontend.log`

### Database connection errors
1. Start postgres: `brew services start postgresql@14`
2. Check DATABASE_URL in .env matches your local setup
3. Verify database exists: `psql -l | grep galipo`

---

Execute these steps in order, reporting the final status summary to the user.
