---
name: dev-checker
description: Runs pre-commit checks and validates code quality. Use when preparing commits, running pre-deploy checks, or validating code before deployment.
version: 1.0.0
---

# Dev Checker Skill

## Purpose
Quick validation before commits/deploys. Run these checks automatically.

## Quick Commands

### 1. Type Check
```bash
pnpm tsc --noEmit
```
✅ Must pass with 0 errors

### 2. Build Check
```bash
pnpm build
```
✅ Should complete in < 5 seconds

### 3. Lint Check
```bash
pnpm lint
```
✅ Fix any warnings

## Pre-Commit Checklist

```
Before committing:
[ ] pnpm tsc --noEmit (0 errors)
[ ] No console.log in code
[ ] No API keys in files
[ ] .env not staged (git status)
```

## Pre-Deploy Checklist

```
Before deploying:
[ ] All tests pass
[ ] Build succeeds
[ ] Edge Functions deployed
[ ] Environment vars set
[ ] Database migrations applied
```

## Common Issues

### TypeScript Errors
```bash
# Find all TS errors
pnpm tsc --noEmit | grep "error TS"

# Common fixes:
# - Add missing imports
# - Fix type definitions
# - Update function signatures
```

### Build Failures
```bash
# Clear cache and rebuild
rm -rf node_modules/.vite
pnpm build
```

## Usage

Just ask: "Run dev checks" or "Check if ready to commit"

I'll automatically run through the checklist and report results.
