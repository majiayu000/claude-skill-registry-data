---
name: devskyy-dashboard-patterns
description: DevSkyy dashboard (devskyy.app) implementation patterns — Next.js 16 App Router, React 19, auth gating, admin pages, WP/WC data wiring. Use for any frontend/ work — pages, components, API routes, deployment. Encodes hard-won production lessons (bug-161, bug-162, Vercel quirks).
---

# DevSkyy Dashboard Patterns

devskyy.app = the agent-management hub (Next.js 16 + React 19 in `frontend/`). skyyrose.co = the WP storefront. **Never cross-wire the two** — dashboard consumes WP/WC via REST, never renders storefront UI.

## Hard-won production rules

- **cacheComponents (bug-161)**: with Next 16 `cacheComponents`, any page reading request-time data must `await connection()` (from `next/server`) before dynamic reads, or it silently serves stale prerender. Admin pages that read live catalog/WC data: always.
- **Auth gate is per-handler `withAuth()` from `frontend/lib/api-auth.ts` (bug-162)** — wrap every API route handler (`export const GET = withAuth(getHandler)`); public exceptions are listed in `frontend/lib/api-public-routes.ts` and `frontend/tests/api-auth-coverage.test.ts` fails on any unwrapped, unlisted route. There is no edge gate: `frontend/proxy.ts` was removed 2026-07-28 — do not add `middleware.ts` auth or recreate a proxy, that is a second, conflicting gate.
- **Deploys: npm, never pnpm** (ERR_INVALID_THIS on Node 22+ with Vercel). `cd frontend && npm run deploy`. Vercel is current but retiring — devskyy.app returns 402 `DEPLOYMENT_DISABLED` `[live 2026-09-18]`; the replacement host is undecided, so do not document one.
- **Env**: Vercel project `skyyroseco/devskyy`, linked at `frontend/.vercel`. Production env synced via `vercel env add <KEY> production`; preview target must be added manually by founder (CLI add silently fails from agent sessions).
- **WP/WC data**: `https://skyyrose.co/wp-json/wc/v3` + BasicAuth consumer key/secret from env (`WC_CONSUMER_KEY`/`WC_CONSUMER_SECRET`); app-password auth for `wp/v2` + `skyyrose/v1`. On WP.com Atomic, `?rest_route=` form 401s for wc/v3 — use `/wp-json/` path there.

## Page conventions

- Admin surfaces live under `app/admin/*` — existing: `/admin/catalog` (lossless CSV editor, SOT read-only), `/admin/renders/review`. Follow their structure for new admin pages: server component shell + client islands, Zod-validated API routes.
- Validation: Zod at every API boundary (mirror backend Pydantic).
- Type-check + lint + build before done: `npm run type-check && npm run lint && npm run build` — a PostToolUse hook also runs `tsc --noEmit` on every edit; heed it.
- State: server components + fetch by default; client state only for interactivity. No new global-state libs without cause.

## Design language (dashboard ≠ storefront)

Dashboard is a TOOL: density allowed, dark-first, brand accents used sparingly (rose-gold `#B76E79` for primary actions only). Tables > cards for operational data. Every list needs loading/empty/error states — no unhandled fetch states in delivered pages.

## Verify

- `npm run build` exit 0 (Turbopack), no type errors.
- New page reachable + auth-gated via proxy (curl logged-out → redirect/401, logged-in → 200).
- If page reads WC/WP: verify one real fetch against live creds from `.env` (never hardcode).
