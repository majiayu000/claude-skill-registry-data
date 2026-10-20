---
name: verification-loop
description: Run a five-phase verification of work in Travel-Tool (build and type check, lint, backend tests, a diff secrets grep, and diff review) across the backend, web and mobile packages, then produce a PASS/FAIL verification report. Use when verifying work after completing a feature or refactor, before creating a PR, or when quality gates must pass.
license: MIT
metadata:
  origin: ECC
---

# Verification Loop Skill

A comprehensive verification system for Claude Code sessions.

## When to Use

Invoke this skill:
- After completing a feature or significant code change
- Before creating a PR
- When you want to ensure quality gates pass
- After refactoring

## Verification Phases

Only verify the packages the change touched: `backend/`, `web/`, `mobile/app/`. Each has its own `package.json` and lockfile. Run `npm ci` in a package first if `node_modules` is missing.

### Phase 1: Build and Type Check

```bash
set -o pipefail
(cd backend && npm run build 2>&1 | tail -30)        # tsc, backend type check
(cd web && npx --no-install tsc --noEmit 2>&1 | head -30)
(cd mobile/app && npx --no-install tsc --noEmit 2>&1 | head -30)
```

If the build fails, STOP and fix it before continuing.

### Phase 2: Lint Check

```bash
(cd backend && npm run lint 2>&1 | tail -30)          # CI runs this
(cd web && npm run lint 2>&1 | tail -30)
(cd mobile/app && npm run lint 2>&1 | tail -30)
```

### Phase 3: Test Suite

```bash
(cd backend && npm test 2>&1 | tail -50)             # CI runs this
```

The backend tests need Postgres (postgis/postgis:15-3.3) loaded with `backend/src/utils/schema.sql`, plus Redis, using the env vars in `.github/workflows/ci.yml`. If they aren't available, report the tests as NOT RUN with the reason, never as PASS. No coverage threshold is configured, so report coverage only if you ran it with `-- --coverage`.

Report:
- Total tests: X
- Passed: X
- Failed: X

### Phase 4: Security Scan
```bash
# Check for secrets
git diff -U0 | grep -nE "^\+.*(sk_live|sk-|api_key|secret|password)\s*[:=]" | head -10   # secrets in the diff

# Check for console.log
git diff -U0 | grep -n "^+.*console.log" | head -10   # only newly added logging
```

### Phase 5: Diff Review
```bash
# Show what changed
git diff --stat
git diff --name-only $(git merge-base HEAD origin/main 2>/dev/null || echo HEAD~1)
```

Review each changed file for:
- Unintended changes
- Missing error handling
- Potential edge cases

## Output Format

After running all phases, produce a verification report:

```
VERIFICATION REPORT
==================

Build+Types: [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL/NOT RUN] (X/Y passed; reason if not run)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```
