---
name: error-handling
description: Error handling patterns including exception hierarchies, error messages, and recovery strategies. Activated when designing exceptions or error handling.
---

# Error handling

## Purpose

Guide for designing robust error handling including exception hierarchies, clear error messages, and recovery strategies.

## When to use

This skill activates when:

- Designing exception classes
- Writing error messages
- Implementing error recovery
- Creating diagnostic output
- Handling validation errors

## Core principles

### Clear error messages

- Tell user what went wrong
- Tell user how to fix it
- Include context (file, line, value)

### Exception hierarchies

- Create project-specific base exception
- Categorize by error type
- Enable selective catching

## Exception hierarchy design

### Base exception

```python
class AppError(Exception):
    """Base exception for all application errors.

    All application-specific exceptions should inherit from this.
    Allows catching all application errors with one except clause.
    """
    pass
```

### Categorized exceptions

```python
class ValidationError(AppError):
    """Raised when validation fails."""

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: object = None,
    ) -> None:
        super().__init__(message)
        self.field = field
        self.value = value

    def __str__(self) -> str:
        if self.field:
            return f"{self.field}: {self.args[0]}"
        return self.args[0]


class ConfigurationError(AppError):
    """Raised when configuration is invalid."""

    def __init__(self, message: str, key: str | None = None) -> None:
        super().__init__(message)
        self.key = key


class ProcessingError(AppError):
    """Raised when processing fails."""

    def __init__(
        self,
        message: str,
        source: str | None = None,
        position: int | None = None,
    ) -> None:
        super().__init__(message)
        self.source = source
        self.position = position
```

## Error message design

### Good error messages

```python
# Bad: Vague
raise ValueError("Invalid input")

# Good: Specific with context
raise ValidationError(
    f"Expected integer between 1 and 100, got {value!r}",
    field="count",
    value=value,
)

# Bad: Technical jargon
raise RuntimeError("NoneType has no attribute 'process'")

# Good: User-focused
raise ProcessingError(
    "Input file is empty or unreadable",
    source=filepath,
)
```

### Error message pattern

```python
def validate_count(value: int) -> int:
    """Validate count is in valid range.

    Error message pattern:
    1. What's wrong
    2. What was expected
    3. What was received
    4. How to fix (if applicable)
    """
    if value < 1:
        raise ValidationError(
            f"Count must be at least 1, got {value}. "
            "Provide a positive integer.",
            field="count",
            value=value,
        )

    if value > 100:
        raise ValidationError(
            f"Count cannot exceed 100, got {value}. "
            "Use a smaller value or process in batches.",
            field="count",
            value=value,
        )

    return value
```

## Error recovery patterns

### Try specific exceptions first

```python
def process_file(path: Path) -> Result:
    """Process file with specific error handling."""
    try:
        content = path.read_text()
    except FileNotFoundError:
        raise ProcessingError(f"File not found: {path}")
    except PermissionError:
        raise ProcessingError(f"Cannot read file (permission denied): {path}")
    except OSError as e:
        raise ProcessingError(f"Cannot read file: {path} ({e})")

    try:
        return parse_content(content)
    except ParseError as e:
        raise ProcessingError(
            f"Invalid file format: {e}",
            source=str(path),
        )
```

### Wrap low-level exceptions

```python
def fetch_data(url: str) -> dict:
    """Fetch data with wrapped exceptions."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise ProcessingError(f"Request timed out: {url}")
    except requests.ConnectionError:
        raise ProcessingError(f"Cannot connect to server: {url}")
    except requests.HTTPError as e:
        raise ProcessingError(f"Server error ({e.response.status_code}): {url}")
    except ValueError:
        raise ProcessingError(f"Invalid JSON response from: {url}")
```

### Aggregate multiple errors

```python
class ValidationErrors(AppError):
    """Collection of validation errors."""

    def __init__(self, errors: list[ValidationError]) -> None:
        self.errors = errors
        messages = [str(e) for e in errors]
        super().__init__(f"Validation failed:\n" + "\n".join(f"  - {m}" for m in messages))

def validate_all(items: list[dict]) -> list[Item]:
    """Validate all items, collecting all errors."""
    errors: list[ValidationError] = []
    results: list[Item] = []

    for i, item in enumerate(items):
        try:
            results.append(validate_item(item))
        except ValidationError as e:
            e.field = f"items[{i}].{e.field}" if e.field else f"items[{i}]"
            errors.append(e)

    if errors:
        raise ValidationErrors(errors)

    return results
```

## Logging vs raising

```python
import logging

logger = logging.getLogger(__name__)

def process_batch(items: list[Item]) -> list[Result]:
    """Process items, logging warnings but raising on failures."""
    results = []

    for item in items:
        try:
            result = process_item(item)
            results.append(result)
        except RecoverableError as e:
            # Log warning, continue processing
            logger.warning(f"Skipping item {item.id}: {e}")
        except FatalError as e:
            # Log error, re-raise to stop processing
            logger.error(f"Fatal error processing {item.id}: {e}")
            raise

    return results
```

## Checklist

- [ ] Application-specific base exception defined
- [ ] Exceptions categorized by error type
- [ ] Error messages are clear and actionable
- [ ] Context included (field, value, source)
- [ ] Low-level exceptions wrapped appropriately
- [ ] Recovery strategies appropriate for error types

---

**Additional resources:**

- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
