---
name: qa
description: Unified QA pass using existing qa-* scripts. Runs appropriate quality checks based on scope (dev/pass/full). Use when user says /qa, "run tests", "quality check", "is it broken", or before shipping work.
---

# QA (Unified Quality Assurance Pass)

## Purpose

Single entry point for all QA scripts. Pick the right level based on context.

## Levels

| Level  | Script                | When                             | Duration |
| ------ | --------------------- | -------------------------------- | -------- |
| `dev`  | `scripts/qa-dev.mjs`  | Quick sanity during development  | ~30s     |
| `pass` | `scripts/qa-pass.mjs` | After completing a feature       | ~2min    |
| `full` | `scripts/qa-full.mjs` | Before shipping / end of session | ~5min    |

## Procedure

### Phase 1: Select Level

- Default: `pass` (covers most cases)
- If user says "quick": use `dev`
- If user says "full" or "everything": use `full`
- If about to `/ship` or `/close-session`: use `full`

### Phase 2: Pre-Flight

1. Confirm dev server at `http://localhost:3100`
2. Run `npx tsc --noEmit --skipLibCheck` first (type errors = instant fail)
3. If tsc fails: fix type errors, then continue

### Phase 3: Execute

```bash
node scripts/qa-[level].mjs
```

Capture output. Parse results.

### Phase 4: Report

```
## QA [level] Results [date]

TypeScript: PASS/FAIL
Tests: X passed, Y failed, Z skipped
Build: PASS/FAIL (if full level)

### Failures (if any)
- [test name]: [error summary]
```

### Phase 5: Fix or Flag

- If < 3 failures and they're in code you touched: fix them
- If failures are in unrelated code: flag but don't block
- If > 5 failures: something systemic, investigate root cause

## Constraints

- Never skip tsc check
- Never report "all good" without actually running the script
- If script doesn't exist or errors on startup, report that (don't fake results)
