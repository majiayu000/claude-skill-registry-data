---
name: result-types
description: "Never throw for expected failures. Use Result<T, E> types with explicit error handling and workflow composition."
version: 1.0.0
libraries: ["@jagreehal/workflow"]
---

# Typed Errors: Never Throw

## Core Principle

Exceptions are invisible, bypass composition, and conflate different failures. Return `Result<T, E>` instead.

```typescript
// WRONG - Signature lies
async function getUser(args): Promise<User> {
  const user = await deps.db.findUser(args.userId);
  if (!user) throw new Error('User not found');  // Hidden!
  return user;
}

// CORRECT - Signature tells the truth
async function getUser(args, deps): Promise<Result<User, 'NOT_FOUND' | 'DB_ERROR'>> {
  try {
    const user = await deps.db.findUser(args.userId);
    return user ? ok(user) : err('NOT_FOUND');
  } catch {
    return err('DB_ERROR');
  }
}
```

## The Result Type

```typescript
type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

type AsyncResult<T, E> = Promise<Result<T, E>>;

const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
const err = <E>(error: E): Result<never, E> => ({ ok: false, error });
```

## Required Behaviors

### 1. Business Functions Return Results

```typescript
async function getUser(
  args: { userId: string },
  deps: GetUserDeps
): Promise<Result<User, 'NOT_FOUND' | 'DB_ERROR'>> {
  try {
    const user = await deps.db.findUser(args.userId);
    if (!user) return err('NOT_FOUND');
    return ok(user);
  } catch {
    return err('DB_ERROR');
  }
}
```

### 2. Use createWorkflow() for Composition

Avoid verbose if-checking with railway-oriented programming:

```typescript
import { createWorkflow } from '@jagreehal/workflow';

// Declare dependencies -> error union computed automatically
const loadUserData = createWorkflow({ getUser, getPosts, enrichUser });

const result = await loadUserData(async (step) => {
  const user = await step(() => getUser({ userId }, deps));
  const posts = await step(() => getPosts({ userId: user.id }, deps));
  const enriched = await step(() => enrichUser({ user, posts }, deps));

  return { user: enriched };
});

// result: Result<{ user: EnrichedUser }, 'NOT_FOUND' | 'DB_ERROR' | 'FETCH_ERROR' | ...>
```

The `step()` function:
- Unwraps `ok` results and continues on happy path
- On `err`, immediately short-circuits and skips remaining steps

### 3. Use step.try() for Throwing Code

Bridge between throwing code and Result pipeline:

```typescript
const workflow = createWorkflow({ getUser });

const result = await workflow(async (step) => {
  const user = await step(() => getUser({ userId }, deps));

  // Throwing function: use step.try() with error mapping
  const config = await step.try(
    () => JSON.parse(user.configJson),
    { error: 'INVALID_CONFIG' as const }
  );

  return { user, config };
});
```

- `step()`: For functions that already return Result (your code)
- `step.try()`: For functions that throw (third-party, built-in)
- `step.fromResult()`: For Result-returning functions where you need to map errors

**For Result-returning functions:** Use `step.fromResult()` to preserve typed errors:

```typescript
// callProvider returns Result<Response, ProviderError>
const callProvider = async (input: string): AsyncResult<Response, ProviderError> => { ... };

const response = await step.fromResult(
  () => callProvider(input),
  {
    onError: (e) => ({
      type: 'PROVIDER_FAILED' as const,
      provider: e.provider,  // TypeScript knows e is ProviderError
      code: e.code,
    })
  }
);
```

### 4. Map Results to HTTP at Boundary

```typescript
const errorToStatus: Record<string, number> = {
  NOT_FOUND: 404,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  VALIDATION_FAILED: 400,
  CONFLICT: 409,
};

function resultToResponse<T, E extends string>(
  result: Result<T, E>,
  res: Response
): Response {
  if (result.ok) {
    return res.status(200).json(result.value);
  }

  const status = errorToStatus[result.error] ?? 500;
  return res.status(status).json({
    error: result.error,
    code: result.error,
  });
}

// Handler becomes simple
app.get('/users/:id', async (req, res) => {
  const result = await getUser({ userId: req.params.id }, deps);
  return resultToResponse(result, res);
});
```

### 5. Exhaustive Error Handling

TypeScript enforces handling all error cases:

```typescript
if (!result.ok) {
  switch (result.error) {
    case 'NOT_FOUND':
      return res.status(404).json({ error: 'User not found' });
    case 'DB_ERROR':
    case 'FETCH_ERROR':
      return res.status(500).json({ error: 'Internal error' });
    // TypeScript will error if you miss a case!
  }
}
```

## Error Type Patterns

### String Literals (Simple)

```typescript
type AppError = 'NOT_FOUND' | 'UNAUTHORIZED' | 'DB_ERROR';
```

### Discriminated Unions (Rich)

```typescript
type AppError =
  | { type: 'NOT_FOUND'; resource: string }
  | { type: 'VALIDATION'; field: string; message: string }
  | { type: 'DB_ERROR'; query: string };
```

### Const Objects (Runtime + Type)

```typescript
const Errors = {
  NOT_FOUND: 'NOT_FOUND',
  DB_ERROR: 'DB_ERROR',
} as const;

type AppError = (typeof Errors)[keyof typeof Errors];

return err(Errors.NOT_FOUND);  // Runtime value available
```

## Error Grouping at Scale

As applications grow, error unions become unwieldy:

```typescript
// This becomes a "Type Wall"
type AllErrors =
  | 'NOT_FOUND'
  | 'DB_ERROR'
  | 'DB_CONNECTION_FAILED'
  | 'DB_TIMEOUT'
  | 'FETCH_ERROR'
  | 'HTTP_TIMEOUT'
  | 'RATE_LIMITED'
  | 'CIRCUIT_OPEN'
  | 'VALIDATION_FAILED'
  // ... 20 more errors
```

**Solution:** Group related errors into categories:

```typescript
// Group by domain
type DatabaseError = 'DB_ERROR' | 'DB_CONNECTION_FAILED' | 'DB_TIMEOUT';
type NetworkError = 'FETCH_ERROR' | 'HTTP_TIMEOUT' | 'RATE_LIMITED';
type BusinessError = 'NOT_FOUND' | 'VALIDATION_FAILED' | 'UNAUTHORIZED';

type AppError = DatabaseError | NetworkError | BusinessError;

// Or use discriminated unions for richer context
type AppError =
  | { type: 'DATABASE'; code: 'CONNECTION_FAILED' | 'TIMEOUT' | 'QUERY_FAILED' }
  | { type: 'NETWORK'; code: 'TIMEOUT' | 'RATE_LIMITED' | 'UNREACHABLE' }
  | { type: 'BUSINESS'; code: 'NOT_FOUND' | 'VALIDATION_FAILED' };
```

This keeps error types manageable while preserving type safety.

## When Throwing Is Still Right

Throw only for:
- **Invariant violation** (programmer error, impossible state)
- **Corrupted process state** (can't recover)
- **Truly unrecoverable** situations

```typescript
// Good: throw for impossible states
if (!user) throw new Error('Unreachable: user should exist after insert');
```

### Using `asserts` for Type Narrowing

The `asserts` keyword creates runtime checks that also narrow types:

```typescript
// Assert function: throws if condition fails, narrows type if succeeds
function assertUser(user: User | null): asserts user is User {
  if (!user) throw new Error('Invariant violated: user must exist');
}

function assertDefined<T>(value: T | undefined, name: string): asserts value is T {
  if (value === undefined) throw new Error(`${name} must be defined`);
}

// Usage: TypeScript narrows the type after the assertion
const user = await deps.db.findUser(userId);
assertUser(user);  // Throws if null
// TypeScript now knows `user` is `User`, not `User | null`
console.log(user.name);  // Safe access
```

**When to use `asserts`:**
- After database inserts (record MUST exist)
- After config loading (values MUST be present)
- After state transitions (state MUST be valid)

**Don't use for:** Normal business logic failures (use Result instead)

## Quick Reference

| Situation | Use |
|-----------|-----|
| Domain failure (not found, validation) | Result |
| Infrastructure failure (recoverable) | Result |
| Programmer error | throw |
| Corrupted state | throw |

## Architecture Layer

```
Handlers / Routes
  -> map Result -> HTTP response

Business Logic
  -> createWorkflow({ ... })(async (step) => { ... })

Core Functions
  -> fn(args, deps): Result<T, E>

Infrastructure
  -> catch exceptions, return Results
```
