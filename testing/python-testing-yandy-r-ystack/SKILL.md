---
name: python-testing
description: 'Guides pytest testing with TDD, fixtures, and mocks. Use when adding Python test coverage, parametrizing pytest cases, or isolating async tests.'
---

# Python Testing Patterns

Comprehensive testing strategies for Python applications using pytest, TDD methodology, and best practices.

## When to Activate

- Writing new Python code (follow TDD: red, green, refactor)
- Designing test suites for Python projects
- Reviewing Python test coverage
- Setting up testing infrastructure

## Critical Rules

- Use pytest; follow TDD (red, green, refactor).
- Use fixtures to eliminate duplication; set scope explicitly (function default, `module`, `session`).
- Use `@pytest.mark.parametrize` for multiple inputs.
- Assert exceptions with `pytest.raises`.
- Use `autospec` when patching so API misuse fails at test time.
- Isolate tests with `tmp_path` and `monkeypatch`; do not share state between tests.
- Gate slow tests with markers (`@pytest.mark.slow`).

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/pytest-core.md](references/pytest-core.md)
  Read when: TDD Workflow for Python, pytest Fundamentals (assertions, pytest.raises), Fixtures (scopes, conftest.py), Parametrization, Markers and Test Selection.

- [references/mocking-and-integration.md](references/mocking-and-integration.md)
  Read when: Mocking and Patching (autospec), Testing Async Code, Testing Exceptions, Testing Side Effects (tmp_path, capsys, monkeypatch), Test Organization, Common Patterns, pytest Configuration.

## Running Tests

```bash
# Run all tests
pytest

# Run a specific file
pytest tests/test_utils.py

# Run a specific test
pytest tests/test_utils.py::test_function

# Verbose output
pytest -v

# Coverage
pytest --cov=mypackage --cov-report=html

# Skip slow tests
pytest -m "not slow"

# Stop at first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Re-run only last failures
pytest --lf

# Match by test name pattern
pytest -k "test_user"

# Drop into pdb on failure
pytest --pdb
```

## Best Practices

**DO:**

- Follow TDD: write tests before code (red-green-refactor)
- Test one behavior per test
- Use descriptive names: `test_user_login_with_invalid_credentials_fails`
- Use fixtures to eliminate duplication
- Mock external dependencies (network, filesystem, time)
- Test edge cases: empty inputs, None values, boundary conditions
- Aim for 80%+ coverage with 100% on critical paths
- Keep tests fast — use `@pytest.mark.slow` to gate integration tests

**DON'T:**

- Test implementation details — test behavior through the public API
- Use complex conditionals in tests — keep them linear
- Ignore test failures or skip flaky tests indefinitely
- Test third-party libraries — trust them to work
- Share state between tests — they must be independent
- Catch exceptions in tests — use `pytest.raises`
- Use `print` for debugging — assertions and `-v` are enough
- Over-specify mocks — brittle tests break on every refactor

## Quick Reference

| Pattern                    | Usage                                   |
| -------------------------- | --------------------------------------- |
| `pytest.raises()`          | Test expected exceptions                |
| `@pytest.fixture`          | Create reusable test fixtures           |
| `@pytest.mark.parametrize` | Run tests with multiple inputs          |
| `@pytest.mark.slow`        | Gate slow tests                         |
| `pytest -m "not slow"`     | Skip slow tests                         |
| `@patch()` / `Mock`        | Mock functions and classes              |
| `tmp_path` fixture         | Automatic temp directory (pathlib.Path) |
| `monkeypatch` fixture      | Safe env var / attribute patching       |
| `capsys` fixture           | Capture stdout / stderr                 |
| `pytest --cov`             | Generate coverage report                |

**Remember**: Tests are code too. Keep them clean, readable, and maintainable. Good tests catch bugs; great tests prevent them.
