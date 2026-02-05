---
name: fix-failed-pr
description: Check GitHub PR status, identify failures in CI/checks, analyze errors, attempt fixes, and push changes. Use this skill when the user asks to fix a failed PR, check PR status, fix CI failures, or resolve PR checks.
---

# Fix Failed Pull Request

## Commands

| Action       | Command                                       |
| ------------ | --------------------------------------------- |
| List PRs     | `gh pr list --state open --limit 10`          |
| Current PR   | `gh pr view --json number,state,checks,title` |
| PR checks    | `gh pr checks`                                |
| Local verify | `npm run verify`                              |
| Push fixes   | `git push`                                    |

## Workflow

### 1. Check PR Status

```bash
# Current branch PR
gh pr view --json number,state,checks,title

# List all open PRs
gh pr list --state open --limit 10

# Detailed checks
gh pr checks
```

### 2. Diagnose Locally

```bash
# Run all checks
npm run verify

# Or run individually
npm run type-check  # Type errors
npm run lint        # Linting
npm run test        # Tests
npm run build       # Build
```

### 3. Fix Issues

**Type Errors:**

- Run `npm run type-check`
- Fix TypeScript issues
- Re-verify

**Lint Errors:**

- Run `npm run lint:fix` (auto-fix)
- Fix remaining issues manually
- Re-verify with `npm run lint`

**Test Failures:**

- Run `npm run test`
- Fix failing tests/code
- Re-verify

**Build Failures:**

- Run `npm run build`
- Fix imports/syntax
- Re-verify

### 4. Commit & Push

```bash
git add .
git commit -m "fix: resolve <failure-type>"
git push
gh pr checks  # Confirm
```

## PR Check Status

```bash
gh pr view --json checks
```

Output:

```json
{
  "checks": [
    {
      "name": "verify",
      "status": "COMPLETED",
      "conclusion": "FAILURE"
    }
  ]
}
```

**Status:**

- `COMPLETED` + `SUCCESS` = ✅ Passed
- `COMPLETED` + `FAILURE` = ❌ Failed
- `IN_PROGRESS` = ⏳ Running
- `QUEUED` = 🕐 Pending

## Full Fix Flow

1. **Check**: `gh pr view --json checks`
2. **Verify**: `npm run verify`
3. **Fix**: Address errors (type/lint/test/build)
4. **Re-verify**: `npm run verify`
5. **Commit**: `git add . && git commit -m "fix: ..."`
6. **Push**: `git push`
7. **Confirm**: `gh pr checks`

## Common Errors

**No PR Found:**

- Create PR first with create-pr skill

**All Checks Pass:**

- No fixes needed

**gh Not Available:**

- Install GitHub CLI

## Tips

- Run `npm run verify` before pushing
- Fix one error type at a time
- Read full error messages
- Commit fixes incrementally
- Use `git push --force-with-lease` for force pushes

## Example

```bash
# Check status
$ gh pr view --json checks
{"checks": [{"name": "verify", "conclusion": "FAILURE"}]}

# Diagnose
$ npm run verify
Type check failed: src/main/index.ts:42:5 - error TS2322

# Fix error in src/main/index.ts

# Verify
$ npm run type-check
Success

# Commit and push
$ git add src/main/index.ts
$ git commit -m "fix: resolve type error in main process"
$ git push

# Confirm
$ gh pr checks
✓ verify - Success
```
