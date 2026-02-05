---
name: ddd-validator
description: Validate DDD architecture compliance including layer separation, dependency rules, and patterns. Use when validating context before commit, checking new features, reviewing refactored code, or ensuring layer isolation (e.g., "Validate User context", "Check Product domain layer").
allowed-tools: Read, Glob, Grep
---

# DDD Architecture Validator

Validate Domain-Driven Design layer separation, dependency rules, and architectural patterns. Non-destructive analysis providing actionable recommendations.

## What This Skill Does

Performs comprehensive analysis of DDD architecture:

- **Dependency Rule Validation**: Checks layer isolation and dependencies
- **Domain Layer Purity**: Ensures zero framework dependencies
- **Pattern Compliance**: Validates entities, value objects, repositories
- **Decorator Validation**: Checks `@injectable()` usage
- **Import Analysis**: Detects unauthorized dependencies

## When to Use This Skill

Use when you need to:
- Validate architecture before committing code
- Check new features for DDD compliance
- Review refactored code
- Ensure layer separation

Examples:
- "Validate the User context for DDD compliance"
- "Check if my Product domain layer has any violations"
- "Analyze Order context for dependency rule violations"

## Dependency Rule

The validator enforces this hierarchy:

```
Presentation → Application → Domain
      ↓            ↓
  Infrastructure
```

**Rules:**
- Domain has ZERO external dependencies
- Application depends only on Domain
- Infrastructure implements Domain interfaces
- Presentation depends on Application and Domain

## Validation Checks

### Domain Layer Checks

**Zero Dependencies:**
- ❌ No Mongoose, Elysia, tsyringe imports
- ❌ No infrastructure imports
- ❌ No application imports
- ✅ Only domain files and Node.js built-ins

**Entity Patterns:**
- ✅ Private constructor
- ✅ Static `create()` method
- ✅ Static `reconstitute()` method
- ✅ Getters for properties
- ❌ No public properties
- ❌ No database annotations

**Value Object Patterns:**
- ✅ Immutable (readonly properties)
- ✅ Private constructor
- ✅ Static `create()` with validation
- ✅ `equals()` method
- ❌ No mutable properties

**Repository Interfaces:**
- ✅ Interface (not class)
- ✅ Returns domain entities
- ✅ Uses domain types
- ❌ No implementation details
- ❌ No database-specific methods

### Application Layer Checks

**UseCase Patterns:**
- ✅ `@injectable()` decorator present
- ✅ Repositories injected with string token
- ✅ Use cases injected by class
- ✅ Single `execute()` method
- ❌ No HTTP concerns
- ✅ Emits domain events

**Import Restrictions:**
- ✅ Can import Domain layer
- ✅ Can import tsyringe for DI
- ✅ Can import global utilities
- ❌ Cannot import Infrastructure
- ❌ Cannot import Presentation

### Infrastructure Layer Checks

**Repository Implementations:**
- ✅ Implements domain interface
- ✅ `@injectable()` decorator
- ✅ Uses mapper for conversions
- ❌ Never exposes persistence details

**Mapper Patterns:**
- ✅ Static `toDomain()` method
- ✅ Static `toPersistence()` method
- ❌ No business logic

### Presentation Layer Checks

**Controller Patterns:**
- ✅ `@injectable()` decorator
- ✅ Injects use cases (not repositories)
- ✅ Maps domain errors to HttpException
- ❌ No business logic
- ✅ Returns plain objects

**Route Patterns:**
- ✅ Versioned with `/v1/`
- ✅ Controller methods bound with `.bind()`
- ✅ Zod schemas applied
- ✅ Swagger metadata present

## Report Format

### Critical Issues (Must Fix)

Violations that break core DDD principles:

```
CRITICAL: Domain importing framework dependency
File: src/contexts/user/domain/entities/user.entity.ts:3
Issue: Importing 'injectable' from tsyringe in domain layer
Fix: Remove @injectable() from entity. Only use in application/infrastructure/presentation.

CRITICAL: Public entity constructor
File: src/contexts/user/domain/entities/user.entity.ts:10
Issue: Constructor is public, should be private
Fix: Change to private constructor with static factory methods
```

### Warnings (Should Fix)

Deviations from best practices:

```
WARNING: Missing reconstitute method
File: src/contexts/user/domain/entities/user.entity.ts
Issue: Only create() found, missing reconstitute()
Recommendation: Add static reconstitute() for loading from database
```

### Suggestions (Nice to Have)

Improvements:

```
SUGGESTION: Extract Email into value object
File: src/contexts/user/domain/entities/user.entity.ts:15
Current: Using string for email
Recommendation: Create Email value object with validation
```

## Common Violations

### Domain Layer Issues

**Framework Imports:**
```typescript
// ❌ WRONG
import { injectable } from 'tsyringe';
import { Schema } from 'mongoose';

// ✅ CORRECT
import { randomUUID } from 'crypto';
import { Email } from '../value-objects/email.vo';
```

**Public Constructor:**
```typescript
// ❌ WRONG
export class User {
  constructor(public id: string, public name: string) {}
}

// ✅ CORRECT
export class User {
  private constructor(
    private readonly id: string,
    private name: string
  ) {}

  static create(data: CreateData): User { ... }
  static reconstitute(data: PersistedData): User { ... }
}
```

**Mutable Value Object:**
```typescript
// ❌ WRONG
export class Email {
  private value: string; // Not readonly
}

// ✅ CORRECT
export class Email {
  private readonly value: string;
}
```

### Application Layer Issues

**Wrong Injection Pattern:**
```typescript
// ❌ WRONG - Repository by class
constructor(
  @inject(UserRepository)
  private repo: IUserRepository
) {}

// ✅ CORRECT - Repository by token
constructor(
  @inject('IUserRepository')
  private repo: IUserRepository
) {}
```

**HTTP Concerns:**
```typescript
// ❌ WRONG
async execute(input: Input): Promise<Output> {
  throw new HttpException(404, 'Not found');
}

// ✅ CORRECT
async execute(input: Input): Promise<Output> {
  throw new EntityNotFoundError(id);
}
```

### Presentation Layer Issues

**Controller Injecting Repository:**
```typescript
// ❌ WRONG
constructor(
  @inject('IUserRepository')
  private repo: IUserRepository
) {}

// ✅ CORRECT
constructor(
  @inject(CreateUserUseCase)
  private createUser: CreateUserUseCase
) {}
```

**Not Binding Controller:**
```typescript
// ❌ WRONG
.post('/', controller.create)

// ✅ CORRECT
.post('/', controller.create.bind(controller))
```

## Output Format

1. **Summary**: Scope of validation
2. **Structure**: Directory verification
3. **Critical Issues**: With file:line references and fixes
4. **Warnings**: With recommendations
5. **Suggestions**: With improvements
6. **Compliance Score**: Percentage of rules passed

## Integration

The validator is read-only - it never modifies code. After review:

1. Fix critical issues first
2. Address warnings when possible
3. Consider suggestions for improvements
4. Re-run validator to verify fixes

## Related Skills

- **api-validator**: Validate API design standards
- **di-helper**: Check dependency injection setup
- **ddd-context-generator**: Generate compliant code