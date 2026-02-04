---
name: ddd-entity-generator
description: Generate domain layer components (entities, value objects, repository interfaces, events, errors). Use when adding entities to existing context, creating value objects for validation, or defining domain-specific errors (e.g., "Create Product entity with Price VO", "Add Customer with Email").
allowed-tools: Read, Write, Edit, Glob, Grep
---

# DDD Entity Generator

Generate domain layer components including entities, value objects, repository interfaces, domain events, and errors following Domain-Driven Design principles.

## What This Skill Does

Creates pure business logic components for the domain layer with zero framework dependencies:

- **Entities**: Business objects with identity, factory methods, and encapsulation
- **Value Objects**: Immutable, validated value types (Email, Money, PhoneNumber, etc.)
- **Repository Interfaces**: Data persistence contracts returning domain entities
- **Domain Events**: Immutable event classes for state changes
- **Domain Errors**: Business-specific error types with error codes

## When to Use This Skill

Use when you need to:
- Add new entities to an existing context
- Create value objects for validation and type safety
- Define repository interfaces for data access
- Add domain events for event-driven architecture
- Create domain-specific errors

Examples:
- "Create a Product entity with Price and SKU value objects"
- "Generate a Customer entity with Email and PhoneNumber"
- "Add an Order entity with OrderLine value objects"

## Key Patterns

### Entity Pattern
```typescript
export class EntityName {
  private constructor(
    private readonly id: string,
    private name: string,
    private readonly createdAt: Date,
    private updatedAt: Date
  ) {}

  static create(data: CreateData): EntityName {
    const id = randomUUID();
    const now = new Date();
    const entity = new EntityName(id, data.name, now, now);
    entity.validate();
    return entity;
  }

  static reconstitute(data: PersistedData): EntityName {
    return new EntityName(
      data.id,
      data.name,
      data.createdAt,
      data.updatedAt
    );
  }

  getId(): string { return this.id; }
  getName(): string { return this.name; }

  changeName(newName: string): void {
    this.name = newName;
    this.updatedAt = new Date();
  }

  private validate(): void {
    if (!this.name) throw new InvalidDataError('Name required');
  }
}
```

### Value Object Pattern
```typescript
export class Email {
  private readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  static create(value: string): Email {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      throw new InvalidEmailError(value);
    }
    return new Email(value.toLowerCase());
  }

  getValue(): string {
    return this.value;
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}
```

### Repository Interface Pattern
```typescript
export interface IEntityRepository {
  save(entity: EntityName): Promise<void>;
  findById(id: string): Promise<EntityName | null>;
  findByEmail(email: Email): Promise<EntityName | null>;
  findAll(limit?: number, offset?: number): Promise<EntityName[]>;
  delete(id: string): Promise<void>;
  exists(id: string): Promise<boolean>;
}
```

### Domain Event Pattern
```typescript
export class EntityCreated {
  constructor(
    public readonly entityId: string,
    public readonly name: string,
    public readonly timestamp: Date = new Date()
  ) {}
}
```

### Domain Error Pattern
```typescript
export class DomainError extends Error {
  constructor(
    message: string,
    public readonly code: string
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class EntityNotFoundError extends DomainError {
  constructor(id: string) {
    super(`Entity with ID '${id}' not found`, 'ENTITY_NOT_FOUND');
  }
}
```

## Critical Rules

**MUST DO:**
- Private constructor for entities
- Static `create()` and `reconstitute()` methods
- Getters for all properties (no public properties)
- Value objects must be immutable (readonly)
- Validation in static factory methods
- Zero framework dependencies
- No database annotations
- Repository interfaces (not implementations)

**MUST NOT:**
- Import framework code (Mongoose, Elysia, etc.)
- Use `any` types
- Make constructors public
- Use mutable value objects
- Add database annotations to entities
- Implement repositories in domain layer

## Generated Files

```
/src/contexts/{Context}/domain/
├── entities/
│   └── {entity}.entity.ts
├── value-objects/
│   ├── email.vo.ts
│   ├── phone-number.vo.ts
│   └── {custom}.vo.ts
├── repositories/
│   └── {entity}.repository.interface.ts
├── events/
│   ├── {entity}-created.event.ts
│   ├── {entity}-updated.event.ts
│   └── {entity}-deleted.event.ts
├── errors/
│   └── {context}.errors.ts
└── index.ts
```

## Common Value Objects

The skill can generate these common value objects:
- **Email**: Email validation with lowercase normalization
- **PhoneNumber**: Phone number validation
- **Money**: Amount + currency with arithmetic operations
- **Address**: Street, city, state, zip validation
- **DateRange**: Start/end date validation
- **URL**: URL validation
- **UUID**: UUID validation

## Validation Checklist

After generation, verify:
- [ ] Entities have private constructor
- [ ] Static `create()` and `reconstitute()` methods present
- [ ] All properties accessed via getters
- [ ] Value objects are immutable (readonly)
- [ ] Validation logic in factory methods
- [ ] No framework imports
- [ ] No database annotations
- [ ] Repository interfaces defined (not implementations)
- [ ] Domain events immutable
- [ ] Error codes included in domain errors

## Integration

Update the domain barrel export (`domain/index.ts`):
```typescript
export * from './entities/{entity}.entity';
export * from './value-objects/{vo}.vo';
export * from './repositories/{entity}.repository.interface';
export * from './errors/{context}.errors';
export * from './events/{entity}.events';
```

## Related Skills

- **ddd-context-generator**: Generate complete bounded context
- **ddd-usecase-generator**: Generate use cases using these entities
- **ddd-validator**: Validate domain layer compliance