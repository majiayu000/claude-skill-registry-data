---
name: fst-e2e-critical-flows
description: Safe Playwright E2E patterns for Otgruzka — test env writes, production read-only unless explicitly allowed.
---

# fst-e2e-critical-flows

Критические пользовательские цепочки. **Production:** по умолчанию только read-only проверки.

## Environments

| Env | Data writes |
|-----|-------------|
| Production Vercel | **Read-only** (login, navigate, assert visible state) unless user explicitly allows test writes |
| Local `npm run dev` | Same Firebase/SQL as prod — treat as prod data; prefer dedicated test accounts |
| Future CI test project | Only place for create/cleanup test entities |

## Critical flows (read-safe on prod)

1. **Login** — Firebase Auth `otgruzka-tovara` (use test/sysadmin account only)
2. **Navigate** — `#/month`, `#/warehouse`, `#/hr`, `#/tasks` load without console errors
3. **Read store** — tables render rows, sync indicator not error-stuck
4. **Print preview** — open print modal, no crash (don't submit post)

## Write flows (test env / explicit permission only)

Pattern:

```
login → navigate → create test entity (unique prefix E2E-<timestamp>) → save
→ assert SQL/post-condition via UI or test API
→ assert journal entry in #/journals
→ reload → state persists
→ cleanup: delete/archive only records created by test
```

Domains requiring **`fst-domain-invariants`** review before write tests:

- Timesheet cell edits (month close)
- Warehouse document post
- HR employee create
- Finance advance post

## Playwright conventions (when adding tests)

- Project folder: prefer `e2e/` or `tests/e2e/` (create when user requests automation)
- `storageState` for auth — never commit credentials file
- Selectors: `data-coach`, role, label — avoid brittle CSS
- Screenshot on failure only

## Post-conditions

| Change type | Check |
|-------------|-------|
| Store mutation | Journal `#/journals` filter by action |
| Warehouse doc | Document status posted + movement row |
| Timesheet | Cell value after F5 |

## Cleanup rules

- Delete only entities with test prefix created in same run
- Never `clear:*` / bulk wipe
- Never import local JSON to SQL

## Related

- Prod UX verify: **`otgruzka-browser-verify`**
- Pre-implementation: **`project-guardian`**
- Post-implementation: **`product-verifier`**
