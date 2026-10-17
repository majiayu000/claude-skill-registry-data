---
name: smoke-coverage
description: "Audit smoke test coverage across all skills. Report which have tests, which don't, and which test scripts actually run. Trigger: /smoke-coverage"
trigger: /smoke-coverage
---
# /smoke-coverage

Every skill should have a smoke test. This skill audits coverage and execution status.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What this is for

- Skills without any fixture or smoke test
- Scripts that reference files missing from fixture
- Smoke test gaps per cluster
- **Read-only skill.** No code changes.

## What You Must Do When Invoked

### Step 1

`-ProjectDir` target

### Step 2

Run collector: per skill check fixture dir, script existence, referenced files

### Step 3

Report gaps by cluster

### Step 4

Write `smoke-coverage-report.md`

## Usage

```
/smoke-coverage           # interactive
/smoke-coverage <dir>     # scan project
/smoke-coverage -help
```

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).