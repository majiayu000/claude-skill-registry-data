---
name: vkc-drizzle-schema-migration
description: Standardize Drizzle schema/migration/seed workflow for Viet K-Connect. Use when adding or changing DB tables, especially DB-driven visa rulesets and document templates (no hardcoding).
metadata:
  short-description: Drizzle schema + migration workflow
---

# VKC Drizzle Schema & Migration

## When to use

- Adding/updating DB tables/enums/indexes
- Introducing DB-driven configuration (visa rulesets, doc templates, regulation snapshots)

## Hard rules

- DB schema lives in `src/lib/db/schema.ts`.
- Migrations are generated/applied via `drizzle-kit` (`npm run db:generate`, `npm run db:migrate`).
- **Visa rulesets and doc templates MUST be DB tables**, not hardcoded TS objects.
- Coordinate ownership: `src/lib/db/schema.ts` and `src/lib/db/migrations/**` should not be modified concurrently by multiple agents.

## Workflow

1) Update `src/lib/db/schema.ts`
- Add table(s), enum(s), indexes.
- Prefer explicit indexes for `(userId, createdAt)` where rate limits depend on time windows.

2) Generate migration
- `npm run db:generate`

3) Apply migration locally (if DB configured)
- `npm run db:migrate`

4) Seed (if needed)
- Use `npm run db:seed` or project seed scripts.

## References

- Rules & examples: `.codex/skills/vkc-drizzle-schema-migration/references/drizzle-rules.md`

