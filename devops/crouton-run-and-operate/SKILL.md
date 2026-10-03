---
name: crouton-run-and-operate
layer: stack
description: Day-to-day operation runbook for nuxt-crouton apps — boot any app/POC locally with auth working, seed and inspect the local database (including the miniflare-vs-.data split that makes seeded data "disappear"), turn on the review overlay / eruda, observe deployed staging (tail, smoke, row counts), and capture screenshots. Use when asked to "run the app", "boot velo/fanfare/a poc locally", "why can't I log in locally", "seed the database", "the seed data doesn't show up", "look at the local db", "check what's on staging", "screenshot the app", or "where do the artifacts land".
---

# crouton-run-and-operate

Operate a running crouton app — locally or on deployed staging — from cold boot to evidence capture. ("crouton" = this monorepo's schema-driven CRUD framework: `@fyit/crouton-*` packages that generated Nuxt apps extend as layers.)

## When to use / when NOT to use

| You want to… | Use |
|---|---|
| Boot, log in, seed, inspect, observe, screenshot a running app | **this skill** |
| Recreate the environment (install/build traps, typecheck story, versions) | `crouton-build-and-env` |
| Deploy to staging / wire CI / first-time Cloudflare setup | `deploy` (apps), `poc-deploy` (pocs); prod only via `deploy-production` |
| Generate/apply Drizzle migrations, `schema.mjs` gotcha, infra tables | `db-migrations` |
| Mirror one D1 env into another (refresh staging from prod) | `db-clone` |
| Run the Playwright fixture smoke (boot+auth+CRUD proof) | `e2e-smoke` |
| Deploy a preview *for UI sign-off* (the gate workflow) | `ui-proposal` |
| Symptom → root-cause lookup | sibling `crouton-diagnostics-index` |
| Measure the harness itself (context budget, traces) | `loop-station` / sibling `crouton-harness-observability` |

## 1. Boot any app locally from cold, with auth working

Prerequisites (one line — full story in `crouton-build-and-env`): `pnpm install && pnpm build:packages`. Apps consume `@fyit/*` packages from `dist/`; skipping `build:packages` = dev-server error on missing `crouton-core/dist`.

```bash
export BETTER_AUTH_SECRET=$(openssl rand -hex 32)   # required (crouton-auth throws if unset); better-auth only WARNS below 32 chars
pnpm --filter velo dev                              # or: cd apps/velo && pnpm dev
```

- **There is no root `dev` script** (verified: root `package.json` scripts). Root CLAUDE.md's "Development Commands" listing `pnpm dev` only works *inside an app dir* — a known doc contradiction; the app `package.json` is ground truth here.
- On Claude-web sessions the SessionStart hook (`.claude/hooks/session-start.sh`) already did install + `build:packages` and exported a cached dev `BETTER_AUTH_SECRET` (from `~/.crouton-dev-auth-secret`) — check `echo $BETTER_AUTH_SECRET` before generating your own.
- Apps ship `.env.example` (copy to `.env`). Trap: it hardcodes `BETTER_AUTH_URL=http://localhost:3000` but each app runs on its own pinned port (table below) — set it to the app's real port or cookies misbehave.
- E2e fixtures (`fixtures/*`) commit a dummy `.env` on purpose (`BETTER_AUTH_SECRET=dev-fixture-secret-do-not-use-in-production`) — they boot with zero env setup.
- **No manual DB step**: `hub: { db: 'sqlite' }` in each app's `nuxt.config.ts` (root CLAUDE.md gotcha — never `hub: { database: true }`) auto-applies all layers' migrations at dev boot; locally it's a sqlite file, at runtime it maps to Cloudflare D1/KV/R2.

**Fixed dev ports** — pinned in each app's/POC's `nuxt.config.ts` `devServer.port`. **Snapshot 2026-07-02 — regenerate with the re-verify block before relying on numbers.**

| App | Port | | POC | Port |
|---|---|---|---|---|
| apps/triage | 3005 | | pocs/alexdeforce | 3001 |
| apps/velo | 3006 | | pocs/sintlukas | 3003 |
| apps/kassa | 3007 | | pocs/crouton-builder-demo | 3010 |
| e2e fixtures | 3000 | | pocs/crouton-builder **and** pocs/kvr | **3011 — collision**; run one with `--port` |
| | | | pocs/loop-station | 3021 |

Pocs that set no port (`blog`, `thinkgraph*`, `three-demo`, `booking-demo` at the snapshot) default to 3000/auto-bump.

**First login** (auth = better-auth via `@fyit/crouton-auth`; facts from `e2e/CLAUDE.md`):
- Login/register is a **RouteModal overlay**, not a page — `/auth/login` redirects to `/` and opens the modal (`useAuthModal`). Register a fresh account in the modal on a fresh DB.
- **Signup creates no team.** Programmatically, create one via the better-auth org API: `POST /api/auth/organization/create` then `/set-active` — both **require an `Origin` header** (CSRF). See `ensureTeam()` in `e2e/helpers.ts` for the exact calls. Or seed staff accounts instead (§2).
- Generated collections render at `/admin/{teamSlug}/crouton/{collectionKey}`.
- Session check: `GET /api/auth/get-session` returns the authenticated user (what `smoke-deployed.mjs` uses as login proof).

Do NOT verify with `nuxt preview`: crouton collection pages currently 500 under production-preset SSR — an internal data-fetch loses the auth cookie (`e2e/CLAUDE.md`, open problem). Operate against `nuxt dev`.

## 1.5 Reproduce a runtime bug locally — MOBILE-FIRST (never push a fix blind)

The method rule is in `AGENTS.md` (*Bug work → reproduce against the running system*): for a runtime bug (reload loop, 500, broken interaction), reproduce + verify the fix locally *before* pushing. Here's the crouton how-to. **This stack is phone-first (#722, `atelier-plan`) — drive at a phone viewport (390×844) by default**; only check desktop when a surface is explicitly wide.

Write a throwaway driver **inside the repo tree** (playwright resolves from repo `node_modules`; a `/tmp` script can't import it) — `repro.local.mjs` at the repo root; don't commit it.

```js
import { chromium } from 'playwright'
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' // glob newest if the build bumped
const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] })
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 }) // MOBILE
const page = await ctx.newPage()
page.on('console', m => console.log('console', m.type(), m.text()))
page.on('load', () => console.log('PAGE LOAD', page.url()))         // count loads → reload vs re-render
page.on('framenavigated', f => f === page.mainFrame() && console.log('nav', f.url()))
page.on('pageerror', e => console.log('PAGEERROR', e.message))
```

**Auth/team bootstrap** for a team-scoped page (better-auth's org calls need an **`origin` header**, else `MISSING_OR_NULL_ORIGIN`). Do it via `ctx.request` so cookies are shared:
`POST /api/auth/sign-up/email {email,password,name}` → `POST /api/auth/organization/create {name,slug}` (headers `{origin, referer}`) → `POST /api/auth/organization/set-active {organizationId}` → seed rows via the collection API `POST /api/teams/<orgId>/<collection>` → `page.goto('/…')`.

**Instrument, then observe — don't theorise.** A full-page reload in Nuxt is often chunk-error auto-reload; counting `load` events tells a reload from a re-render. (#988 board reload: three blind pushes vs one local repro that found it — autosave→refetch→reload — in minutes.)

## 2. Seeding

**Package demo data** — every app has `db:seed` scripts (verified in the apps' `package.json`):

```bash
pnpm --filter velo db:seed          # = crouton-seed --db velo-db --with-staff (local)
pnpm --filter velo db:seed:staging  # = crouton-seed --db velo-staging-db --remote --with-staff
```

`crouton-seed` (bin: `packages/crouton-cli/bin/crouton-seed.mjs`) discovers `SeedProvider`s from every extended `@fyit/crouton-*` package, emits idempotent upsert SQL, and executes it via `npx wrangler d1 execute <db> --local|--remote`. Flags (verified): `--db` (required) `--remote` `--dir` `--team` (default `test1`) `--locale` (default `nl`) `--with-staff` `--dry-run`. It also seeds the app's default layout: `crouton.layout.json` → a `layout_configs` row with id `default` (#709; `lib/seed-app.ts`).

**⚠️ THE seed-visibility trap (code-derived, not reproduced end-to-end):** a local `crouton-seed` writes via `wrangler d1 execute --local` into `<app>/.wrangler/state/v3/d1/miniflare-D1DatabaseObject/*.sqlite` (miniflare = wrangler's local Cloudflare simulator), but `nuxt dev` with `hub: { db: 'sqlite' }` reads `<app>/.data/db/sqlite.db`. `seed-app.ts` has **no copy step** into `.data/` (verified: it only shells out to `wrangler d1 execute` — re-check with the seed grep in the re-verify block). So locally-seeded data may never appear in the dev app. `crouton db-pull` handles the split explicitly — `lib/db-pull.ts` copies the imported DB to `.data/db/sqlite.db` and marks `_hub_migrations` applied. If seeded data "doesn't show up", this split is why; workaround is copying the sqlite file into `.data/db/sqlite.db` by hand (stop dev first).

**App-specific content seeds** (`seedData/` convention): velo keeps CSVs/markdown under `apps/velo/seedData/{school-velotek,velosolidaire}/`, consumed by HTTP endpoints `POST /api/seed` and `POST /api/seed/velosolidaire` (`apps/velo/server/api/seed/*.post.ts` — additive, dedupes users by email, hashes passwords properly). This is the "per-collection seeding" the `db-clone` skill contrasts itself with.

**Pull real remote data local**:

```bash
cd apps/velo && npx crouton db-pull --env staging --dry-run   # then drop --dry-run
```

Flags (verified in `bin/crouton-generate.js` `dbPullCmd`): `--env`, `--config`, `--keep-sql`, `--dry-run`. Flow: export remote D1 → wipe local wrangler D1 → import → copy to `.data/db/sqlite.db`.

## 3. Inspecting the local DB

- File: `<app>/.data/db/sqlite.db` — exists only after dev has run once. Inspect with plain `sqlite3`:
  ```bash
  sqlite3 apps/velo/.data/db/sqlite.db '.tables'
  ```
- **No Drizzle Studio wiring exists in the repo** (verified: zero `db:studio`/`drizzle-kit studio` hits) — but none is needed on a normal dev machine: NuxtHub core itself launches Drizzle Studio as the "Database" tab in Nuxt DevTools during `nuxt dev` whenever `hub.db` is set (`@nuxthub/core` `launchDrizzleStudio()` → `startStudioSQLiteServer`, iframe at `local.drizzle.studio` — verified in the dist, not exercised live). It needs a browser + egress to that host, so it's unusable in the headless sandbox — there, raw `sqlite3` is the reality.
- Remote row counts (read-only, safest remote check):
  ```bash
  node scripts/db-counts.mjs --app velo --env staging   # or: pnpm db:counts -- --app velo --env staging
  ```
  Discovers the DB name from the app's `wrangler.jsonc`; a real run needs `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN`, `--dry-run` needs neither. (These CF creds are typically absent in the interactive sandbox — remote inspection then goes through CI.)
- Ad-hoc remote SQL: `npx wrangler d1 execute <db-name> [--env staging] --remote --command "SELECT …"`.

## 4. Review overlay and eruda

- **Review overlay** — `NUXT_PUBLIC_CROUTON_REVIEW=true` at **build time** (read in `packages/crouton-devtools/src/module.ts`) makes `@fyit/crouton-devtools` install `@fyit/crouton-feedback` (epic #960) with the GitHub sink defaulted: a glasses launcher with Console (eruda), Annotate (pin a comment on an element → resolves the source file → lands as a `🎯 Preview feedback` PR comment), and Changelog. Generated `cf:staging` scripts bake the flag in; zero prod footprint. The sign-off *workflow* around it belongs to the `ui-proposal` skill.
- **Eruda mobile devtools layer** — opt-in per app: `extends: ['@fyit/crouton-devtools/eruda']`, active in local dev or when `NUXT_PUBLIC_CROUTON_ERUDA=true` at build (verified in `packages/crouton-devtools/eruda/nuxt.config.ts`; default off, chunk never fetched in prod). Set the flag in `cf:staging` only, never `cf:deploy`.

## 5. Observing deployed staging

Deploy/migrate mechanics live in the `deploy` skill — this is the *watching* side.

| Need | Command | Caveat |
|---|---|---|
| Live Worker logs | `pnpm --filter triage logs` / `--filter fanfare logs` (= `npx wrangler tail triage\|fanfare`) | Only some apps have a `logs` script (grep for it — re-verify block), and those tail the **production** worker. No staging tail script exists anywhere (verified at the snapshot); hand-run `npx wrangler tail <app>-staging` (unverified against a live worker — needs CF creds). No log persistence: an error nobody was tailing is gone. |
| Prove a deployed preview works | `node scripts/smoke-deployed.mjs --url https://<app>.pmcp.dev --email <e> --password <pw> [--app <n>] [--manifest <app>/deploy.config.json]` | Login proof via `/api/auth/get-session` → optional CRUD round-trip (from `deploy.config.json` `smoke.crud`) → screenshot `screenshots/<app>-smoke.png`. CI runs it per deploy, report-only unless `smoke.required: true`. |
| Seed a loginable review account on a deploy | `node scripts/seed-review-login.mjs --url <deployedUrl> --email <e> --password <pw>` | Uses the app's own HTTP auth routes (real password hashing); best-effort. `--seed-team <slug>` attaches it to the seeded demo org — with `--db <d1>` (remote, the deploy path) **or** `--sqlite <path>` (the local `.data/db/sqlite.db`, #1777). |
| **Look at a change locally, in one command** | `pnpm preview <app>` | Boot + seed + disposable review login + a **prefilled** one-click URL (`scripts/app-preview.mjs`, #1777). Use this instead of hand-rolling boot→seed→login; it's the only preview a **packages-only** change gets, since PR deploy previews match only `apps/<app>/**` by design. `--no-seed` / `--no-login` for faster re-runs; landing page comes from `reviewLogin.landing` in the app's `deploy.config.json`. |
| What's in the staging DB | `node scripts/db-counts.mjs --app <app> --env staging` | §3. |

At last verification, no runtime analytics was wired in any deployed app: `packages/crouton-analytics` exists but no app/poc/fixture depends on it (unverified beyond a grep of `package.json`s — re-run that grep before relying on it; from the #1073 discovery sweep, adapters were in-flight, #947).

## 6. Screenshots

```bash
node scripts/app-shots.mjs <baseUrl> <path[:name]> [more paths...] [--out <dir>] [--desktop|--viewport WxH]
# e.g. node scripts/app-shots.mjs http://localhost:3006 /:home /auth/login:login   # MOBILE (default)
```

**Shots are MOBILE (390×844) by default** — this stack is phone-first (#722); verify the phone layout first and only add `--desktop` (1280×900) for surfaces that are explicitly wide. (Also `pnpm app:shots`.) Writes `screenshots/<name>.png`; exits 1 on any failure. It auto-resolves the **pre-installed** chromium under `/opt/pw-browsers/` (globs the newest build; override with `PLAYWRIGHT_CHROMIUM_PATH`) — a failing `npx playwright install` does NOT mean "no browser"; doctrine: `crouton-harness-observability` §5. All screenshots go in `screenshots/` at repo root (HARD GATE, root CLAUDE.md).

## 7. Where artifacts land

| Artifact | Location | Committed? |
|---|---|---|
| Local dev DB (NuxtHub) | `<app>/.data/db/sqlite.db` (+ applied-migration copies in `.data/db/migrations/sqlite/`) | No (`.data` gitignored — verified `git check-ignore`) |
| Wrangler-local D1 (miniflare) | `<app>/.wrangler/state/v3/d1/miniflare-D1DatabaseObject/*.sqlite` | No |
| Build output | `<app>/.output/` | No |
| Screenshots | `screenshots/<name>.png` | No (`*.png` gitignored) |
| Drizzle migrations (source of truth) | `<app>/server/db/migrations/sqlite/` | **Yes** |
| e2e outputs | `e2e/.auth/`, `playwright-report/`, `test-results/` | No |

## Provenance and maintenance

verified: 2026-07-02

```bash
grep -rn devServer apps/*/nuxt.config.ts pocs/*/nuxt.config.ts         # ports table
grep -n '"dev"\|"logs"\|db:seed' apps/*/package.json                   # scripts / tail gap
grep -n 'wrangler\|\.data' packages/crouton-cli/lib/seed-app.ts        # seed write target (has a .data copy step appeared?)
grep -rln crouton-analytics apps pocs fixtures --include=package.json  # analytics still unconsumed?
head -20 scripts/app-shots.mjs scripts/smoke-deployed.mjs              # usage lines
grep -n CROUTON_REVIEW packages/crouton-devtools/src/module.ts         # review-overlay gate
```
