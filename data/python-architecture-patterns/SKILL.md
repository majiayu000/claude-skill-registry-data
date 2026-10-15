---
name: python-architecture-patterns
description: Use when planning, implementing, or reviewing code for any Python project — designing architecture, writing classes or functions, organizing business logic, or reviewing pull requests. Not for throwaway snippets or one-off scripts. Prevents coupling, god objects, Demeter violations, and leaky abstractions
---

# Python Architecture Patterns

## Overview

**Architecture determines testability.** If your code requires deep mock chains or real databases to test, the design needs work.

**Proven OOP principles are non-negotiable.** SOLID, Law of Demeter, Composition over Inheritance, and Separation of Concerns are not academic theory — they are battle-tested engineering constraints. Treat violations as bugs, not style preferences. When you spot a violation during planning, implementation, or review, flag it and fix it.

**Core principles:**
- Depend on abstractions (Protocol, ABC), not concrete implementations
- Separate domain logic from infrastructure
- Use classes for state, functions for stateless logic
- Type-annotate everything, use dataclasses for data
- Obey the Law of Demeter — talk to friends, not strangers

## When to Use

Load this skill whenever you **plan, implement, or review** code for a Python project:
- Planning an implementation — designing modules, services, or class hierarchies
- Writing classes or functions that interact with external services (DB, API, cache)
- Organizing business logic in models, services, or controllers
- Reviewing pull requests or completed code for architectural quality
- Refactoring existing code with mixed concerns

**Don't use for:** pure algorithms, data processing with no external dependencies, throwaway scripts or one-off snippets.

## Quick Reference

| Smell | Detection | Fix |
|-------|-----------|-----|
| **Hardcoded Side Effects in `__init__`** | Constructor opens DB, creates HTTP client | Dependency Injection — pass dependencies in |
| **Global State** | Module-level DB/cache clients | Inject dependencies, use factories |
| **Leaky Abstractions** | SQL queries, HTTP codes in business logic | Repository Pattern, Adapter Pattern |
| **Fat Model/Controller** | Model/view has 10+ methods, mixed concerns | Service Layer, separate domain objects |
| **God Object** | One class referenced everywhere | Single Responsibility — split by concern |
| **No Abstraction Layer** | Direct library calls (boto3, requests) everywhere | Protocol/ABC for interfaces |
| **Law of Demeter Violation** | `order.customer.address.city` chain traversals | Expose a method on the direct collaborator |
| **Deep Mock Chains** | `mock.return_value.foo.return_value.bar` | Fix architecture — test real logic with fake deps |
| **Stateless Class** | Class with no attributes, only methods | Use plain functions instead |
| **Deep Inheritance** | 3+ levels of class hierarchy | Composition — objects contain other objects |
| **Manual `__init__` boilerplate** | `self.x = x; self.y = y` for data containers | Use `@dataclass` |
| **Missing Type Hints** | `def process(data):` with no annotations | Add parameter and return type annotations |

## Python Idioms

### 1. Type Hints — Always

Every function signature needs parameter and return type annotations.

```python
# ❌ def process(data): ...
# ✅
def process(data: dict[str, Any]) -> ProcessedResult: ...
def find_users(filters: UserFilters, limit: int = 100) -> list[User]: ...
```

Use type aliases for complex types: `type Permissions = dict[UserId, set[Role]]`

### 2. dataclasses for Data Objects

Use `@dataclass` for classes that primarily hold data. Use `frozen=True` for immutable value objects. Don't use dataclass for service classes whose purpose is behavior with injected dependencies.

```python
# ❌ Manual __init__ with self.x = x boilerplate
# ✅
@dataclass
class User:
    id: str
    email: str
    name: str
    active: bool = True
```

### 3. Functions vs. Classes — Use Classes Only for State

If a class has no attributes and only methods, use functions. A class needs meaningful state (including injected dependencies).

```python
# ❌ Stateless class used as namespace
class MathHelper:
    def calculate_tax(self, amount: float, rate: float) -> float:
        return amount * rate

# ✅ Plain function
def calculate_tax(amount: float, rate: float) -> float:
    return amount * rate

# ✅ Class with state (injected dependency)
class TaxService:
    def __init__(self, tax_rates: TaxRateRepository):
        self.tax_rates = tax_rates

    def calculate(self, amount: float, country: str) -> float:
        return amount * self.tax_rates.get_rate(country)
```

**Rule of thumb:** If `self` is only used to call other methods (never to access attributes), you have functions pretending to be a class.

### 4. Composition Over Inheritance

Deep inheritance hierarchies make code rigid. Prefer composing objects from smaller, focused components via Protocol-based interfaces.

```python
# ❌ Animal → Mammal → Pet → Dog (4 levels, breaks when you need a swimming dog)
# ✅ Compose capabilities
class Speaker(Protocol):
    def speak(self) -> str: ...

@dataclass
class Animal:
    name: str
    owner: str | None = None
    voice: Speaker | None = None  # Compose, don't inherit
```

**When inheritance IS appropriate:** framework base classes (Django Model), shallow 1-level hierarchies with genuine is-a relationships, ABCs defining interfaces.

### 5. Law of Demeter — Talk to Friends, Not Strangers

An object should only call methods on: (1) itself, (2) its own attributes, (3) objects it received as parameters, (4) objects it created. Never reach through one object to access another's internals.

```python
# ❌ Reaching through objects — coupled to entire chain
city = order.customer.address.city
if order.customer.membership.tier == "gold": ...

# ✅ Ask the direct collaborator — each object exposes behavior, not structure
@dataclass
class Customer:
    address: Address
    membership: Membership

    def is_gold_member(self) -> bool:
        return self.membership.tier == "gold"

    def region(self) -> str:
        return self.address.region

@dataclass
class Order:
    customer: Customer
    total: Decimal

    def regional_discount(self) -> Decimal:
        if self.customer.is_gold_member():
            return get_discount(self.customer.region(), self.total)
        return Decimal("0")
```

**Detection:** More than one dot reaching into data (not fluent/builder APIs) is likely a violation. `order.customer.address.city` — three dots, three coupling points.

### 6. Encapsulation Conventions

- `_name`: Internal — other modules and classes should not access this.
- `__name`: Name-mangled — use sparingly, mainly to avoid collisions in inheritance.
- No underscore: Public API.
- Use `__all__` in modules to declare the public API.

Treat the leading underscore as a contract — don't access `_internal` members from outside.

## Architecture Patterns

### 1. Dependency Injection (Not Hardcoded Side Effects)

```python
# ❌ Side effects in constructor — impossible to test without real DB/API
class WeatherService:
    def __init__(self, api_key: str):
        self.db = psycopg2.connect(host='localhost', database='weather')
        self.http = requests.Session()

# ✅ Dependencies injected via Protocol — test with fakes, swap implementations freely
class WeatherRepository(Protocol):
    def get_cached(self, city: str) -> dict | None: ...
    def save(self, city: str, data: dict) -> None: ...

class WeatherService:
    def __init__(self, repository: WeatherRepository, http_client: HTTPClient, api_key: str):
        self.repository = repository
        self.http_client = http_client
        self.api_key = api_key
```

### 2. Repository Pattern (Not Leaky Abstractions)

Business logic should not contain SQL, Redis commands, or HTTP status codes. Hide infrastructure behind a Protocol.

```python
# ❌ SQL and Redis details in business logic
result = db.query("SELECT * FROM products")
cache.setex(cache_key, 300, json.dumps(result))

# ✅ Business logic depends on Protocol, not Redis/SQL
class ProductRepository(Protocol):
    def get_all(self) -> list[Product]: ...

def get_products(repo: ProductRepository) -> list[Product]:
    return repo.get_all()
```

### 3. Service Layer (Not Fat Models/Controllers)

Domain objects hold data and core invariants. Services orchestrate operations with injected dependencies. Split by concern — don't put auth, reset, profile, and billing in one class.

```python
# ❌ User class with login(), logout(), reset_password(), update_profile(), ... (God Object)
# ✅ Separate domain object + focused services
@dataclass
class User:
    id: str
    email: str
    password_hash: str

    def verify_password(self, password: str) -> bool:
        return check_password(password, self.password_hash)

class AuthenticationService:
    def __init__(self, user_repo: UserRepository, session_mgr: SessionManager):
        self.user_repo = user_repo
        self.session_mgr = session_mgr

    def login(self, email: str, password: str) -> Session:
        user = self.user_repo.get_by_email(email)
        if not user or not user.verify_password(password):
            raise AuthenticationError("Invalid credentials")
        return self.session_mgr.create(user.id)
```

### 4. Adapter Pattern (Not Leaky Infrastructure)

Wrap external services (SMTP, Twilio, S3) behind a Protocol. Business logic calls the Protocol; adapters handle the wiring.

```python
# ❌ smtplib/twilio details scattered across business code
# ✅ Protocol defines the contract, adapters implement it
class NotificationChannel(Protocol):
    def send(self, recipient: str, message: str) -> None: ...

class EmailChannel:
    def __init__(self, smtp_config: SMTPConfig):
        self.config = smtp_config

    def send(self, recipient: str, message: str) -> None:
        # SMTP details isolated here
        ...
```

## Testing Architecture

Deep mock chains (`mock.return_value.foo.return_value.bar`) are a design smell. Use fakes for complex dependencies, simple `Mock(spec=...)` for simple interfaces, `patch` for environment/time.

```python
# ❌ Testing the mock, not the code
mock_service.return_value.process_payment.return_value = Mock(status="success")

# ✅ Fake with behavior
class FakePaymentGateway:
    def __init__(self):
        self.charges: list[float] = []

    def charge(self, amount: float) -> ChargeResult:
        self.charges.append(amount)
        return ChargeResult(status="success", transaction_id="fake_123")
```

**Guidelines:**
- Mock at boundaries (external APIs, system calls), not your own service classes
- If mock setup is longer than test logic, fix the design or use a fake
- Integration tests verify adapters against real services (sandbox environments)

## Working with Legacy Code

- **Write new code using proper patterns** — don't refactor old code unless asked (Strangler Fig pattern)
- **Don't copy antipatterns for "consistency"** — one correct implementation creates an example
- `def process(gateway: Gateway)` takes the same effort as `def process()` — the difference is testability

## Red Flags

**Technical smells — apply patterns from this skill in new code:**
- Side effects in `__init__` (DB connections, HTTP clients)
- Module-level database/cache clients
- SQL queries outside a repository
- Import statements inside functions (circular dependency workaround)
- Deep mock chains in tests
- Law of Demeter violations — dot chains reaching through objects (`a.b.c.d`)
- `**kwargs` everywhere (hiding the contract)
- One class with 10+ methods doing unrelated things
- Stateless classes (no attributes, only methods)
- Deep inheritance hierarchies (3+ levels)
- Manual `__init__` boilerplate for data containers
- Missing type hints on function signatures
- Accessing `_internal` members from outside the class/module

**Rationalization smells — don't let these justify bad new code:**
- "For consistency" — to justify matching bad patterns
- "Out of scope" — to avoid doing new code correctly
- "We'll refactor after [milestone]" — to skip patterns that cost nothing extra
- "Don't over-engineer" — applied to basic DI or typing

## The Bottom Line

**Architecture is not "over-engineering" — it's making code testable and changeable.**

**Proven OOP principles are guardrails, not suggestions.** SOLID, Law of Demeter, Composition over Inheritance, and Separation of Concerns exist because decades of production code proved that violating them leads to brittle, untestable systems. Apply them by default. Deviate only with a concrete reason, never out of convenience.

If you can't test it with fakes, the design is coupled.
If a class has no state, use functions.
If you're building deep hierarchies, use composition.
If you're chaining through objects (`a.b.c.d`), you're violating Demeter — delegate instead.
If your data objects have manual `__init__` boilerplate, use `@dataclass`.
If your functions lack type hints, add them — they cost nothing and prevent errors.
