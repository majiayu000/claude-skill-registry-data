---
name: japa-backend-auditor
description: Full systematic audit of the JapaConnect Go backend API for standards drift, missing features, unwired handlers, missing catalog entries, security gaps, and architectural conformance. Use when the user says "run backend audit", "audit the backend", "full backend sweep", or triggers /japa-backend-auditor. Cross-references codebase against the JEOS specification catalogs (routes, Asynq tasks, Valkey keys, system settings, RBAC, migrations, env vars).
---

# Japa Backend Auditor

Systematic sweep of the JapaConnect Go backend against JEOS catalogs. Not a code reviewer (single PR) or debugger (specific bug) — this is a proactive full-backend conformance audit.

## Stack

- Go 1.26, Chi router, sqlc + pgx/v5 + PostgreSQL 18 (pgvector)
- Asynq (68 tasks catalogued in JEOS), Valkey (jc: namespace, 34 key patterns)
- Meilisearch 1.45, SeaweedFS, imgproxy, Honcho (separate logical DB)
- GlitchTip (self-hosted), Env var prefix: JC_, API base: /api/v1

## Audit Checklist

### 0 Route Completeness
1. List every Chi route registered in the codebase.
2. Verify if the api backend routes and features cover all use cases in .JEOS Specification
3. Verify all entities are properly gated using RBAC acccording to JEOS
3. Verify all RBAC entities have CRUD operation endpoints
4. Flag: routes and features not covered yet in JEOS

### 1. Route Catalog Coverage
2. Cross-reference against the API routes catalog in JEOS (`conventions/api-routes-catalog.md`).
3. Flag: route in code but absent from catalog (undocumented).
4. Flag: route in catalog but absent from code (phantom).
5. Confirm all routes mounted under `/api/v1`.

### 2. Asynq Task Catalog Coverage
1. List every task name registered in the Asynq server mux.
2. List every task enqueued anywhere in the codebase.
3. Cross-reference both lists against the 68-task JEOS catalog (`sections/11-job-queue-asynq.md`).
4. Flag: task in code but not in catalog (undocumented).
5. Flag: task in catalog but no handler registered (dead entry).
6. Flag: task enqueued but no matching handler (orphaned enqueue).

### 3. Valkey Key Pattern Compliance
1. List every Valkey key string constructed in the codebase.
2. Confirm each key begins with `jc:` prefix.
3. Cross-reference against the 34-pattern JEOS catalog (`conventions/valkey-keys-catalog.md`).
4. Flag: key pattern not in catalog.
5. Flag: key written without explicit TTL where one is expected.

### 4. System Settings Catalog Coverage
1. List every `system_settings` key read or written.
2. Cross-reference against the 49-key JEOS catalog (`conventions/system-settings-catalog.md`).
3. Flag: key used in code but absent from catalog.
4. Flag: key in catalog never read or written in code (stale).

### 5. Migration & Table Integrity
1. Count total migration files; confirm they account for all 145 tables in `schemas/MIGRATION-ORDER.md`.
2. Confirm migration files numbered/ordered correctly — no gaps, no duplicates.
3. Flag: table referenced in sqlc queries but absent from migrations.
4. Flag: table in migrations with no corresponding sqlc query file.
5. Confirm Honcho DB schema entirely separate from main migration pipeline.

### 6. RBAC Coverage
1. For every non-public Chi route, confirm authentication middleware is applied.
2. For every write/update/delete handler, confirm permission check (UserGroup → UserRole → Permission).
3. List all permission nodes in code; cross-reference against JEOS permissions catalog.
4. Confirm all `ai.context.*` permission nodes default to OFF in catalog and seed data.

### 7. Security Sweep
1. Check all handler input-parsing paths for missing validation/sanitization before reaching sqlc queries or external services.
3. Confirm Honcho erasure on account deletion is hard deletion (not soft, not best-effort, not queued-only).
4. Check for direct MinIO references (MinIO archived per ADR-048; must use SeaweedFS).

### 8. Financial Integrity
1. Confirm no mutable balance or running-total column in Wallet/Credits tables — ledger must be purely transactional.
2. Confirm no Credits → Points reverse conversion in any code path.
3. Confirm Points → Credits conversion is one-way and irreversible in code (not just docs).
4. Confirm no Credits expiration logic in any handler, task, or scheduled job.

### 9. SQLC & Database Hygiene
1. List sqlc query files with no corresponding handler (orphaned queries).
2. Check for raw pgx query execution (`conn.Exec`, `conn.Query` with inline SQL) where sqlc should be used.
3. Check for N+1 query patterns: loops issuing individual SELECTs where JOIN/IN would be correct.

### 10. Environment Variable Compliance
1. List every `os.Getenv` or config struct field.
2. Confirm all env var names begin with `JC_` prefix.
3. Flag: env var in code but not in JEOS env var catalog.
4. Flag: hardcoded credential, hostname, or secret that should be an env var.

### 11. Error Tracking Coverage
1. Confirm GlitchTip capture in all top-level error paths (unrecoverable handler errors, Asynq panics, critical Valkey/DB failures).
2. Flag: error path that logs to stdout only without GlitchTip capture.

### 12. House Rules Compliance
1. Scan commits/PRs for AI-generated labels (AGENTS.md Rule 17). Flag violations.
2. Confirm no Coupon embed stores a resolved coupon code — only entity IDs.
3. Confirm no Honcho code passes through main sqlc/migrate pipeline.

## Output Format

Produce a structured audit report:

```
SUMMARY
- Total findings by severity: Critical / High / Medium / Low / Info
- Total findings by category

FINDINGS
  ID:        AUDIT-BE-###
  Category:  Routes | Tasks | Valkey | Settings | Migrations | RBAC |
             Security | Financial | Database | Environment | Monitoring |
             Standards
  Severity:  Critical | High | Medium | Low | Info
  Location:  File path and line range (or "catalog" if catalog-only)
  Finding:   One sentence describing the deviation
  Action:    The specific change required to resolve it

CATALOG GAPS
- Undocumented routes, tasks, keys, or settings found in code
- Dead catalog entries with no code counterpart

CLEAN AREAS
- Explicitly confirm each checklist area that found no issues
```

## JEOS Files to Load

Before running the audit, load these JEOS reference files:
- `JEOS.md` (index)
- `conventions/api-routes-catalog.md`
- `sections/11-job-queue-asynq.md`
- `conventions/valkey-keys-catalog.md`
- `conventions/system-settings-catalog.md`
- `schemas/MIGRATION-ORDER.md`
- `sections/03-rbac.md`
- `conventions/permissions-catalog.md`
- `sections/02-authentication-sessions.md`

Load `sections/` files referenced by specific findings as needed. Do not load all 56 sections at once.
