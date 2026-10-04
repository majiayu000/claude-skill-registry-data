---
name: python-architecture
description: Python architecture patterns including KISS, SRP, separation of concerns, composition over inheritance, dependency injection, project structure, module organization, and public API design. Use when designing new components, organizing projects, planning directory layouts, refactoring complex code, or deciding between inheritance and composition.
---

# Python Architecture

Build maintainable Python systems with clear design principles and well-organized project structure. Good architecture makes code easy to understand, test, and change.

## When to Use This Skill

- Designing new components or services
- Refactoring complex or tangled code
- Deciding whether to create an abstraction
- Choosing between inheritance and composition
- Evaluating code complexity and coupling
- Planning modular architectures
- Starting a new Python project from scratch
- Reorganizing an existing codebase for clarity
- Defining module public APIs with `__all__`
- Deciding between flat and nested directory structures
- Determining test file placement strategies

## Core Concepts

**KISS** — Choose the simplest solution that works. Complexity must be justified.

**SRP** — Each unit has one reason to change. Separate concerns into focused components.

**Composition** — Build behavior by combining objects, not extending classes.

**Rule of Three** — Wait until you have three instances before abstracting.

**Flat Hierarchies** — Prefer shallow directory structures. Add depth only for genuine sub-domains.

**Explicit Interfaces** — Define what's public with `__all__`. Everything else is internal.

---

## Design Principles

### Pattern 1: KISS — Keep It Simple

Before adding complexity, ask: does a simpler solution work?

```python
# Over-engineered: Factory with registration
class OutputFormatterFactory:
    _formatters: dict[str, type[Formatter]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(formatter_cls):
            cls._formatters[name] = formatter_cls
            return formatter_cls
        return decorator

    @classmethod
    def create(cls, name: str) -> Formatter:
        return cls._formatters[name]()

@OutputFormatterFactory.register("json")
class JsonFormatter(Formatter): ...

# Simple: Just use a dictionary
FORMATTERS = {
    "json": JsonFormatter,
    "csv": CsvFormatter,
    "xml": XmlFormatter,
}

def get_formatter(name: str) -> Formatter:
    if name not in FORMATTERS:
        raise ValueError(f"Unknown format: {name}")
    return FORMATTERS[name]()
```

The factory pattern adds code without adding value here. Save patterns for when they solve real problems.

### Pattern 2: Single Responsibility Principle

Each class or function should have one reason to change.

```python
# BAD: Handler does everything
class UserHandler:
    async def create_user(self, request: Request) -> Response:
        data = await request.json()
        if not data.get("email"):
            return Response({"error": "email required"}, status=400)
        user = await db.execute("INSERT INTO users ...", data["email"], data["name"])
        return Response({"id": user.id, "email": user.email}, status=201)

# GOOD: Separated concerns
class UserService:
    """Business logic only."""
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def create_user(self, data: CreateUserInput) -> User:
        user = User(email=data.email, name=data.name)
        return await self._repo.save(user)

class UserHandler:
    """HTTP concerns only."""
    def __init__(self, service: UserService) -> None:
        self._service = service

    async def create_user(self, request: Request) -> Response:
        data = CreateUserInput(**(await request.json()))
        user = await self._service.create_user(data)
        return Response(user.to_dict(), status=201)
```

Now HTTP changes don't affect business logic, and vice versa.

### Pattern 3: Separation of Concerns — Layered Architecture

Organize code into distinct layers. Each layer depends only on layers below it.

```
┌─────────────────────────────────────────────────────┐
│  API Layer (handlers)                                │
│  - Parse requests, call services, format responses   │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│  Service Layer (business logic)                      │
│  - Domain rules and validation                       │
│  - Orchestrate operations                            │
│  - Pure functions where possible                     │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│  Repository Layer (data access)                      │
│  - SQL queries, external API calls, cache ops        │
└─────────────────────────────────────────────────────┘
```

```python
# Repository: Data access only
class UserRepository:
    async def get_by_id(self, user_id: str) -> User | None:
        row = await self._db.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        return User(**row) if row else None

# Service: Business logic only
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def get_user(self, user_id: str) -> User:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

# Handler: HTTP concerns only
@app.get("/users/{user_id}")
async def get_user(user_id: str) -> UserResponse:
    user = await user_service.get_user(user_id)
    return UserResponse.from_user(user)
```

**Directory layout for layered architecture:**

```
myapp/
├── api/           # HTTP handlers, request/response schemas
│   ├── routes/
│   └── middleware/
├── services/      # Business logic
├── repositories/  # Data access
├── models/        # Domain entities
├── schemas/       # API schemas (Pydantic)
└── config/        # Configuration
```

### Pattern 4: Composition Over Inheritance

Build behavior by combining objects rather than inheriting.

```python
# Inheritance: Rigid and hard to test
class EmailNotificationService(NotificationService):
    def __init__(self):
        super().__init__()
        self._smtp = SmtpClient()  # Hard to mock

    def notify(self, user: User, message: str) -> None:
        self._smtp.send(user.email, message)

# Composition: Flexible and testable
class NotificationService:
    def __init__(
        self,
        email_sender: EmailSender,
        sms_sender: SmsSender | None = None,
        push_sender: PushSender | None = None,
    ) -> None:
        self._email = email_sender
        self._sms = sms_sender
        self._push = push_sender

    async def notify(
        self,
        user: User,
        message: str,
        channels: set[str] | None = None,
    ) -> None:
        channels = channels or {"email"}
        if "email" in channels:
            await self._email.send(user.email, message)
        if "sms" in channels and self._sms and user.phone:
            await self._sms.send(user.phone, message)
        if "push" in channels and self._push and user.device_token:
            await self._push.send(user.device_token, message)

# Easy to test with fakes
service = NotificationService(
    email_sender=FakeEmailSender(),
    sms_sender=FakeSmsSender(),
)
```

### Pattern 5: Rule of Three

Wait until you have three instances before abstracting.

```python
# Two similar functions? Don't abstract yet
def process_orders(orders: list[Order]) -> list[Result]:
    results = []
    for order in orders:
        validated = validate_order(order)
        result = process_validated_order(validated)
        results.append(result)
    return results

def process_returns(returns: list[Return]) -> list[Result]:
    results = []
    for ret in returns:
        validated = validate_return(ret)
        result = process_validated_return(validated)
        results.append(result)
    return results

# These look similar but have different validation, processing, and errors.
# Duplication is often better than the wrong abstraction.
# Wait for a third case before deciding if there's a real pattern.
```

### Pattern 6: Function Size Guidelines

Keep functions focused. Extract when a function:
- Exceeds ~50 lines
- Serves multiple distinct purposes
- Has deeply nested logic (3+ levels)

```python
# Too long, multiple concerns mixed
def process_order(order: Order) -> Result:
    # 50 lines of validation...
    # 30 lines of inventory check...
    # 40 lines of payment processing...
    # 20 lines of notification...
    pass

# Better: Composed from focused functions
def process_order(order: Order) -> Result:
    """Process a customer order through the complete workflow."""
    validate_order(order)
    reserve_inventory(order)
    payment_result = charge_payment(order)
    send_confirmation(order, payment_result)
    return Result(success=True, order_id=order.id)
```

### Pattern 7: Dependency Injection

Pass dependencies through constructors for testability.

```python
from typing import Protocol

class Cache(Protocol):
    async def get(self, key: str) -> str | None: ...
    async def set(self, key: str, value: str, ttl: int) -> None: ...

class Logger(Protocol):
    def info(self, msg: str, **kwargs) -> None: ...
    def error(self, msg: str, **kwargs) -> None: ...

class UserService:
    def __init__(
        self,
        repository: UserRepository,
        cache: Cache,
        logger: Logger,
    ) -> None:
        self._repo = repository
        self._cache = cache
        self._logger = logger

    async def get_user(self, user_id: str) -> User:
        cached = await self._cache.get(f"user:{user_id}")
        if cached:
            self._logger.info("Cache hit", user_id=user_id)
            return User.from_json(cached)
        user = await self._repo.get_by_id(user_id)
        if user:
            await self._cache.set(f"user:{user_id}", user.to_json(), ttl=300)
        return user

# Production
service = UserService(
    repository=PostgresUserRepository(db),
    cache=RedisCache(redis),
    logger=StructlogLogger(),
)

# Testing
service = UserService(
    repository=InMemoryUserRepository(),
    cache=FakeCache(),
    logger=NullLogger(),
)
```

---

## Project Organization

### Pattern 8: One Concept Per File

Each file should focus on a single concept. Consider splitting when a file:
- Handles multiple unrelated responsibilities
- Grows beyond ~300-500 lines
- Contains classes that change for different reasons

```python
# Good: Focused files
# user_service.py    - User business logic
# user_repository.py - User data access
# user_models.py     - User data structures

# Avoid: Kitchen sink files
# user.py            - Contains service, repository, models, utilities...
```

### Pattern 9: Explicit Public APIs with `__all__`

Define the public interface for every package. Unlisted members are internal implementation details.

```python
# mypackage/services/__init__.py
from .user_service import UserService
from .order_service import OrderService
from .exceptions import ServiceError, ValidationError

__all__ = [
    "UserService",
    "OrderService",
    "ServiceError",
    "ValidationError",
]
# Internal helpers remain private by omission

# mypackage/__init__.py — top-level package interface
from .core import MainClass, HelperClass
from .exceptions import PackageError, ConfigError
from .config import Settings

__all__ = ["MainClass", "HelperClass", "PackageError", "ConfigError", "Settings"]
__version__ = "1.0.0"

# Consumers import cleanly:
from mypackage import MainClass, Settings
```

### Pattern 10: Flat Directory Structure

Prefer minimal nesting. Deep hierarchies make imports verbose and navigation difficult.

```
# Preferred: Flat structure
project/
├── api/
│   ├── routes.py
│   └── middleware.py
├── services/
│   ├── user_service.py
│   └── order_service.py
├── models/
│   ├── user.py
│   └── order.py
└── utils/
    └── validation.py

# Avoid: Deep nesting
project/core/internal/services/impl/user/
```

Add sub-packages only when there's a genuine sub-domain requiring isolation.

### Pattern 11: Test File Organization

Choose one approach and apply it consistently.

**Option A: Colocated Tests** — Tests live next to the code they verify.
```
src/
├── user_service.py
├── test_user_service.py
├── order_service.py
└── test_order_service.py
```

**Option B: Parallel Test Directory** — Standard for larger projects.
```
src/
├── services/
│   ├── user_service.py
│   └── order_service.py
tests/
├── services/
│   ├── test_user_service.py
│   └── test_order_service.py
```

### Pattern 12: Domain-Driven Structure

For complex applications, organize by business domain rather than technical layer.

```
ecommerce/
├── users/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
├── orders/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
└── shared/
    ├── database.py
    └── exceptions.py
```

### Pattern 13: File and Module Naming

```python
# snake_case for all file and module names
user_repository.py   # Good
usr_repo.py          # Avoid abbreviations

# Match class names to file names
# UserService lives in user_service.py
# OrderRepository lives in order_repository.py

# Absolute imports (not relative)
from myproject.services import UserService  # Preferred
from ..services import UserService          # Avoid — breaks when modules move
```

---

## Best Practices Summary

**Design**
1. **Keep it simple** — Choose the simplest solution that works
2. **Single responsibility** — Each unit has one reason to change
3. **Separate concerns** — Distinct layers, dependencies flow downward
4. **Compose, don't inherit** — Combine objects for flexibility and testability
5. **Rule of three** — Wait before abstracting; duplication beats wrong abstraction
6. **Keep functions small** — ~50 lines max, one purpose
7. **Inject dependencies** — Constructor injection for testability
8. **Explicit over clever** — Readable code beats elegant code

**Project Structure**
9. **One concept per file** — Split at ~300-500 lines
10. **Define `__all__` explicitly** — Make public interfaces clear
11. **Prefer flat structures** — Add depth only for genuine sub-domains
12. **Use absolute imports** — More reliable and refactor-safe
13. **Be consistent** — Apply naming and organization uniformly
14. **Match names to content** — File names should describe their purpose
