---
name: hexagonal-review
description: Hexagonal architecture standards. Use when writing, generating, or reviewing code involving ports, adapters, or layer boundaries.
allowed-tools: Read, Grep, Glob
---

# Hexagonal Architecture Review Skill

## When to Use
Invoke this skill when reviewing code for hexagonal architecture compliance, evaluating ports and adapters design, or assessing separation of concerns between core domain and external systems.

## Core Concepts

### Ports
Interfaces that define how the application core communicates with the outside world. They specify a protocol/contract without committing to implementation details.

**Key Properties:**
- Define abstract API for communication
- Can be implemented by any suitable technical means
- Protocol depends on purpose (method calls, RPC, web services)

### Adapters
The glue between components and the external world. They translate between external systems and the ports defined by the application core.

**Key Properties:**
- Multiple adapters can implement one port
- Adapters are interchangeable without changing core logic
- Examples: GUI, CLI, test scripts, automated data sources

---

## Review Checklist

### Port Design

| Check | Question |
|-------|----------|
| **Abstraction** | Is the port defined as an interface, not a concrete implementation? |
| **Independence** | Can the port be implemented without knowing specific technology? |
| **Completeness** | Does the port define all operations needed by the core? |
| **Minimalism** | Does the port avoid exposing unnecessary details? |

### Adapter Design

| Check | Question |
|-------|----------|
| **Translation** | Does the adapter translate between external format and domain model? |
| **Isolation** | Is external system logic contained entirely within the adapter? |
| **Swappability** | Can this adapter be replaced without modifying core logic? |
| **Testability** | Can the adapter be mocked for testing the core? |

### Architecture Boundaries

| Layer | Should Contain | Should NOT Contain |
|-------|----------------|-------------------|
| **Domain/Core** | Business logic, entities, use cases | Framework code, I/O, external dependencies |
| **Ports** | Interfaces/abstractions | Implementation details |
| **Adapters** | External integrations, translations | Business logic |
| **Infrastructure** | Concrete implementations, configs | Domain rules |

---

## Common Ports

| Port Type | Purpose | Example Interface |
|-----------|---------|-------------------|
| **Database** | Data persistence operations | `Repository` interface for CRUD |
| **HTTP** | Handle incoming HTTP requests | `Handler` interface for request processing |
| **Messaging** | Message broker communication | `Publisher`/`Subscriber` interfaces |
| **Filesystem** | File I/O operations | `FileStore` interface for read/write |
| **Authentication** | User identity verification | `Authenticator` interface |
| **Payment Gateway** | Payment processing | `PaymentProcessor` interface |

---

## Common Adapters

| Adapter Type | Translates Between | Example |
|--------------|-------------------|---------|
| **Database** | Domain model ↔ Database schema | SQLAlchemy, GORM, SQLx |
| **REST API** | HTTP requests ↔ Domain commands | Chi handlers, Gin controllers |
| **Message Queue** | Domain events ↔ Queue messages | RabbitMQ, Kafka clients |
| **CLI** | Command-line args ↔ Domain commands | Cobra, Click |
| **Filesystem** | Domain data ↔ File formats | Local/cloud storage clients |
| **Email** | Domain events ↔ Email messages | SMTP, SendGrid adapters |
| **GUI** | User interactions ↔ Domain events | GTK, Qt, React |

---

## Reference Directory Structure

```
my-app/
├── cmd/
│   └── server/
│       └── main.go                 # Entry point, wiring
│
├── internal/
│   ├── config/
│   │   └── config.go               # Configuration handling
│   │
│   ├── app/
│   │   └── application.go          # Application service interface
│   │
│   ├── domain/
│   │   ├── model/
│   │   │   └── entity.go           # Domain entities (CORE)
│   │   └── repository/
│   │       └── repository.go       # Repository interfaces (PORTS)
│   │
│   ├── usecase/
│   │   └── usecase.go              # Use case implementations (CORE)
│   │
│   ├── interfaces/                 # ADAPTERS (Driving/Primary)
│   │   ├── rest/
│   │   │   └── controller.go       # REST controller
│   │   └── cli/
│   │       └── cli.go              # CLI interface
│   │
│   └── infrastructure/             # ADAPTERS (Driven/Secondary)
│       ├── db/
│       │   ├── db.go               # Database implementation
│       │   └── migration/
│       ├── http/
│       │   ├── handler/
│       │   └── router.go
│       └── logger/
│
└── pkg/
    └── util/                       # Shared utilities
```

---

## Red Flags

### Architecture Violations

| Violation | Symptom | Fix |
|-----------|---------|-----|
| **Leaky Abstraction** | Port exposes database-specific types (e.g., `sql.Row`) | Use domain types in port interface |
| **Core Depends on Framework** | Domain imports HTTP/DB packages | Inject dependencies via ports |
| **Adapter Contains Logic** | Business rules in handler/repository | Move logic to use case layer |
| **Missing Port** | Core directly calls external service | Extract interface, create port |
| **God Adapter** | Single adapter handles multiple concerns | Split into focused adapters |

### Dependency Direction

```
WRONG: Domain → Infrastructure
       (core imports database package)

RIGHT: Infrastructure → Domain
       (adapter implements domain interface)
```

---

## Quick Reference

| Question | Expected Answer |
|----------|-----------------|
| Can I swap the database without changing business logic? | Yes, via repository port |
| Can I test use cases without a real database? | Yes, with mock adapter |
| Does the domain layer import external packages? | No, only standard library |
| Are external systems abstracted behind interfaces? | Yes, as ports |
| Can I add a CLI without modifying existing code? | Yes, new adapter for existing port |
