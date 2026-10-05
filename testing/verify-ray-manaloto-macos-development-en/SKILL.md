---
name: verify
description: Run full verification suite (ruff check, ruff format, ty type check, pytest) and report results. Use before committing, before marking work done, or when asked to verify changes.
---

Run the full verification suite for the mde project. Execute each step sequentially and report all results — do not stop at the first failure.

## Steps

1. **Lint**: `uv run ruff check src/mde/ tests/`
2. **Format check**: `uv run ruff format --check src/mde/ tests/`
3. **Type check**: `uv run ty check src/mde/`
4. **Tests**: `uv run pytest tests/ -v`
5. **mise format**: `mise fmt --check`

## Rules

- Run ALL 5 steps even if earlier ones fail — report the full picture
- Read ALL output including warnings and deprecation notices, not just exit codes
- Zero tolerance: every warning must be addressed, never dismissed as "pre-existing"
- If any step fails, list the specific failures and suggest fixes
- Report final score as `X/5 passed`
- If all 5 pass, confirm ready to commit
