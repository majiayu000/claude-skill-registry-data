---
name: python-engineering
description: Comprehensive Python engineering guidelines for writing production-quality Python code. This skill should be used when writing Python code, performing Python code reviews, working with Python tools (uv, ruff, mypy, pytest), or answering questions about Python best practices and patterns. Applies to CLI tools, AI agents (langgraph), and general Python development.
---

# Python Engineering Excellence

This skill provides comprehensive Python engineering guidelines for modern Python development. Use this when writing or reviewing Python code for production systems, CLI tools, and AI agents.

## Core Philosophy

### The Zen of Python (Selected)

1. **Explicit is better than implicit** - Make intentions clear
2. **Simple is better than complex** - Favor straightforward solutions
3. **Readability counts** - Code is read more than written
4. **Errors should never pass silently** - Handle or propagate errors explicitly
5. **There should be one obvious way to do it** - Follow established patterns

### Design Principles

- Pass dependencies explicitly, avoid global state
- Favor composition over inheritance
- Keep functions small and focused
- Make side effects obvious

## Project Structure

### Standard Layout

```
project/
  src/
    mypackage/
      __init__.py
      core.py
      cli.py
      agents/
        __init__.py
        graph.py
  tests/
    __init__.py
    test_core.py
    conftest.py
  pyproject.toml
  README.md
```

**Guidelines:**
- Use `src/` layout to avoid import confusion
- One package per project under `src/`
- Tests mirror source structure
- All configuration in `pyproject.toml`

### pyproject.toml (uv)

```toml
[project]
name = "mypackage"
version = "0.1.0"
description = "My package description"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.9.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
]

[project.scripts]
mycli = "mypackage.cli:app"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Naming Conventions

### PEP 8 Rules

```python
# Good
module_name          # modules: lowercase_with_underscores
ClassName            # classes: CamelCase
function_name        # functions: lowercase_with_underscores
variable_name        # variables: lowercase_with_underscores
CONSTANT_NAME        # constants: UPPERCASE_WITH_UNDERSCORES
_private_var         # private: leading underscore
__mangled            # name mangling: double underscore

# Bad
ClassName()          # Don't use for functions
functionName         # Don't use camelCase for functions
VariableName         # Don't use CamelCase for variables
```

### Specific Conventions

```python
# Good - descriptive names
def calculate_total_price(items: list[Item]) -> Decimal:
    ...

user_count = len(users)
is_valid = check_validity(data)

# Good - short names for small scopes
for i, item in enumerate(items):
    process(item)

# Bad - single letters for large scopes
def process(d):  # What is d?
    ...
```

### Boolean Naming

```python
# Good - question-like predicates
is_active = True
has_permission = user.can_edit
should_retry = attempt < max_retries

# Bad
active = True        # Unclear if boolean
permission = True    # Noun, not predicate
```

## Code Organization

### Imports

Use `import` statements for packages and modules, not for individual classes or functions (except from `typing` and `collections.abc`).

```python
# Good - grouped and sorted (ruff handles this)
from __future__ import annotations

import asyncio
import os
from pathlib import Path

import httpx
from pydantic import BaseModel

from mypackage.core import process
from mypackage.models import User

# Good - import modules, not individual items
from sound.effects import echo
echo.EchoFilter(...)

# Good - typing symbols can be imported directly
from typing import Any, TypeVar
from collections.abc import Sequence, Mapping

# Good - use aliases when needed
import pandas as pd  # Standard abbreviations OK
from mypackage.submodule import very_long_module as vlm

# Bad - importing individual classes (non-typing)
from sound.effects.echo import EchoFilter

# Bad - ungrouped, relative imports in library code
from .core import process  # Avoid relative imports
import os, sys  # Never multiple imports on one line
```

### Module Structure

```python
# Good - clear __all__ for public API
__all__ = ["Client", "process_data", "DataError"]

class DataError(Exception):
    """Raised when data processing fails."""

class Client:
    """HTTP client for the service."""
    ...

def process_data(data: bytes) -> dict:
    """Process raw data into structured format."""
    ...

# Private helpers below public API
def _validate(data: bytes) -> bool:
    ...
```

### Class Organization

```python
class Service:
    """Service for processing requests."""

    def __init__(self, client: Client, config: Config) -> None:
        self._client = client
        self._config = config

    # Public methods first
    def process(self, request: Request) -> Response:
        data = self._fetch(request)
        return self._transform(data)

    # Private methods after
    def _fetch(self, request: Request) -> bytes:
        ...

    def _transform(self, data: bytes) -> Response:
        ...
```

## Error Handling

### Exception Patterns

```python
# Good - custom exceptions with context
class ProcessingError(Exception):
    """Raised when processing fails."""

    def __init__(self, message: str, item_id: str) -> None:
        super().__init__(message)
        self.item_id = item_id

# Good - raise with context
def process(item: Item) -> Result:
    try:
        return transform(item)
    except ValueError as e:
        raise ProcessingError(f"failed to transform: {e}", item.id) from e

# Good - use built-in exceptions appropriately
def set_age(age: int) -> None:
    if age < 0:
        raise ValueError("age must be non-negative")

# Bad - bare except (catches KeyboardInterrupt, SystemExit)
try:
    process(item)
except:  # Never do this
    pass

# Bad - catching Exception without re-raising
try:
    process(item)
except Exception:
    pass  # Silently swallowing errors

# OK - catching Exception only if re-raising or at isolation point
try:
    process(item)
except Exception:
    logger.exception("Processing failed")
    raise  # Re-raise after logging
```

### Assertions

Do not use `assert` for validation or preconditions—use explicit conditionals:

```python
# Bad - assert can be disabled with -O flag
def process(data: bytes) -> dict:
    assert data, "data required"  # Skipped in optimized mode!
    return parse(data)

# Good - explicit validation
def process(data: bytes) -> dict:
    if not data:
        raise ValueError("data required")
    return parse(data)

# OK - assert in tests (pytest)
def test_process():
    result = process(b"test")
    assert result["status"] == "ok"
```

### Context Managers

```python
# Good - use context managers for cleanup
from contextlib import contextmanager

@contextmanager
def managed_connection(dsn: str):
    conn = connect(dsn)
    try:
        yield conn
    finally:
        conn.close()

# Usage
with managed_connection(dsn) as conn:
    conn.execute(query)

# Good - async context manager
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_session():
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()
```

### Guard Clauses

```python
# Good - early returns reduce nesting
def process_user(user: User | None) -> Result:
    if user is None:
        raise ValueError("user required")

    if not user.is_active:
        return Result.inactive()

    if not user.has_permission("process"):
        return Result.forbidden()

    # Main logic at base indentation
    return do_processing(user)

# Bad - deeply nested
def process_user(user: User | None) -> Result:
    if user is not None:
        if user.is_active:
            if user.has_permission("process"):
                return do_processing(user)
            else:
                return Result.forbidden()
        else:
            return Result.inactive()
    else:
        raise ValueError("user required")
```

## Async/Await

### Basic Patterns

```python
# Good - async function
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Good - gather for concurrent operations
async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# Bad - sequential when concurrent is possible
async def fetch_all_slow(urls: list[str]) -> list[dict]:
    results = []
    for url in urls:
        data = await fetch_data(url)  # Sequential!
        results.append(data)
    return results
```

### Task Management

```python
# Good - structured concurrency with TaskGroup (Python 3.11+)
async def process_items(items: list[Item]) -> list[Result]:
    results = []
    async with asyncio.TaskGroup() as tg:
        for item in items:
            task = tg.create_task(process_item(item))
            results.append(task)
    return [t.result() for t in results]

# Good - timeout handling
async def fetch_with_timeout(url: str, timeout: float = 30.0) -> dict:
    async with asyncio.timeout(timeout):
        return await fetch_data(url)
```

### Async Context

```python
# Good - async generators
async def stream_results(query: str):
    async with get_connection() as conn:
        async for row in conn.execute(query):
            yield process_row(row)

# Usage
async for result in stream_results(query):
    handle(result)
```

## Type Hints

### Gradual Typing Approach

Type hints encouraged but not enforced. Prioritize:
1. Public API functions and methods
2. Function signatures (args + return)
3. Complex data structures
4. Code that benefits from IDE support

```python
# Good - typed public API
def process_items(items: list[Item], *, strict: bool = False) -> list[Result]:
    """Process items and return results."""
    ...

# OK - internal helper without full typing
def _transform(data):
    # Complex internal logic
    ...
```

### Common Patterns

```python
from typing import TypeVar, Protocol, Callable
from collections.abc import Iterator, Sequence

# Generic types
T = TypeVar("T")

def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None

# Protocols for structural typing
class Processor(Protocol):
    def process(self, data: bytes) -> dict: ...

def run(processor: Processor, data: bytes) -> dict:
    return processor.process(data)

# Callable types
Handler = Callable[[Request], Response]

def with_logging(handler: Handler) -> Handler:
    def wrapper(request: Request) -> Response:
        log(request)
        return handler(request)
    return wrapper

# Union and Optional (use | syntax in 3.10+)
def find_user(user_id: str) -> User | None:
    ...

# TypedDict for structured dicts
from typing import TypedDict

class UserData(TypedDict):
    name: str
    email: str
    age: int | None
```

### Type Narrowing

```python
# Good - type narrowing with isinstance
def process(value: str | int) -> str:
    if isinstance(value, str):
        return value.upper()  # Type narrowed to str
    return str(value)

# Good - assert for narrowing (use sparingly)
def process_user(user: User | None) -> str:
    assert user is not None, "user required"
    return user.name  # Type narrowed to User
```

## Formatting

### Line Length and Indentation

- Maximum 80 characters per line (URLs and long imports excepted)
- Use 4 spaces for indentation; never tabs
- Use implicit line continuation inside parentheses, brackets, braces

```python
# Good - implicit continuation with aligned elements
result = some_function(
    argument_one,
    argument_two,
    argument_three,
)

# Good - hanging indent
result = some_function(
    argument_one, argument_two,
    argument_three,
)

# Bad - backslash continuation
result = some_long_function_name() \
    + another_function()

# Good - parentheses for continuation
result = (
    some_long_function_name()
    + another_function()
)
```

### Whitespace

```python
# Good
spam(ham[1], {eggs: 2})
x = 1
dict["key"] = list[index]
def func(default: str = "value") -> None: ...

# Bad - spaces inside brackets
spam( ham[ 1 ], { eggs: 2 } )

# Bad - space before bracket
spam (ham[1])
dict ["key"]

# Good - break at highest syntactic level
if (
    condition_one
    and condition_two
    and condition_three
):
    do_something()

# Bad - break in middle of expression
if (condition_one and
    condition_two):
    do_something()
```

### Blank Lines

- Two blank lines between top-level definitions (functions, classes)
- One blank line between method definitions
- No blank line after `def` line

## Comprehensions

Use comprehensions for simple transformations. Avoid complex comprehensions.

```python
# Good - simple comprehension
squares = [x * x for x in range(10)]
evens = {x for x in numbers if x % 2 == 0}
mapping = {k: v for k, v in pairs}

# Good - generator for large data
total = sum(x * x for x in range(1000000))

# Bad - multiple for clauses (hard to read)
result = [
    (x, y, z)
    for x in range(5)
    for y in range(5)
    for z in range(5)
    if x != y
]

# Good - use nested loops instead
result = []
for x in range(5):
    for y in range(5):
        for z in range(5):
            if x != y:
                result.append((x, y, z))

# Bad - complex conditions in comprehension
result = [transform(x) for x in data if validate(x) and x.enabled and x.value > 0]

# Good - extract to function or use loop
def should_include(x):
    return validate(x) and x.enabled and x.value > 0

result = [transform(x) for x in data if should_include(x)]
```

## Strings

### Formatting

Use f-strings for interpolation. For logging, use `%` format with pattern strings.

```python
# Good - f-strings for general use
message = f"Processing {item.name} (id={item.id})"

# Good - logging with % patterns (deferred formatting)
logger.info("Processing %s (id=%s)", item.name, item.id)

# Bad - f-strings in logging (always formatted even if not logged)
logger.debug(f"Data: {expensive_repr(data)}")

# Good - join for concatenation in loops
parts = []
for item in items:
    parts.append(str(item))
result = ", ".join(parts)

# Or simply:
result = ", ".join(str(item) for item in items)

# Bad - += concatenation in loop
result = ""
for item in items:
    result += str(item) + ", "  # Creates many intermediate strings
```

### Multiline Strings

```python
# Good - textwrap.dedent for indented multiline
import textwrap

long_string = textwrap.dedent("""\
    First line
    Second line
    Third line
""")

# Good - implicit concatenation
message = (
    "This is a very long message that needs "
    "to be split across multiple lines for "
    "readability purposes."
)
```

## Configuration

### Pydantic Settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYAPP_",
        env_file=".env",
    )

    database_url: str
    api_key: str
    debug: bool = False
    max_workers: int = 4

# Usage
settings = Settings()  # Loads from env vars / .env
```

### CLI Arguments with Typer

```python
import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def main(
    input_file: Annotated[Path, typer.Argument(help="Input file path")],
    output: Annotated[Path, typer.Option("--output", "-o")] = Path("out.json"),
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Process input file and write results."""
    if verbose:
        print(f"Processing {input_file}")

    result = process(input_file)
    output.write_text(json.dumps(result))

if __name__ == "__main__":
    app()
```

## Testing

### Pytest Basics

```python
# tests/test_core.py
import pytest
from mypackage.core import process, ProcessingError

def test_process_valid_input():
    result = process(b"valid data")
    assert result["status"] == "ok"

def test_process_empty_input():
    with pytest.raises(ProcessingError) as exc_info:
        process(b"")
    assert "empty" in str(exc_info.value)
```

### Fixtures

```python
# tests/conftest.py
import pytest
from mypackage import Client, Config

@pytest.fixture
def config() -> Config:
    return Config(api_url="http://test", timeout=1.0)

@pytest.fixture
def client(config: Config) -> Client:
    return Client(config)

# Fixture with cleanup
@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test.db"
    db = create_database(db_path)
    yield db
    db.close()

# Async fixtures
@pytest.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client
```

### Parametrized Tests

```python
@pytest.mark.parametrize(
    "input_data,expected",
    [
        (b"hello", {"word": "hello", "length": 5}),
        (b"world", {"word": "world", "length": 5}),
        (b"", None),
    ],
    ids=["hello", "world", "empty"],
)
def test_parse(input_data: bytes, expected: dict | None):
    result = parse(input_data)
    assert result == expected
```

### Mocking

```python
from unittest.mock import Mock, AsyncMock, patch

def test_with_mock():
    mock_client = Mock()
    mock_client.fetch.return_value = {"data": "test"}

    service = Service(client=mock_client)
    result = service.process()

    mock_client.fetch.assert_called_once()
    assert result == {"data": "test"}

# Async mock
async def test_async_service():
    mock_client = AsyncMock()
    mock_client.fetch.return_value = {"data": "test"}

    service = AsyncService(client=mock_client)
    result = await service.process()

    assert result == {"data": "test"}

# Patching
@patch("mypackage.core.external_api")
def test_with_patch(mock_api):
    mock_api.return_value = "mocked"
    result = function_using_api()
    assert result == "mocked"
```

## CLI Development

### Typer Application Structure

```python
# src/mypackage/cli.py
import typer
from rich.console import Console

app = typer.Typer(help="My CLI application")
console = Console()

@app.command()
def init(
    name: str,
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing"),
) -> None:
    """Initialize a new project."""
    if Path(name).exists() and not force:
        console.print(f"[red]Error:[/red] {name} already exists")
        raise typer.Exit(1)

    create_project(name)
    console.print(f"[green]Created[/green] {name}")

@app.command()
def run(
    config: Path = typer.Option(Path("config.yaml"), "--config", "-c"),
) -> None:
    """Run the application."""
    settings = load_config(config)
    execute(settings)

if __name__ == "__main__":
    app()
```

### Subcommands

```python
# Main app with subcommands
app = typer.Typer()
db_app = typer.Typer(help="Database commands")
app.add_typer(db_app, name="db")

@db_app.command("migrate")
def db_migrate():
    """Run database migrations."""
    ...

@db_app.command("seed")
def db_seed():
    """Seed database with test data."""
    ...

# Usage: mycli db migrate
```

## AI Agents / LangGraph

### State Management

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context: dict
    next_step: str | None

def create_agent() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("process", process_node)
    graph.add_node("decide", decision_node)
    graph.add_node("execute", execute_node)

    graph.add_edge("process", "decide")
    graph.add_conditional_edges(
        "decide",
        route_decision,
        {"execute": "execute", "end": "__end__"},
    )
    graph.add_edge("execute", "process")

    graph.set_entry_point("process")
    return graph.compile()
```

### Tool Definitions

```python
from langchain_core.tools import tool

@tool
def search_database(query: str) -> list[dict]:
    """Search the database for matching records.

    Args:
        query: Search query string

    Returns:
        List of matching records
    """
    return db.search(query)

@tool
async def fetch_url(url: str) -> str:
    """Fetch content from a URL.

    Args:
        url: URL to fetch

    Returns:
        Page content as text
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

### Node Functions

```python
from langchain_core.messages import HumanMessage, AIMessage

async def process_node(state: AgentState) -> AgentState:
    """Process incoming messages and update context."""
    last_message = state["messages"][-1]

    if isinstance(last_message, HumanMessage):
        # Process user input
        context = await analyze_message(last_message.content)
        return {"context": context}

    return {}

def decision_node(state: AgentState) -> AgentState:
    """Decide next action based on context."""
    context = state["context"]

    if context.get("needs_execution"):
        return {"next_step": "execute"}

    return {"next_step": "end"}

def route_decision(state: AgentState) -> str:
    """Route based on decision."""
    return state.get("next_step", "end")
```

## Dependency Injection

### Constructor Injection

```python
# Good - dependencies passed explicitly
class UserService:
    def __init__(self, db: Database, cache: Cache, logger: Logger) -> None:
        self._db = db
        self._cache = cache
        self._logger = logger

    def get_user(self, user_id: str) -> User | None:
        if cached := self._cache.get(user_id):
            return cached

        user = self._db.find_user(user_id)
        if user:
            self._cache.set(user_id, user)
        return user

# Bad - hidden dependencies
class UserService:
    def get_user(self, user_id: str) -> User | None:
        return global_db.find_user(user_id)  # Hidden dependency
```

### Factory Functions

```python
def create_service(config: Config) -> Service:
    """Create service with all dependencies configured."""
    db = Database(config.database_url)
    cache = RedisCache(config.redis_url)
    logger = setup_logger(config.log_level)

    return Service(db=db, cache=cache, logger=logger)

# In tests
def create_test_service() -> Service:
    return Service(
        db=InMemoryDatabase(),
        cache=DictCache(),
        logger=NullLogger(),
    )
```

## Main Entry Point

Always guard module-level code to prevent execution on import:

```python
# Good - guarded entry point
def main() -> None:
    """Application entry point."""
    config = load_config()
    result = process(config)
    print(result)


if __name__ == "__main__":
    main()

# With CLI framework (typer)
import typer

app = typer.Typer()

@app.command()
def main(config: Path = typer.Option(...)) -> None:
    """Process with configuration."""
    ...

if __name__ == "__main__":
    app()
```

## Anti-patterns to Avoid

### Mutable Default Arguments

```python
# Bad - mutable default shared across calls
def append_item(item, items=[]):
    items.append(item)
    return items

# Good - use None and create new list
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Bare Except

```python
# Bad - catches everything including KeyboardInterrupt
try:
    process()
except:
    pass

# Good - catch specific exceptions
try:
    process()
except ProcessingError as e:
    logger.error(f"Processing failed: {e}")
    raise
```

### Star Imports

```python
# Bad - pollutes namespace, unclear origins
from module import *

# Good - explicit imports
from module import SpecificClass, specific_function
```

### Overusing Inheritance

```python
# Bad - deep inheritance hierarchy
class Animal: ...
class Mammal(Animal): ...
class Dog(Mammal): ...
class GermanShepherd(Dog): ...

# Good - composition and protocols
class Animal(Protocol):
    def speak(self) -> str: ...

class Dog:
    def __init__(self, breed: str) -> None:
        self.breed = breed

    def speak(self) -> str:
        return "woof"
```

### God Classes

```python
# Bad - class doing too much
class Application:
    def connect_database(self): ...
    def send_email(self): ...
    def process_payment(self): ...
    def generate_report(self): ...
    def authenticate_user(self): ...

# Good - single responsibility
class DatabaseConnection: ...
class EmailService: ...
class PaymentProcessor: ...
class ReportGenerator: ...
class AuthService: ...
```

### Avoid Power Features

Avoid metaclasses, dynamic attribute access via `__getattr__`, bytecode manipulation, and reflection tricks. Use simpler alternatives.

```python
# Bad - metaclass for simple use case
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# Good - module-level instance or factory function
_instance = None

def get_instance() -> Service:
    global _instance
    if _instance is None:
        _instance = Service()
    return _instance
```

### Avoid staticmethod

Use module-level functions instead of `@staticmethod`:

```python
# Bad - staticmethod
class StringUtils:
    @staticmethod
    def clean(text: str) -> str:
        return text.strip().lower()

# Good - module-level function
def clean_text(text: str) -> str:
    return text.strip().lower()
```

### Boolean Evaluation Pitfalls

```python
# Good - explicit None check
if value is not None:
    process(value)

# Bad - falsy check when 0 or "" are valid
if value:  # Fails for value=0 or value=""
    process(value)

# Good - explicit comparison for sequences
if len(items) == 0:
    return default

# OK - implicit boolean for sequences (when falsy means empty)
if not items:
    return default
```

## Documentation

### Docstrings

```python
def process_data(
    data: bytes,
    *,
    encoding: str = "utf-8",
    strict: bool = False,
) -> dict:
    """Process raw bytes into structured data.

    Args:
        data: Raw bytes to process
        encoding: Text encoding to use
        strict: If True, raise on invalid data

    Returns:
        Parsed data as dictionary

    Raises:
        ProcessingError: If data is invalid and strict=True

    Example:
        >>> result = process_data(b'{"key": "value"}')
        >>> result["key"]
        'value'
    """
    ...
```

### Class Docstrings

```python
class DataProcessor:
    """Process and transform data from various sources.

    This class handles reading data from files or URLs,
    validating the format, and transforming it into
    the required output structure.

    Attributes:
        config: Processor configuration
        stats: Processing statistics

    Example:
        >>> processor = DataProcessor(Config())
        >>> result = processor.process(data)
    """

    def __init__(self, config: Config) -> None:
        """Initialize processor with configuration.

        Args:
            config: Processor configuration object
        """
        self.config = config
        self.stats = Stats()
```

## Tooling Workflow

### uv Commands

```bash
# Create new project
uv init myproject
cd myproject

# Add dependencies
uv add httpx pydantic typer

# Add dev dependencies
uv add --dev pytest pytest-asyncio mypy ruff

# Sync dependencies
uv sync

# Run commands in venv
uv run python script.py
uv run pytest
uv run mypy src/

# Build package
uv build
```

### ruff Commands

```bash
# Check for issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .
```

### mypy Commands

```bash
# Type check
uv run mypy src/

# Strict mode (if desired)
uv run mypy --strict src/

# Generate stub files
uv run stubgen -p mypackage
```

### pytest Commands

```bash
# Run all tests
uv run pytest

# Verbose with output
uv run pytest -v -s

# Run specific test
uv run pytest tests/test_core.py::test_process

# Run with coverage
uv run pytest --cov=mypackage --cov-report=html

# Run async tests (with pytest-asyncio)
uv run pytest  # asyncio_mode = "auto" in pyproject.toml
```

### Pre-commit Workflow

```bash
# 1. Format
uv run ruff format .

# 2. Lint and fix
uv run ruff check --fix .

# 3. Type check
uv run mypy src/

# 4. Run tests
uv run pytest

# 5. All checks pass, ready to commit
```

## Additional Resources

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Typer Documentation](https://typer.tiangolo.com/)

---

**Remember:** These guidelines support writing clear, maintainable Python code. Adapt them to your specific context, but always favor readability, explicitness, and simplicity.
