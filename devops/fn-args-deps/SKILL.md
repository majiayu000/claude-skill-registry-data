---
name: fn-args-deps
description: "Enforce the fn(args, deps) pattern: functions over classes with explicit dependency injection"
version: 1.0.0
libraries: ["vitest-mock-extended"]
---

# Functions Over Classes: fn(args, deps)

## Core Pattern

All business logic functions MUST follow this signature:

```typescript
fn(args, deps)
```

- **args**: Per-call input data (varies each invocation)
- **deps**: Long-lived collaborators (injected infrastructure)

## Why Two Parameters (Not One Object)

`args` and `deps` have **different lifetimes**:
- `args` are per-call data
- `deps` are long-lived collaborators

Keeping them separate makes dependency bloat visible and composition easier.

## Required Behaviors

### 1. Per-Function Dependency Types

ALWAYS declare explicit deps types for each function:

```typescript
// CORRECT
type GetUserDeps = {
  db: Database;
  logger: Logger;
};

async function getUser(
  args: { userId: string },
  deps: GetUserDeps
): Promise<User | null> {
  deps.logger.info(`Getting user ${args.userId}`);
  return deps.db.findUser(args.userId);
}
```

```typescript
// WRONG - God object with all deps
async function getUser(
  args: { userId: string },
  deps: AllServiceDeps  // Contains mailer, cache, metrics that getUser doesn't use
): Promise<User | null>
```

### 2. No Classes for Business Logic

Classes become problematic when:
- 10+ methods accumulate over time
- Private helpers create implicit coupling via `this`
- Constructor grows to satisfy every method's needs

```typescript
// WRONG
class UserService {
  constructor(
    private db: Database,
    private logger: Logger,
    private mailer: Mailer,  // only createUser needs this
    private cache: Cache,     // only someOtherMethod needs this
  ) {}
}

// CORRECT
type GetUserDeps = { db: Database; logger: Logger };
type CreateUserDeps = { db: Database; logger: Logger; mailer: Mailer };
```

### 3. Factory at the Boundary (Composition Root)

Wire deps ONCE at the boundary, not at every call site:

```typescript
// user-service/index.ts
export function createUserService({ deps }: { deps: UserServiceDeps }) {
  return {
    getUser: ({ userId }: { userId: string }) =>
      getUser({ userId }, deps),
    createUser: ({ name, email }: { name: string; email: string }) =>
      createUser({ name, email }, deps),
  };
}

// main.ts (Composition Root)
const deps = { db, logger, mailer };
const userService = createUserService({ deps });

// Handlers stay clean
await userService.getUser({ userId: '123' });
```

### 4. Inject Only What You'll Mock

Only inject things that hit network, disk, or clock. Import pure utilities directly:

```typescript
// WRONG - Over-injecting
function createUser(args, deps: { db, logger, slugify, randomUUID }) { }

// CORRECT - Only inject what you'll mock
import { slugify } from 'slugify';
import { randomUUID } from 'crypto';
function createUser(args, deps: { db, logger }) { }
```

### 5. Type-Only Imports for Interfaces

Use `import type` to prevent runtime coupling:

```typescript
// CORRECT
import type { Mailer } from '../infra/mailer';

// WRONG - Runtime import creates coupling
import { mailer } from '../infra/mailer';
```

## Testing Pattern

```typescript
import { describe, it, expect } from 'vitest';
import { mock } from 'vitest-mock-extended';
import { getUser, type GetUserDeps } from './get-user';

it('returns user when found', async () => {
  const mockUser = { id: '123', name: 'Alice', email: 'alice@test.com' };

  const deps = mock<GetUserDeps>();
  deps.db.findUser.mockResolvedValue(mockUser);

  const result = await getUser({ userId: '123' }, deps);
  expect(result).toEqual(mockUser);
});
```

## Migration Strategy (Strangler Fig)

### Phase 1: Add deps with defaults (backward compatible)
```typescript
import { mailer as _mailer, type Mailer } from '../infra/mailer';

const defaultDeps: SendEmailDeps = { mailer: _mailer };

export async function sendEmail(
  recipient: User,
  sender: User,
  deps: SendEmailDeps = defaultDeps  // Default for existing callers
) { ... }
```

### Phase 2: Remove defaults (explicit DI required)
```typescript
import type { Mailer } from '../infra/mailer';

export async function sendEmail(
  recipient: User,
  sender: User,
  deps: SendEmailDeps  // No default - must inject
) { ... }
```

### Phase 3 (Optional): Use object parameters
```typescript
export async function sendEmail(
  args: { recipient: User; sender: User },
  deps: SendEmailDeps
) { ... }
```

## When Classes ARE Acceptable

Classes are fine for:

| Use Case | Why It's OK |
|----------|-------------|
| **Framework integration** | NestJS, Express middleware require class syntax |
| **Stateful resources** | Connection pools, caches with lifecycle |
| **Builder patterns** | Fluent APIs where method chaining adds clarity |
| **Thin wrappers** | Delegating to pure functions (see below) |

Classes are NOT OK for:
- Business logic (use functions)
- Anything that will grow beyond 3-4 methods
- When you find yourself adding private helpers

## Framework Integration (NestJS)

Use classes as thin wrappers, keep logic in pure functions:

```typescript
// Pure function - your actual logic
async function createUser(
  args: CreateUserInput,
  deps: { db: Database; logger: Logger }
): Promise<Result<User, 'EMAIL_EXISTS' | 'DB_ERROR'>> {
  // Business logic here
}

// NestJS wrapper - thin delegation layer
@Injectable()
export class UserService {
  constructor(private db: Database, private logger: Logger) {}

  async createUser(args: CreateUserInput) {
    return createUser(args, { db: this.db, logger: this.logger });
  }
}
```

## Performance Considerations

Critics sometimes worry that creating many small objects (`args` objects, `deps` bags, factory functions) increases garbage collection pressure.

**The reality:** Modern V8 engines (Orinoco) use generational garbage collection. Objects that die young—like the temporary objects created during request handling—are reclaimed almost instantly. V8 is *extremely* efficient at this.

For I/O-bound web applications:

| Operation | Typical Latency |
|-----------|-----------------|
| Database query | 1-50ms |
| HTTP request | 10-500ms |
| Object allocation | 0.0001ms |

The database query is 10,000-500,000x slower than object allocation. The architectural clarity and type safety of the `fn(args, deps)` pattern far outweigh any micro-overhead.

**When to worry about allocation:**
- Tight loops processing millions of items
- Real-time systems with hard latency requirements
- Memory-constrained embedded environments

For typical web services, **don't optimize for GC**. Optimize for correctness, testability, and maintainability.

## Enforcement

Enable in tsconfig.json:
```json
{
  "compilerOptions": {
    "verbatimModuleSyntax": true
  }
}
```

ESLint rule to prevent infra imports:
```javascript
"no-restricted-imports": ["error", {
  patterns: [{
    group: ["**/infra/**"],
    message: "Domain code must not import from infra. Inject dependencies instead."
  }]
}]
```
