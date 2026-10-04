---
name: python-testing
description: Write focused, deterministic, well-documented pytest tests for AI-authored code.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: testing
  since: "2025-02-24"
---

## What I do

I help with three pytest workflows:
1. **Write tests** — generate focused, well-documented tests following project conventions
2. **Check coverage** — detect untested lines per file or folder
3. **Bootstrap setup** — install dev dependencies and apply recommended pytest configuration

Supporting files in this skill:
- `assets/pytest.ini.template` — ready-to-copy pytest configuration
- `scripts/analyze_coverage.sh [path]` — coverage analysis helper (whole src or specific folder/module)
  - Run from repo root as: `./.claude/skills/python-testing/scripts/analyze_coverage.sh [path]`
  - Or use repo-root-safe path: `"$(git rev-parse --show-toplevel)/.claude/skills/python-testing/scripts/analyze_coverage.sh" [path]`

## When to use me

Use when you want to:
- Write new tests for a module or feature
- Review and improve existing test quality
- Check coverage for a specific file, folder, or the whole project
- Bootstrap pytest for a new project (deps + config)

## Example usage

"Write tests for the `slugify` function in `src/utils/text.py`"
"Check coverage for `src/services/payment.py`"
"Set up pytest for this project with coverage and async support"

---

## Conventions

### Naming
- Files: `test_<module_or_feature>.py`
- Functions: `test_<unit>__<behavior>__<condition>`
- Mark every AI-generated test with `@pytest.mark.ai`

### Docstring (required on every test)
Three-part format:
```
Purpose: What this test verifies.
Why this matters: Business or technical consequence if it breaks.
Setup summary: What's arranged and what's asserted.
```

### Structure
- AAA pattern: Arrange – Act – Assert
- No conditionals or loops in test body (use parametrization)
- One responsibility per test

### Fixtures
- Centralize in `<domain>_fixtures.py`
- Register via `pytest_plugins = ["tests.fixtures"]` in `conftest.py`
- Return typed objects; modify only what changes per test

### Mocking
- Use `mocker` fixture (pytest-mock)
- Mock at the import boundary of the code under test
- Use `spec=True` for type safety

### Coverage
- Target ≥ 80% for AI-authored tests
- `./.claude/skills/python-testing/scripts/analyze_coverage.sh` — full src coverage
- `./.claude/skills/python-testing/scripts/analyze_coverage.sh src/services` — coverage for a specific folder
- `./.claude/skills/python-testing/scripts/analyze_coverage.sh src/utils/text.py` — coverage for a single file

### Test scope & quality
- Test every public function and method you touched
- Cover happy paths plus negative scenarios, validation failures, and async edge cases
- Keep tests deterministic and isolated (clean up temp data, reset mocks)
- Mock only external dependencies using `pytest-mock`'s `mocker` or hand-rolled fixtures
- Document why each test matters using the required docstring template

### Test cases to include
- Happy path scenarios that reflect realistic inputs
- Edge cases such as empty inputs, boundary values, and timeout paths
- Error handling or exception flows (raise and capture specific exceptions)
- Dependency failures (e.g., network timeouts, missing files) while staying fast
- Concurrency and async behavior when applicable (use `pytest.mark.asyncio` or trio)

## Test quality checklist
- [ ] Tested all public functions and methods touched by the change
- [ ] Covered happy path scenarios plus edge cases and negative flows
- [ ] Added or updated tests for error handling and exception cases
- [ ] Mocked external dependencies appropriately and kept mocks scoped
- [ ] Ensured all tests are deterministic and repeatable
- [ ] Kept tests focused (one assertion per behavior) and avoided loops/conditionals
- [ ] Documented each test with the three-part docstring
- [ ] Verified coverage with `scripts/analyze_coverage.sh` when changes affect multiple modules

### Setup (new project)
1. Install dev dependencies:
   - uv: `uv add --dev pytest pytest-cov pytest-asyncio pytest-mock`
   - pip: `pip install pytest pytest-cov pytest-asyncio pytest-mock`
2. Copy `assets/pytest.ini.template` → `pytest.ini` at the project root
3. Add `tests/` directory with an empty `__init__.py` and `conftest.py`
