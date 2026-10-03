---
name: ls-supabase
description: Guide Supabase application work. Use for Supabase Auth, Postgres, RLS,
  Edge Functions, Storage, Realtime, migrations, and local development.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/supabase/agent-skills
    source_path: skills/supabase/SKILL.md
    source_commit: 1356046015476711a769601079262b5635929427
    source_ref: main
    source_sha256: 1171386737b231610fa42485707272765c3516a9bbc0bd2c6c161a8cee3d7d33
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Supabase

Use this skill when working on Supabase tasks.

## Workflow

- Inspect project config, migrations, generated types, RLS policies, auth flow, and environment variables before changes.
- Treat service-role keys and database URLs as secrets; prefer local development and migration review before production.
- Validate RLS, schema changes, and auth edge cases with focused tests or SQL checks.
- For performance work, start with the query shape and `EXPLAIN` plan before adding indexes, denormalizing data, or changing client code.
- Review indexes with workload context, including candidate, redundant, partial, composite, and foreign-key indexes; use Supabase advisor tooling where available.
- Check RLS policy performance separately from correctness. Avoid policy predicates that force avoidable per-row work on hot paths.
- Use `pg_stat_statements` or equivalent query statistics to identify slow, frequent, or high-variance statements before optimizing.
- Inspect connection pooling, transaction scope, lock waits, long-running transactions, and migration ordering when performance or deploy safety is involved.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.
- Primary Supabase docs for Postgres review:
  - https://supabase.com/docs/guides/database/query-optimization
  - https://supabase.com/docs/guides/database/postgres/indexes
  - https://supabase.com/docs/guides/database/debugging-performance
  - https://supabase.com/docs/guides/database/extensions/pg_stat_statements
  - https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv

## Provenance

- Source: `https://github.com/supabase/agent-skills`
- Ref: `main` at `1356046015476711a769601079262b5635929427`
- Source path: `skills/supabase/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `1171386737b231610fa42485707272765c3516a9bbc0bd2c6c161a8cee3d7d33`
