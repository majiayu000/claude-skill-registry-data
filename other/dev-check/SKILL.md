---
name: dev-check
description: Run ReVision's full local verification gate — ruff lint, ruff format check, and pytest — the same checks CI enforces. Use before committing non-trivial changes, or when asked to "check", "lint", "run the tests", or "verify the build".
---

# dev-check

Run ReVision's pre-commit verification gate. This mirrors `.github/workflows/ci.yml`
so a green run locally means CI should pass.

## Steps

Run these from the repository root, in order, and report any failures:

```bash
ruff check .
ruff format --check .
pytest -q
```

- `ruff check .` — lint (rules `E, F, I, UP, B, SIM`, line length 100).
- `ruff format --check .` — verify formatting without modifying files. If it
  reports files that would be reformatted, run `ruff format .` to fix them.
- `pytest -q` — the full test suite (`tests/` mirrors `src/revision/`).

## Notes

- In some environments `pytest`/`ruff` are standalone binaries, not in the
  active interpreter's site-packages. If `python -m pytest` reports
  "No module named pytest", call `pytest` / `ruff` directly (as above).
- No network or API key is needed: tests inject a fake Anthropic client and run
  a live server on port 0.
- Do not commit unless all three pass.
