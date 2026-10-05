---
description: Assess release readiness with risk analysis, checklists and go/no-go verdict
---

# Release Readiness

## Pre-Release Checklist

1. All planned work completed or explicitly scoped out
2. Tests pass (`/project:test-full`)
3. No uncommitted changes
4. Migrations are idempotent (IF NOT EXISTS, DO $$...$$)
5. ENV_REFERENCE.md updated if new env vars
6. No secrets in diff (`/project:secrets-scan`)
7. Compose config validates
8. Rollback path documented
9. CHANGELOG.md updated

## Risk Categories

| Category | Check |
|----------|-------|
| Code | Untested changes, large diffs |
| Migration | New SQL, schema changes |
| Config | New env vars, compose changes |
| Rollback | Data migrations, one-way changes |
| Docs | Changes without updated docs |

## Verdict Options

- **GO**: All checks pass, risks mitigated
- **CONDITIONAL-GO**: Minor risks with documented mitigations
- **NO-GO**: Blocking issues exist, must resolve first
