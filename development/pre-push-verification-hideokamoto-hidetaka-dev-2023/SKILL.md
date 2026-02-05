---
name: "Pre-push Verification"
description: "Execute lint, test, and build checks before pushing code"
instructions: |
  This skill runs the pre-push verification command to ensure code quality.
---

# Pre-push Verification Skill

This skill executes all mandatory checks before pushing code to ensure code quality and prevent CI failures.

## What This Skill Does

Runs the following checks in sequence:

1. **Lint Check** - Validates code style and quality with Biome
2. **Unit Tests** - Runs all unit tests with Vitest
3. **Build Verification** - Compiles TypeScript and builds the Next.js project

## Usage

Simply run:

```bash
npm run pre-push
```

Or have Claude Code execute this skill when preparing to push code.

## What Gets Checked

### Lint Check (`npm run lint:check`)
- Code style consistency
- Potential bugs and anti-patterns
- Accessibility compliance (a11y)
- TypeScript type correctness

### Unit Tests (`npm run test`)
- All Vitest tests pass
- No regression in existing functionality
- New code is properly tested

### Build Check (`npm run build`)
- TypeScript compilation succeeds
- No type errors across the codebase
- All imports and dependencies resolve
- Next.js static generation works

## When to Use

- **Before committing**: Run `npm run pre-push` to verify changes
- **Before pushing**: Ensure this passes before `git push`
- **After major changes**: Run to catch issues early
- **In CI/CD workflows**: This is enforced by the Git pre-push hook

## Output

The command displays:
- ✅ Pass/❌ Fail status for each check
- Detailed error messages for failures
- Suggestions for fixing issues

## If Checks Fail

The tool will stop at the first failure. Follow these steps:

**Lint failures:**
```bash
npm run lint        # Auto-fix most issues
npm run lint:check  # Verify fixes
```

**Test failures:**
```bash
npm run test        # Review error messages
# Fix failing tests
npm run test        # Re-run to confirm
```

**Build failures:**
```bash
npm run build       # Check TypeScript errors
# Fix all errors in source code
npm run build       # Re-run to verify
```

## Integration with Git Hooks

This skill is also enforced by a Git pre-push hook at `.git/hooks/pre-push`.

Even if you forget to run this skill before pushing, the hook will:
- Automatically run these checks
- Block the push if any check fails
- Provide error output to fix issues

**Note:** The hook can be bypassed with `git push --no-verify`, but this is not recommended as it may cause CI failures.

## Related Documentation

- **Development Guide**: See `/CLAUDE.md` for full development workflow
- **Code Quality Standards**: Biome config at `biome.json`
- **Testing Guide**: Vitest config at `vitest.config.ts`
- **Build Configuration**: Next.js config at `next.config.ts`
