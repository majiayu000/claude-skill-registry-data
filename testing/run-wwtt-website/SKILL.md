---
name: run-wwtt-website
description: Run, start, build, screenshot, or test the WanderWave Travel & Tours website (React/Vite frontend + Node/Express backend). Use when asked to run the app, verify a change works visually, take a screenshot, or check a route.
---

WanderWave Travel & Tours is a full-stack travel-booking web app. The **frontend** is React 19 / Vite 7, served at `http://localhost:3000`. The **backend** is Node.js / Express on port 5000, with MongoDB. In dev the Vite proxy forwards `/api` requests to the production Render backend (`https://wanderwaveph.onrender.com`) — you do **not** need a local backend to run the frontend against real data.

The agent path is [`.claude/skills/run-wwtt-website/driver.mjs`](.claude/skills/run-wwtt-website/driver.mjs), which wraps Playwright (already in `frontend/devDependencies`) and supports one-shot commands or a REPL over stdin.

## Prerequisites

Node.js ≥ 18 (tested on v24). Playwright's Chromium browser:

```
cd frontend
npx playwright install chromium
```

That's it. No OS packages needed on Windows — Playwright ships its own Chromium.

## Build

```
cd frontend
npm install
```

The backend has its own deps:

```
cd backend
npm install
```

## Run (agent path)

Start the Vite dev server — **use port 3000 or 3001** (these are in the production backend's CORS allowlist; other ports will cause API calls to fail with CORS errors):

```
cd frontend
npx vite --port 3000
```

Vite prints the actual port if 3000 is busy. Note it.

Then run the driver from the **repo root** (`c:\Users\hhsarmiento\Desktop\WWTT-Website`):

```
# One-shot screenshot of the main page
node .claude/skills/run-wwtt-website/driver.mjs screenshot packages.png http://localhost:3000/packages

# One-shot screenshot of a specific route
node .claude/skills/run-wwtt-website/driver.mjs screenshot flights.png http://localhost:3000/flights

# Navigate and print page title
node .claude/skills/run-wwtt-website/driver.mjs navigate http://localhost:3000/packages
```

The driver must be run from the **repo root** — it resolves Playwright via an explicit path to `frontend/node_modules/playwright/index.mjs`, so no separate install is needed.

Alternatively use REPL mode for an interactive session:

```
node .claude/skills/run-wwtt-website/driver.mjs
# → driver ready — send: screenshot <path> [url] | navigate <url> | click <sel> | text <sel> | quit
screenshot packages.png http://localhost:3000/packages
click text=FLIGHT SEARCH
screenshot flights.png
quit
```

### Environment variables

| Var | Default | Purpose |
|-----|---------|---------|
| `BASE_URL` | `http://localhost:3000` | Override default base |
| `HEADLESS` | `true` | Set to `false` to open a visible window |

## Run (human path)

```
cd frontend && npm run dev
```

Opens the dev server; navigate to `http://localhost:3000/packages` (the real homepage — `/` has no route and shows 404).

To run the backend locally:

```
cd backend && npm run dev
```

Backend needs a `backend/.env` file with `MONGO_URI`, `JWT_SECRET`, `CLOUDINARY_*`, `AMADEUS_*`, etc. The `.env` file already exists in the repo (not committed).

Then update `frontend/vite.config.js` to proxy to `https://wanderwaveph.onrender.com` instead of the Render URL.

## Key routes

| Route | What it is |
|-------|------------|
| `/packages` | **Main page** — package deals listing |
| `/flights` | Flight search (Amadeus API) |
| `/tours` | Tour packages |
| `/transfers` | Transfer packages |
| `/other-services` | Visa, passport, etc. |
| `/dashboard` | User dashboard (requires login) |

> **`/` has no route** — it shows 404. Always start at `/packages`.

## Tests

Frontend (Playwright e2e — currently no test files, only infra):

```
cd frontend && npx playwright test
```

Backend (Jest):

```
cd backend && npm test
```

## Gotchas

- **Port matters for CORS.** The production backend allowlists `http://localhost:3000` and `http://localhost:3001` only. If Vite bumps to 3002+ (because those ports are busy), all `/api` calls will silently fail with CORS errors in the browser console but the page shell still renders. Fix: free up port 3000 or 3001 before starting.

- **No "/" route.** Navigating to `http://localhost:3000` renders the 404 NotFound component. The real landing page is `/packages`. This is intentional — the nav's "HOME" item navigates to `/packages`.

- **Driver must run from repo root.** The driver resolves Playwright via an explicit file URL to `frontend/node_modules/playwright/index.mjs`. Running it from any other directory still works as long as you provide an absolute `--cwd` — but the simplest path is always from the repo root. The `cd frontend && node ...` pattern will break because the relative depth calculation is anchored to the skill file, not the working directory.

- **`networkidle` can time out on CORS failures.** If the backend is unreachable, the page fires API calls that never settle. The driver uses a 30-second timeout. If it times out, switch to `{ waitUntil: 'load' }` or use a free port 3000/3001.

- **Anti-tamper is prod-only.** The `vite.config.js` injects an obfuscated anti-debugging script only in `vite build` production mode. It does not run in dev, so DevTools work normally.

## Troubleshooting

**`Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'playwright'`**
→ Run the driver from the repo root, not from `frontend/` or the skill directory.

**`Access to fetch ... has been blocked by CORS policy`**
→ Vite is not on port 3000 or 3001. Kill competing processes and restart with `npx vite --port 3000`.

**`Port 3000 is in use, trying another one...`**
→ Find and kill the process using 3000: on Windows `Get-NetTCPConnection -LocalPort 3000 | Select OwningProcess` then `Stop-Process -Id <pid>`.

**`Error: Error connecting to the API.`** shown in UI
→ Same CORS issue as above, or the Render backend is sleeping (free tier). Wait 30 s for Render to wake, then reload.
