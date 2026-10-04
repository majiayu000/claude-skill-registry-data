---
model_tier: medium
name: schema-review
description: "Use when reviewing a migration diff or schema change for scale hazards — indexes, unsafe migrations, unbounded growth, N+1. Triggers on 'review this migration', 'will this scale'."
domain: engineering
workspaces:
  - engineering
packs:
  - scale-discipline
trust:
  level: professional
install:
  default: false
  removable: true
---

# schema-review

## When to use

- A migration diff, new migration file, or schema change is under review
  and the question is scale-shaped: indexes, reversibility, growth,
  query patterns against the new columns.
- The user asks "will this scale", "review this migration", "check the
  schema", or a PR touches `migrations/`, `schema.prisma`, or raw `.sql`
  migration files.
- NOT for runtime performance analysis of live traffic (no APM here —
  route to `performance-analysis`) and NOT for authoring a new migration
  from scratch (route to `laravel-migration` or the stack-native tool,
  then come back with the diff).

## Procedure

1. **Detect the stack surface** in the diff: Laravel migrations
   (`database/migrations/*.php`), Prisma (`schema.prisma` +
   `prisma/migrations/**/migration.sql`), raw SQL (`*.sql`). One diff can
   carry several.
2. **Run the deterministic linter** on the touched files plus the query
   surface that references the changed tables:

   ```bash
   npx tsx node_modules/@event4u/agent-config/src/scripts/lint_persistence.ts -- --dir <path> [--stack eloquent|prisma|raw-sql] --format json
   ```

   The linter emits `gate` findings (pattern-detected: F1 N+1, F2
   index-parity, F3 unbounded reads, F6 migration-safety, F7
   growth-budget, F8 audit-coverage, F9 sync-in-handler, F11 non-durable
   async) and `advice` findings (heuristics — never treat as blockers).
3. **Walk the gap table** — for every `gate` finding decide: fix, or
   waiver with a reason (`// no-index: <reason>`, `// sync-required:
   <reason>`, `-- no-retention: <reason>`, …). An empty waiver reason is
   itself a finding.
4. **Check the R-A6/R-A7 invariants by hand** where the linter is blind:
   reversibility of data transformations, retention policy for any new
   append-only table (the `-- retention: <policy>` line), backfill plan
   for new NOT NULL columns on large tables.
5. **Report waiver density neutrally** — count waivers per rule; state
   both readings (informed exceptions vs rule misfit) and let the human
   decide. Density alone is never a verdict.

## Output

The review MUST contain:

1. **Gap table** — one row per finding: `rule · file:line · finding ·
   proposed action (fix | waiver | accepted)`, gate findings first,
   advice findings clearly marked as advice.
2. **Waiver-density line** — `N waivers across M findings` with the
   two-reading note (informed exceptions vs rule misfit).
3. A one-line verdict: ready / needs fixes / needs human schema decision
   — never a bare "looks good" without the table.

## Gotcha

- The linter proves **pattern presence**, not instance-level correctness
  — a flagged `Http::` call in a controller may be legitimately sync
  (then it gets a `// sync-required:` waiver with a reason), and a clean
  run does not prove the schema scales. Say what was checked, not more.
- Prisma's `@relation` fields are indexed implicitly on some connectors
  and not on others — when the linter reports a missing FK index on a
  Prisma model, verify the connector before calling it a defect.

## Do NOT

- Do NOT gate a review on `advice`-tier findings (F4 denormalization,
  F10 event-decoupling heuristics) — they are review inputs, not
  blockers.
- Do NOT strip or rewrite existing waivers — surface stale-looking ones
  and ask.
- Do NOT invent index recommendations for columns the query surface
  never filters or orders by — index parity cuts both ways; unused
  indexes cost write throughput.
