---
name: bundle-size-enforcer
description: Monitor and enforce the frontend bundle size budget. Use when checking bundle size, preventing regressions, or validating build output against budget constraints.
---

# Bundle Size Enforcer

Monitor and enforce LibrAgent's frontend bundle size budget.

## Budget Configuration

Bundle size budgets are defined in `bundle-size-budget.json` and checked by `scripts/check-bundle-size.ts`.

## Verification

```bash
# Build and check bundle size
pnpm build && pnpm perf:bundle
```

CI runs this command and fails on budget overruns.

## Audit Checklist

- [ ] Production build completes without errors
- [ ] `perf:bundle` passes all budget checks
- [ ] No new large dependencies added without budget review
- [ ] Dynamic imports used for code splitting where appropriate
- [ ] Tree shaking is effective (no unused exports from dependencies)

## Common Bundle Bloat Patterns

1. **Large dependencies**: Check for accidental inclusion of test/build-only packages
2. **Unused code**: Run `pnpm dead-code` to find unused exports
3. **Duplicate code**: Check for duplicated utility functions
4. **Large assets**: Images, fonts, and other assets should be optimized
5. **Unused styles**: Tailwind PurgeCSS may remove custom classes - use safelist if needed

## Pre-commit Check

Run before committing frontend changes:

```bash
pnpm build && pnpm perf:bundle
```

If budget is exceeded:

1. Identify the new/changed dependency or code
2. Consider dynamic imports or lazy loading
3. Update `bundle-size-budget.json` only if the increase is justified
