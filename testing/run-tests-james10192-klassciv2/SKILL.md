---
name: run-tests
description: Run project tests and quality checks. Use before creating a PR or when asked to run tests.
---

Detect the project stack and run the appropriate quality checks.

## Step 1 — Detect stack

Look at the project root for:
- `package.json` → Node.js / Next.js / React Native
- `pyproject.toml` / `setup.py` / `requirements.txt` → Python
- `composer.json` → PHP / Laravel
- `pubspec.yaml` → Flutter/Dart

## Step 2 — Run checks by stack

### Node.js / Next.js / React
```bash
# Lint
npx eslint . --ext .ts,.tsx,.js,.jsx

# Type check (if TypeScript)
npx tsc --noEmit

# Tests
npx jest --coverage
# or
npx vitest run --coverage
# or
npm test
```

### Python (FastAPI / Django)
```bash
# Lint + format
ruff check .
ruff format --check .

# Type check
mypy . --ignore-missing-imports

# Tests with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

### PHP / Laravel
```bash
# Static analysis
./vendor/bin/phpstan analyse

# Tests
php artisan test
# or
./vendor/bin/pest
```

## Step 3 — Report results

Summarize:
- Lint: pass/fail
- Types: pass/fail
- Tests: X passed, Y failed
- Coverage: X% (if available)
- Any failing tests with their error messages

If tests fail, analyze the errors and suggest fixes — do NOT auto-fix without asking first.

$ARGUMENTS
