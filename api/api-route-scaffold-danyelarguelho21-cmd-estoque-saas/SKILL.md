---
name: api-route-scaffold
description: Use when adding a new Next.js App Router API route under services/app/src/app/api/** — new endpoint file (route.ts), new HTTP method on an existing route, or a new list/GET endpoint needing pagination. Also use when reviewing a route.ts diff for missing requireRole/handleRoute or ad-hoc error handling.
---

# API Route Scaffold

## Overview

All 46+ route files under `services/app/src/app/api/**/route.ts` follow one shape:
`handleRoute(async () => { requireRole/requireSession; parseJsonBody/parseQuery; call the
domain module; return ok/created/noContent })`. `handleRoute` (in `services/app/src/lib/http.ts`)
is the ONLY place that translates errors to the API's standard `{code, message, details,
trace_id}` envelope (`api/openapi/_common.yaml`) — domain code never formats an HTTP response
itself. Deviating from this (hand-rolled try/catch, skipping `requireRole`, validating with raw
`await req.json()`) reintroduces exactly the bug QA finding H-1 fixed: an uncaught Prisma P2025
("no record found") falling through to a generic 500 instead of the documented 404.

## The Pattern (evidence: stock/entries/route.ts, products/route.ts)

```ts
import { z } from "zod";
import { requireRole } from "@/modules/auth";
import { doTheThing } from "@/modules/<domain>";
import { created, handleRoute, ok, parseJsonBody, parseQuery } from "@/lib/http";

const BodySchema = z.object({ /* zod schema mirroring api/openapi/<domain>.yaml */ });

export async function POST(req: Request): Promise<Response> {
  return handleRoute(async () => {
    const ctx = await requireRole("<domain>:write");   // throws 403 if role lacks permission
    const input = await parseJsonBody(req, BodySchema); // throws 400 ValidationError on bad JSON/shape
    const result = await doTheThing(ctx.tenantId, ctx.userId, input);
    return created(result); // 201; use ok() for 200, noContent() for 204
  });
}
```

Never write your own `try { ... } catch { return Response.json(...) }` — `handleRoute` already:
maps any `AppError` subclass (`NotFoundError`, `ValidationError`, `ForbiddenError`,
`UnauthorizedError`, ...) to its documented status/body; maps Prisma's `P2025`
(`findUniqueOrThrow`/`findFirstOrThrow` on an RLS-invisible or missing row) to `NotFoundError`
automatically — this is why domain code is free to use `findUniqueOrThrow` directly instead of
manual null-checks; logs genuinely unexpected errors server-side with a `trace_id` (never leaked
to the client) so failures are traceable instead of silent 500s.

## List Endpoints: Cursor Pagination Convention

Every `GET` list endpoint (evidence: `catalog/products.ts` `listProducts`,
`catalog/suppliers.ts`) uses the same Prisma cursor idiom, never offset/page-number pagination:

```ts
// Route: query schema
const ListQuerySchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).optional(), // ALWAYS clamp -- see HI-1 below
  // ...domain filters
});

// Module: query
const limit = filters.limit ?? 20;
const rows = await tx.someModel.findMany({
  where: { /* ... */ },
  orderBy: [{ createdAt: "desc" }, { id: "desc" }], // tie-break on id -- required for a stable cursor
  take: limit + 1,                                   // fetch one extra to detect has_more
  ...(filters.cursor ? { cursor: { id: filters.cursor }, skip: 1 } : {}),
});
const hasMore = rows.length > limit;
const page = hasMore ? rows.slice(0, limit) : rows;
return { items: page, page: { next_cursor: hasMore ? (page.at(-1)?.id ?? null) : null, has_more: hasMore } };
```

If the list needs a derived value per row (e.g. current stock), batch it with ONE query over the
whole page's ids (see `getCurrentStockForProducts` in `stock-operation-scaffold`), never one
query per row in a loop — that exact per-row loop was code-reviewer finding HI-1 across four
endpoints, precisely because a hand-written list endpoint skipped this convention.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Custom try/catch instead of `handleRoute` | Always wrap the whole handler body in `handleRoute(async () => { ... })` |
| Calling the domain function before `requireRole`/`requireSession` | Auth check is always the FIRST line inside `handleRoute`'s callback |
| Validating body with raw `await req.json()` | Use `parseJsonBody(req, ZodSchema)` — gets the standard 400 `ValidationError` shape for free |
| Unbounded `limit` on a list endpoint | `z.coerce.number().int().min(1).max(100).optional()` — an unclamped limit turns a list endpoint into an unbounded query |
| Per-row query in a `.map`/loop over a list result | Batch with `WHERE id = ANY($1)`-style query over the whole page, per HI-1 |
| New AppError-like condition without a subclass | Add/reuse an `AppError` subclass in `libs/shared` so `handleRoute`/`toErrorResponse` map it automatically — don't format `Response.json` by hand in domain code |
