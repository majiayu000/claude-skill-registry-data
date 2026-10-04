---
name: software-architecture
description: Software architecture design from Google Principal Engineers. Use when designing folder structures, implementing Clean Architecture or Hexagonal Architecture, applying Domain-Driven Design (DDD), enforcing SOLID principles, choosing design patterns (Repository, Factory, Strategy, Observer), refactoring complex modules, or planning system boundaries. Triggers on architecture, clean code, DDD, SOLID, design patterns, folder structure, refactoring, or code organization.
---

# Software Architecture - Clean Code & Domain Expertise

**Purpose**: Design maintainable, scalable software systems using Clean Architecture, DDD, and SOLID principles

**Agent**: Google Software Architect
**Use When**: Complex business logic, long-term maintainability critical, or code organization guidance needed

---

## Quick Reference

### Clean Architecture Layers

```
External (UI, DB, APIs)
        ↓
Interface Adapters (Controllers, Gateways)
        ↓
Use Cases (Business Workflows)
        ↓
Entities (Core Domain)
```

**Dependency Rule**: Dependencies point inward only

---

## Core Concepts

### 1. Clean Architecture

**Purpose**: Separate business logic from infrastructure

**Layers**:
- **Entities**: Core business objects (no dependencies)
- **Use Cases**: Business workflows (depends on entities)
- **Interface Adapters**: Controllers, presenters (depends on use cases)
- **Frameworks**: UI, DB, external services (depends on adapters)

**Benefits**:
- ✅ Testable without UI/DB
- ✅ Framework-independent
- ✅ Easy to change infrastructure
- ✅ Business logic is clear

**Example Structure**:
```
src/
├── domain/          # Entities, value objects
├── application/     # Use cases, ports
├── infrastructure/  # Database, external APIs
└── presentation/    # Controllers, UI
```


---

### 2. Domain-Driven Design (DDD)

**Purpose**: Model complex business domains accurately

**Key Concepts**:
- **Ubiquitous Language**: Shared vocabulary
- **Bounded Contexts**: Logical domain boundaries
- **Entities**: Objects with identity
- **Value Objects**: Immutable, defined by attributes
- **Aggregates**: Consistency boundaries
- **Domain Events**: Things that happened

**When to Use**:
- Complex business rules
- Multiple teams
- Long-lived projects
- Domain experts available

**Example**:
```typescript
// Entity
class Order {
  constructor(
    private id: OrderId,
    private items: OrderItem[],
    private status: OrderStatus
  ) {}

  place(): void {
    if (this.items.length === 0) {
      throw new Error('Cannot place empty order')
    }
    this.status = OrderStatus.PLACED
  }
}

// Value Object
class Money {
  constructor(
    private amount: number,
    private currency: string
  ) {}

  add(other: Money): Money {
    return new Money(this.amount + other.amount, this.currency)
  }
}
```


---

### 3. SOLID Principles

**S**ingle Responsibility: One class, one reason to change
**O**pen/Closed: Open for extension, closed for modification
**L**iskov Substitution: Subtypes must be substitutable
**I**nterface Segregation: Many specific > one general
**D**ependency Inversion: Depend on abstractions


---

### 4. Design Patterns

**Creational**:
- Factory: Create objects without specifying exact class
- Builder: Construct complex objects step by step
- Singleton: Ensure only one instance exists

**Structural**:
- Adapter: Make incompatible interfaces work together
- Decorator: Add behavior without modifying original
- Facade: Simplified interface to complex subsystem

**Behavioral**:
- Strategy: Encapsulate algorithms, make them interchangeable
- Observer: Notify dependents when state changes
- Command: Encapsulate requests as objects


---

## Common Architecture Patterns

### Hexagonal Architecture (Ports & Adapters)

```
┌─────────────────────────────────┐
│        Application Core         │
│  (Business Logic, Use Cases)    │
│                                 │
│  Ports (Interfaces):            │
│  ├─ Input Ports (Commands)      │
│  └─ Output Ports (Repositories) │
└──────────┬──────────────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
Adapters      Adapters
(HTTP, CLI)   (Database, Email)
```

**Benefits**: Swap adapters without changing core

---

### CQRS (Command Query Responsibility Segregation)

```
Commands (Write)     Queries (Read)
      ↓                    ↓
  Write Model          Read Model
      ↓                    ↓
  PostgreSQL           Elasticsearch
```

**When to Use**: Different read/write patterns

---

### Event-Driven Architecture

```
Service A → Publishes Event → Event Bus → Service B Subscribes
```

**Benefits**: Loose coupling, scalability

---

## Folder Structure Examples

### Clean Architecture (TypeScript)

```
src/
├── domain/
│   ├── entities/
│   │   ├── Order.ts
│   │   └── User.ts
│   ├── value-objects/
│   │   └── Money.ts
│   └── repositories/        # Interfaces
│       └── IOrderRepository.ts
│
├── application/
│   ├── use-cases/
│   │   ├── CreateOrder.ts
│   │   └── PlaceOrder.ts
│   └── ports/
│       ├── input/
│       └── output/
│
├── infrastructure/
│   ├── persistence/
│   │   ├── PostgresOrderRepository.ts
│   │   └── migrations/
│   └── external-services/
│       └── StripePaymentService.ts
│
└── presentation/
    ├── api/
    │   ├── controllers/
    │   │   └── OrderController.ts
    │   └── dto/
    └── web/
```

### DDD (Python)

```
app/
├── domain/
│   ├── model/
│   │   ├── order.py          # Aggregate
│   │   ├── order_item.py     # Entity
│   │   └── money.py          # Value Object
│   ├── events/
│   │   └── order_placed.py
│   └── repositories/
│       └── order_repository.py
│
├── application/
│   ├── commands/
│   │   └── create_order.py
│   └── handlers/
│       └── order_handler.py
│
└── infrastructure/
    ├── persistence/
    │   └── sqlalchemy_order_repo.py
    └── messaging/
```

---

## When to Use Each Pattern

### Simple CRUD App
- ✅ Keep it simple: Controllers → Services → Repositories
- ❌ Don't over-architect
- Focus: Readability

### Complex Business Logic
- ✅ Clean Architecture or DDD
- ✅ Separate domain from infrastructure
- Focus: Maintainability

### Microservices
- ✅ One service = one bounded context
- ✅ Event-driven communication
- Focus: Loose coupling

### Legacy Refactoring
- ✅ Strangler Fig pattern
- ✅ Extract domain logic incrementally
- Focus: Gradual improvement

---

## Anti-Patterns to Avoid

❌ **Anemic Domain Model**: Entities with no behavior
❌ **God Objects**: One class doing everything
❌ **Leaky Abstractions**: Domain knowing about HTTP/DB
❌ **Circular Dependencies**: A depends on B depends on A
❌ **Over-Engineering**: Using DDD for simple CRUD

---

## Best Practices

1. **Start Simple**: Don't over-architect MVPs
2. **Evolve Architecture**: Refactor as complexity grows
3. **Test First**: If hard to test, architecture is wrong
4. **Domain First**: Model business before infrastructure
5. **Pragmatic**: Balance purity with practicality

---

---

**Philosophy**: "Make it work, make it right, make it fast" - in that order.

**Remember**: Architecture serves the business, not the other way around.

**Created**: 2026-02-04
**Maintained By**: Google Software Architect
