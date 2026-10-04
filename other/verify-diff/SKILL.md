---
name: verify-diff
description: Compare test results and behavior between the current branch and the base branch. Proves changes work by diffing test output and catching regressions before push.
disable-model-invocation: true
allowed-tools: Read Bash
---

# Verify Diff — Prove It Works

Compare the current branch against the **base branch** (`main`, or `develop`/whatever your project integrates into) to verify no regressions were introduced.

> Substitute your base branch and your project's own quality-gate commands throughout. The commands below use generic placeholders — read the real ones from `package.json` scripts / your build config.

## Steps

### 1. Identify Changed Files
```bash
git diff main...HEAD --name-only
```

### 2. Run Tests on Current Branch
```bash
<test command> 2>&1 | tee /tmp/verify-diff-current.txt
```

### 3. Run Type Check
```bash
<typecheck command> 2>&1 | tee /tmp/verify-diff-types.txt
```

### 4. Run Lint
```bash
<lint command> 2>&1 | tee /tmp/verify-diff-lint.txt
```

### 5. Compare Against the Base Branch
```bash
git stash
git checkout main
<test command> 2>&1 | tee /tmp/verify-diff-base.txt
git checkout -
git stash pop
```

### 6. Diff Results
Compare test output between branches. Report:
- New test failures (tests that passed on the base branch but fail on the current branch)
- New lint errors introduced
- New type errors introduced
- Tests that were removed (may indicate coverage regression)

## Output Format

```
## Verify Diff Report

**Branch:** feature/my-feature vs main
**Changed files:** 12

### Test Comparison
- base:    142 passed, 0 failed
- current: 143 passed, 0 failed (+1 new test)
- No regressions ✓

### Type Check
- No new type errors ✓

### Lint
- No new lint errors ✓

### Verdict: PASS — Safe to push
```

If regressions are found:
```
### Verdict: FAIL — Regressions detected
- `someModule.test.ts > handles empty input` — FAILED (was passing on the base branch)
```

## Pre-Push Hook

If the skill folder includes a companion `pre-push-check.sh`, it runs a lightweight version (tests + types only) to gate pushes. Wire your project's actual commands into it before relying on it.
