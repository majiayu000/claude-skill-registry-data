---
name: check
description: Run the repo's gate (make ci and bandit, plus the site build when docs or site/ changed) and fix what it reports. Use before every commit and after any code change.
---

Run from the repo root:

```bash
make ci                                    # ruff lint, ruff format check, ty, import-linter, pytest, alembic drift check
uv run bandit -q -c pyproject.toml -r .    # CI runs bandit; make ci does not
cd site && npm run build                   # only when docs/ or site/ changed
```

Rules:

- Fix failures at the source. Do not add `# noqa`, `# type: ignore`, `# nosec` or a skipped test to get green. A `# nosec` is acceptable only for a false positive, on that line, with the reason (see `SECRET_PREFIX` in `modules/runpod/service.py`).
- `ty` prints warnings for the whole repo. Only errors fail the gate. Do not add new ones: for SQLAlchemy columns use `typing.cast(int, row.id)`, not `int(row.id)`.
- Tests share one database per session. A test that writes rows deletes them in its fixture teardown, including org secrets, or other tests see them.
- `alembic check` fails when a model changed without a migration. See the `migration` skill.

Report which step failed, what you changed, and the final status of each command.
