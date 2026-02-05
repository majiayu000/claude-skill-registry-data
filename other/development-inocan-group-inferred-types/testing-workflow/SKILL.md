---
name: testing-workflow
description: Testing workflow patterns and quality standards. Activate when working with tests, test files, test directories, code quality tools, coverage reports, or testing tasks. Includes zero-warnings policy, targeted testing during development, mocking patterns, and best practices across languages.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Testing Workflow

Testing workflow patterns and quality standards for various frameworks and languages.

## CRITICAL: Zero Warnings Tolerance

**Treat all warnings as errors. No exceptions.**

| Status | Output | Action |
|--------|--------|--------|
| ✅ PASS | All tests passed, no warnings | Proceed |
| ❌ FAIL | Tests passed with DeprecationWarning | Fix immediately |
| ❌ FAIL | Any warning present | Block commit |

**Pre-Commit Requirements:**
- ✅ All tests pass
- ✅ Zero warnings
- ✅ No linting errors
- ✅ No type errors
- ✅ Code formatted

**MUST NOT commit with:**
- ❌ Failing tests
- ❌ Any warnings
- ❌ Linting errors
- ❌ Unformatted code

## Testing Strategy

### Test Pyramid
1. **Unit Tests (70%)** - Fast, isolated, test individual functions/classes
2. **Integration Tests (20%)** - Test component interactions
3. **End-to-End Tests (10%)** - Full system tests

### What to Test
✅ **DO test:**
- Public APIs and interfaces
- Business logic and calculations
- Edge cases (empty inputs, None values, boundaries)
- Error handling and exceptions
- Data validation
- Critical paths through the application

❌ **DON'T test:**
- Private implementation details
- Third-party library internals
- Trivial getters/setters
- Framework magic (unless you suspect bugs)

### Development Workflow
**During Development:**
- Run targeted tests for fast iteration
- Fix issues immediately

**Before Commit:**
- Run full suite
- Fix all warnings/errors
- May run 1500+ tests

## Test Organization

### Directory Structure
```
tests/
├── __init__.py / conftest.py  # Shared fixtures and setup
├── unit/                      # Fast, isolated tests
│   └── test_*.py
├── integration/               # Component interaction tests
│   └── test_*.py
└── e2e/                       # End-to-end tests
    └── test_*.py
```

### Naming Conventions
- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*` (e.g., `TestUserService`)
- Test functions: `test_*` (e.g., `test_create_user_success`)
- Fixtures: Descriptive names (e.g., `user_service`, `mock_database`)

**CRITICAL:** MUST NOT name non-test classes with "Test" prefix - framework will try to collect them as tests.

## Coverage Requirements

### Coverage Goals
- **Minimum:** 80% overall coverage
- **Critical paths:** 100% coverage
- **New code:** Should not decrease overall coverage
- **Focus:** Behavior over line count

### What to Cover
**Test these:**
- Business logic, algorithms
- Edge cases, boundary conditions
- Error handling and exceptions
- Integration points, APIs
- Data validation
- Security-critical paths

**Skip these:**
- Trivial getters/setters
- Private implementation details
- Third-party library internals
- Simple data classes
- Framework magic (unless suspected bug)

### Edge Cases to Test
- Empty inputs (empty strings, empty collections)
- None/null values
- Boundary values (zero, maximum, minimum)
- Single item cases
- Negative numbers
- Large numbers
- Mixed positive and negative values

## Test Structure - Arrange-Act-Assert Pattern

All tests follow the **Arrange-Act-Assert (AAA)** pattern for clarity:

1. **Arrange** - Set up test data and conditions
2. **Act** - Execute the functionality being tested
3. **Assert** - Verify the results

This structure makes tests:
- Easy to understand at a glance
- Simple to maintain
- Consistent across the codebase

### Python Example
```python
# ✅ GOOD - Clear AAA structure
def test_user_registration():
    # Arrange
    user_data = {"email": "test@example.com", "password": "secure"}
    # Act
    result = register_user(user_data)
    # Assert
    assert result.success
    assert result.user.email == "test@example.com"

# ❌ BAD - Testing implementation details
def test_internal_method():
    obj = MyClass()
    assert obj._internal_state == expected  # Don't test private state
```

## Fixtures

```python
# conftest.py
@pytest.fixture
def db_connection():
    conn = create_test_database()
    yield conn
    conn.close()

@pytest.fixture
def sample_user():
    return User(email="test@example.com", name="Test User")

# test_file.py
def test_save_user(db_connection, sample_user):
    save_user(db_connection, sample_user)
    assert user_exists(db_connection, sample_user.email)
```

**Scopes:** `function` (default), `class`, `module`, `session`

## Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    (None, None),
])
def test_uppercase_conversion(input, expected):
    assert to_uppercase(input) == expected
```

## Mocking

```python
from unittest.mock import Mock, patch

# Mock external API
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_data()
    assert result["status"] == "ok"

# Dependency injection for testability
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection

def test_get_user():
    mock_db = Mock()
    mock_db.query.return_value = {"id": 1, "name": "Test"}
    service = UserService(mock_db)
    assert service.get_user(1)["name"] == "Test"
```

## Testing Exception Handling

Tests should verify that exceptions are raised with correct messages for invalid inputs:

```python
# ✅ GOOD - Testing exception
def test_create_user_invalid_email(user_service):
    """Test user creation fails with invalid email."""
    user_data = {
        "username": "testuser",
        "email": "invalid-email",  # Invalid format
        "age": 25
    }
    # Expect exception when invalid email is provided
    with pytest.raises(ValidationError) as exc_info:
        user_service.create_user(user_data)

    assert "email" in str(exc_info.value)
```

## Mocking External Dependencies

Tests should mock external dependencies to:
- Isolate the code being tested
- Avoid real external calls (APIs, databases, network)
- Control behavior for edge cases
- Speed up test execution

```python
from unittest.mock import Mock, patch

# Mock external service
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_data()
    # Verify mock was called and behavior is correct
    mock_get.assert_called_once()
    assert result["status"] == "ok"

# Dependency injection for testability
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection

def test_get_user():
    mock_db = Mock()
    mock_db.query.return_value = {"id": 1, "name": "Test"}
    service = UserService(mock_db)
    assert service.get_user(1)["name"] == "Test"
```

## Integration Testing

Integration tests verify that multiple components work together correctly. They typically:
- Use real or test databases/services
- Test API endpoints with real infrastructure
- Verify component interactions
- Run slower than unit tests

```python
@pytest.fixture(scope="module")
def test_database():
    """Provide test database for integration tests."""
    db = create_test_database()
    run_migrations(db)
    yield db
    cleanup_database(db)

def test_user_operations(test_database):
    """Test user repository with real database."""
    user = create_user(test_database, email="test@example.com")
    assert user.id is not None

    retrieved = get_user(test_database, user.id)
    assert retrieved.email == "test@example.com"
```

## TDD Pattern Example

```python
# 1. Write failing test
def test_calculate_discount():
    result = calculate_discount(price=100, discount_percent=10)
    assert result == 90

# 2. Implement
def calculate_discount(price, discount_percent):
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return price - (price * discount_percent / 100)
```

## Test Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=app",
    "--cov-report=term-missing",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
```

## Test Markers and Categorization

Tests can be categorized with markers to allow selective execution:

**Common marker categories:**
- `slow` - Tests that take longer to run (deselect with `-m "not slow"`)
- `integration` - Integration tests that use external services
- `unit` - Unit tests (fast, isolated)
- `e2e` - End-to-end tests
- `performance` - Performance/benchmark tests

```python
@pytest.mark.slow
def test_expensive_operation():
    result = process_large_dataset()
    assert result.success

@pytest.mark.integration
def test_database_integration():
    result = query_database()
    assert result is not None

# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration
```

## Performance Testing

Performance tests verify that operations complete within acceptable time limits:

```python
import time

def test_performance_within_limit(data_processor):
    """Test processing completes within time limit."""
    large_dataset = generate_test_data(10000)

    start = time.time()
    result = data_processor.process(large_dataset)
    duration = time.time() - start

    assert duration < 1.0  # Should complete in under 1 second
    assert len(result) == 10000
```

## Development Workflow

1. Write/modify code
2. Run targeted tests
3. Fix issues immediately
4. Run full suite (`make check`)
5. Commit when zero warnings

**MUST:**
- ✅ Test after every change
- ✅ Fix warnings immediately
- ✅ Add tests for new features

**MUST NOT:**
- ❌ Commit with failures/warnings
- ❌ Skip tests after changes
- ❌ Ignore failures as "known issues"

## Essential Commands

```bash
# Development - Targeted
pytest tests/unit/test_file.py -v           # Specific file
pytest -k "test_name" -v                    # Pattern match
pytest tests/unit/test_file.py::test_func   # Exact test
pytest -v --tb=short                        # Cleaner errors

# Debugging
pytest -l                                   # Show locals
pytest --pdb                                # Debug on failure
pytest -x                                   # Stop on first failure
pytest --lf                                 # Rerun last failed

# Coverage
pytest --cov=app --cov-report=html          # HTML report
pytest --cov=app --cov-report=term-missing  # Terminal report

# Verification
make check                                  # Full suite + quality
uv run pytest                               # All tests
uv run black --check app/ tests/            # Format check
uv run isort --check app/ tests/            # Import order
uv run flake8 app/ tests/                   # Linting
uv run mypy app/ tests/                     # Type check
```

## Test Quality Checklist

- ✅ Run in isolation (no shared state)
- ✅ Deterministic (same result every time)
- ✅ Fast (mock slow operations)
- ✅ Clear names document behavior
- ✅ Test edge cases and errors
- ✅ Zero warnings in output
- ✅ >80% coverage on critical paths

## Advanced Testing Patterns

| Pattern | Description |
|---------|-------------|
| **Local-first** | All tests MUST run locally without external dependencies |
| **Testcontainers** | Use testcontainers for integration tests |
| **Flaky policy** | 48-hour remediation, then quarantine or delete |
| **Thread safety** | Go's `-race` flag, TSAN for thread safety |
| **Idempotence** | Verify operations are safely re-runnable |
| **Factories > Fixtures** | Prefer factories for flexible test data |
| **Soak tests** | Long-running tests for memory leak detection |
| **Acceptance tests** | BDD with domain language |

## Out of Scope

- Python-specific pytest patterns → see `python-testing`
- TypeScript-specific patterns → see `typescript-testing`

---

**TL;DR: Zero warnings policy. Follow test pyramid. Arrange-Act-Assert pattern. Mock external dependencies. Test behavior not implementation. >80% coverage on critical paths. Run targeted tests during development, full suite before commit.**
