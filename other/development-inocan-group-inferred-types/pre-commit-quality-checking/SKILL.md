---
name: Pre-Commit Quality Checking
description: Runs mandatory quality checks before commits. Executes build, tests, and pattern validation from code-review-standards.md. Use when ready to commit code or when asked to verify code quality meets project standards.
---

# Pre-Commit Quality Checking

Automates the mandatory checklist from `.claude/modules/code-review-standards.md`.

## Quick Workflow

When ready to commit, run these checks in order:

1. **Build verification**: `npm run build`
2. **Test verification**: `npm test`
3. **Pattern validation**: `bash .claude/skills/pre-commit-quality/scripts/validate-patterns.sh`

All three must pass before committing.

## Step-by-Step Process

### Step 1: Run Build
```bash
npm run build
```

**Must pass with zero errors.** If build fails:
- Fix TypeScript errors shown in output
- Rerun build until it passes
- See [typescript-standards.md](../../modules/typescript-standards.md) for type safety patterns

### Step 2: Run Tests
```bash
npm test
```

**All tests must pass.** If tests fail:
- Review failing test output
- Fix the issues causing failures
- Rerun tests until all pass
- See [testing-standards.md](../../modules/testing-standards.md) for testing patterns

### Step 3: Validate Patterns
```bash
bash .claude/skills/pre-commit-quality/scripts/validate-patterns.sh
```

**No violations allowed.** Script checks for:
- `any` types (use specific types or `unknown`)
- Wrong Supabase client in wrong environment
- `console.log` in production code

If validation fails, fix the reported issues and rerun.

## Complete Review Checklist

For the full pre-commit checklist, see:
- [code-review-standards.md](../../modules/code-review-standards.md) - Complete checklist
- [nextjs-patterns.md](../../modules/nextjs-patterns.md) - Next.js patterns
- [supabase-security.md](../../modules/supabase-security.md) - Supabase security
- [anti-patterns.md](../../modules/anti-patterns.md) - What to avoid

## Common Issues and Fixes

### Build Fails: TypeScript Errors
- Check for missing types
- Ensure imports are correct
- Fix any `any` types to specific types

### Tests Fail
- Read the test output carefully
- Fix the code causing the failure
- Ensure all test files are updated

### Pattern Validation Fails
**`any` types found**:
- Replace with specific type: `Recipe`, `User`, etc.
- Use `unknown` if type is truly unknown
- Add type guards for union types

**Wrong Supabase client**:
- Server Components: `import { createClient } from '@/lib/supabase/server'`
- Client Components: `import { createClient } from '@/lib/supabase/client'`

**console.log found**:
- Remove from production code
- Use proper logging if needed
- console.log is fine in test files

## After All Checks Pass

Once all checks pass:
1. Stage your changes: `git add .`
2. Commit with descriptive message
3. See CLAUDE.md for commit message format

## Philosophy

This skill enforces quality standards without you having to remember every check. It references the documentation in modules/ for the "why" and "what", while providing the "how" to validate.
