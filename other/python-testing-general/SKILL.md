---
name: python-testing-general
description: General standards for writing reliable, isolated pytest tests in Python projects. Use this skill for test structure, fixtures, mocking, and test organization patterns.
auto_load:
  enabled: true
  triggers:
    keywords: [pytest, test, mock, fixture, unittest, conftest]
    file_patterns: ["test_*.py", "*_test.py", "**/tests/**/*.py", "conftest.py"]
  priority: high
  load_with: [python-fundamentals]
---

# Python Testing

Standards for writing reliable, isolated pytest tests in Python projects. Use this skill for test structure, fixtures, mocking, and test organization patterns.

## When to Use This Skill

- Writing pytest tests for Python code
- Creating test fixtures and helpers
- Mocking external dependencies
- Organizing test files and directories
- Implementing parametrized tests
- Testing async code

---

## Test Structure

### Naming Conventions

```python
# Test files: test_<module>.py
test_user_service.py
test_build_wrapper.py

# Test functions: test_<behavior>
def test_detect_wrapper_finds_unix_on_unix():
    ...

def test_returns_none_when_missing():
    ...
```

### AAA Pattern

Structure tests with Arrange-Act-Assert:

```python
def test_calculate_total():
    # Arrange
    items = [Item(price=10), Item(price=20)]

    # Act
    result = calculate_total(items)

    # Assert
    assert result == 30
```

---

## Test Isolation

### Working Directory Restoration

Tests that change `cwd` must restore it. Use an autouse fixture as a safety net:

```python
import os
import pytest

@pytest.fixture(autouse=True)
def _restore_cwd():
    """Restore cwd after each test to prevent pollution."""
    original_cwd = os.getcwd()
    yield
    if os.getcwd() != original_cwd:
        os.chdir(original_cwd)
```

For explicit cwd changes within a test, use `monkeypatch`:

```python
def test_script_in_different_directory(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    # Test runs with tmp_path as cwd
    # Automatically restored after test
```

### Temporary Directories

Use `tmp_path` for isolated file operations:

```python
def test_creates_output_file(tmp_path):
    output = tmp_path / "result.json"
    generate_report(output)
    assert output.exists()
```

### Script Path Discovery

Scripts using `Path.cwd()` break when tests run from different directories. Use dual-path discovery:

```python
from pathlib import Path

# Script-relative path (works regardless of cwd)
SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT_FROM_SCRIPT = SCRIPT_DIR.parent.parent.parent

def find_project_root() -> Path | None:
    """Find root with cwd-first, script-relative fallback.

    cwd-first allows tests to use fixture directories.
    Script-relative fallback works when cwd is different.
    """
    # Check cwd-based paths first (supports test fixtures)
    if (Path.cwd() / 'expected_marker').is_dir():
        return Path.cwd()

    # Fallback to script-relative (works regardless of cwd)
    if _ROOT_FROM_SCRIPT.is_dir():
        return _ROOT_FROM_SCRIPT

    return None
```

---

## Fixtures

### Scope and Autouse

```python
# Function scope (default) - runs for each test
@pytest.fixture
def sample_data():
    return {"key": "value"}

# Module scope - runs once per test file
@pytest.fixture(scope="module")
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()

# Session scope - runs once per test session
@pytest.fixture(scope="session")
def app_config():
    return load_config()

# Autouse - runs automatically for every test
@pytest.fixture(autouse=True)
def _clear_cache():
    cache.clear()
    yield
```

### Fixture with Cleanup

```python
@pytest.fixture
def temp_database():
    db = create_test_database()
    yield db
    db.destroy()
```

### Parametrized Fixtures

```python
@pytest.fixture(params=[True, False])
def debug_mode(request):
    return request.param
```

---

## Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert input.upper() == expected

# Multiple parameters
@pytest.mark.parametrize("email,valid", [
    ("test@example.com", True),
    ("invalid", False),
    ("", False),
    ("a@b.c", True),
])
def test_validate_email(email: str, valid: bool):
    result = validate_email(email)
    assert result == valid
```

---

## Mocking

### Patching Module State

```python
from unittest.mock import patch

def test_platform_detection():
    with patch('module.IS_WINDOWS', True):
        result = detect_wrapper()
        assert 'bat' in result
```

### Patching Functions

```python
def test_fallback_to_system(tmp_path):
    with patch('shutil.which', return_value='/usr/bin/tool'):
        result = detect_wrapper(str(tmp_path), 'tool', 'tool.bat', 'tool')
        assert result == 'tool'
```

### Async Mocking

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_user_sends_email():
    with patch('app.services.send_email', new_callable=AsyncMock) as mock:
        user = await create_user(UserCreate(email="test@example.com"))
        mock.assert_called_once()

# Using AsyncMock directly
async def test_async_function():
    mock = AsyncMock(return_value=User(id=1))
    result = await mock()
```

### Mocking with pytest-mock

```python
def test_with_mocker(mocker):
    mocker.patch('module.function', return_value='mocked')
    result = module.function()
    assert result == 'mocked'

def test_spy(mocker):
    mocker.spy(module, 'function')
    module.function()
    module.function.assert_called_once()
```

---

## Assertions

### Basic Assertions

```python
assert result == expected
assert item in collection
assert value is None
assert len(items) == 3
assert response.status_code == 200
```

### Exception Testing

```python
import pytest

def test_raises_on_invalid_input():
    with pytest.raises(ValueError, match="must be positive"):
        process_value(-1)

def test_raises_specific_exception():
    with pytest.raises(NotFoundError) as exc_info:
        get_resource(999)
    assert exc_info.value.resource == "user"
```

### Approximate Comparisons

```python
assert result == pytest.approx(3.14159, rel=1e-3)
```

### Asserting on Collections

```python
# Check contents
assert "error" in result
assert all(item.is_valid() for item in items)

# Dictionary assertions
assert response["status"] == "success"
assert "data" in response

# Using pytest assertions
from pytest import asserts

asserts.assert_equal(result, expected)
asserts.assert_in("key", data)
```

---

## Async Testing

### Basic Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data("url")
    assert result is not None
```

### Async Fixtures

```python
import pytest
from httpx import AsyncClient

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def db_session():
    async with async_session() as session:
        yield session
        await session.rollback()
```

### Concurrent Async Tests

```python
import asyncio

@pytest.mark.asyncio
async def test_concurrent_requests():
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
    )
    assert len(results) == 2
```

---

## Test Organization

### Shared Infrastructure

Place shared fixtures and helpers in `conftest.py`:

```python
# test/conftest.py
import pytest

@pytest.fixture
def sample_config():
    return {"debug": True}

def run_script(script_path, *args):
    """Helper to run scripts with subprocess."""
    ...
```

### Test File Structure

```
test/
├── conftest.py              # Shared fixtures
├── bundle_name/
│   ├── conftest.py          # Bundle-specific fixtures
│   ├── test_feature.py
│   └── test_integration.py
├── unit/
│   ├── test_services.py
│   └── test_models.py
└── integration/
    ├── test_api.py
    └── test_database.py
```

---

## Factory Pattern for Tests

```python
from factory import Factory, Faker

class UserFactory(Factory):
    class Meta:
        model = User

    email = Faker('email')
    name = Faker('name')
    is_active = True

# Usage
user = UserFactory()
inactive_user = UserFactory(is_active=False)
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run specific module
pytest tests/unit/test_services.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run tests matching pattern
pytest -k "test_user"

# Run tests in parallel
pytest -n auto

# Run with profiling
pytest --profile

# Stop on first failure
pytest -x

# Run tests matching name pattern
pytest --test-name-pattern="test_user"
```

---

## Test Organization Best Practices

1. **Mirror source structure** - Tests should mirror `src/` directory structure
2. **Test methods start with `test_`** - pytest convention
3. **Use test class suites** - For `def foo()` create `class TestFoo`
4. **Keep names concise** - Omit class suite name from method
5. **Check for tests when changing code** - Always ensure appropriate unit tests

---

## Quality Guidelines

- **Use AAA pattern** - Arrange, Act, Assert
- **Tests should be useful** - Readable, concise, maintainable
- **Avoid massive diffs** - Don't create tests that become burdensome
- **Mock external dependencies** - Database, API calls, file system
- **Use meaningful assertions** - Test behavior, not implementation
- **One assertion per test** - Or few related assertions
- **Independent tests** - No order dependency between tests

---

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)

## Additional References

For production-ready patterns beyond this guide, see:

- **[Pytest Fixtures Cookbook](references/pytest-fixtures-cookbook.md)** - Token bucket rate limiter, retry with exponential backoff, connection pools, batch processors, event bus, transaction context managers, async cache with TTL, graceful shutdown handlers
