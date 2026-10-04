---
name: run-devskyy-dashboard
description: Build, launch, and drive the DevSkyy Next.js dashboard at `frontend/` headlessly. Use when asked to run, start, launch, smoke, screenshot, verify, boot, or take a picture of the dashboard, the admin UI, the storefront preview, or any route on `localhost:3000` / `devskyy.app`. Ships a Playwright-library driver (`driver.mjs`) that boots Chromium, asserts HTTP 200, and writes PNGs.
---

# run-devskyy-dashboard

The dashboard is the Next.js 16 / React 19 app at `frontend/` that deploys to `devskyy.app`. It serves the admin UI, the storefront preview, and all `/api/*` routes that bridge to WordPress and Pinecone. This skill drives it from a clean shell: install → boot dev server → run a Playwright-library smoke harness that screenshots the homepage and `/admin` sign-in page.

**Paths in this doc are relative to `frontend/`** unless absolute. The driver lives inside the skill itself at `.claude/skills/run-devskyy-dashboard/driver.mjs`.

## Prerequisites

- macOS or Linux. Node 22+ on PATH (this session used `v25.6.1`).
- **npm**, not pnpm. Vercel/Node 22+ throws `ERR_INVALID_THIS` under pnpm in this repo (see `frontend/CLAUDE.md:14`).
- Playwright Chromium binary cached at `~/Library/Caches/ms-playwright/chromium-*` (macOS) or `~/.cache/ms-playwright/chromium-*` (Linux). If missing, `npx playwright install chromium` downloads it.
- `frontend/.env.local` must exist and contain at minimum `NEXTAUTH_URL=http://127.0.0.1:3000` and `NEXTAUTH_SECRET=<value>`. Template at `frontend/.env.example`. Without `NEXTAUTH_SECRET` the dev server boots but `/admin` and any auth-gated route 500.

## Install

```bash
cd frontend
npm install
# only if the Playwright Chromium cache is missing:
npx playwright install chromium
```

The repo keeps `frontend/node_modules` checked out as the active workspace — do not mix it with the root project's `.venv` or with root `package.json`. Each workspace is self-contained per `CLAUDE.md`.

## Run — agent path (primary)

```bash
cd frontend

# 1. Boot dev server in the background.
npm run dev > /tmp/devskyy-dev.log 2>&1 &
DEV_PID=$!

# 2. Block until the server is serving 200 on the root.
until curl -sf -o /dev/null http://127.0.0.1:3000/; do sleep 1; done

# 3. Drive it. Default smoke visits `/` and `/admin`, asserts HTTP 200 +
#    non-empty DOM, and writes PNGs to ./screenshots/ next to the driver.
node .claude/skills/run-devskyy-dashboard/driver.mjs smoke

# 4. Clean up.
kill $DEV_PID
```

`smoke` exits `0` on success, `2` on any route that returned non-200 or threw, `64` on usage error, `1` on driver fault. The final stdout line is a JSON result object suitable for piping into `jq`.

### Driver commands

| Command | Use |
|---|---|
| `node driver.mjs smoke` | Run the canonical route list (`/`, `/admin`), screenshot each, exit non-zero on any failure. |
| `node driver.mjs ss <url> <out.png>` | One-shot screenshot. Path may be relative or absolute. |
| `node driver.mjs eval <url> "<js>"` | `page.evaluate()` a snippet; result printed as JSON. Pass a string expression — Playwright wraps it. |

### Driver env vars

| Var | Default | Purpose |
|---|---|---|
| `BASE_URL` | `http://127.0.0.1:3000` | Where the dev server is listening. |
| `OUT_DIR` | `./screenshots` (relative to `driver.mjs`) | Where smoke PNGs land. Absolute paths also accepted. |
| `TIMEOUT_MS` | `60000` | Page navigation timeout. Next.js first-compile in dev is ~5–8s on Apple Silicon — leave generous. |

### Verified output (this session)

```text
[driver] OK   http://127.0.0.1:3000/      status=200 body=61165b -> screenshots/home.png
[driver] OK   http://127.0.0.1:3000/admin status=200 body=34299b -> screenshots/admin.png
```

`screenshots/admin.png` shows the actual NextAuth sign-in form ("Welcome back" / DS logo / Email + Password fields / brand-pink Sign-in button). `screenshots/home.png` is `fullPage: true` and captures the full 6376-px storefront — masthead, collection nav, footer.

## Run — human path

```bash
cd frontend
npm run dev
# open http://localhost:3000 in a browser
# Ctrl-C to stop
```

Use this only when you need real WebGL — the 3D collection portals on `/` don't initialize in headless Chromium (see Gotchas).

## Direct invocation — API routes via curl

The dev server exposes `/api/*` routes. To exercise an API change without driving the UI:

```bash
curl -sS http://127.0.0.1:3000/api/<route> | jq
```

`frontend/app/api/` lists all routes. Most write routes require an authenticated NextAuth session cookie; read routes can usually be hit unauthenticated for shape checks.

## Gotchas

- **Three.js portal sections render black in headless.** `/`'s collection portals require WebGL/GPU acceleration that headless Chromium fakes. The middle ~5000px of `screenshots/home.png` is dark because of this, not because the page is broken. Use the human path with real Chrome for visual QA of 3D scenes, or set `channel: 'chrome'` on the launch options.
- **`next dev` first-compile is slow.** 5–8s typical on Apple Silicon; longer on cold cache. Driver's 60s default `TIMEOUT_MS` accommodates this.
- **`playwright.config.ts` and the on-disk dir are mismatched.** Config has `testDir: './tests/e2e'` but `e2e/` *also* contains specs (`auth.setup.ts`, `login-dashboard.spec.ts`). `npx playwright test` will only pick up `tests/e2e/`. Use this skill's driver (not the test runner) for smoke; route the test runner question to whoever owns the e2e suite.
- **Empty `.claude/skills/run-devskyy-dashboard/CLAUDE.md` files re-appear.** Auto-injected by the claude-mem plugin. Harmless. `rm` them; do not commit.
- **`outputFileTracingRoot` env gate is load-bearing.** `next.config.ts` sets `outputFileTracingRoot` and `turbopack.root` to the repo root ONLY when `!process.env.VERCEL`. Removing the gate ships a doubled-path bug to Vercel (`/vercel/path1/path1/.next/...` ENOENT) and breaks every deploy. See `frontend/CLAUDE.md:95`.
- **`/admin` is auth-walled.** The smoke run hits the NextAuth sign-in form, not the dashboard. To screenshot the actual admin UI a future agent needs to either inject a valid session cookie via `context.addCookies()` in the driver or stub NextAuth — neither is implemented here.
- **Cache Components mode is on.** `cacheComponents: true` in `next.config.ts` means every request-time data reader needs to live under `<Suspense>`. If a route 500s with `Uncached data was accessed outside of <Suspense>`, that's a real code defect in the route, not the driver. Fix the route per `frontend/CLAUDE.md:53`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `EADDRINUSE :::3000` when starting dev | `lsof -ti:3000 \| xargs kill` then retry. |
| Driver exits 2 with `status: undefined` | Dev server isn't actually listening. `tail /tmp/devskyy-dev.log` and check for compile errors. |
| `Cannot find module 'playwright'` | Run from `frontend/`. The driver resolves Playwright via `frontend/node_modules`. If you ran from repo root, `cd frontend` first. |
| Screenshot blank or near-black | (1) Three.js section, expected — see Gotchas. (2) The page rendered an error boundary — check the dev log. (3) `fullPage: true` may help if content is below 900px. |
| `npm install` warnings about lockfile root | Expected when both `package-lock.json` files (root + frontend) are present locally. `next.config.ts` handles it. Don't "fix" by removing the env gate. |
| `npx playwright install chromium` hangs | Network. Use `HTTPS_PROXY` if behind one, or copy the cache dir from another machine. |

## Limits / known not-yet-done

- The driver does not log into NextAuth. Smoke covers the unauthenticated surface only.
- 3D scenes are not exercised. Add `channel: 'chrome'` + `headless: false` and a viewport-only screenshot path if you need to see Three.js init.
- Production build (`npm run build`) is not part of `smoke`. Add a `build` subcommand to `driver.mjs` if a future task wants pre-deploy verification — `cacheComponents` makes the dev server lenient where build is strict.
