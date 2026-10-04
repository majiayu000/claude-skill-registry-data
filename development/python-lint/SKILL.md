---
description: Fix Python build, type, and lint errors with minimal surgical fixes
---

# Python Lint

Fix Python build errors, type errors, and lint issues incrementally. Invokes the python-build-resolver agent for minimal, surgical fixes.

## When to Use

- `mypy` reports type errors
- `ruff check` or `flake8` shows lint violations
- `python -m py_compile` fails with SyntaxError
- Import errors block execution
- CI pipeline fails on Python checks

## What This Command Does

1. **Run diagnostics** (`dev/lint` or `dev/test-backend`)
2. **Parse errors** grouped by file and severity
3. **Fix incrementally**, one error at a time
4. **Verify each fix** with re-run
5. **Report summary** of fixes and remaining issues

## Common Errors Fixed

| Error | Typical Fix |
|-------|------------|
| `Missing type annotation` | Add type hints |
| `ModuleNotFoundError` | Fix imports or install package |
| `Incompatible types` | Add type conversion or annotation |
| `Optional access without check` | Add None guard |
| `SyntaxError` | Fix syntax |
| `IndentationError` | Fix indentation |
| `Unused import` | Remove import |

## Fix Strategy

1. **SyntaxError** first (blocks everything)
2. **ImportError** second (blocks module loading)
3. **Type errors** third
4. **Lint warnings** last

## Stop Conditions

- Same error after 3 attempts
- More errors introduced than fixed
- Architectural changes required
- Missing external dependency that can't be installed

## Related

- `/python-review` - Code review
- `/python-tdd` - TDD workflow
- Skills: `python-patterns`

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, reports, and summaries must be written in Japanese**
