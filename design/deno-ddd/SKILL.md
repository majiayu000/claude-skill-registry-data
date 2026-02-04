---
name: deno-ddd
description: "Domain-Driven Design patterns and architecture for Deno TypeScript applications. Use when building complex business logic, implementing bounded contexts, or structuring large-scale Deno applications with clear separation of concerns."
---

# Domain-Driven Design in Deno

## When to Use This Skill

Use this skill when:
- Building applications with complex business logic
- Implementing hexagonal/clean architecture in Deno
- Structuring large-scale Deno applications
- Separating domain logic from infrastructure
- Working with bounded contexts and aggregates
- Need clear separation between layers

**Prerequisites:** Always read `deno-core.md` first for essential Deno configuration.

---

## Project Philosophy

> **Clean, Modern TypeScript**: Embrace Deno's vision of secure, modern JavaScript/TypeScript development without the baggage of Node.js legacy patterns.

> **Domain-Driven Design**: Follow DDD principles with clear separation between domain logic, application services, and infrastructure concerns.

> **TypeScript-First**: Leverage TypeScript's type system for safety and developer experience. No `any` types in production code.

---

## Core DDD Principles

### Ubiquitous Language
- Use domain terminology consistently in code, docs, and conversations
- Type names, method names, and variables should match business concepts
- Avoid technical jargon in domain layer

### Bounded Contexts
- Each context has its own models and language
- Clear boundaries between contexts
- Explicit translation between contexts

### Layered Architecture
1. **Domain Layer** - Pure business logic, no dependencies
2. **Application Layer** - Use cases, orchestration
3. **Infrastructure Layer** - External services, databases, APIs
4. **API Layer** - HTTP handlers, CLI, GraphQL resolvers

---

## Project Structure

### Recommended Directory Layout

```
src/
├── domain/                    # Domain layer - core business logic
│   ├── entities/              # Domain entities (Memory, User, Order)
│   │   ├── user.ts
│   │   └── order.ts
│   ├── value-objects/         # Immutable values (Email, Money, Status)
│   │   ├── email.ts
│   │   ├── money.ts
│   │   └── order-status.ts
│   ├── aggregates/            # Consistency boundaries
│   │   └── order-aggregate.ts
│   ├── repositories/          # Repository interfaces (ports)
│   │   ├── user-repository.ts
│   │   └── order-repository.ts
│   ├── services/              # Domain services
│   │   └── pricing-service.ts
│   ├── events/                # Domain events
│   │   └── order-created.ts
│   └── errors/                # Domain-specific errors
│       ├── validation-error.ts
│       └── business-rule-error.ts
│
├── application/               # Application layer - use cases
│   ├── use-cases/             # Use case implementations
│   │   ├── create-order.ts
│   │   ├── update-user.ts
│   │   └── process-payment.ts
│   ├── services/              # Application services
│   ├── dto/                   # Data transfer objects
│   │   ├── create-order-dto.ts
│   │   └── user-response-dto.ts
│   └── errors/                # Application-specific errors
│       ├── not-found-error.ts
│       └── unauthorized-error.ts
│
├── infrastructure/            # Infrastructure layer - technical details
│   ├── persistence/           # Database implementations
│   │   ├── postgres/
│   │   │   ├── user-repository-impl.ts
│   │   │   └── order-repository-impl.ts
│   │   └── migrations/
│   ├── external/              # External service integrations
│   │   ├── payment-gateway.ts
│   │   └── email-service.ts
│   ├── logging/               # Structured logging
│   │   └── logger.ts
│   ├── config/                # Configuration
│   │   └── database.ts
│   └── errors/                # Infrastructure errors
│       ├── database-error.ts
│       └── external-api-error.ts
│
├── web/                       # Web/API layer - HTTP entry points
│   ├── controllers/           # Request handlers
│   │   ├── user-controller.ts
│   │   └── order-controller.ts
│   ├── middleware/            # HTTP middleware
│   │   ├── auth.ts
│   │   ├── validation.ts
│   │   ├── error-handler.ts
│   │   └── logging.ts
│   ├── routes/                # Route definitions
│   │   ├── user-routes.ts
│   │   └── order-routes.ts
│   └── server.ts              # HTTP server setup
│
└── shared/                    # Shared kernel
    ├── types/
    │   └── result.ts
    └── utils/
        └── validation.ts

tests/
├── domain/                    # Domain tests (unit)
│   ├── entities/
│   │   └── user.test.ts
│   └── value-objects/
│       └── email.test.ts
├── application/               # Application tests (integration)
│   └── use-cases/
│       └── create-order.test.ts
└── e2e/                       # End-to-end tests
    └── order-workflow.test.ts
```

### Import Map Configuration

Configure `deno.json` for clean imports across all layers:

```json
{
  "imports": {
    "@/": "./src/",
    "@/domain/": "./src/domain/",
    "@/application/": "./src/application/",
    "@/infrastructure/": "./src/infrastructure/",
    "@/web/": "./src/web/",
    "@/shared/": "./src/shared/"
  }
}
```

---

## Layer Dependencies

Understanding and enforcing layer dependencies is critical for maintaining a clean DDD architecture.

### Allowed Dependencies

- **`domain`** → (no external dependencies - pure business logic)
- **`application`** → `domain`
- **`infrastructure`** → `domain` + `application`
- **`web`** (or `api`) → `domain` + `application` + `infrastructure`

### Forbidden Dependencies

**NEVER allow these dependencies:**
- **`domain`** → `application`, `infrastructure`, `web`
- **`application`** → `infrastructure`, `web`
- **`infrastructure`** → `web`

### Dependency Flow Visualization

```
    ┌─────────────┐
    │     web     │  (HTTP handlers, routes, middleware)
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │infrastructure│  (Database, external APIs)
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ application │  (Use cases, orchestration)
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   domain    │  (Entities, value objects, business rules)
    └─────────────┘
```

**Key Principle:** Dependencies flow inward. Inner layers have no knowledge of outer layers.

---

## Domain Layer

### Entities

Entities have identity and lifecycle. Use classes with private constructors.

```typescript
// src/domain/entities/user.ts
import type { Email } from "@/domain/value-objects/email.ts";
import type { UserId } from "@/domain/value-objects/user-id.ts";

export class User {
  private constructor(
    private readonly id: UserId,
    private name: string,
    private email: Email,
    private readonly createdAt: Date,
  ) {}

  // Factory method - ensures valid construction
  static create(name: string, email: Email): User {
    if (name.trim().length === 0) {
      throw new Error("User name cannot be empty");
    }
    return new User(
      UserId.generate(),
      name,
      email,
      new Date(),
    );
  }

  // Reconstruct from persistence
  static reconstitute(
    id: UserId,
    name: string,
    email: Email,
    createdAt: Date,
  ): User {
    return new User(id, name, email, createdAt);
  }

  // Business logic methods
  changeName(newName: string): void {
    if (newName.trim().length === 0) {
      throw new Error("User name cannot be empty");
    }
    this.name = newName;
  }

  // Getters
  getId(): UserId { return this.id; }
  getName(): string { return this.name; }
  getEmail(): Email { return this.email; }
  getCreatedAt(): Date { return this.createdAt; }
}
```

### Value Objects

Value objects have no identity, compared by value.

```typescript
// src/domain/value-objects/email.ts
export class Email {
  private constructor(private readonly value: string) {}

  static create(value: string): Email {
    if (!Email.isValid(value)) {
      throw new Error(`Invalid email: ${value}`);
    }
    return new Email(value.toLowerCase());
  }

  private static isValid(value: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value);
  }

  getValue(): string { return this.value; }
  equals(other: Email): boolean { return this.value === other.value; }
  toString(): string { return this.value; }
}
```

```typescript
// src/domain/value-objects/money.ts
export class Money {
  private constructor(
    private readonly amount: number,
    private readonly currency: string,
  ) {}

  static create(amount: number, currency: string): Money {
    if (amount < 0) {
      throw new Error("Money amount cannot be negative");
    }
    if (!["USD", "EUR", "GBP"].includes(currency)) {
      throw new Error(`Unsupported currency: ${currency}`);
    }
    return new Money(amount, currency);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error("Cannot add money with different currencies");
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return new Money(this.amount * factor, this.currency);
  }

  getAmount(): number { return this.amount; }
  getCurrency(): string { return this.currency; }
  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}
```

### Aggregates

Aggregates enforce consistency boundaries and business invariants.

```typescript
// src/domain/aggregates/order-aggregate.ts
import type { OrderId } from "@/domain/value-objects/order-id.ts";
import type { Money } from "@/domain/value-objects/money.ts";
import type { OrderLine } from "@/domain/entities/order-line.ts";

export enum OrderStatus {
  PENDING = "PENDING",
  CONFIRMED = "CONFIRMED",
  SHIPPED = "SHIPPED",
  DELIVERED = "DELIVERED",
  CANCELLED = "CANCELLED",
}

export class Order {
  private constructor(
    private readonly id: OrderId,
    private status: OrderStatus,
    private readonly lines: OrderLine[],
    private readonly createdAt: Date,
  ) {}

  static create(lines: OrderLine[]): Order {
    if (lines.length === 0) {
      throw new Error("Order must have at least one line");
    }
    return new Order(
      OrderId.generate(),
      OrderStatus.PENDING,
      lines,
      new Date(),
    );
  }

  // Business logic - enforce invariants
  confirm(): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new Error(`Cannot confirm order with status ${this.status}`);
    }
    this.status = OrderStatus.CONFIRMED;
  }

  cancel(): void {
    if (this.status === OrderStatus.SHIPPED || this.status === OrderStatus.DELIVERED) {
      throw new Error("Cannot cancel shipped or delivered order");
    }
    this.status = OrderStatus.CANCELLED;
  }

  calculateTotal(): Money {
    return this.lines.reduce(
      (total, line) => total.add(line.getSubtotal()),
      Money.create(0, "USD"),
    );
  }

  getId(): OrderId { return this.id; }
  getStatus(): OrderStatus { return this.status; }
  getLines(): ReadonlyArray<OrderLine> { return this.lines; }
}
```

### Repository Interfaces (Ports)

Define interfaces in domain layer, implement in infrastructure.

```typescript
// src/domain/repositories/user-repository.ts
import type { User } from "@/domain/entities/user.ts";
import type { UserId } from "@/domain/value-objects/user-id.ts";
import type { Email } from "@/domain/value-objects/email.ts";

export interface UserRepository {
  save(user: User): Promise<void>;
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  delete(id: UserId): Promise<void>;
}
```

---

## Application Layer

### Use Cases

Use cases orchestrate domain logic without containing business rules.

```typescript
// src/application/use-cases/create-order.ts
import type { UserRepository } from "@/domain/repositories/user-repository.ts";
import type { OrderRepository } from "@/domain/repositories/order-repository.ts";
import { Order } from "@/domain/aggregates/order-aggregate.ts";
import { OrderLine } from "@/domain/entities/order-line.ts";
import type { CreateOrderDto } from "@/application/dto/create-order-dto.ts";
import { Result } from "@/shared/types/result.ts";

export class CreateOrderUseCase {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly orderRepository: OrderRepository,
  ) {}

  async execute(dto: CreateOrderDto): Promise<Result<Order>> {
    try {
      const user = await this.userRepository.findById(dto.userId);
      if (!user) {
        return Result.fail("User not found");
      }

      const lines = dto.items.map((item) =>
        OrderLine.create(item.productId, item.quantity, item.price)
      );

      const order = Order.create(lines);
      await this.orderRepository.save(order);

      return Result.ok(order);
    } catch (error) {
      return Result.fail(error.message);
    }
  }
}
```

---

## Error Handling by Layer

### Domain Layer - Domain Errors

```typescript
// src/domain/errors/validation-error.ts
export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ValidationError";
  }
}
```

### Application Layer - Application Errors

```typescript
// src/application/errors/not-found-error.ts
export class MemoryNotFoundError extends Error {
  constructor(id: string) {
    super(`Memory with id ${id} not found`);
    this.name = "MemoryNotFoundError";
  }
}
```

### Infrastructure Layer - Infrastructure Errors

```typescript
// src/infrastructure/errors/database-error.ts
export class DatabaseError extends Error {
  constructor(message: string, public readonly cause?: Error) {
    super(message);
    this.name = "DatabaseError";
  }
}
```

### Web Layer - HTTP Error Handling

```typescript
// src/web/middleware/error-handler.ts
import { ValidationError } from "@/domain/errors/validation-error.ts";
import { MemoryNotFoundError } from "@/application/errors/memory-not-found-error.ts";
import { DatabaseError } from "@/infrastructure/errors/database-error.ts";

export function errorHandler(error: Error): Response {
  if (error instanceof ValidationError) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { "Content-Type": "application/json" } },
    );
  }

  if (error instanceof MemoryNotFoundError) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 404, headers: { "Content-Type": "application/json" } },
    );
  }

  if (error instanceof DatabaseError) {
    console.error("Database error:", error);
    return new Response(
      JSON.stringify({ error: "Database service unavailable" }),
      { status: 503, headers: { "Content-Type": "application/json" } },
    );
  }

  console.error("Unexpected error:", error);
  return new Response(
    JSON.stringify({ error: "Internal server error" }),
    { status: 500, headers: { "Content-Type": "application/json" } },
  );
}
```

---

## Common Patterns

### Result Type

Avoid throwing exceptions across boundaries.

```typescript
// src/shared/types/result.ts
export class Result<T> {
  private constructor(
    private readonly success: boolean,
    private readonly value?: T,
    private readonly error?: string,
  ) {}

  static ok<T>(value: T): Result<T> {
    return new Result(true, value);
  }

  static fail<T>(error: string): Result<T> {
    return new Result(false, undefined, error);
  }

  isSuccess(): boolean { return this.success; }
  isFailure(): boolean { return !this.success; }

  getValue(): T {
    if (!this.success) throw new Error("Cannot get value from failed result");
    return this.value!;
  }

  getError(): string {
    if (this.success) throw new Error("Cannot get error from successful result");
    return this.error!;
  }
}
```

---

## Anti-Patterns to Avoid

### Anemic Domain Model

```typescript
// BAD - No behavior, just data
export class User {
  id: string;
  name: string;
  email: string;
}

// GOOD - Rich domain model
export class User {
  private name: string;

  changeName(newName: string): void {
    if (newName.trim().length === 0) {
      throw new Error("Name cannot be empty");
    }
    this.name = newName;
  }
}
```

### Infrastructure Leaking into Domain

```typescript
// BAD - Domain depends on infrastructure
import { Pool } from "@db/postgres";

export class User {
  async save(pool: Pool): Promise<void> { /* ... */ }
}

// GOOD - Domain defines interface
export interface UserRepository {
  save(user: User): Promise<void>;
}
```

### Exposing Mutable State

```typescript
// BAD - Direct access to mutable array
export class Order {
  public lines: OrderLine[] = [];
}

// GOOD - Encapsulation with readonly
export class Order {
  private readonly lines: OrderLine[];

  getLines(): ReadonlyArray<OrderLine> {
    return this.lines;
  }
}
```

---

## Key Principles Summary

1. **Domain layer has no dependencies** - pure business logic
2. **Follow dependency flow** - dependencies point inward
3. **TypeScript-first** - No `any` types in production code
4. **Use value objects for immutable concepts**
5. **Entities have identity and lifecycle**
6. **Aggregates enforce invariants**
7. **Repositories are interfaces in domain**
8. **Use cases orchestrate, don't contain business rules**
9. **DTOs cross boundaries**
10. **Layer-specific error handling**
11. **Test domain logic in isolation**
12. **Encapsulate state**
13. **Use Result type for expected failures**
14. **Error translation at boundaries**

---

## Additional Resources

- **DDD Book (Eric Evans):** https://www.domainlanguage.com/ddd/
- **Implementing DDD (Vaughn Vernon):** https://vaughnvernon.com/
- **Martin Fowler's DDD:** https://martinfowler.com/tags/domain%20driven%20design.html
