---
name: interactive-dev
description: Interactive Development — Institutional capability and runbook for interactive-dev.
---

# SKILL: Interactive Development
## Domain: Full-Stack Live Debugging — UI → Backend → Database

**Activation triggers:** interactive dev, live debugging, full-stack debug, run all services,
capture logs, browser logs, backend logs, postgres logs, reproduce bug, end-to-end debug,
dev runner, watch mode, hot reload, inspect network, inspect error, dev session, stack trace,
frontend error, backend error, 500 error, CORS debug, WebSocket debug, UI bug.

---

## What This Skill Does

The Interactive Dev skill gives the agent **complete visibility** across the entire running
stack — browser, Vite proxy, all three backends, PostgreSQL — so bugs can be reproduced,
traced, and fixed without switching tools.

**Core capabilities:**
1. One-command full-stack launch (dev_runner.py)
2. Simultaneous log tailing from all services
3. Browser network/console capture via Claude-in-Chrome
4. Live PostgreSQL session monitoring
5. End-to-end bug reproduction workflow
6. Hot-reload-aware development loop

---

## Quick Start — Full Stack in One Command

```bash
ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"

# Launch all services + stream all logs
python3 "$ROOT/software-factory/context-engine/dev_runner.py" --start-all --follow

# Just health check (all services must already be running)
python3 "$ROOT/software-factory/context-engine/dev_runner.py" --health

# Watch mode — restart on failure, re-stream logs
python3 "$ROOT/software-factory/context-engine/dev_runner.py" --start-all --watch
```

---

## Service Launch Reference

### Infrastructure (must be first)
```bash
# Verify PostgreSQL and Redis are up
pg_isready -h localhost -p 5432 || sudo systemctl start postgresql
redis-cli -p 6380 ping || sudo systemctl start redis
```

### Market Backend (:8000)
```bash
cd "$ROOT/integral-market-backend"
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload \
  > /tmp/market-backend.log 2>&1 &
echo "Market PID: $!"
```

### Expert Backend (:8002) — Podman (ppc/macOS) or Docker
```bash
cd "$ROOT/integral-expert-backend"
# Podman:
podman compose up -d expert-backend
# Docker:
docker compose up -d expert-backend
```

### IMI Backend (:8003)
```bash
cd "$ROOT/integral-market-intelligence"
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload \
  > /tmp/imi-backend.log 2>&1 &
```

### Frontend (:5173)
```bash
cd "$ROOT/app"
nohup pnpm dev > /tmp/frontend.log 2>&1 &
```

---

## Log Streaming — All Services Simultaneously

```bash
# Stream all logs in one terminal (color-coded by service)
tail -f \
  /tmp/market-backend.log \
  /tmp/imi-backend.log \
  /tmp/frontend.log \
  | awk '
    /market-backend/ { print "\033[34m[MARKET]\033[0m " $0 }
    /imi-backend/    { print "\033[35m[IMI]\033[0m " $0 }
    /frontend/       { print "\033[36m[FRONT]\033[0m " $0 }
    { print $0 }
  '

# Expert backend (container):
podman logs -f integral-expert-backend &

# PostgreSQL queries in real time:
sudo tail -f /var/log/postgresql/postgresql-*.log | grep -v "^$"
```

---

## Browser Debug Protocol

### Using Claude-in-Chrome (agent-driven)

```
1. mcp__Claude_in_Chrome__navigate to http://localhost:5173
2. mcp__Claude_in_Chrome__read_console_messages  → capture JS errors
3. mcp__Claude_in_Chrome__read_network_requests  → capture XHR/fetch calls + status codes
4. mcp__Claude_in_Chrome__find the failing element (CSS selector)
5. mcp__Claude_in_Chrome__screenshot for visual context
6. mcp__Claude_in_Chrome__javascript_tool to run: window.__REACT_QUERY_GLOBALCACHE__
```

### Network Request Inspection Pattern

After reproducing a bug, capture the full request/response cycle:

```javascript
// Paste in browser console to intercept all fetch calls:
const _fetch = window.fetch;
window.fetch = async (...args) => {
  console.log('[FETCH]', args[0], args[1]?.method || 'GET');
  const res = await _fetch(...args);
  const clone = res.clone();
  const body = await clone.text();
  console.log('[RESPONSE]', res.status, body.slice(0, 500));
  return res;
};
```

---

## End-to-End Bug Reproduction Workflow

```
STEP 1 — Reproduce the bug
  mcp__Claude_in_Chrome__navigate to the failing page
  mcp__Claude_in_Chrome__read_console_messages
  mcp__Claude_in_Chrome__read_network_requests
  → Identify: which API call fails? What status code?

STEP 2 — Trace to backend
  tail -f /tmp/market-backend.log | grep "ERROR\|CRITICAL\|Traceback"
  podman logs integral-expert-backend --tail 50
  → Identify: which route? Which exception?

STEP 3 — Trace to database (if needed)
  # Enable PostgreSQL query logging temporarily:
  psql -U postgres -c "ALTER SYSTEM SET log_statement = 'all';"
  psql -U postgres -c "SELECT pg_reload_conf();"
  sudo tail -f /var/log/postgresql/postgresql-*.log | grep -v "autovacuum"
  → Identify: missing index? Bad join? N+1?

STEP 4 — Fix and verify
  # Backend fix → hot reload picks it up automatically (--reload flag)
  # Frontend fix → Vite HMR refreshes instantly
  mcp__Claude_in_Chrome__navigate (refresh)
  mcp__Claude_in_Chrome__read_console_messages → should be clean
  curl http://localhost:8000/health → should return 200

STEP 5 — Revert PostgreSQL query logging (IMPORTANT)
  psql -U postgres -c "ALTER SYSTEM SET log_statement = 'none';"
  psql -U postgres -c "SELECT pg_reload_conf();"
```

---

## Live PostgreSQL Monitoring

```bash
# Active queries (run this while reproducing a bug):
psql -U postgres -d integral_market -c "
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;"

# Slow query log (live):
psql -U postgres -c "
SELECT query, calls, total_exec_time/calls AS avg_ms, rows
FROM pg_stat_statements
ORDER BY avg_ms DESC
LIMIT 20;"

# Table sizes:
psql -U postgres -d integral_market -c "
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;"

# Lock contention:
psql -U postgres -d integral_market -c "
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
WHERE NOT blocked_locks.granted;"
```

---

## Common Bug Patterns and Fixes

### HTTP 500 with CORS — No CORS headers on error response
```
Root cause: CORSMiddleware does not wrap unhandled exceptions
Fix: Global exception handler that returns JSONResponse (not raw exception)
Location: app/main.py — @app.exception_handler(Exception)
Verify: curl -H "Origin: http://localhost:5173" -v http://localhost:8000/broken
```

### 401 Unauthorized on every request
```
Root cause: JWT token not sent OR cookie not included in CORS
Fix: Check fetch() includes credentials: 'include' for cookie auth
     OR check Authorization: Bearer <token> header is attached
Verify: mcp__Claude_in_Chrome__read_network_requests → check request headers
```

### TypeScript type error blocking compilation
```
Fix: cd app && pnpm type-check → find the file
     Update the TS type to match the backend Pydantic schema
     Both must change together — never update one without the other
```

### WebSocket connection refused
```
Root cause: Vite proxy ws: true not set, or backend not running
Fix: Check vite.config.ts → /ws/expert points to :8002, ws: true
     Check: podman logs integral-expert-backend | grep "WebSocket"
     Test: wscat -c ws://localhost:5173/ws/expert
```

### Alembic migration out of sync
```
cd integral-expert-backend && source venv/bin/activate
alembic check  → shows what's missing
alembic upgrade head
alembic check  → should print "OK"
```

---

## Interactive Dev Loop — Best Practice

```
OUTER LOOP (per feature):
  1. Start dev_runner.py --start-all --watch
  2. Open Claude-in-Chrome pointed at localhost:5173
  3. Open a PostgreSQL monitor in a separate pane

INNER LOOP (per change):
  1. Edit file → hot reload fires
  2. mcp__Claude_in_Chrome__read_console_messages → check for JS errors
  3. mcp__Claude_in_Chrome__read_network_requests → check API responses
  4. Check backend log for exceptions
  5. If DB change: alembic upgrade head first, then reload
  6. When feature works → run pnpm type-check + alembic check
```

---

## Health Check Script

```bash
python3 software-factory/context-engine/dev_runner.py --health
```

Outputs:
```
✅ PostgreSQL    :5432  accepting connections
✅ Redis         :6380  PONG
✅ Market        :8000  {"status":"ok"}
✅ Expert        :8002  {"status":"ok"}
✅ IMI           :8003  {"status":"ok"}
✅ Frontend      :5173  HTTP 200
```

---

## Anti-Patterns

```
✗ Tailing only one log (bugs span service boundaries)
✗ Leaving PostgreSQL log_statement='all' in production (massive I/O)
✗ console.log debugging — use structured logger + read_console_messages
✗ Testing in production DB — always use dev/test DB
✗ Killing backends with SIGKILL — uvicorn needs SIGTERM for graceful shutdown
✗ Not disabling hot-reload in load tests (causes race conditions)
✗ Hardcoding localhost:800X in frontend (breaks Vite proxy)
```
