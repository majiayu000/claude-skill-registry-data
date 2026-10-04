---
name: model-schema-check
description: >
  Review model vs database schema consistency on ndestates-io using the local cache and project tooling.
  Use before/after migrations or when schema drift is suspected. Strictly test DB only.
argument-hint: "Scope, e.g. 'Property model', 'valuation tables', 'all', 'after recent migrations'"
user-invocable: true
disable-model-invocation: false
---

# Model Schema Check (Cache-First + Safe)

**First action**: Load cache via `/load-project-cache-first`.

## Required Cache Reads
- `docs/codebase/CONVENTIONS.md` — Migration and schema rules (never blanket migrate on live, use --path, safety)
- `docs/codebase/TESTING.md` — Test DB rules (always target `test`)
- `docs/codebase/CONCERNS.md` — Any open schema items
- `config/model-schema-checker.php` or equivalent project checker (if present)
- Latest TODO and `.grok/memories/INDEX.md`

## Execution Rules (non-negotiable)
- All checks must run against the `test` database only. Confirm with `ddev exec php -r "echo getenv('DB_DATABASE');"`.
- Never run destructive commands on `db`.
- Use DDEV for all: `ddev exec ...`
- Prefer read-only inspection (`php artisan model-schema-check` or project script if defined).
- Run security checklist after schema-impacting changes.
- Follow copilot-instructions.md §5-7 (data safety, recovery-first).

## Output Requirements
- List of models/tables checked
- Any mismatches (columns, types, indexes, FKs)
- Mapping to specific migration files
- Reference to numbered CONCERNS if applicable
- Safe remediation suggestions only (no auto-execution)

Always cite the exact cache files and lines used. Hand off execution to main or todo if needed.

Source: `.grok/prompts/model-schema-check.md` (full content embedded here + in prompts dir)
