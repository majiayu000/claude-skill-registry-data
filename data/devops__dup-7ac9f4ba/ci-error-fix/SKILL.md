---
name: ci-error-fix
description: Fixing CI errors systematically. Follows a structured workflow of understanding the error, checking if it exists on the main branch, reproducing locally, fixing, and verifying. Use when CI pipelines fail and you need to diagnose and fix the errors.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# CI Error Fix Skill

A systematic skill for diagnosing and fixing Continuous Integration (CI) errors. This skill emphasizes understanding the root cause, checking main branch status, local reproduction, and iterative fixing until CI passes.

## When to Use

Use this skill when:
- A CI pipeline fails and you need to fix the errors
- You need to diagnose why tests pass locally but fail in CI
- You're debugging build failures, linting errors, or test failures in CI
- You need to ensure your changes don't break the CI pipeline

## Process

### 1. Understand the Cause of the Error

**CRITICAL FIRST STEP: Thoroughly analyze the CI error before attempting any fix**

1. **Read the CI error logs carefully**
   - Identify the exact error message
   - Note which job, step, or stage failed
   - Understand the full context around the error
   - Look for stack traces, line numbers, and file references

2. **Categorize the error type:**
   - **Build errors**: Compilation failures, missing dependencies
   - **Lint errors**: Code style violations, static analysis warnings
   - **Test failures**: Unit tests, integration tests, E2E tests
   - **Configuration errors**: CI config issues, environment problems
   - **Resource errors**: Timeouts, memory limits, disk space

3. **Document what you understand about the error**
   - What command failed?
   - What was the expected vs actual behavior?
   - What files or code paths are involved?

### 2. Check if the CI on Main Branch Has the Same Error

**CRITICAL: Determine if this is a new error or a pre-existing issue**

1. **Check the main branch CI status**
   ```bash
   # View recent CI runs on main branch
   gh run list --branch main --limit 5

   # View details of a specific run
   gh run view <run-id>

   # View logs of a failed job
   gh run view <run-id> --log-failed
   ```

2. **Compare with your branch**
   - If main branch CI has the same error: The issue is pre-existing, not caused by your changes
   - If main branch CI passes: Your changes introduced the error

3. **Decision point:**
   - **Same error on main**: Consider if fixing is within scope, or if it should be a separate issue
   - **New error from your changes**: Proceed to fix the issue

### 3. Investigate the Cause from the Current Codebase

1. **Read the failing code**
   - Use Read tool to examine the files mentioned in errors
   - Understand the code logic and recent changes
   - Check git diff to see what changed

2. **Search for related patterns**
   - Use Grep to find similar code that might be affected
   - Look for tests that cover the failing functionality
   - Check for configuration that might affect the behavior

3. **Understand dependencies**
   - Check package versions in CI vs local
   - Look for environment differences
   - Review CI configuration files

### 4. Reproduce the Error Locally

**CRITICAL: Always reproduce before fixing**

1. **Run the exact failing command locally**
   ```bash
   # For test failures
   npm test
   go test ./...
   pytest

   # For lint errors
   npm run lint
   golangci-lint run
   shellcheck *.sh

   # For build errors
   npm run build
   go build ./...
   make build
   ```

2. **Match the CI environment as closely as possible**
   - Use the same Node/Go/Python version
   - Install the same dependencies
   - Set similar environment variables
   - Consider using Docker to match CI environment exactly

3. **Confirm you can reproduce the error**
   - If you can reproduce: Proceed to fix
   - If you cannot reproduce: Investigate environment differences

### 5. Fix the Cause of the Error

1. **Make minimal, focused changes**
   - Fix only what is necessary
   - Avoid unrelated refactoring
   - Keep changes reviewable

2. **Update test code if needed**
   - Fix broken tests
   - Add new tests for edge cases discovered
   - Remove obsolete tests if appropriate

3. **Follow project guidelines**
   - Check `.claude/docs/guideline.md` for coding standards
   - Match existing code patterns
   - Follow error handling conventions

### 6. Verify the Fix Works

1. **Run the failing command locally**
   ```bash
   # Run the specific failing test/lint/build
   <exact-command-that-failed>
   ```

2. **Run full verification suite**
   ```bash
   # Run all tests
   npm test
   go test ./...

   # Run all linters
   npm run lint
   golangci-lint run

   # Run build
   npm run build
   go build ./...
   ```

3. **Confirm fix resolves the issue**
   - All tests pass
   - No lint errors
   - Build succeeds
   - No new errors introduced

### 7. Repeat Until CI Passes Successfully

**CRITICAL: Do not stop until the CI passes**

1. **Push your fix**
   ```bash
   git add -A
   git commit -m "fix: resolve CI error - <brief description>"
   git push
   ```

2. **Monitor CI status**
   ```bash
   # Watch CI run progress
   gh run watch

   # View CI run status
   gh run list --limit 3
   ```

3. **If CI still fails**
   - Return to Step 1: Understand the new error
   - Repeat the entire process
   - Continue iterating until CI passes

4. **Only consider the task complete when:**
   - The CI pipeline passes successfully
   - No new errors are introduced
   - All jobs in the pipeline complete successfully

## Common CI Error Patterns

### Test Failures

```bash
# Reproduce locally
npm test -- --verbose
go test -v ./...
pytest -v

# Run specific failing test
npm test -- --testNamePattern="failing test name"
go test -v -run TestName ./package/...
pytest -v -k "test_name"
```

### Linting Errors

```bash
# JavaScript/TypeScript
npm run lint
npx eslint --fix .

# Go
golangci-lint run
gofmt -w .

# Bash
shellcheck *.sh

# Python
flake8 .
black .
```

### Build Errors

```bash
# JavaScript/TypeScript
npm run build
npm run type-check

# Go
go build ./...
go vet ./...

# General
make build
```

### Dependency Issues

```bash
# Clear caches
rm -rf node_modules && npm ci
go clean -modcache && go mod download

# Check for version mismatches
npm outdated
go list -m -u all
```

## Environment Matching

### Using Docker to Match CI

```bash
# If CI uses a specific image
docker run -v $(pwd):/app -w /app <ci-image> <failing-command>

# For GitHub Actions, use act
gh act -l  # List available jobs
gh act -j <job-name>  # Run specific job
```

### Checking Versions

```bash
# Node.js
node --version
npm --version

# Go
go version

# Python
python --version
pip --version
```

## Checklist

### Before Fixing
- [ ] Read and understand the CI error logs completely
- [ ] Check if main branch CI has the same error
- [ ] Identify the exact command that failed
- [ ] Categorize the error type (build/lint/test/config)

### During Fixing
- [ ] Reproduce the error locally
- [ ] Make minimal, focused changes
- [ ] Follow project coding guidelines
- [ ] Update tests if needed
- [ ] Verify fix works locally

### After Fixing
- [ ] Run all local verification (tests, lint, build)
- [ ] Push changes and monitor CI
- [ ] If CI fails, return to understanding the new error
- [ ] **CRITICAL: Repeat until CI passes completely**

## Key Principles

1. **Understand Before Fix**: Never fix blindly; understand the root cause first
2. **Check Main Branch**: Determine if error is new or pre-existing
3. **Reproduce Locally**: Always reproduce before attempting to fix
4. **Minimal Changes**: Make only necessary changes, avoid scope creep
5. **Verify Completely**: Test thoroughly before pushing
6. **Iterate Until Success**: Do not stop until CI passes completely
7. **Document Learnings**: Note patterns for future reference

## Version History

- **v1.0.0** (2025-01-30): Initial version with systematic CI error fixing workflow
  - Understanding error causes
  - Main branch comparison
  - Local reproduction
  - Iterative fixing until CI passes
  - Common error patterns and solutions
