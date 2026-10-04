---
name: add-api-route
description: Scaffold a new Express API route file with JWT auth, org-isolation middleware, zod validation, Prisma queries, and standard error handling. Use when the user asks to "add an API endpoint", "create a route", or "expose X over HTTP".
---

# add-api-route

Create a new route file under `apps/api/routes/` that follows the project's conventions. **Org isolation is non-negotiable** — every route handler must apply `injectOrgFilter` (reads) or `injectWriteFilter` (writes) unless the user is `WEBSITE_ADMIN`.

## Inputs to gather

- **Route name** (e.g. `commissions`)
- **Mount path** (e.g. `/api/commissions`)
- **Endpoints needed** (GET list, GET :id, POST, PATCH :id, DELETE :id, custom)
- **Owning Prisma model** (must already exist — if not, run `/add-prisma-model` first)
- **Required roles** for write endpoints

## Steps

1. **Read a sibling route** as reference. Default: `apps/api/routes/leads.ts` (post-E2 conventions: org isolation, calculated fields, batch endpoints).
2. **Create** `apps/api/routes/{name}.ts` containing:
   - `import { Router } from "express"` + `authenticateToken` + `injectOrgFilter`/`injectWriteFilter`
   - `import { z } from "zod"` for request validation
   - One zod schema per write endpoint
   - Try/catch with `console.error` + 500 fallback
   - `res.json(...)` with consistent shape (`data`, or array)
3. **Mount the router** in `apps/api/index.ts` (or `apps/api/server.ts`) under the chosen path.
4. **Apply org isolation** — every handler that touches multi-tenant data must:
   - Use `req.user.organizationId` from JWT (never accept it from body)
   - Use the middleware (preferred) OR explicit `where: { organizationId: req.user.organizationId }`
5. **Add rate limiting** if it's a public/auth-adjacent endpoint (the global 100/min limiter applies automatically; use the stricter limiter for sensitive routes).
6. **Run `/typecheck`** then `/audit-org-isolation` to verify scoping.
7. **Update the vault**: append the new endpoint to `Aqarkom_Knowledge/Architecture/API Routes.md` under the matching domain.

## Verification checklist

- [ ] Mounted in the main router
- [ ] Every handler reaches Prisma through the org filter
- [ ] zod validation on every body-accepting endpoint
- [ ] No `req.body.organizationId` used (security risk)
- [ ] `/typecheck` passes
- [ ] `/audit-org-isolation` shows zero violations
- [ ] curl test: returns 401 without token, 200 with token, scoped data only

## Anti-patterns

- Don't bypass `injectOrgFilter` "just for an admin endpoint" — gate by role instead
- Don't return raw Prisma errors to the client (they leak schema)
- Don't paginate via offset alone for big tables — use cursor pagination matching `leads.ts`
