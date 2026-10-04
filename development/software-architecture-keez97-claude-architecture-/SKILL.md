---
name: software-architecture
description: >
  Design scalable systems with Clean Architecture, SOLID principles, and Architecture Decision Records.
  Use this for decomposing systems, choosing architectural patterns, documenting decisions, and avoiding
  over-engineering. Language-agnostic: applies to any tech stack.
---

# Software Architecture Skill

You've got a system to design or refactor. This skill cuts through the academic noise and gives you practical architecture decisions rooted in trade-offs, not dogma.

## When to Use This Skill

- **"How should I structure this?"** — system decomposition, boundaries, layering
- **"Should I use microservices/CQRS/event-driven?"** — pattern selection with honest trade-offs
- **"This code is becoming a mess"** — coupling, cohesion, and refactoring strategy
- **SOLID violations** — identifying coupling, hard-to-test code, tight dependencies
- **Architectural decisions** — documenting why you chose Pattern X over Pattern Y
- **Any language-agnostic design question** — these principles transcend tech stacks

*Not for Python-specific style/lint questions—use python-architecture-review for that.*

---

## Review Mode: Architecture Health Audit

When analyzing existing systems, the skill produces:

### Architecture Health Score
Visual assessment using a structured template with these dimensions:

```
Architecture Health Score
=========================

Coupling              ████░░░░░░  [Good/Needs Work] - module interdependencies and circular refs
Cohesion             ██████░░░░  [Good/Needs Work] - components do one thing well
Abstraction Level    ███████░░░  [Good/Needs Work] - appropriate abstraction vs. over-engineering
Testability          ██░░░░░░░░  [Critical Issues] - ability to unit test in isolation
Pattern Consistency  █████░░░░░  [Good/Needs Work] - architectural patterns applied uniformly

Overall: [One-sentence verdict on system's architectural health]
```

Assess across these five dimensions:
- **Coupling**: module interdependencies and circular references. Loose coupling = easier to change.
- **Cohesion**: whether components do one thing well. High cohesion = components with clear purpose.
- **Abstraction Level**: choosing right level of abstraction. Too little = scattered logic; too much = over-engineering.
- **Testability**: ability to unit test in isolation. Can you test business logic without HTTP/DB?
- **Pattern Consistency**: architectural patterns applied uniformly. Inconsistent patterns = hard to navigate.

### Findings Table
Present every finding in a structured table for easy prioritization:

| ID | Severity | Finding | Impact | Fix | Effort | Unlocks |
|----|----|---------|--------|-----|--------|---------|
| F1 | High | God object in UserService (500+ lines) | Hard to test, blocks parallelization | Extract Repository, Factory patterns | Medium | Async refactor (F3) |
| F2 | High | Circular import: models → utils → models | Unpredictable load order, brittle | Move shared code to `common/` | Low | Can parallelize tests |
| F3 | Medium | No seams for database layer | Can't test business logic in isolation | Inject data access interface | Medium | Integration test suite |

For each finding, include:
- **ID** — Reference number (F1, F2, ...)
- **Severity** — CRITICAL / HIGH / MEDIUM / LOW (impact on production, testing, or developer velocity)
- **Finding** — What the problem is, with file/module references
- **Impact** — What actually goes wrong. Quantify: "At 10k users, this class will be unchageable" beats generic "hard to maintain."
- **Fix** — Concrete code showing the solution
- **Effort** — Quick (< 1 hour), Moderate (half day), Significant (1-2 days), Large (week+)
- **Unlocks** — What other fixes this enables

### Anti-Patterns & Over-Engineering Flags
- **Repository pattern** on a simple table? Usually overkill. Justify before adding it.
- **Event-driven everywhere?** Each event adds latency, tracing complexity, and eventual consistency headaches.
- **Microservices at 3 engineers?** You're paying for distributed systems complexity; get value or consolidate.
- **Abstract interface on every class** — tight coupling to abstraction. Only abstract what varies.

### Before/After Showcase
For the 2-3 most impactful findings, show complete before/after code transformations. Include enough context that the reader sees how it fits into the broader codebase.

**Example 1: Tight Coupling → Dependency Injection**

```python
# BEFORE: UserService tightly coupled to PostgreSQL
class UserService:
    def __init__(self):
        self.db = PostgreSQL(host="localhost", db="users")

    def get_user(self, user_id: int):
        return self.db.query("SELECT * FROM users WHERE id = ?", user_id)
```

```python
# AFTER: Depend on abstraction, inject concrete implementation
class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User: ...

class PostgreSQLUserRepository(UserRepository):
    def __init__(self, engine):
        self.engine = engine

    def get_by_id(self, user_id: int) -> User:
        return self.engine.query(User).filter(User.id == user_id).first()

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, user_id: int) -> User:
        return self.repo.get_by_id(user_id)

# At bootstrap:
repo = PostgreSQLUserRepository(engine)
service = UserService(repo)  # Now testable with mock repo
```

**Example 2: Mixed Concerns (SRP Violation) → Extracted Services**

```python
# BEFORE: UserService handles auth AND email notifications AND audit logging
class UserService:
    def register(self, email: str, password: str):
        user = User(email=email, password_hash=hash(password))
        db.save(user)
        send_email(email, "Welcome!")  # Not user service's job
        audit_log("user_registered", user.id)  # Not user service's job
        return user
```

```python
# AFTER: Single responsibility, inject dependencies
class UserService:
    def __init__(self, email_service: EmailService, audit: AuditService):
        self.email = email_service
        self.audit = audit

    def register(self, email: str, password: str) -> User:
        user = User(email=email, password_hash=hash(password))
        db.save(user)
        self.email.send_welcome(email)  # Delegated
        self.audit.log("user_registered", user.id)  # Delegated
        return user
    # Now testable: mock email_service and audit_service
```

---

## Design Mode: New System Architecture

When designing from scratch or major refactors:

### 1. Requirements Restatement
- **Scale targets**: RPS, data volume, read/write ratio, peak burst
- **Operational constraints**: deployment frequency, SLA, latency budgets
- **Coupling points**: what can be loosely coupled, what must be tightly coupled
- **Common change patterns**: what do users/product ask for most frequently?

### 2. Architecture Decision Records (ADRs)

Create ADRs for all significant decisions. Use this template:

```
# ADR-001: [Short title]

## Status
Proposed | Accepted | Deprecated

## Context
Why this decision matters. What problem are we solving?
- Technical constraints
- Business constraints
- Trade-offs being evaluated

## Decision
What we chose and why.

## Alternatives Considered
- Alt A: pros/cons, decision rationale
- Alt B: pros/cons, decision rationale

## Consequences
What becomes easier? What becomes harder?
- Positive: ...
- Negative: ...
- Risks: ...

## Revisit When
- Scale hits X RPS
- Team grows beyond N engineers
- New tech emerges (e.g., "if FastAPI adds streaming native support")
- Requirements change (e.g., "if we need sub-second latency")
```

**Key ADRs for most systems**:
- API transport (REST vs gRPC vs GraphQL)
- Database strategy (monolithic SQL vs sharding vs event sourcing)
- Async patterns (message queue vs function triggers)
- Deployment model (monolith vs services)

### 3. Component Decomposition

- **Domain-driven boundaries**: align technical structure to business domains
- **What data lives where**: which service owns the source of truth?
- **Synchronous vs async calls**: where is strong consistency required?
- **Failure mode design**: if component X fails, what breaks and why?

### 4. Design Patterns Applied Judiciously

**Use a pattern if it solves an actual pain point, not because it sounds professional.**

#### Repository Pattern
- **When**: multiple data sources (SQL + cache + API), want pluggable implementations
- **When NOT**: single well-designed table with ORM, complexity tax isn't worth it
- **Fix Example**: Instead of `UserRepository.get_by_email()`, inject data layer interface

#### Factory Pattern
- **When**: complex object creation, parametric type selection
- **When NOT**: simple constructors; you're not saving real complexity
- **Real use**: Create different logger implementations based on environment

#### Strategy Pattern
- **When**: multiple algorithms for the same task; client needs to swap them
- **Real example**: Payment processors (Stripe vs Square vs PayPal), swap based on config
- **Anti-pattern**: Strategy for "is user admin?" — that's an if statement, not a pattern

#### Observer/Pub-Sub
- **When**: decoupling event producers from consumers (e.g., user signup → email, analytics, audit log)
- **Cost**: eventual consistency, harder debugging (event fired but subscriber down?), monitoring complexity
- **Design**: Keep synchronous work in the request, async work in subscribers

#### Mediator Pattern
- **When**: many objects need coordinated interaction (orchestration)
- **Cost**: single point of failure, hard to test (mediator knows everything)
- **Prefer**: explicit interfaces between components over hidden mediator magic

---

## SOLID Principles: Applied, Not Preached

### Single Responsibility Principle (SRP)
**Problem**: Class does two things, changes for two reasons, hard to test.

```python
# VIOLATION: UserService handles both auth AND email notifications
class UserService:
    def register(self, email, password):
        user = User(email, self.hash(password))
        db.save(user)
        self.send_welcome_email(user)  # Not your job
```

**Fix**: Inject an email service, decouple notification policy.

```python
class UserService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def register(self, email, password):
        user = User(email, self.hash(password))
        db.save(user)
        self.email_service.send_welcome(user)  # Now testable
```

### Open/Closed Principle (OCP)
**Problem**: Adding a new payment processor requires changing existing code.

```python
# VIOLATION: Modify the router for each provider
if processor == "stripe":
    charge_stripe(...)
elif processor == "square":
    charge_square(...)  # Edit the handler every time
```

**Fix**: Strategy pattern with registry.

```python
class PaymentRouter:
    def __init__(self, providers: dict[str, PaymentProvider]):
        self.providers = providers

    def charge(self, provider_name, amount):
        return self.providers[provider_name].charge(amount)

# Register once at startup
router = PaymentRouter({
    "stripe": StripeProvider(...),
    "square": SquareProvider(...)
})
```

### Liskov Substitution Principle (LSP)
**Problem**: Subclass breaks the contract of the parent.

```python
# VIOLATION: CachedUserRepository is not truly a UserRepository
class UserRepository:
    def get(self, id): ...

class CachedUserRepository(UserRepository):
    def get(self, id):
        if id in cache: return cache[id]
        # Lies: doesn't fetch from DB; caller thinks it's fresh
```

**Fix**: Don't inherit; compose or make caching explicit in the interface.

### Interface Segregation Principle (ISP)
**Problem**: Class depends on a fat interface with methods it doesn't use.

```python
# VIOLATION: UserService imports PaymentProcessor but only uses one method
class UserService:
    def __init__(self, payment: PaymentProcessor):  # Has 10 methods
        self.payment = payment

    def refund_subscription(self, user_id):
        self.payment.refund(user_id)  # Uses only this one
```

**Fix**: Depend on a narrower interface.

```python
class RefundService:
    def __init__(self, refunder: Refundable):  # Single method interface
        self.refunder = refunder

    def refund_subscription(self, user_id):
        self.refunder.refund(user_id)
```

### Dependency Inversion Principle (DIP)
**Problem**: High-level modules depend on low-level concrete details.

```python
# VIOLATION: UserService is tightly coupled to PostgreSQL
class UserService:
    def __init__(self):
        self.db = PostgreSQL(...)  # Hardcoded dependency
```

**Fix**: Depend on abstraction; inject concrete implementation.

```python
class UserService:
    def __init__(self, repo: UserRepository):  # Interface dependency
        self.repo = repo

# At bootstrap:
app.use(UserService(PostgreSQLUserRepository(...)))
```

---

## Architectural Styles: Trade-Offs Explained

### Clean Architecture
- **Layers**: Entities → Use Cases → Interface Adapters → Frameworks
- **Benefit**: Business logic independent of frameworks, testable without database
- **Cost**: Can feel heavy for CRUD apps; over-engineering at small scale
- **Use when**: Long-lived product, changing requirements, large team

### Hexagonal (Ports & Adapters)
- **Core idea**: Business logic at center, all external I/O at edges
- **Benefit**: Swap adapters (PostgreSQL → MongoDB, REST → gRPC)
- **Cost**: More interfaces to maintain, indirection
- **Use when**: Multiple I/O protocols (API + CLI + background job), multiple persistence options

### Layered
- **Layers**: Presentation → Business → Data
- **Benefit**: Simple, familiar, works for most web apps
- **Cost**: Business logic often leaks into presentation/data layers
- **Use when**: Standard CRUD app, small team, fast iteration

### Event-Driven
- **Pattern**: Components communicate via events (produced → broker → consumed)
- **Benefit**: Decouples producers from consumers, scales reads independently
- **Cost**: Eventual consistency, harder debugging, requires idempotent consumers
- **Use when**: High-scale systems, many independent subscribers, can tolerate eventual consistency

### CQRS (Command Query Responsibility Segregation)
- **Split**: Separate write model (commands) from read model (queries)
- **Benefit**: Optimize reads independently (caching, denormalization), scale reads
- **Cost**: Dual models, eventual consistency, complex migrations
- **Use when**: Complex queries on simple writes, read-heavy workloads (analytics, dashboards)

---

## System Design Checklist

### Decomposition
- [ ] Identify bounded contexts (business domains)
- [ ] Assign one service/module per domain
- [ ] Define contracts between modules (APIs, events)
- [ ] Map data ownership (who is the source of truth?)

### Boundaries & Coupling
- [ ] Synchronous calls only where strong consistency required
- [ ] Async (events, queues) for eventual consistency paths
- [ ] Circular dependencies? Extract shared module or reverse dependency
- [ ] Test each component in isolation without starting others

### Evolution Planning
- [ ] What changes most frequently? Keep that layer thinnest.
- [ ] What is a business rule vs. infrastructure detail?
- [ ] Can you add a feature without touching 5 files?
- [ ] If load doubles, can you scale horizontally?

### Operational Concerns
- [ ] How do you deploy? (Monolith, blue-green, rolling, canary?)
- [ ] How do you observe failures? (Logging, metrics, traces)
- [ ] How do you rollback a bad deploy?
- [ ] What's the SLA and latency budget per layer?

---

## Anti-Patterns & Red Flags

| Red Flag | Why It Hurts | Fix |
|----------|-------------|-----|
| Every class has an interface | Over-abstraction; hard to read | Abstract only what varies |
| 10+ constructor parameters | Hidden coupling; hard to test | Inject fewer, larger objects |
| Circular imports | Load order fragile; circular logic | Extract shared → higher level |
| God object (500+ lines) | Does many things; hard to test | Extract responsibilities |
| No clear data ownership | Bugs from conflicting updates | Define source of truth per domain |
| Async everywhere | Unpredictable latency, tracing nightmare | Keep happy path synchronous |

---

## Destructive Operations: Structural Refactoring Safety

Architecture reviews often recommend structural changes: splitting monolithic files,
extracting modules, reorganizing directories, changing barrel exports. These are
among the most dangerous operations in software development because they touch
import chains across the entire codebase and can silently corrupt code.

### Risk Classification

Every structural recommendation must include a risk classification:

| Risk Level | Operation Type | Required Protocol |
|------------|---------------|-------------------|
| **Low** | Single-file refactoring, function extraction within a file | Standard review |
| **Medium** | Extracting code to a new file, adding a new module | Build verification after change |
| **High** | Splitting files into multiple modules, restructuring directories | Write → Verify → Delete order, git checkpoints per round |
| **Critical** | Changing build config, module boundaries, or project structure | User approval + full file-split protocol |

### The File Split Trap

The most common destructive mistake: recommending that a large file (1,000+ lines)
be split into many smaller modules. This sounds like good architecture advice, and
it often is — but the *execution* is where codebases get destroyed.

What goes wrong:
- Text-based splitting cuts function bodies in half
- Interfaces get truncated mid-definition
- Orphaned closing braces become syntax errors in downstream files
- Barrel files miss re-exports, breaking every consumer
- `export *` doesn't forward default exports (TypeScript/JavaScript trap)

When recommending a file split:
1. Classify it as HIGH or CRITICAL risk
2. Estimate effort including verification overhead (not just the code move)
3. Note that the original file must be preserved until all splits compile
4. Recommend incremental rounds of 3-5 files maximum per round
5. Require full compilation check between rounds

**A working monolith is always better than a broken set of small files.**

## Next Steps

1. **Capture decisions as ADRs** — even retrofit existing systems
2. **Map current state** — identify coupling, circular deps, fat objects
3. **Plan migration path** — phased refactoring toward target architecture
4. **Measure progress** — coupling metrics, test coverage, time-to-feature
5. **Revisit annually** — scale changes, team changes, tech changes invalidate old decisions
6. **Verify structural changes** — any refactoring that moves code between files
   requires compilation gates and git checkpoints
