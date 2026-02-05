---
name: rulebook-quality-gates
description: Automated quality checks and enforcement for code commits. Use when validating code quality, running pre-commit checks, ensuring test coverage, or enforcing coding standards before commits and pushes.
version: "1.0.0"
category: core
author: "HiveLLM"
tags: ["quality", "testing", "coverage", "linting", "pre-commit", "git-hooks"]
dependencies: []
conflicts: []
---

# Quality Gates Enforcement

## Pre-Commit Checklist

**MUST run these checks before every commit:**

```bash
npm run type-check    # Type check
npm run lint          # Lint (0 warnings)
npm run format        # Format check
npm test              # All tests (100% pass)
npm run build         # Build verification
npm run test:coverage # Coverage check (95%+)
```

**If ANY fail, FIX before committing.**

## Quality Thresholds

| Check | Requirement |
|-------|-------------|
| Type Check | Zero errors |
| Lint | Zero warnings |
| Tests | 100% pass rate |
| Coverage | 95%+ |
| Build | Must succeed |

## Git Hooks

Rulebook can install automated Git hooks:

```bash
rulebook init  # Prompts to install hooks
```

### Pre-commit Hook
- Format check
- Lint check
- Type check

### Pre-push Hook
- Build verification
- All tests
- Coverage threshold check

## Fixing Common Issues

```bash
npm run type-check  # See type errors
npm run lint        # See lint warnings
npm run lint:fix    # Auto-fix lint issues
npm test            # Run all tests
npm run test:coverage  # See coverage report
```
