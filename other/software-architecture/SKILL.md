---
name: software-architecture
version: 1.0.0
author: Param
description: Enforces system design, project structure, dependency management, error handling, testing, and documentation standards at principal-engineer level.
applies-to: .py, .toml, .yaml, .yml, project scaffolding, module design, service design, refactoring
---

## Intent

This skill ensures that every system designed or modified in this session follows the structural discipline of a principal engineer: clear separation of concerns, explicit dependencies, testable units, structured error handling, and documentation that survives team turnover. It rejects the two most common failure modes of software projects — premature complexity and insufficient structure — by applying opinionated rules at the file, module, and system level. Every architectural decision must be recorded; every dependency must be abstractable; every module must have a single, well-named responsibility.

See also: [`python-excellence/SKILL.md`](../python-excellence/SKILL.md) for code style standards, [`api-and-system-design/SKILL.md`](../api-and-system-design/SKILL.md) for API and distributed systems patterns.

---

## 1. Architecture Decision Records (ADRs)

**Every new module, service, or significant design decision must be recorded.** At the top of the primary file for any new module or service, include an ADR comment block:

```python
"""
ADR: UserAuthenticationService
================================
Problem:
    Session token storage was not meeting compliance requirements (SOC2 audit finding).
    Tokens were stored in plaintext in the application database.

Alternatives Considered:
    1. Encrypt tokens in the existing database — rejected: still a single point of compromise.
    2. Use Redis with TTL — rejected: adds infrastructure complexity for a non-performance problem.
    3. Delegate to AWS Cognito — chosen: managed service with compliance certifications built in.

Decision:
    Delegate all session management to AWS Cognito. This service wraps the Cognito SDK
    and abstracts its interface so it can be replaced in tests and future migrations.

Consequences:
    + Compliance requirement satisfied.
    + Auth logic is no longer our responsibility to maintain.
    - Adds an external dependency; requires network availability.
    - Cognito-specific error codes must be mapped to domain errors.
"""
```

**Prefer composition over inheritance.** Every use of class inheritance must be justified in a comment:
```python
# Justified: TransactionError IS-A DomainError; all domain errors share structured logging behavior.
# Composition was considered but rejected because 12+ error types would each need the same boilerplate.
class TransactionError(DomainError): ...
```

**Depend on abstractions. Define interfaces (Protocols) first, then implement.**

```python
# Define the interface first
class UserRepository(Protocol):
    def find_by_id(self, user_id: UUID) -> User | None: ...
    def save(self, user: User) -> None: ...

# Then implement
class PostgresUserRepository:
    def find_by_id(self, user_id: UUID) -> User | None: ...
    def save(self, user: User) -> None: ...
```

**Single Responsibility Principle is non-negotiable.** If a class or function does more than one thing, it must be split. The test: can you describe what it does without using the word "and"?

---

## 2. Project Structure — Enforced Layout

**All non-trivial Python projects must use the `src/` layout with `pyproject.toml`.**

```
project-root/
├── pyproject.toml          # Single source of truth for all tool config
├── README.md
├── src/
│   └── mypackage/
│       ├── __init__.py     # Re-exports only; no logic
│       ├── models/         # Domain models / entities
│       ├── services/       # Business logic
│       ├── repositories/   # Data access layer
│       ├── schemas/        # Pydantic input/output schemas
│       ├── config.py       # pydantic-settings Config class
│       └── utils/          # Pure utility functions (no I/O, no state)
└── tests/
    ├── unit/
    │   └── services/       # Mirrors src/mypackage/services/
    ├── integration/
    └── conftest.py
```

**Never use a flat layout for anything beyond single-file scripts.**

**Separation of concerns is enforced by directory:**
- `models/`: Domain entities and value objects — no I/O, no framework imports
- `services/`: Business logic — depends on repositories via interfaces, not concrete implementations
- `repositories/`: All database and external API interactions — never imported by models
- `schemas/`: Pydantic models for request/response validation — never contain business logic
- `utils/`: Pure functions only — no side effects, no imports from the rest of the package

**Entry points must be thin.** `main.py` or `app.py` wires dependencies only:

```python
# WRONG — business logic in main
def main():
    db = Database()
    users = db.query("SELECT * FROM users WHERE active = true")
    for user in users:
        send_email(user.email, "Hello!")

# CORRECT — main wires, services act
def main():
    db = PostgresDatabase(settings.DATABASE_URL)
    email_client = SendGridEmailClient(settings.SENDGRID_API_KEY)
    user_repo = PostgresUserRepository(db)
    notification_service = NotificationService(user_repo, email_client)
    notification_service.send_activation_reminders()
```

---

## 3. Configuration Management

**All configuration must come from environment variables or a config file. Never hardcode configuration values.**

Always use `pydantic-settings` (preferred) or `dynaconf`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    api_key: str
    debug: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
```

**Never instantiate `Settings()` inside a function or class.** Create a single module-level instance and import it.

**Secrets must never appear in code, config files committed to git, or log output.** Flag any value that looks like a credential and suggest a secrets manager.

---

## 4. Dependency Management

**Always use dependency injection. Avoid global state and module-level singletons for mutable objects.**

```python
# WRONG — global mutable state, untestable
_db_connection = connect(DATABASE_URL)

def get_user(user_id: int) -> User:
    return _db_connection.query(...)

# CORRECT — injected dependency, testable
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def get_user(self, user_id: int) -> User:
        return self._repo.find_by_id(user_id)
```

**Abstract all external dependencies behind interfaces.** Databases, external APIs, file systems, clocks, and random number generators must all be injectable for testing.

**Pin all dependencies with exact versions in production applications.** Use version ranges (`>=`, `~=`) only in library `pyproject.toml` files, never in application deployments.

```toml
# Application (pin exactly)
[project]
dependencies = [
    "fastapi==0.111.0",
    "sqlalchemy==2.0.30",
    "pydantic==2.7.1",
]

# Library (allow ranges)
[project]
dependencies = [
    "pydantic>=2.0,<3.0",
]
```

---

## 5. Error Handling Philosophy

**Never swallow exceptions silently.** `except: pass` and `except Exception: pass` without logging are forbidden.

**Define custom exception hierarchies for domain errors.** Every domain has failure modes; name them.

```python
class DomainError(Exception):
    """Base class for all domain errors. Carries structured context."""
    def __init__(self, message: str, context: dict | None = None) -> None:
        super().__init__(message)
        self.context = context or {}

class UserNotFoundError(DomainError): ...
class InsufficientFundsError(DomainError): ...
class InvalidTransactionStateError(DomainError): ...
```

**At system boundaries, catch, log with full context, and return structured error responses.**

```python
# API handler — boundary
@router.post("/transactions")
async def create_transaction(request: TransactionRequest) -> TransactionResponse:
    try:
        result = transaction_service.create(request.to_domain())
        return TransactionResponse.from_domain(result)
    except InsufficientFundsError as e:
        logger.warning("Insufficient funds", extra={"context": e.context, "user_id": request.user_id})
        raise HTTPException(status_code=422, detail={"code": "INSUFFICIENT_FUNDS", "message": str(e)})
    except DomainError as e:
        logger.error("Unexpected domain error", extra={"context": e.context}, exc_info=True)
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR"})
```

**Deep in business logic, raise specific exceptions. Never raise generic `Exception`.**

```python
# WRONG
raise Exception("Something went wrong")

# CORRECT
raise InsufficientFundsError(
    f"Account {account_id} has balance {balance}, required {amount}",
    context={"account_id": str(account_id), "balance": balance, "required": amount}
)
```

---

## 6. Logging and Observability

**Never use `print()` in production code.** Use the standard `logging` module or a structured logging library (`structlog`).

**Use structured logging in JSON format for production; human-readable for development.**

```python
import structlog

logger = structlog.get_logger()

# Every significant event carries context
logger.info(
    "model_prediction_completed",
    model_id=model_id,
    input_shape=X.shape,
    output_shape=predictions.shape,
    latency_ms=elapsed * 1000,
    request_id=request_id,
)
```

**Every service must emit these fields on every request:**
- `request_id`: unique identifier, propagated from the caller
- `latency_ms`: end-to-end processing time
- `input_shape` / `input_size`: shape or byte size of the input
- `output_shape` / `output_size`: shape or byte size of the output
- `error_context`: full exception details including type, message, and traceback on errors

**Log at the correct level — always:**
- `DEBUG`: internal state, intermediate values, branch taken — verbose, for development only
- `INFO`: significant events that confirm correct behavior (request received, job completed, model loaded)
- `WARNING`: degraded but recoverable state (retry attempted, fallback used, cache miss rate high)
- `ERROR`: failures that require investigation (exception caught at boundary, downstream unavailable)
- `CRITICAL`: system integrity violations (data corruption detected, security event)

---

## 7. Testing Standards

**Follow the test pyramid:** unit tests (many, fast, no I/O) > integration tests (fewer, slower) > end-to-end tests (minimal, slowest).

**Every public function and method must have at least one test.** No exceptions for "obviously correct" code.

**Use `pytest` with fixtures. Never use `unittest.TestCase` for new code.**

```python
# tests/unit/services/test_transaction_service.py

import pytest
from unittest.mock import MagicMock
from mypackage.services.transaction_service import TransactionService
from mypackage.models import Transaction, Account
from mypackage.exceptions import InsufficientFundsError

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return TransactionService(repository=mock_repo)

def test_create_transaction_raises_on_insufficient_funds(service, mock_repo):
    mock_repo.find_account.return_value = Account(id=1, balance=50.0)
    with pytest.raises(InsufficientFundsError):
        service.create_transaction(account_id=1, amount=100.0)
```

**Mock at the boundary: mock external services, not internal logic.** If you find yourself mocking a service class to test another service class, that is a design smell — the dependency should be injected via an interface.

**Test file structure must mirror source structure:**
```
src/mypackage/services/transaction_service.py
→ tests/unit/services/test_transaction_service.py
```

**Enforce coverage thresholds in `pyproject.toml`:**
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-fail-under=80"

[tool.coverage.report]
fail_under = 80
exclude_lines = ["if TYPE_CHECKING:", "pragma: no cover"]
```

**Minimum 80% overall coverage. Minimum 90% for core business logic (services, models).**

---

## 8. Documentation Standards

**Every module must have a one-paragraph module docstring** explaining its purpose, its primary abstraction, and how it fits into the larger system.

**Every public class and function must have a Google-style docstring:**

```python
def calculate_churn_probability(
    user_features: pd.DataFrame,
    model: ChurnModel,
    threshold: float = 0.5,
) -> pd.Series:
    """Calculate churn probability for a batch of users.

    Runs the churn model on the provided feature set and returns
    calibrated probabilities. Does not apply the decision threshold —
    callers are responsible for converting to labels if needed.

    Args:
        user_features: DataFrame with columns matching the model's
            expected feature schema. See FeatureRegistry.CHURN_FEATURES.
        model: Trained ChurnModel instance. Must include preprocessing pipeline.
        threshold: Not applied here — included for documentation of the
            downstream convention (default 0.5 for binary label conversion).

    Returns:
        Series of float values in [0, 1], indexed by user_id.

    Raises:
        FeatureValidationError: If required features are missing or have
            unexpected dtypes.
        ModelNotLoadedError: If the model artifact has not been loaded.

    Example:
        >>> probs = calculate_churn_probability(features_df, churn_model)
        >>> high_risk = probs[probs > 0.7].index.tolist()
    """
```

**README must contain all of:**
1. What the project does (2–3 sentences, non-technical summary)
2. Architecture overview (diagram or bulleted description of major components)
3. Installation instructions (exact commands, tested)
4. How to run (development and production modes)
5. How to test (exact command, expected output)
6. Environment variables reference (name, purpose, example value, required/optional)
7. Contributing guide or link to one
