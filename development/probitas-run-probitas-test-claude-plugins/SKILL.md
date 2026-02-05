---
name: probitas-run
description: Running and validating Probitas scenarios. Use when executing tests, running scenarios, or debugging test failures.
---

## Instructions

Run `/probitas-run` command (or `/probitas-run <selector>` with filter).

If project not initialized → run `/probitas-init` first.

## Selector Examples

```bash
probitas run -s tag:api             # Match tag
probitas run -s "!tag:slow"         # Exclude tag
probitas run -s user                # Match scenario name
```

## If Tests Fail

1. Run `/probitas-check` for validation errors
2. Check error messages for assertion details
3. Verify environment variables (API_URL, DATABASE_URL)
4. Use `--verbose` or `--debug` for more output
