---
name: gaa-admin-change
description: "Checklist to run before changing apps/web/gaa-admin, which folds five formerly separate apps (cap, hr, wxwatch, wxproducts, salesbus) into one, so an edit can break another module. Use when about to edit apps/web/gaa-admin/src, especially shared layout, providers or auth."
---

# gaa-admin Cross-Cutting Change

`gaa-admin` is the single most-repeated caution in this repo's `AGENTS.md` (the
Blast-Radius Gate names it explicitly) — this skill is that caution turned
into a checklist, because "remember gaa-admin is cross-cutting" is easy to
read and easy to forget mid-task.

## First question: which module, and is the change actually scoped to it?

The five folded modules, their route prefix, and data source:

| Prefix | Data | Notes |
|---|---|---|
| `/hr` | FastAPI `/api/v1/hr/*` | duty roster, approvals inbox, HR Setup |
| `/cap` | FastAPI `/api/cap/*` (server-side direct, `CAP_API_URL`) | |
| `/salesbus` | FastAPI `/api/v1/stores/*` (Stores module: internal requisition) | own `CartProvider`, own `AppShell`; PWA dropped; URL kept until a rename is approved |
| `/wxwatch` | FastAPI `/api/v1/wxwatch/*` | image downloads via `/_backend/wxwatch/` |
| `/wxproducts` | FastAPI `/api/v1/wxproducts/*`, **separate wxproducts Postgres** | Saved-revision PDF export via FastAPI `/products/{id}/revisions/{revision}/pdf` |

If your change stays entirely inside `(admin)/<prefix>/` and `components/<prefix>/`
for exactly one of these, and doesn't touch anything below, the blast radius is
that module alone — say so and proceed normally.

## Shared surfaces — touching any of these affects all five modules

- `(admin)/layout.tsx` — the single auth gate; every module is gated here, not
  per-page. A bug here breaks auth for cap/hr/wxwatch/wxproducts/salesbus at
  once.
- `src/providers/` (`QueryProvider`, etc.) and anything under
  `src/components/providers/ApiProvider.tsx`
- `src/lib/server-session.ts`, `src/lib/auth.ts`, `src/lib/auth-config.ts`,
  `src/lib/auth-redirect.ts` — shared auth helpers, not per-module
- `src/app/api/[...path]/route.ts` + `src/proxy.ts` — the shared API proxy
- `@barrelsgd/ui` primitives imported by more than one module
- `src/lib/query-client.ts` — shared query client config
- `src/lib/fonts/registry.ts`, `globals.css` — shared design tokens/fonts

If the change touches any of these, the Blast-Radius Gate applies at full
strength: check all five modules, not just the one you started in.

## Domain boundaries that must NOT be crossed

- **Weather ownership**: `wxwatch`/`wxproducts` migrations and authored
  products belong to FastAPI (Alembic) — never introduce a Drizzle writer or
  migration for these two. gaa-admin has no ORM or database access; use the
  generated `@barrelsgd/api-client` types.
- **Database separation**: `janitorial`, `transport`,
  `wxwatch`/`wxproducts` (all FastAPI/Alembic) are separate domain databases —
  never merge them, even if a query would be simpler joined.
- **salesbus** keeps its own `CartProvider` and `AppShell`, scoped via
  `(admin)/salesbus/layout.tsx` — don't lift its state into a shared provider.

## Verification

```bash
# From apps/web/gaa-admin
pnpm vitest run                    # unit tests
pnpm test:coverage                 # if the change touches business logic
# There is no gaa-admin test:e2e script. Use its Vitest suite and browser smoke checks.

# From repo root
turbo run test --filter=@barrelsgd/web-gaa-admin
pnpm guardrails:staged             # catches FastAPI route/schema changes without openapi.json
```

If the change touched a shared surface (see above), also smoke-test at least
one route from each of the other four modules, not just the one you changed —
the folded-app auth gate and shared providers mean a regression there often
shows up as "unrelated module broke," not an error at the point of change.
