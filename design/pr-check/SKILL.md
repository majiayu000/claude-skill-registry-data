---
name: pr-check
description: Pre-submit validation checklist for PRs
disable-model-invocation: true
---

# PR Check Skill

## Purpose

Run comprehensive pre-submit validation before creating a pull request.

## Checklist

### 1. Type Check

```bash
pnpm --filter portal type-check
```

- Must pass with no errors

### 2. Lint Check

```bash
pnpm lint
```

- Must pass with no warnings

### 3. Format Check

```bash
pnpm exec prettier --check "**/*.{ts,tsx,md}"
```

- If fails, run `pnpm format` to fix

### 4. Test Suite

```bash
# Unit tests
pnpm --filter portal test

# E2E tests (requires dev server)
pnpm test:e2e
```

### 5. Design System Audit

Check for forbidden patterns in changed files:

- `font-bold`, `font-semibold` -> use `font-medium`
- `bg-white/5`, `border-white/10` -> use design tokens
- `shadow-*` -> use border for depth
- Direct `clsx`/`tailwind-merge` -> use `cn()` from `@repo/ui/lib/utils`

### 6. Build Verification

```bash
pnpm --filter portal build
```

- Must complete without errors

### 7. Git Status

- No uncommitted changes
- Branch name follows convention (feature/_, fix/_, chore/\*)

## Output Format

```
## PR Check Results

- [ ] Type check: PASS/FAIL
- [ ] Lint: PASS/FAIL
- [ ] Format: PASS/FAIL
- [ ] Tests: PASS/FAIL (X passed, Y failed)
- [ ] Design system: PASS/FAIL (list violations)
- [ ] Build: PASS/FAIL

Ready to submit: YES/NO
```

## If Failures Found

List each failure with:

1. Command that failed
2. Error message
3. Suggested fix
