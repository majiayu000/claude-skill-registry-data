---
name: error-handling-patterns
description: Production-grade error handling for Node.js/TypeScript backends. Error classes, HTTP mapping, logging, retry strategies.
type: pattern
tier: library
domains: [backend, api]
trigger: "error handling, exception, try catch, error class, HTTP error, retry, circuit breaker"
---

## Error Class Hierarchy

```typescript
// Base application error
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Domain-specific errors
export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404, { resource, id });
  }
}

export class ValidationError extends AppError {
  constructor(field: string, message: string) {
    super(message, 'VALIDATION_ERROR', 400, { field });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401);
  }
}

export class ConflictError extends AppError {
  constructor(resource: string) {
    super(`${resource} already exists`, 'CONFLICT', 409, { resource });
  }
}
```

## Express Error Middleware

```typescript
// Always the LAST middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        ...(process.env.NODE_ENV === 'development' ? { context: err.context } : {}),
      },
    });
  }

  // Unexpected error — log and return 500
  console.error('Unexpected error:', err);
  return res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' },
  });
});
```

## Async Handler Wrapper

```typescript
// Eliminates try/catch boilerplate in route handlers
export const asyncHandler = (fn: RequestHandler): RequestHandler =>
  (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

// Usage
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  if (!user) throw new NotFoundError('User', req.params.id);
  res.json(user);
}));
```

## Retry Pattern

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  { maxAttempts = 3, delay = 100, backoff = 2 } = {}
): Promise<T> {
  let lastError: Error;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err as Error;
      if (attempt === maxAttempts) break;
      await new Promise(r => setTimeout(r, delay * backoff ** (attempt - 1)));
    }
  }
  throw lastError!;
}

// Usage
const user = await withRetry(() => db.user.findUnique({ where: { id } }));
```

## Result Type (No-throw Alternative)

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

async function safeGetUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.user.findUnique({ where: { id } });
    if (!user) return { ok: false, error: new NotFoundError('User', id) };
    return { ok: true, value: user };
  } catch (err) {
    return { ok: false, error: err as Error };
  }
}
```

## Checklist

- [ ] All error types extend AppError
- [ ] HTTP status codes correctly mapped (400 client, 500 server)
- [ ] Unexpected errors logged with context
- [ ] Async routes wrapped (no unhandled rejections)
- [ ] Sensitive data NOT in error responses (no stack traces in prod)
