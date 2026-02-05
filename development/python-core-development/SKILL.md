---
name: python-core-development
description: Implement Python code with dataclasses, type hints, protocols, error handling, and async programming. Use when designing classes, implementing type safety, handling exceptions, or writing async code.
---

# Python Core Development Specialist

Specialized in Python class design, type safety, error handling, and asynchronous programming.

## When to Use This Skill

- Designing Python classes with dataclasses or regular classes
- Implementing type hints and type-safe code
- Creating custom exceptions and error handling
- Writing asynchronous code with async/await
- Implementing context managers
- Using Protocol for structural typing

## Core Principles

- **Type Safety First**: Always use type hints for function signatures and class attributes
- **Explicit is Better Than Implicit**: Clear, readable code over clever tricks
- **Fail Fast with Clear Errors**: Raise exceptions early with descriptive messages
- **Dataclasses for Data**: Use dataclasses for data containers
- **Protocol for Duck Typing**: Use Protocol for structural subtyping
- **Async for I/O**: Use async/await for I/O-bound operations

## Implementation Guidelines

### Dataclass Pattern

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User data model."""

    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Validate data after initialization."""
        if not self.email or "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")

@dataclass
class Order:
    """Order with validation."""

    id: int
    user_id: int
    items: list[str]
    total: float
    status: str = "pending"

    def __post_init__(self):
        """WHY: Ensure business rules are enforced at object creation."""
        if self.total < 0:
            raise ValueError("Total cannot be negative")
        if not self.items:
            raise ValueError("Order must have at least one item")
```

### Type Hints and Protocol

```python
from typing import Protocol, Optional, Sequence
from collections.abc import Iterator

# Protocol for structural typing
class Drawable(Protocol):
    """Protocol for objects that can be drawn."""

    def draw(self) -> str:
        """Return string representation."""
        ...

class Circle:
    """Circle implements Drawable protocol."""

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(radius={self.radius})"

# Function using Protocol
def render(shapes: Sequence[Drawable]) -> list[str]:
    """Render multiple shapes.

    Args:
        shapes: Sequence of drawable objects

    Returns:
        List of rendered strings
    """
    return [shape.draw() for shape in shapes]

# Type hints for complex types
def process_items(
    items: Sequence[str],
    max_count: Optional[int] = None,
    *,  # Force keyword-only arguments after this
    case_sensitive: bool = True
) -> Iterator[str]:
    """Process items with optional filtering.

    Args:
        items: Sequence of items to process
        max_count: Optional maximum number of items to process
        case_sensitive: Whether to preserve case (keyword-only)

    Yields:
        Processed items
    """
    count = 0
    for item in items:
        if max_count is not None and count >= max_count:
            break

        processed = item if case_sensitive else item.lower()
        yield processed
        count += 1
```

### Custom Exceptions and Error Handling

```python
# Custom exception hierarchy
class ApplicationError(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.code = code

class ValidationError(ApplicationError):
    """Raised when validation fails."""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, code="VALIDATION_ERROR")
        self.field = field

class NotFoundError(ApplicationError):
    """Raised when resource is not found."""

    def __init__(self, resource: str, id: int | str):
        super().__init__(
            f"{resource} with id {id} not found",
            code="NOT_FOUND"
        )
        self.resource = resource
        self.id = id

# Usage with proper error handling
def create_user(email: str, name: str) -> User:
    """Create user with validation.

    Args:
        email: User email address
        name: User display name

    Returns:
        Created user object

    Raises:
        ValidationError: If email or name is invalid
    """
    # WHY: Validate early to fail fast with clear error
    if not email or "@" not in email:
        raise ValidationError("Invalid email format", field="email")

    if not name or len(name) < 2:
        raise ValidationError("Name must be at least 2 characters", field="name")

    return User(id=generate_id(), email=email, name=name)

# Error handling in caller
def register_user(email: str, name: str) -> dict:
    """Register new user with error handling."""
    try:
        user = create_user(email, name)
        return {"success": True, "user": user}
    except ValidationError as e:
        return {
            "success": False,
            "error": e.message,
            "field": e.field
        }
    except Exception as e:
        # WHY: Log unexpected errors for debugging
        logger.error(f"Unexpected error during registration: {e}")
        return {
            "success": False,
            "error": "An unexpected error occurred"
        }
```

### Async/Await Pattern

```python
import asyncio
from typing import Optional

# Async function
async def fetch_user(user_id: int) -> Optional[dict]:
    """Fetch user from database asynchronously.

    Args:
        user_id: User ID to fetch

    Returns:
        User data or None if not found
    """
    async with database.connection() as conn:
        result = await conn.fetchone(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        return dict(result) if result else None

# Async with multiple concurrent operations
async def fetch_user_with_orders(user_id: int) -> dict:
    """Fetch user and their orders concurrently.

    Args:
        user_id: User ID

    Returns:
        Dict with user and orders data
    """
    # WHY: Run queries concurrently to improve performance
    user_task = fetch_user(user_id)
    orders_task = fetch_orders(user_id)

    user, orders = await asyncio.gather(user_task, orders_task)

    if not user:
        raise NotFoundError("User", user_id)

    return {
        "user": user,
        "orders": orders
    }

# Async context manager
class DatabaseConnection:
    """Async database connection context manager."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn: Optional[Connection] = None

    async def __aenter__(self) -> Connection:
        """Establish connection."""
        self.conn = await connect(self.connection_string)
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """WHY: Ensure connection is closed even on error."""
        if self.conn:
            await self.conn.close()

# Usage
async def query_users() -> list[dict]:
    """Query users using async context manager."""
    async with DatabaseConnection("postgresql://...") as conn:
        results = await conn.fetch("SELECT * FROM users")
        return [dict(row) for row in results]
```

### Context Manager Pattern

```python
from typing import Optional, TextIO
from pathlib import Path

# Context manager for file operations
class FileProcessor:
    """Process file with automatic cleanup."""

    def __init__(self, file_path: Path, mode: str = "r"):
        self.file_path = file_path
        self.mode = mode
        self.file: Optional[TextIO] = None

    def __enter__(self) -> TextIO:
        """Open file."""
        self.file = open(self.file_path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """WHY: Ensure file is closed even if error occurs."""
        if self.file:
            self.file.close()

# Usage
def process_log_file(file_path: Path) -> int:
    """Process log file and count lines."""
    with FileProcessor(file_path) as f:
        return sum(1 for _ in f)
```

## Tools to Use

- `Read`: Read existing Python files
- `Write`: Create new Python modules
- `Edit`: Modify existing code
- `Bash`: Run Python code, tests, and linters

### Bash Commands

```bash
# Run Python script
python script.py

# Type checking with mypy
mypy app/

# Linting and formatting with ruff (modern)
ruff check --fix .
ruff format .

# Traditional linting and formatting
black .
isort .
flake8 .

# Run tests
pytest tests/
pytest --cov=app tests/
```

## Workflow

1. **Understand Requirements**: Clarify what needs to be implemented
2. **Write Tests First**: Use `pytest-testing` skill
3. **Verify Tests Fail**: Confirm tests fail correctly (Red)
4. **Implement Code**: Write implementation with type hints
5. **Run Tests**: Ensure tests pass (Green)
6. **Run Type Checker**: Validate with mypy
7. **Run Linter/Formatter**: Clean up code style
8. **Refactor**: Improve code quality
9. **Commit**: Create atomic commit

## Related Skills

- `pytest-testing`: For writing unit and integration tests
- `python-api-development`: For FastAPI/Flask development
- `pytest-api-testing`: For testing API endpoints

## Coding Standards

See [Python Coding Standards](../_shared/python-coding-standards.md)

## TDD Workflow

Follow [Python TDD Workflow](../_shared/python-tdd-workflow.md)

## Key Reminders

- Always use type hints for function signatures and class attributes
- Use dataclasses for data containers (avoid writing boilerplate)
- Create custom exceptions for domain-specific errors
- Fail fast with clear, descriptive error messages
- Use async/await for I/O-bound operations
- Use context managers for resource management
- Use Protocol for structural typing (duck typing with type safety)
- Write tests before implementation (TDD)
- Run mypy for type checking
- Use ruff or black+isort+flake8 for code quality
- Write comments explaining WHY, not WHAT
