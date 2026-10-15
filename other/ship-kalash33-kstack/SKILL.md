---
name: ship
description: |
  Release engineer that syncs main, runs tests, audits coverage, pushes, and
  opens a PR. Bootstraps test frameworks if missing. Blocks on failing tests
  or critical review findings.
  Use when: "ship it", "create a pr", "push to main", "deploy", "merge",
  or when code is ready to go.
---

# /ship — Release Engineer

Tests pass. Coverage audited. PR opened. Done.

## When to Use

- Code is ready to merge
- After `/review` and `/qa` pass
- When you say "ship it"

## Process

### Step 1: Pre-flight Checks

```bash
# Sync with main
git fetch origin main
git rebase origin/main

# Run tests
{test_command}

# Check for uncommitted changes
git status
```

If tests fail → stop, report, suggest `/qa`.
If merge conflicts → stop, report, help resolve.

### Step 2: Coverage Audit

Run coverage tool and report:
```
Coverage: 87% (target: 80%) ✅
  src/api.ts: 92%
  src/queue.ts: 71% ⚠️ (below target)
  src/utils.ts: 100%
```

### Step 3: Commit & Push

- Ensure all changes are committed with conventional commit messages
- Push to the feature branch
- If no feature branch, create one: `feat/{slug}`

### Step 4: Open PR

Create a PR with:
- **Title**: Conventional format — `feat: {description}` or `fix: {description}`
- **Body**: What changed, why, how to test
- **Labels**: Auto-detect (feature, bugfix, docs, etc.)
- **Linked issues**: If plan references an issue

### Step 5: Report

```
## Ship Report

Branch: feat/notification-triage
Tests: 51 passed, 0 failed
Coverage: 87% (+4% from last ship)
PR: github.com/you/app/pull/42

### Changes
- 3 files changed, +142 -23
- New: src/triage.ts, tests/triage.test.ts
- Modified: src/api.ts
```

## Blockers

Ship will NOT proceed if:
- Tests are failing
- Critical security issues from `/review` are unresolved
- Uncommitted changes exist without explanation
- Branch is behind main with conflicts

## Chaining

- **Before**: `/review` + `/qa` (both should pass first)
- **After**: `/retro` (reflect on what shipped)
