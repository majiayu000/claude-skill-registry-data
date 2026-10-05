---
name: factory-stack
description: Cross-build locked stack decisions and decision criteria for divergent choices. Read at the start of any new project. Covers runtime, language, ORM, auth provider, component library, deployment, and observability — what's a hard pick, what depends on context, and the criteria for context-driven picks.
---

# Factory stack

## Locked decisions (no per-project relitigation)

| Layer | Choice | Why |
|---|---|---|
| Runtime | Next.js App Router | Convergent across all customer repos; ecosystem fit for tRPC / server actions / Vercel deploy |
| Language | TypeScript | Convergent; non-negotiable |
| Validation | Zod | Pairs with both tRPC and server actions; field registry pattern depends on it |
| Server state | TanStack Query | Convergent across all repos that need server state |
| DB | Postgres via Neon (dev branches) or RDS (compliance) | Convergent |
| Forms | react-hook-form + Zod via resolver | Convergent |
| Email | Resend | Convergent |
| Linting | ESLint + Prettier + ESLint Drizzle rules where applicable | Convergent |
| Env vars | t3-oss/env-nextjs (Zod-validated, server/client split) | Convergent |

## Decision-criteria choices (pick per project; document in project's CLAUDE.md or DECISIONS.md)

### ORM — Drizzle vs Supabase auto-types vs raw pg

- **Drizzle** — default. Schema partitioning by domain (`_shared.ts`, `<domain>.ts`) + shared `timestamps` helper. `pgTableCreator()` for prefixing if the DB is shared.
- **Supabase auto-generated types** — when Supabase Auth + RLS is already doing real work. RLS policies are the contract; auto-types are a free byproduct.
- **Raw `pg`** — never for new projects. Migrate if encountered.

### Auth — Better Auth + orgs vs Supabase Auth + RLS vs Clerk

- **Better Auth + organization plugin** — default. Org + RBAC + 2FA out of the box; pairs with Drizzle.
- **Supabase Auth + RLS** — when RLS pays for itself (multi-role partner/distributor model, deeply branched authz at row level).
- **Clerk** — consumer/SSO-heavy, or when managed auth UI components matter.

The wrapper interface is the same regardless: `requireAuth()`, `requireRole()`, `withOrgContext()`. See `factory-auth.md` (Phase B) for the canonical wrapper shape.

### API style — server actions vs tRPC

- **Server actions** — default for feature-folder-colocated apps with one frontend consumer. Pairs with TanStack Query (`useMutation` wrapping the action).
- **tRPC** — when typed RPC contracts add leverage: ≥3 entities with cross-feature queries, multiple consumers, or a public API surface.
- **Pitfall:** don't import both. Pick a side per project.

### Component library — Mantine vs shadcn

- **Mantine** — CRUD-heavy / form-table dense / internal-tool surfaces. Built-in date pickers, multiselects, notifications save weeks. Pair with `mantine-form-zod-resolver`.
- **shadcn** — design flexibility / marketing-adjacent / unified Tailwind styling with a landing site. Pair with `react-hook-form` + `zodResolver`.
- **Same project, one choice.** Mixing leads to design drift.

### Deploy

- **Web (Next.js):** Vercel. PR previews via Neon dev branches in GitHub Actions.
- **Python services:** Cloud Run. CLI / Cloud Run API / Pub/Sub handler — see `factory-data-pipelines.md`.
- **Infra-as-code:** Terraform with environments/modules layout when AWS/RDS or HIPAA/FDA compliance is in play; skip when Vercel + Neon is sufficient.

### Observability

- **PostHog + Sentry from day one.** Non-negotiable. Easiest to start early, most expensive to backfill.
- Tag events by tool/feature so per-tool usage is queryable later.
- See `factory-observability.md` (Phase B) for activity logging and trace ID patterns.

## How to use this skill

1. At project kickoff, read this file end-to-end.
2. For decision-criteria choices, make the pick **explicitly** in the project's `CLAUDE.md` or a one-page `DECISIONS.md` (one line per decision).
3. Refer back when the project considers changing course — the criteria are the basis for that conversation.

## Pitfalls referenced elsewhere

See `factory-pitfalls.md` for the anti-patterns digest indexed across all `factory-*.md` skills.
