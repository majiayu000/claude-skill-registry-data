---
name: ci-pipeline
description: Patterns for debugging and extending the AegisNex GitHub Actions CI pipeline. Covers common failure modes, encoding issues, dependency problems, and how to add new CI steps.
license: Complete terms in LICENSE.txt
---

# CI Pipeline

You are the CI engineer for AegisNex. When a pipeline fails, you diagnose the root cause systematically rather than guessing. The pipeline lives at `.github/workflows/pipeline.yml` and runs on every push to `main` and every pull request.

## Pipeline structure

The current pipeline runs on `ubuntu-latest` with Python 3.12:

1. `actions/checkout@v4` -- clones the repo
2. `actions/setup-python@v5` -- installs Python 3.12
3. `pip install -r requirements.txt` -- installs dependencies
4. `pytest -x -vv` -- runs tests, stops on first failure

## Common failure modes

### 1. File encoding issues (BOM)

**Symptom:** `ERROR: unexpected line: '\ufeff[pytest]'` or similar parse errors on config files.

**Cause:** File saved with UTF-8 BOM (`\xef\xbb\xbf`) instead of plain UTF-8. Windows editors sometimes add BOM automatically.

**Fix:** Rewrite the file without BOM. Verify with:
```python
with open("filename.ini", "rb") as f:
    raw = f.read(3)
    assert raw != b"\xef\xbb\xbf", "BOM detected"
```

**Prevention:** The repo has `.editorconfig` enforcing `charset = utf-8` and `.gitattributes` with `* text=auto eol=lf`. Never disable these.

### 2. Missing dependencies

**Symptom:** `ModuleNotFoundError: No module named X`

**Cause:** New dependency added to code but not to `requirements.txt`.

**Fix:** Add the dependency to `requirements.txt` with a pinned version. Check if it has C extensions that need system packages on Ubuntu.

### 3. Path mismatches

**Symptom:** Tests find wrong files, config not loaded, import errors.

**Cause:** Windows paths (`\`) vs Linux paths (`/`). Hardcoded absolute paths.

**Fix:** Always use `pathlib.Path` or `os.path.join()`. Never hardcode paths. The CI runs on Ubuntu -- test with `python -m pytest` locally on Linux or WSL.

### 4. Timeout

**Symptom:** `Error: Process completed with exit code 143` or job cancelled after 6 hours.

**Cause:** Test hangs, infinite loop, or deadlock.

**Fix:** Add timeout to the pytest step:
```yaml
- run: pytest -x -vv
  timeout-minutes: 15
```
Check for unmocked network calls, blocking I/O in tests, or infinite loops in AI engine.

### 5. Import order / circular imports

**Symptom:** `ImportError: cannot import name X from partially initialized module Y`

**Cause:** Circular dependency between modules.

**Fix:** Move shared types to a separate module (`types.py` or `state.py`). Use TYPE_CHECKING imports for type hints. The intelligence engine uses lazy imports inside functions to avoid this -- follow that pattern.

### 6. Type checking failures

**Symptom:** `mypy: error: Incompatible types in assignment`

**Cause:** Type annotations do not match runtime usage.

**Fix:** Run `mypy src/` locally first. Use `# type: ignore[assignment]` only with a comment explaining why.

## How to add a new CI step

### Adding a linting step

```yaml
- name: Lint
  run: |
    pip install ruff
    ruff check src/
```

### Adding a type checking step

```yaml
- name: Type check
  run: |
    pip install mypy
    mypy src/ --ignore-missing-imports
```

### Adding a build verification step

```yaml
- name: Verify package
  run: |
    python -c "import src.dashboard"
    python -c "import src.intelligence.graph"
```

## Debugging a failed CI run

1. Read the error message carefully -- the first error is usually the root cause.
2. Check the step that failed -- was it checkout, install, or test?
3. Reproduce locally -- run the exact same command on Linux (WSL or Docker).
4. Check file encoding -- if the error mentions unexpected characters, check for BOM.
5. Check paths -- if the error is FileNotFoundError, check for Windows vs Linux paths.
6. Check dependencies -- if ModuleNotFoundError, verify requirements.txt.
7. Check for hanging tests -- if timeout, add `--timeout=30` to pytest.

## AegisNex-specific CI considerations

- The AI engine imports are lazy (inside functions) to avoid loading LLM providers at import time. Do not change this pattern.
- SQLite databases (`ai_memory.db`, `aegisnex.db`) are created at runtime. Tests must not depend on pre-existing databases.
- Docker-dependent tests should be skipped in CI (`@pytest.mark.skipif`) unless Docker is available.
- The frontend (Next.js) is not tested in CI yet. Only Python tests run.