---
name: run-meal-advice
description: Run Gram meal tracker with hot-reload development servers (backend :8000, frontend :5173)
---

# Gram Meal Tracker Dev Environment

Gram is a self-hosted meal/calorie tracker: Svelte SPA frontend (Tailwind + DaisyUI) + FastAPI backend + SQLite, runs on Raspberry Pi in production.

**In development:** both servers run with hot reload — backend FastAPI on `:8000`, frontend Vite on `:5173`. Agent interaction uses `chromium-cli` against the frontend; backend is testable via curl.

## Prerequisites

Ubuntu/Debian packages:
```bash
apt-get update && apt-get install -y python3 python3-venv python3-pip nodejs npm
```

Paths in this guide are relative to the project root.

## Build

The driver handles all setup. First run takes 30-60 seconds (deps, venv setup):

```bash
./.claude/skills/run-meal-advice/driver.sh start
```

This does:
1. Creates Python venv if missing
2. Installs `backend/requirements.txt` (FastAPI, uvicorn, pydantic)
3. Installs `frontend/package.json` (Vite, Svelte, Tailwind, DaisyUI)
4. Starts backend uvicorn on `:8000` with `--reload`
5. Starts frontend Vite dev server on `:5173`
6. Waits for both to be healthy (backend: `/api/health`, frontend: HTTP 200)

## Run (agent path)

### Launch

```bash
./.claude/skills/run-meal-advice/driver.sh start
```

Outputs logs to:
- `/tmp/gram-backend.log` — backend startup, errors, warnings
- `/tmp/gram-frontend.log` — Vite compilation, HMR events

### Interact with frontend

Use `chromium-cli` to drive the SPA:

```bash
chromium-cli http://localhost:5173/ <<'SCRIPT'
navigate http://localhost:5173/
screenshot gram-app.png
# Add a food
click "input[placeholder*='food']"
type "Apple"
click "button:has-text('Add')"
screenshot after-add.png
wait "text=Apple"
SCRIPT
```

### Test backend API

Direct curl calls (no browser needed):

```bash
# Health check
curl http://localhost:8000/api/health

# Add a food (per-100g nutrition values)
curl -X POST http://localhost:8000/api/foods \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Banana",
    "calories": 89,
    "protein": 1.1,
    "carbohydrate": 23,
    "fat": 0.3
  }'

# Log an entry (amount_grams × nutrition = daily totals)
curl -X POST http://localhost:8000/api/entries \
  -H "Content-Type: application/json" \
  -d '{
    "food_id": 1,
    "amount_grams": 100,
    "meal": "breakfast",
    "consumed_date": "2026-06-26"
  }'

# Today's totals
curl http://localhost:8000/api/today/summary

# Search foods
curl "http://localhost:8000/api/foods?q=apple"

# See all endpoints
curl http://localhost:8000/docs  # Swagger UI
```

### Stop

```bash
./.claude/skills/run-meal-advice/driver.sh stop
```

### Check status

```bash
./.claude/skills/run-meal-advice/driver.sh status
```

## Run (human path)

**Terminal 1 — backend:**
```bash
python3 -m venv .venv && ./.venv/bin/pip install -r backend/requirements.txt
./.venv/bin/uvicorn backend.app.main:app --reload   # :8000
```

**Terminal 2 — frontend:**
```bash
cd frontend
npm install
npm run dev   # :5173, proxies /api → :8000
```

Open http://localhost:5173 in browser.

## Direct API Testing (no frontend)

Useful for PRs touching only backend logic:

```bash
# Start just the backend
./.venv/bin/uvicorn backend.app.main:app --reload

# In another shell, run test queries (see "Test backend API" above)
```

## Gotchas

**Port conflicts:** If `:8000` or `:5173` are in use, driver fails silently (curl timeout). Kill conflicting processes or use `lsof -i :8000` / `lsof -i :5173` to find them.

**Stale node_modules:** If `frontend/package-lock.json` changes but `node_modules` is missing, `npm install` runs fresh but Vite may serve old code. The driver always runs `npm install`, so this is rare.

**SQLite location:** By default, `meals.db` lives at `/tmp/meals.db` (see `backend/app/config.py` `MEAL_DB` env var). Each fresh start has a clean database — no persistent data between runs unless you move the `.db` file.

**API field names:** Nutrition fields on POST are **not** `_per_100g` suffixed — they're `calories`, `protein`, `carbohydrate`, `fat` (and optional: `saturated_fat`, `sugar`, `fiber`, `salt`). The database stores per-100g values; the entry POST body multiplies by `amount_grams`.

**Vite HMR:** Frontend changes hot-reload instantly. Backend changes restart the uvicorn process automatically (triggered by file watch on `backend/`).

## Troubleshooting

| Symptom | Fix |
|---|---|
| `error: connect ECONNREFUSED 127.0.0.1:8000` | Backend failed to start. Check `/tmp/gram-backend.log` for errors. Usually: missing Python deps or port in use. |
| `curl: (7) Failed to connect to localhost:5173` | Frontend failed to start. Check `/tmp/gram-frontend.log`. Usually: missing npm deps or Node/npm version issue. |
| `uvicorn: command not found` | Python venv not activated. Driver handles this; if running manually, use `./.venv/bin/uvicorn`. |
| `npm: command not found` | Node/npm not installed. Run `apt-get install -y nodejs npm` (or homebrew on macOS). |
| All blank page in browser, console errors | SQLite perms or corrupted `.db` file. Clear `/tmp/meals.db` and restart. |
| Stale frontend code after git checkout | Hard-reset Vite cache: `rm -rf frontend/node_modules/.vite` then restart driver. |
| Playwright sees old code despite page reload | Service worker serves stale assets. Unregister it first: `await page.evaluate(() => navigator.serviceWorker.getRegistrations().then(regs => Promise.all(regs.map(r => r.unregister()))))` then reload. Do this once at the start of each Playwright session. |
