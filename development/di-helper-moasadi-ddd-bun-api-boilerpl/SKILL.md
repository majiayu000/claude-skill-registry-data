---
name: di-helper
description: Manage tsyringe DI container registration, scan injectable classes, detect missing registrations, validate injection patterns, and generate registration code. Use when registering repositories, fixing DI errors, or setting up new context (e.g., "Register ProductRepository", "Check DI setup").
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Dependency Injection Helper

Manage tsyringe dependency injection container registration. Scans for injectable classes, detects missing registrations, validates injection patterns, and generates ready-to-use registration code.

## What This Skill Does

Comprehensive DI container management:

- **Scan Injectable Classes**: Find all `@injectable()` decorated classes
- **Detect Missing Registrations**: Compare found vs registered
- **Validate Injection Patterns**: Check token vs class injection
- **Generate Registration Code**: Ready-to-paste code with imports
- **Event Listener Registration**: Check event bus setup
- **Route Registration**: Verify route module registration

## When to Use This Skill

Use when you need to:
- Register new repositories after creation
- Set up DI for new context
- Fix DI resolution errors
- Verify all injectable classes are registered
- Generate registration boilerplate

Examples:
- "Help me register the ProductRepository"
- "Check if all repositories are registered"
- "Generate DI registration for User context"
- "Verify event listener registration"

## Dependency Injection Patterns

### Repositories: Singleton with Token

```typescript
// In /src/global/container/container.ts
import type { IUserRepository } from '@/contexts/user/domain';
import { UserRepository } from '@/contexts/user/infrastructure/repositories/user.repository';

container.registerSingleton<IUserRepository>(
  'IUserRepository',  // String token
  UserRepository      // Implementation class
);
```

### Use Cases: Auto-registered

Use cases are automatically registered by tsyringe when decorated with `@injectable()`:

```typescript
@injectable()
export class CreateUserUseCase {
  // No explicit registration needed
}
```

### Controllers: Auto-registered

Controllers are auto-registered like use cases:

```typescript
@injectable()
export class UserController {
  // No explicit registration needed
}
```

### Event Listeners: Manual Registration

Listeners must be resolved and registered with event bus:

```typescript
// In /src/main.ts
import { UserCreatedListener } from '@/contexts/user/application';

const listener = container.resolve(UserCreatedListener);
eventBus.on('UserCreated', listener.handle.bind(listener));
```

## Injection Patterns

### Repository Injection (by token)

```typescript
constructor(
  @inject('IUserRepository')
  private readonly userRepo: IUserRepository
) {}
```

### UseCase Injection (by class)

```typescript
constructor(
  @inject(CreateUserUseCase)
  private readonly createUser: CreateUserUseCase
) {}
```

## Validation Checks

### Missing `@injectable()` Decorator

**Scans for classes that should be injectable:**

```
MISSING: @injectable() decorator
File: src/contexts/user/infrastructure/repositories/user.repository.ts:5
Issue: UserRepository missing @injectable() decorator
Fix: Add decorator:

import { injectable } from 'tsyringe';

@injectable()
export class UserRepository implements IUserRepository {
```

### Missing Repository Registration

**Compares found vs registered repositories:**

```
MISSING: UserRepository not registered
File: src/contexts/user/infrastructure/repositories/user.repository.ts
Required: Add to /src/global/container/container.ts

import type { IUserRepository } from '@/contexts/user/domain';
import { UserRepository } from '@/contexts/user/infrastructure/repositories/user.repository';

container.registerSingleton<IUserRepository>(
  'IUserRepository',
  UserRepository
);
```

### Wrong Injection Pattern

**Checks constructor injection:**

```
ERROR: Wrong repository injection pattern
File: src/contexts/user/application/usecases/create-user.usecase.ts:12
Issue: Repository injected by class instead of token
Current:
  @inject(UserRepository)
  private repo: IUserRepository

Fix:
  @inject('IUserRepository')
  private repo: IUserRepository
```

### Missing Event Listener Registration

**Checks main.ts for event listener setup:**

```
MISSING: UserCreatedListener not registered
File: src/contexts/user/application/listeners/user-created.listener.ts
Required: Add to /src/main.ts

import { UserCreatedListener } from '@/contexts/user/application';

const userCreatedListener = container.resolve(UserCreatedListener);
eventBus.on('UserCreated', userCreatedListener.handle.bind(userCreatedListener));
```

### Missing Route Registration

**Checks main.ts for route registration:**

```
MISSING: User routes not registered
File: src/contexts/user/presentation/user.routes.ts
Required: Add to /src/main.ts

import { registerUserRoutes } from '@/contexts/user/presentation/user.routes';

app.use(registerUserRoutes());
```

### Unused Registrations

**Finds registrations without implementations:**

```
WARNING: Unused registration
File: src/global/container/container.ts:15
Registration: 'IProductRepository' → ProductRepository
Issue: ProductRepository class not found
Action: Remove registration or implement the class
```

## Generated Registration Code

### Complete Container Setup

```typescript
// /src/global/container/container.ts
import 'reflect-metadata';
import { container } from 'tsyringe';

// User context
import type { IUserRepository } from '@/contexts/user/domain';
import { UserRepository } from '@/contexts/user/infrastructure/repositories/user.repository';

// Product context
import type { IProductRepository } from '@/contexts/product/domain';
import { ProductRepository } from '@/contexts/product/infrastructure/repositories/product.repository';

// Order context
import type { IOrderRepository } from '@/contexts/order/domain';
import { OrderRepository } from '@/contexts/order/infrastructure/repositories/order.repository';

export const registerDependencies = (): void => {
  // User repositories
  container.registerSingleton<IUserRepository>(
    'IUserRepository',
    UserRepository
  );

  // Product repositories
  container.registerSingleton<IProductRepository>(
    'IProductRepository',
    ProductRepository
  );

  // Order repositories
  container.registerSingleton<IOrderRepository>(
    'IOrderRepository',
    OrderRepository
  );
};
```

### Event Listener Registration

```typescript
// Add to /src/main.ts after DI setup

// Event listener imports
import { UserCreatedListener } from '@/contexts/user/application';
import { UserUpdatedListener } from '@/contexts/user/application';
import { ProductCreatedListener } from '@/contexts/product/application';
import { OrderPlacedListener } from '@/contexts/order/application';

// Event listener registration
const userCreatedListener = container.resolve(UserCreatedListener);
eventBus.on('UserCreated', userCreatedListener.handle.bind(userCreatedListener));

const userUpdatedListener = container.resolve(UserUpdatedListener);
eventBus.on('UserUpdated', userUpdatedListener.handle.bind(userUpdatedListener));

const productCreatedListener = container.resolve(ProductCreatedListener);
eventBus.on('ProductCreated', productCreatedListener.handle.bind(productCreatedListener));

const orderPlacedListener = container.resolve(OrderPlacedListener);
eventBus.on('OrderPlaced', orderPlacedListener.handle.bind(orderPlacedListener));
```

### Route Registration

```typescript
// Add to /src/main.ts

// Route imports
import { registerUserRoutes } from '@/contexts/user/presentation/user.routes';
import { registerProductRoutes } from '@/contexts/product/presentation/product.routes';
import { registerOrderRoutes } from '@/contexts/order/presentation/order.routes';

// Route registration
app.use(registerUserRoutes());
app.use(registerProductRoutes());
app.use(registerOrderRoutes());
```

## Validation Checklist

The skill checks:

- [ ] All repositories have `@injectable()`
- [ ] All use cases have `@injectable()`
- [ ] All controllers have `@injectable()`
- [ ] All event listeners have `@injectable()`
- [ ] Repositories registered as singleton
- [ ] Correct interface tokens used
- [ ] Type parameters included
- [ ] Event listeners resolved and registered
- [ ] Routes imported and registered
- [ ] No unused registrations

## Common Issues

### Missing Decorator

```typescript
// ❌ WRONG
export class UserRepository implements IUserRepository {
  // Missing @injectable()
}

// ✅ CORRECT
import { injectable } from 'tsyringe';

@injectable()
export class UserRepository implements IUserRepository {
```

### Wrong Registration

```typescript
// ❌ WRONG - Using class as token
container.registerSingleton<IUserRepository>(
  IUserRepository,  // Wrong: class
  UserRepository
);

// ✅ CORRECT - Using string token
container.registerSingleton<IUserRepository>(
  'IUserRepository',  // Correct: string
  UserRepository
);
```

### Wrong Injection

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

### Missing Event Listener Binding

```typescript
// ❌ WRONG - Not binding
eventBus.on('UserCreated', listener.handle);

// ✅ CORRECT - Binding
eventBus.on('UserCreated', listener.handle.bind(listener));
```

## Report Format

1. **Summary**: Injectable classes found by type
2. **Missing Decorators**: Classes needing `@injectable()`
3. **Missing Registrations**: Unregistered repositories
4. **Wrong Patterns**: Injection pattern violations
5. **Unused Registrations**: Dead code to remove
6. **Generated Code**: Complete, ready-to-use registration code

## Integration Steps

After getting the generated code:

1. **Update container.ts**: Copy repository registrations
2. **Update main.ts**: Add event listener registrations
3. **Update main.ts**: Add route registrations
4. **Test**: Run application and verify resolution works

## Related Skills

- **ddd-context-generator**: Generates code needing registration
- **ddd-validator**: Validates DI decorator usage
- **ddd-usecase-generator**: Creates use cases needing registration