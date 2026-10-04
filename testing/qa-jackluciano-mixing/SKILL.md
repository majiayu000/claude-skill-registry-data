---
name: qa
description: Pre-commit sanity check — compile all Python modules, run the pytest suite, and verify core imports before committing changes to the betting engine. Use after editing tippmix_system/ or service/ and before any commit.
---

# QA Gate

Catch breakage before it ships. Run this after touching the engine and before committing.

## Steps

1. **Compile** the core modules (fast syntax gate):
   ```bash
   python -m py_compile tippmix_system/*.py service/*.py
   ```
2. **Imports** resolve (catches missing symbols the compiler misses):
   ```bash
   python -c "from tippmix_system.cli import main; from tippmix_system.recommendations import generate_recommendations, generate_combinations; from tippmix_system.evaluation import evaluate_run; from tippmix_system.analysis import analyze_match; print('imports OK')"
   ```
3. **Tests**:
   ```bash
   python -m pytest tests/ -q
   ```
4. Report pass/fail honestly. If tests fail, show the failing output — do not claim green.
5. For UI changes, also run the TS build:
   ```bash
   cd ui && npm run build
   ```

## Notes

- Core logic is stdlib-only (no numpy); a failed import usually means a typo or a
  removed/renamed symbol, not a missing dependency.
- Never commit secrets — `data/.auth_secret` and `data/avatars/` are gitignored; the
  commit-guard hook will block known sensitive paths if staged.
