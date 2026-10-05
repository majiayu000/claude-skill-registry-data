---
description: Build a complete Angular frontend page end-to-end — design system lookup, component scaffold, feature service, reactive form validation, loading/error/empty states, and route registration. Use for "build me a page for X" or "add the Y management screen".
argument-hint: <page name and app, e.g. "product list page in admin-web" or "checkout page in customer-web">
---

# Build Page: $ARGUMENTS

## Step 1 — Design system lookup

Before writing a line of code, search for design guidance:

```bash
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "$ARGUMENTS" --design-system --stack angular
```

If the global `ui-ux-pro-max` skill is not installed, use the principles from `.claude/skills/ui-ux-pro-max/SKILL.md` directly.

## Step 2 — Identify the target app

- admin-web (Angular standalone) → feature components in `src/app/features/{feature}/`
- customer-web (Angular standalone) → same structure, plus `Title`/`Meta` SEO calls
- customer-mobile (Ionic Angular) → pages in `src/app/pages/`, components in `src/app/components/{feature}/`

## Step 3 — Read the Prisma model

Find the Prisma model that backs this domain (in the correct `schema.*.prisma` per `relational-database.md`). Before writing the Angular `Validators`, map every field constraint using the table in `validation-chain.instructions.md`:
- Required fields → `Validators.required`
- `@db.VarChar(N)` → `Validators.maxLength(N)`
- Email fields → `Validators.email`
- Phone fields → `Validators.pattern(/^(\+27|0)[6-8][0-9]{8}$/)`
- Enums → `Validators.required` + a constrained `<select>`
- `@unique` fields → handled by server 409, not client-side `Validators`

The Angular `Validators` must mirror the backend `class-validator` DTO exactly.

## Step 4 — Generate in this order

1. **Feature service** (`features/{domain}/{domain}.service.ts`) — typed request/response via `ApiClientService`
2. **List component** — data table or content layout with Signals for `items`/`loading`/`error`
3. **Form component** — `FormBuilder` + `Validators`, `submitting` signal, `serverError` signal
4. **Route registration** — `app.routes.ts` with `loadComponent` + `MsalGuard`

## Non-negotiable for every page

- Loading skeleton while data fetches
- Error state with a retry button
- Empty state with a clear call-to-action
- **Client `Validators` failure → inline error below the field, no server round-trip**
- **Server 400/409/500 → `serverError` signal or toast, no inline error**
- All forms: required validation, email format, phone format, max lengths matching `@db.VarChar(N)` from Prisma
- No `alert()`, `confirm()`, or native HTML form validation attributes
- Every list page: search input + filter controls + pagination
- Tailwind utility classes only — no inline styles, no CSS modules
- No `any` type anywhere
- Signals for all component state — never `BehaviorSubject`

## Step 5 — Typecheck

```bash
pnpm --filter <app-name> typecheck
```

Zero errors before marking complete.
