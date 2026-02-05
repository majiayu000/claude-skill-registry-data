---
name: vkc-api-route-pattern
description: Standardize Next.js App Router API route implementations under src/app/api/** (auth/session, input validation, Drizzle queries, rate limiting, response shape). Use when creating or refactoring API routes in this repo.
metadata:
  short-description: API Route skeleton + rules
---

# VKC API Route Pattern

## When to use

- Creating new endpoints under `src/app/api/**`
- Refactoring existing endpoints to match house style

## House style (this repo)

- **Auth**: `getSession` (user) or `getAdminSession` (admin)
- **DB**: `db` from `@/lib/db`, tables from `@/lib/db/schema`
- **Rate limit** (if needed): `checkRateLimit` + `rateLimitResponse`
- **Responses**:
  - Public APIs: prefer `@/lib/api/response` helpers
  - Admin APIs: typically `NextResponse.json(...)` directly (keep consistent within `/api/admin/**`)
- **Validation**: repo currently uses explicit runtime checks (no Zod dependency yet). If Zod is added later, migrate route-by-route.

## Canonical references

- Public route w/ validation + rate-limit: `src/app/api/reports/route.ts`
- Public route w/ typed allowlists: `src/app/api/events/route.ts`
- Admin CRUD + schedule fields: `src/app/api/admin/news/route.ts`

## Template

- Full skeleton (copy + customize): `.codex/skills/vkc-api-route-pattern/references/api-route-template.ts`

