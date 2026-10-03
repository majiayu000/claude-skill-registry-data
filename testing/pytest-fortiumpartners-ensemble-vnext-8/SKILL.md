---
name: pytest
description: Execute and generate pytest tests for Python projects with fixtures, parametrization, and mocking support
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Pytest Testing Skill

Generate pytest-based test code that uses class-based organization,
leverages pytest's native features, and ensures comprehensive coverage.

## Scope

- Pytest test organization and structure
- Class-based test suites
- Fixture usage and scoping
- Parametrization patterns
- Mocking and isolation techniques
- Coverage requirements (happy paths, edge cases, error conditions)

**Out of Scope:** `unittest.TestCase` tests, integration tests requiring
full application context, performance/load testing.

---

## Quick Rules Summary

- **Class-based organization**: All tests in `TestSomething` classes
- **No top-level functions**: Prohibit module-level `test_*` functions
- **No unittest.TestCase**: Use plain pytest classes
- **Fixtures over setup**: Use pytest fixtures, not `setUp`/`tearDown`
- **Parametrize variants**: Use `@pytest.mark.parametrize` for multiple inputs
- **Mock external I/O**: Isolate by mocking APIs, databases, file systems
- **Test negative paths**: Include tests for invalid inputs and errors
- **Descriptive names**: Test methods named `test_*` with clear names
- **No `__init__`**: Test classes should not define `__init__` methods
- **Isolation**: Tests must be independent and runnable in any order

---

## Quantified Expectations

- **Test coverage**: >= 80% line coverage; 100% for critical paths
- **Test class size**: Each class tests one logical component/behavior
- **Test method length**: <= 20 lines per test; extract helpers if needed
- **Assertions per test**: Prefer 1-3 assertions for clarity
- **Parametrization**: Use for >= 3 similar test cases
- **Fixture scope**: Default to function; class/module for immutable shared
- **Test categories**: Every public function/method should have:
  - At least 1 happy path test
  - At least 1 edge case test
  - At least 1 error condition test (if applicable)

---

## Directory Structure

```
project_root/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── parser.py
│       └── validator.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures
│   ├── test_parser.py
│   └── test_validator.py
├── pytest.ini
└── requirements-test.txt
```

## Naming Conventions

- Test files: `test_*.py` or `*_test.py`
- Test classes: `TestSomething` (PascalCase with Test prefix)
- Test methods: `test_*` (snake_case with test_ prefix)
- Fixtures: Descriptive snake_case names

---

## Class-Based Test Organization

Always organize tests into classes. Never use top-level test functions.

```python
# BAD: Top-level test function
def test_normalize_token_success():
    result = normalize_token("  Hello  ")
    assert result == "hello"


# GOOD: Class-based organization
class TestNormalizeToken:
    """Tests for the normalize_token function."""

    def test_success_with_whitespace(self):
        result = normalize_token("  Hello  ")
        assert result == "hello"

    def test_empty_string(self):
        result = normalize_token("")
        assert result == ""

    def test_none_raises_error(self):
        with pytest.raises(ValueError, match="cannot be None"):
            normalize_token(None)
```

### Grouping Related Tests

```python
import pytest
from mypackage.parser import Parser, ParserError


class TestParserInitialization:
    """Tests for Parser initialization."""

    def test_default_configuration(self):
        parser = Parser()
        assert parser.strict_mode is False
        assert parser.encoding == "utf-8"

    def test_custom_configuration(self):
        parser = Parser(strict_mode=True, encoding="latin-1")
        assert parser.strict_mode is True

    def test_invalid_encoding_raises_error(self):
        with pytest.raises(ValueError, match="Invalid encoding"):
            Parser(encoding="invalid-encoding")


class TestParserParsing:
    """Tests for Parser parsing functionality."""

    def test_parse_valid_input(self):
        parser = Parser()
        result = parser.parse("valid data")
        assert result == {"data": "valid data"}

    def test_parse_empty_input(self):
        parser = Parser()
        result = parser.parse("")
        assert result == {}
```

---

## Fixtures: Setup and Dependency Injection

Use fixtures for setup instead of `setUp`/`tearDown` or `__init__`.

```python
# BAD: Using unittest-style setUp
class TestDatabase:
    def setUp(self):  # Won't work in pytest!
        self.db = Database()


# GOOD: Using pytest fixtures
@pytest.fixture
def db():
    """Provide a Database instance."""
    database = Database()
    yield database
    database.disconnect()  # Teardown


class TestDatabase:
    """Tests for Database class."""

    def test_connect(self, db):
        db.connect()
        assert db.is_connected

    def test_execute_query(self, db):
        db.connect()
        result = db.execute("SELECT 1")
        assert result == [1]
```

### Fixture Scopes

```python
# Function scope (default): New instance per test
@pytest.fixture
def cache():
    """Fresh cache for each test."""
    return Cache()


# Class scope: Shared across tests in a class
@pytest.fixture(scope="class")
def config():
    """Shared immutable configuration."""
    return Config.from_file("test_config.yaml")


# Module scope: Shared across module
@pytest.fixture(scope="module")
def expensive_resource():
    """Expensive resource shared across module."""
    resource = ExpensiveResource()
    resource.initialize()
    yield resource
    resource.cleanup()
```

### Shared Fixtures in conftest.py

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_logger():
    """Provide a mock logger for testing."""
    return Mock()


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
    }


@pytest.fixture
def temp_file(tmp_path):
    """Provide a temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path
```

---

## Parametrization: Testing Multiple Cases

Use `@pytest.mark.parametrize` to test multiple inputs.

```python
# BAD: Duplicated test methods
class TestValidateEmail:
    def test_valid_email_1(self):
        assert validate_email("user@example.com") is True

    def test_valid_email_2(self):
        assert validate_email("test@example.co.uk") is True


# GOOD: Parametrized test
class TestValidateEmail:
    """Tests for email validation."""

    @pytest.mark.parametrize("email", [
        "user@example.com",
        "test.user@example.co.uk",
        "user+tag@example.com",
    ])
    def test_valid_emails(self, email):
        assert validate_email(email) is True

    @pytest.mark.parametrize("email", [
        "invalid",
        "@example.com",
        "user@",
        "",
    ])
    def test_invalid_emails(self, email):
        assert validate_email(email) is False
```

### Multiple Parameters

```python
class TestCalculator:
    """Tests for Calculator class."""

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (0.1, 0.2, 0.3),
    ])
    def test_add(self, a, b, expected):
        calc = Calculator()
        result = calc.add(a, b)
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize("a,b", [
        (1, 0),
        (100, 0),
        (-5, 0),
    ])
    def test_divide_by_zero_raises_error(self, a, b):
        calc = Calculator()
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(a, b)
```

### Named Parametrizations

```python
class TestParseConfig:
    """Tests for configuration parsing."""

    @pytest.mark.parametrize("config_string,expected", [
        pytest.param(
            "key=value",
            {"key": "value"},
            id="simple_key_value"
        ),
        pytest.param(
            "key1=value1\nkey2=value2",
            {"key1": "value1", "key2": "value2"},
            id="multiple_entries"
        ),
        pytest.param(
            "",
            {},
            id="empty_config"
        ),
    ])
    def test_parse_config(self, config_string, expected):
        result = parse_config(config_string)
        assert result == expected
```

---

## Mocking and Isolation

### Mocking External Dependencies

```python
import pytest
from unittest.mock import Mock, patch
from mypackage.api_client import ApiClient, ApiError


class TestApiClient:
    """Tests for ApiClient class."""

    @pytest.fixture
    def mock_response(self):
        """Provide a mock HTTP response."""
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"data": "success"}
        return response

    def test_fetch_data_success(self, mock_response):
        with patch("requests.get", return_value=mock_response):
            client = ApiClient(base_url="https://api.example.com")
            result = client.fetch_data("/endpoint")
            assert result == {"data": "success"}

    def test_fetch_data_http_error(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection error")
            client = ApiClient(base_url="https://api.example.com")
            with pytest.raises(ApiError, match="Failed to fetch"):
                client.fetch_data("/endpoint")
```

### Monkeypatch for Environment Variables

```python
class TestLoadConfig:
    """Tests for configuration loading."""

    def test_load_from_environment(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.setenv("DEBUG", "true")

        config = load_config()
        assert config.api_key == "test-key-123"
        assert config.debug is True

    def test_missing_required_env_var(self, monkeypatch):
        monkeypatch.delenv("API_KEY", raising=False)

        with pytest.raises(ValueError, match="API_KEY is required"):
            load_config()
```

### Mocking Time

```python
from unittest.mock import patch
from datetime import datetime


class TestScheduler:
    """Tests for Scheduler class."""

    def test_is_time_to_run(self):
        with patch("mypackage.scheduler.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2025, 1, 1, 10, 0)
            scheduler = Scheduler(run_hour=10)
            assert scheduler.is_time_to_run() is True
```

---

## Testing Error Conditions

```python
class TestValidateAge:
    """Tests for age validation."""

    @pytest.mark.parametrize("age", [0, 18, 100, 120])
    def test_valid_ages(self, age):
        validate_age(age)  # Should not raise

    @pytest.mark.parametrize("age,error_message", [
        (-1, "Age cannot be negative"),
        (151, "Age exceeds maximum"),
    ])
    def test_invalid_ages(self, age, error_message):
        with pytest.raises(ValidationError, match=error_message):
            validate_age(age)

    def test_non_integer_type(self):
        with pytest.raises(TypeError, match="must be an integer"):
            validate_age("25")
```

### Verify Error Messages Contain Context

```python
class TestParserErrors:
    """Tests for Parser error handling."""

    def test_parse_error_includes_line_number(self):
        parser = Parser()
        invalid_input = "line1\nline2\ninvalid line 3"

        with pytest.raises(ParseError) as exc_info:
            parser.parse(invalid_input)

        error_message = str(exc_info.value)
        assert "line 3" in error_message
        assert "invalid" in error_message
```

---

## Testing File Operations

Use pytest's `tmp_path` fixture.

```python
class TestFileManager:
    """Tests for FileManager class."""

    def test_write_and_read_file(self, tmp_path):
        file_path = tmp_path / "test.txt"
        manager = FileManager()

        manager.write(file_path, "test content")
        content = manager.read(file_path)

        assert content == "test content"

    def test_read_nonexistent_file_raises_error(self, tmp_path):
        file_path = tmp_path / "nonexistent.txt"
        manager = FileManager()

        with pytest.raises(FileNotFoundError):
            manager.read(file_path)
```

---

## Testing Side Effects

```python
from unittest.mock import Mock, call


class TestDataProcessor:
    """Tests for DataProcessor class."""

    def test_process_logs_progress(self):
        mock_logger = Mock()
        processor = DataProcessor(logger=mock_logger)

        processor.process([{"id": 1}, {"id": 2}])

        mock_logger.info.assert_has_calls([
            call("Processing started"),
            call("Processed 2 items"),
            call("Processing completed"),
        ])

    def test_process_calls_callbacks(self):
        callback = Mock()
        processor = DataProcessor(on_complete=callback)

        processor.process([{"id": 1}])

        callback.assert_called_once_with(success=True, count=1)
```

---

## Anti-Patterns and Corrections

### Top-Level Test Functions

```python
# BAD
def test_add():
    assert add(1, 2) == 3

# GOOD
class TestMathOperations:
    def test_add(self):
        assert add(1, 2) == 3
```

### Using unittest.TestCase

```python
# BAD
import unittest

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

# GOOD
import pytest

@pytest.fixture
def parser():
    return Parser()

class TestParser:
    def test_parse(self, parser):
        result = parser.parse("data")
        assert result == expected
```

### Test Interdependence

```python
# BAD: Tests depend on each other
class TestBadSequence:
    shared_state = None

    def test_step_1(self):
        self.shared_state = create_resource()

    def test_step_2(self):
        self.shared_state.process()  # Depends on step_1!


# GOOD: Tests are independent
@pytest.fixture
def resource():
    return create_resource()

class TestGoodIsolation:
    def test_create_resource(self, resource):
        assert resource is not None

    def test_process_resource(self, resource):
        result = resource.process()
        assert result is not None
```

---

## Do and Do Not

### Do

- Organize all tests into `TestSomething` classes
- Use fixtures for setup/teardown via dependency injection
- Use `@pytest.mark.parametrize` for multiple similar test cases
- Mock external I/O (APIs, databases, file system, time)
- Test happy paths, edge cases, and error conditions
- Use descriptive test names
- Use `pytest.raises()` to test exceptions
- Use `tmp_path` fixture for file testing
- Use `monkeypatch` for environment variables
- Verify error messages contain helpful context
- Use `pytest.approx()` for floating-point comparisons
- Structure tests with Arrange-Act-Assert pattern

### Do Not

- Write top-level `test_*` functions
- Inherit from `unittest.TestCase`
- Use `setUp`/`tearDown` methods
- Define `__init__` in test classes
- Create test interdependencies
- Test implementation details
- Make external network calls in unit tests
- Use `time.sleep()` in tests
- Write tests without assertions
- Catch exceptions in tests (let pytest handle it)
- Hardcode file paths (use `tmp_path`)
- Rely on test execution order

---

## Acceptance Checklist

- [ ] All tests organized into `Test*` classes
- [ ] Zero module-level `test_*` functions
- [ ] No `unittest.TestCase` inheritance
- [ ] Setup uses fixtures, not `setUp`/`tearDown`
- [ ] Similar tests use `@pytest.mark.parametrize`
- [ ] External I/O is mocked appropriately
- [ ] Happy paths, edge cases, and errors tested
- [ ] Tests can run in any order
- [ ] Test names clearly describe what is tested
- [ ] Exceptions tested with `pytest.raises()`
- [ ] Error message content validated
- [ ] Every test has at least one assertion
- [ ] No `time.sleep()` calls in tests
- [ ] File tests use `tmp_path` fixture
- [ ] All tests pass with pytest

---

## pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --verbose
    --tb=short
    --cov=src
    --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

---

## When Uncertain

- Ask for clarification on what behavior needs testing
- Consult pytest documentation for patterns
- Check if fixture or parametrization would simplify tests
- Consider if testing behavior or implementation
- Verify tests are isolated and can run independently

Good tests are isolated, readable, and focused on behavior.
They document what the code should do and catch regressions early.
