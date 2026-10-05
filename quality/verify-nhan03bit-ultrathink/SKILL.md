---
name: verify
description: Full pre-PR verification pipeline — build, typecheck, lint, test, secrets, git status
layer: utility
category: quality
triggers:
  - "verify"
  - "verification"
  - "ready for pr"
  - "pre-pr check"
  - "is it ready"
  - "check everything"
  - "run all checks"
inputs:
  - mode: "quick | full (default) | pre-commit | pre-pr"
  - path: "Project root or specific directory"
outputs:
  - report: "Structured pass/fail per check"
  - verdict: "Ready for PR: YES | NO"
linksTo:
  - quality-gate
  - test
  - code-review
  - security-scanner
  - build-resolver
linkedFrom:
  - cook
  - ship
  - plan-validate
preferredNextSkills:
  - pr-writer
  - code-review
fallbackSkills:
  - quality-gate
  - fix
riskLevel: low
memoryReadPolicy: none
memoryWritePolicy: selective
sideEffects:
  - "Runs test suite (may create test artifacts)"
---

# Verify

## Purpose

Run a comprehensive verification pipeline to determine if code is ready for PR or
deployment. Unlike quality-gate (which checks changed files), verify checks the
entire project state.

Use this when:
- About to open a PR
- Before merging to main
- After a large refactor
- CI is too slow and you want local verification first

## Key Concepts

### Verification Pipeline

Checks run in order. Each produces a PASS/FAIL/SKIP status:

| # | Check | Command | Blocks PR |
|---|-------|---------|-----------|
| 1 | Build | `npm run build` / `next build` | YES |
| 2 | Typecheck | `tsc --noEmit` | YES |
| 3 | Lint | `biome lint` / `eslint .` | On errors |
| 4 | Tests | `vitest run` / `jest` / `pytest` | YES |
| 5 | Console.log | `grep -rn` in src/ | WARNING |
| 6 | Secrets | Pattern grep | YES |
| 7 | Git Status | `git status` / `git diff --stat` | INFO |

### Modes

| Mode | Checks | Use When |
|------|--------|----------|
| **quick** | Typecheck + Lint | Mid-development sanity check |
| **full** | All 7 checks | Default, before PR |
| **pre-commit** | Format + Type + Lint + Secrets | Git pre-commit hook |
| **pre-pr** | All 7 + coverage threshold + branch check | Final PR readiness |

### Pre-PR Additional Checks

In `pre-pr` mode, also verify:
- Test coverage meets threshold (configurable, default 80%)
- Branch is up to date with base (`git merge-base --is-ancestor`)
- No merge conflict markers in files
- CHANGELOG or commit messages follow convention

## Workflow

### Phase 1: Environment Detection

```bash
# Detect project type and available tools
[[ -f package.json ]]     && PROJECT_TYPE="node"
[[ -f pyproject.toml ]]   && PROJECT_TYPE="python"
[[ -f go.mod ]]           && PROJECT_TYPE="go"
[[ -f Cargo.toml ]]       && PROJECT_TYPE="rust"

# Detect available runners
[[ -f biome.json ]]       && LINTER="biome"
[[ -f .eslintrc* ]]       && LINTER="eslint"
command -v vitest          && TEST_RUNNER="vitest"
command -v jest            && TEST_RUNNER="jest"
command -v pytest          && TEST_RUNNER="pytest"
```

### Phase 2: Execute Checks

Run each check, capture output, determine status:

```bash
# 1. Build
BUILD_OUT=$(npm run build 2>&1)
BUILD_STATUS=$?

# 2. Typecheck
TSC_OUT=$(npx tsc --noEmit 2>&1)
TSC_STATUS=$?

# 3. Lint
LINT_OUT=$(npx biome lint ./src 2>&1)
LINT_STATUS=$?

# 4. Tests
TEST_OUT=$(npx vitest run --reporter=verbose 2>&1)
TEST_STATUS=$?

# 5. Console.log
LOG_OUT=$(grep -rn 'console\.log' src/ --include='*.ts' --include='*.tsx' \
  | grep -v '\.test\.' | grep -v '\.spec\.' | grep -v 'node_modules')

# 6. Secrets
SECRET_PATTERNS='(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36}|password\s*=\s*["\x27][^"\x27]+)'
SECRET_OUT=$(grep -rn -E "$SECRET_PATTERNS" src/ --include='*.ts' --include='*.tsx' \
  | grep -v '\.test\.' | grep -v '\.env\.example')

# 7. Git Status
GIT_OUT=$(git status --porcelain)
GIT_DIFF=$(git diff --stat HEAD)
```

### Phase 3: Verdict

```
VERIFICATION: [PASS|FAIL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Build      ✅ Success (12.3s)
  Typecheck  ✅ Clean
  Lint       ⚠️  3 warnings
  Tests      ✅ 47/47 passed (94% coverage)
  Logs       ⚠️  2 console.log found
  Secrets    ✅ Clean
  Git        📋 3 files changed, 1 untracked

Ready for PR: YES (with minor warnings)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 4: Remediation (on FAIL)

For each failing check, output:
- The specific error/failure
- The file and line number
- The recommended fix
- Whether build-resolver or fix skill should handle it

## Best Practices

1. **Run verify before every PR** — catches issues CI would flag, saves round-trip time
2. **Use quick mode during development** — full mode only before PR
3. **Fix blockers before warnings** — build/type/test failures first
4. **Don't suppress warnings globally** — fix them or acknowledge them
5. **Check git status last** — ensures you know what's being committed
6. **Track verification results** — log to memory for session analytics
7. **Chain to build-resolver** — if typecheck fails, hand off to build-resolver agent

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Running full build every time | Slow feedback loop | Use quick mode for typecheck-only |
| Ignoring lint warnings | Accumulate technical debt | Address warnings or configure rules |
| Not checking git status | Commit unintended files | Always review what's staged |
| Skipping test step | Ship broken functionality | Tests are non-negotiable in full mode |
| Secret false positives fatigue | Real secrets slip through | Refine patterns, add allowlists |
| Not checking branch freshness | Merge conflicts after PR | In pre-pr mode, check merge-base |

## Examples

### Quick Verification

```
> /verify --quick

VERIFICATION: PASS
  Typecheck  ✅ Clean
  Lint       ✅ Clean
  Ready: YES (quick mode — run full before PR)
```

### Failed Verification

```
> /verify

VERIFICATION: FAIL
  Build      ❌ Failed (exit code 1)
    Error: src/app/page.tsx: Cannot find module './components/Header'
  Typecheck  ❌ 3 errors
    src/lib/auth.ts(12,5): TS2322 Type 'null' not assignable to 'User'
    src/api/route.ts(8,1): TS2305 Module has no exported member 'handler'
    src/api/route.ts(15,3): TS2345 Argument type mismatch
  Lint       SKIP (blocked by build failure)
  Tests      SKIP (blocked by build failure)
  Logs       ✅ Clean
  Secrets    ✅ Clean
  Git        📋 5 files changed

  Ready for PR: NO
  Recommendation: Run build-resolver to fix 3 type errors, then re-verify
```

## Chaining

Verify integrates with the skill mesh:

```
verify FAIL → build-resolver (fix types) → verify PASS → pr-writer (create PR)
verify FAIL → fix (complex logic errors) → test (add missing tests) → verify PASS
cook → implement → verify → code-review → ship
```
