---
name: python
description: Modern Python coding standards using uv — full type annotations, Pydantic v2 runtime validation, Ruff linting/formatting, mypy strict mode, and loguru structured logging.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# python

Modern Python coding standards using **uv** as the package and project manager.  
Implements all mandatory rules from [`code-quality`](../../code-quality/SKILL.md): full type safety, typed errors, immutability, and clean naming.

## Instructions

Apply these rules to every Python project (scripts, APIs, libraries, CLIs).

---

## Guidelines

### Project Setup — uv

[uv](https://docs.astral.sh/uv/) is the standard tool for dependency management, virtual environments, and script running.

#### Bootstrap a new project

```bash
# Create a new project (generates pyproject.toml, .python-version, src/ layout)
uv init my-project
cd my-project

# Add runtime dependencies
uv add pydantic fastapi loguru

# Add dev/test dependencies
uv add --dev mypy ruff pytest pytest-cov

# Run a script inside the managed venv
uv run python src/my_project/main.py

# Run tests
uv run pytest

# Sync the venv to exactly match uv.lock
uv sync

# Update all dependencies to latest compatible versions
uv lock --upgrade
```

#### `pyproject.toml` baseline

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
    "loguru>=0.7",
]

[tool.uv]
dev-dependencies = [
    "mypy>=1.9",
    "ruff>=0.4",
    "pytest>=8.0",
    "pytest-cov>=5.0",
]

[tool.mypy]
strict = true
python_version = "3.12"
plugins = ["pydantic.mypy"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E", "W",   # pycodestyle
    "F",        # pyflakes
    "I",        # isort
    "UP",       # pyupgrade
    "B",        # flake8-bugbear
    "SIM",      # flake8-simplify
    "ANN",      # flake8-annotations (enforce type hints)
    "RUF",      # Ruff-specific rules
]
ignore = ["ANN101", "ANN102"]  # no annotation required for self/cls

[tool.ruff.lint.isort]
force-sort-within-sections = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts   = "--cov=src --cov-report=term-missing"
```

### Type Safety

#### Full annotations on every function and variable

```python
# ❌ no annotations — mypy cannot check this
def get_user(user_id):
    return db.query(user_id)

# ✅ all parameters, return types, and class fields annotated
def get_user(user_id: str) -> User | None:
    return db.query(user_id)
```

#### Modern type syntax (Python 3.10+)

```python
# Use | instead of Union, X | None instead of Optional
def find(name: str) -> User | None: ...

# Use built-in generics (no need to import from typing)
def process(items: list[str]) -> dict[str, int]: ...

# TypeAlias for readability
type UserId = str          # Python 3.12+ type statement
type Matrix = list[list[float]]
```

#### Pydantic v2 for every external boundary

Validate all data that crosses a trust boundary (HTTP request, file, env vars, config):

```python
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from pydantic import ConfigDict

class CreateUserRequest(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    email:    EmailStr
    age:      int
    role:     Literal['admin', 'member', 'guest']

    @field_validator('age')
    @classmethod
    def age_must_be_positive(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError(f'Age must be between 0 and 150, got {v}')
        return v
```

#### Validated environment variables with pydantic-settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', frozen=True)

    database_url: str
    port:         int = 8000
    environment:  Literal['development', 'test', 'production']
    jwt_secret:   str

    @field_validator('jwt_secret')
    @classmethod
    def secret_must_be_long_enough(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError('JWT_SECRET must be at least 32 characters')
        return v

# Module-level singleton — validated at import time (fail fast)
settings = Settings()
```

#### TypedDict and Protocol for structural typing

```python
from typing import Protocol, TypedDict, runtime_checkable

# TypedDict for plain data structures (no behaviour)
class UserRecord(TypedDict):
    id:    str
    email: str
    role:  str

# Protocol for duck-typed interfaces (no inheritance required)
@runtime_checkable
class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None: ...

# Any class with a matching `send` method satisfies Notifier
class EmailNotifier:
    def send(self, recipient: str, message: str) -> None:
        ...  # implementation

class SmsNotifier:
    def send(self, recipient: str, message: str) -> None:
        ...  # implementation
```

#### dataclasses for immutable value objects

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)   # frozen=True → immutable; slots=True → fast
class Money:
    amount:   int      # in cents
    currency: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f'Amount cannot be negative: {self.amount}')
        if len(self.currency) != 3:
            raise ValueError(f'Currency must be ISO 4217 (3 chars): {self.currency}')

    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError('Cannot add different currencies')
        return Money(self.amount + other.amount, self.currency)
```

### Error Handling

#### Typed domain exceptions — never raise bare `Exception`

```python
# ❌ caller cannot distinguish error types
raise Exception('user not found')

# ✅ domain-specific, typed, catchable
class DomainError(Exception):
    """Base class for all domain errors."""

class UserNotFoundError(DomainError):
    def __init__(self, user_id: str) -> None:
        super().__init__(f'User not found: {user_id}')
        self.user_id = user_id

class InsufficientFundsError(DomainError):
    def __init__(self, available: int, required: int) -> None:
        super().__init__(
            f'Insufficient funds: available={available}, required={required}'
        )
        self.available = available
        self.required  = required
```

#### Never silently swallow exceptions

```python
# ❌ hides bugs — caller has no idea something went wrong
try:
    result = process(data)
except Exception:
    pass

# ✅ always handle or re-raise with added context
try:
    result = process(data)
except ValidationError as exc:
    logger.error('Validation failed', user_id=user_id, error=str(exc))
    raise UserInputError('Invalid data provided') from exc
```

#### Structured logging with loguru

```python
from loguru import logger

# Configure once at application entry point
logger.remove()  # remove default handler
logger.add(
    sys.stderr,
    format='{time:ISO8601} | {level} | {name}:{function}:{line} | {message}',
    level='INFO',
    serialize=True,   # JSON output for structured log aggregators
)

# Log with context — always include relevant IDs
logger.info('User created', user_id=user.id, email=user.email)
logger.error('Payment failed', order_id=order.id, error=str(exc))
```

### Immutability

- Use `frozen=True` on `dataclass` and Pydantic models
- Prefer `tuple` over `list` for fixed collections
- Never mutate function parameters — clone if modification is needed
- Use `Final` for module-level constants

```python
from typing import Final

MAX_RETRIES: Final = 3
DEFAULT_TIMEOUT_SECONDS: Final = 30.0

# Immutable collection
SUPPORTED_CURRENCIES: Final = frozenset({'USD', 'EUR', 'GBP', 'JPY'})
```

### Naming Conventions

| Entity | Convention | Example |
|--------|-----------|---------|
| Variable / function | `snake_case` | `get_user_by_email` |
| Class | `PascalCase` | `UserService`, `CreateUserRequest` |
| Module / file | `snake_case` | `user_service.py` |
| Package / directory | `snake_case` | `user_management/` |
| Constant (module-level) | `SCREAMING_SNAKE_CASE` | `MAX_PAGE_SIZE` |
| Type alias | `PascalCase` | `UserId`, `Matrix` |
| Boolean | `is_/has_/can_` prefix | `is_authenticated`, `has_permission` |
| Private method/attribute | `_single_underscore` | `_validate_input` |

- Avoid single-letter names except loop indices (`i`, `j`) and math notation (`x`, `y`, `n`)
- Names must express intent: `get_user_by_email()` not `get_user()` or `fetch()`

### Code Organisation

```
my-project/
  pyproject.toml
  uv.lock
  .python-version          ← pinned Python version (e.g. 3.12)
  src/
    my_project/
      __init__.py
      domain/              ← pure business logic; no HTTP/DB imports
        user.py            ← entity, value objects, domain errors
        user_service.py
      infra/               ← adapters: DB, HTTP clients, queues
        db.py
        email_client.py
      api/                 ← HTTP layer: routes, schemas, middleware
        routes.py
        schemas.py
      lib/                 ← shared utilities (result, logger, settings)
        settings.py
        logger.py
      main.py
  tests/
    unit/
    integration/
```

- **`domain/` must not import from `infra/` or `api/`**
- One class per file for complex domain objects; small helpers may be grouped
- Keep files ≤ 300 lines; functions ≤ 30 lines

### Documentation

```python
def find_user_by_email(email: str) -> User | None:
    """Find a user by their email address.

    Args:
        email: A valid, normalised email address.

    Returns:
        The matching ``User`` instance, or ``None`` if not found.

    Raises:
        DatabaseError: When the database connection fails.
    """
```

- All public functions, classes, and methods must have Google-style or NumPy-style docstrings
- Use `Args:`, `Returns:`, `Raises:` sections
- No commented-out code in committed files

### Tooling Baseline

| Tool | Purpose | Run with |
|------|---------|---------|
| **uv** | Package / venv management | `uv add`, `uv run`, `uv sync` |
| **mypy** `--strict` | Static type checking | `uv run mypy src` |
| **Ruff** | Linting + formatting | `uv run ruff check src`, `uv run ruff format src` |
| **Pydantic v2** | Runtime validation | Schema classes |
| **pydantic-settings** | Env var validation | `Settings()` at boot |
| **loguru** | Structured logging | `from loguru import logger` |
| **pytest** + **pytest-cov** | Testing | `uv run pytest` |

---

## Examples

### Fully typed service with domain errors

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from loguru import logger
from pydantic import BaseModel, EmailStr, ConfigDict

# --- Constants ---
MIN_AGE: Final = 0
MAX_AGE: Final = 150

# --- Value objects ---
@dataclass(frozen=True, slots=True)
class UserId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError('UserId cannot be empty')

# --- Domain errors ---
class UserAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f'User already exists: {email}')
        self.email = email

# --- Pydantic schema (API boundary) ---
class CreateUserRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr
    age:   int
    role:  str

# --- Domain entity ---
@dataclass(frozen=True, slots=True)
class User:
    id:    UserId
    email: str
    age:   int
    role:  str

# --- Repository protocol ---
from typing import Protocol

class UserRepository(Protocol):
    def find_by_email(self, email: str) -> User | None: ...
    def save(self, user: User) -> None: ...

# --- Service ---
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def create(self, request: CreateUserRequest) -> User:
        """Create a new user.

        Args:
            request: Validated user creation payload.

        Returns:
            The newly created ``User``.

        Raises:
            UserAlreadyExistsError: If the email is already registered.
        """
        existing = self._repo.find_by_email(request.email)
        if existing is not None:
            raise UserAlreadyExistsError(request.email)

        user = User(
            id=UserId(generate_uuid()),
            email=request.email,
            age=request.age,
            role=request.role,
        )
        self._repo.save(user)
        logger.info('User created', user_id=user.id.value, email=user.email)
        return user
```

### FastAPI route with Pydantic validation

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, ConfigDict

app = FastAPI()

class CreateUserRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    email: EmailStr
    age:   int
    role:  str

class UserResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id:    str
    email: str
    role:  str

@app.post('/users', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: CreateUserRequest) -> UserResponse:
    """Create a new user account."""
    try:
        user = user_service.create(body)
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={'code': 'USER_ALREADY_EXISTS', 'email': exc.email},
        ) from exc
    return UserResponse(id=user.id.value, email=user.email, role=user.role)
```

## References

- [uv documentation](https://docs.astral.sh/uv/)
- [Pydantic v2 documentation](https://docs.pydantic.dev/)
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [mypy strict mode](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-strict)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [loguru documentation](https://loguru.readthedocs.io/)
- [PEP 695 — Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [Python typing — Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [code-quality skill](../../code-quality/SKILL.md)
