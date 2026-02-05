---
name: Testing & Verification
description: Test execution workflows after code generation, bug fixes, or refactoring. Invoke when new code exists to verify correctness and quality.
allowed-tools: [Bash, Read]
---

# Testing & Verification

## Invocation Context

After: code generation, bug fix, refactor, architecture-sensitive changes

## Commands

### Quick Verification
- `composer test:fast` - syntax, unit, style (~5-10s, use first)
- `composer test` - full suite before commit (~30-60s)

### Targeted Tests
- `composer test:unit` - unit only
- `composer test:integration` - DB/filesystem
- `composer test:architecture` - constraints/naming/complexity (23 tests)
- `composer test:security` - dangerous functions check

### Static Analysis
- `composer test:types` - PHPStan level 9
- `composer test:style` - PHP CS Fixer validation
- `composer test:syntax` - parallel-lint parse check

### Coverage
- `composer test:coverage` - enforce 95% threshold
- `composer test:coverage-report` - HTML report in build/coverage-html/

### Architecture Analysis
- `composer analyze:architecture` - Deptrac layer boundaries

## Execution Patterns

### Post-Generation
```
composer test:fast → if fail, fix → rerun → composer test
```

### Bug Fix
```
composer test:unit (or test:integration) → composer test
```

### Refactor
```
composer analyze:architecture → composer test:architecture → composer test → composer test:coverage
```

## Pre-commit Integration

**v2.1 Conditional Checks** (based on what changed):
- Docs-only: All checks skipped (~2-12s)
- App code: Full suite + dual PHPStan (~40-110s)
- Config tools: Full suite (~30-90s)
- Composer: Full suite + audit (~40-120s)

**Key Features**:
- Dual PHPStan on app changes (staged → full project)
- Config file detection (phpstan.neon, deptrac.yaml, etc.)
- Conditional composer audit (only when dependencies change)

Any fail = commit blocked

Fix: `composer fix:style` → `composer test` → commit
Details: `docs/PRE-COMMIT-HOOK.md`

## Result Handling

- `OK (N tests, M assertions)` - proceed
- Any failure - invoke Error Resolution Skill

## Test Organization

```
tests/
├── Unit/          - mocked, fast
├── Integration/   - DB/filesystem
├── Architecture/  - 23 constraint tests
└── Security/      - dangerous functions
```
