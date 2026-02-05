---
name: resilience
description: "Add retry, timeout, and circuit breaker patterns at the workflow level. Business functions stay clean."
version: 1.0.0
libraries: ["@jagreehal/workflow"]
---

# Resilience Patterns

## Core Principle

Resilience is a **composition concern**, not a business logic concern. Add retry/timeout at the workflow level, not inside functions.

```
Workflows
  -> step.retry() and step.withTimeout()
  -> (resilience here)

Business Functions
  -> fn(args, deps): Result<T, E>
  -> (no retry logic here)

Infrastructure
  -> pg, redis, http
  -> (just transport)
```

## Required Behaviors

### 1. Retry at Workflow Level Only

NEVER add retry logic inside business functions:

```typescript
// WRONG - Retry inside function
async function getUser(args, deps) {
  let attempts = 0;
  while (attempts < 3) {
    try {
      return await deps.db.findUser(args.userId);
    } catch { attempts++; }
  }
}

// CORRECT - Clean function, workflow handles retry
async function getUser(args, deps) {
  const user = await deps.db.findUser(args.userId);
  return user ? ok(user) : err('NOT_FOUND');
}

// Workflow adds resilience
const result = await workflow(async (step) => {
  const user = await step.retry(
    () => getUser({ userId }, deps),
    { attempts: 3, backoff: 'exponential' }
  );
  return user;
});
```

### 2. Never Double-Retry

Retry at ONE level only. Multiple layers create retry explosion:

```
3 (API) × 3 (Service) × 3 (DB Client) = 27 attempts!
```

This DDoS's your own infrastructure.

### 3. Only Retry Transient Errors

| Error Type | Retry? | Why |
|-----------|--------|-----|
| `TIMEOUT` | Yes | Transient |
| `CONNECTION_ERROR` | Yes | Network hiccup |
| `RATE_LIMITED` | Yes | Wait and retry |
| `NOT_FOUND` | NO | Resource doesn't exist |
| `UNAUTHORIZED` | NO | Credentials wrong |
| `VALIDATION_FAILED` | NO | Input invalid |

```typescript
const data = await step.retry(
  () => fetchFromApi(),
  {
    attempts: 3,
    retryOn: (error) => {
      const retryable = ['TIMEOUT', 'CONNECTION_ERROR', 'RATE_LIMITED'];
      return retryable.includes(error);
    },
  }
);
```

### 4. Never Retry Non-Idempotent Writes

```typescript
// DANGEROUS - May double-charge
await step.retry(() => chargeCard(amount), { attempts: 3 });

// SAFE - Read is idempotent
await step.retry(() => getUser(userId), { attempts: 3 });

// SAFE - With idempotency key
await step.retry(
  () => chargeCard(amount, { idempotencyKey }),
  { attempts: 3 }
);
```

### 5. Always Set Timeouts

Never let operations hang indefinitely:

```typescript
const data = await step.withTimeout(
  () => slowOperation(),
  { ms: 2000 }
);
```

### 6. Always Use Jitter

Prevents thundering herd when multiple instances retry:

```typescript
// Without jitter - all instances retry at same time
// With jitter - spread out, infrastructure can recover

step.retry(() => fetchData(), {
  attempts: 3,
  backoff: 'exponential',
  jitter: true,  // ALWAYS enable in production
});
```

### 7. Combine Retry and Timeout

Each attempt gets its own timeout:

```typescript
const data = await step.retry(
  () => fetchData(),
  {
    attempts: 3,
    timeout: { ms: 2000 },  // 2s per attempt
  }
);
// Total max time: 3 × 2s = 6s
```

## Recommended Defaults

| Operation | Attempts | Backoff | Initial Delay | Timeout |
|-----------|----------|---------|---------------|---------|
| DB read | 3 | exponential | 50ms | 5s |
| DB write | 1 | - | - | 10s |
| HTTP API | 3 | exponential | 100ms | 30s |
| Cache | 2 | fixed | 10ms | 500ms |

## Full Example

```typescript
import { createWorkflow } from '@jagreehal/workflow';

// Clean business function
async function getUser(args, deps): AsyncResult<User, 'NOT_FOUND' | 'DB_ERROR'> {
  try {
    const user = await deps.db.findUser(args.userId);
    return user ? ok(user) : err('NOT_FOUND');
  } catch {
    return err('DB_ERROR');
  }
}

// Workflow adds resilience
const loadUser = createWorkflow({ getUser });

const result = await loadUser(async (step) => {
  const user = await step.retry(
    () => getUser({ userId }, deps),
    {
      attempts: 3,
      backoff: 'exponential',
      initialDelay: 100,
      maxDelay: 2000,
      jitter: true,
      timeout: { ms: 5000 },
    }
  );
  return user;
});
```

### 8. Retrying Multi-Step Operations

Sometimes you need to retry a multi-step operation. Use `step.retry()` to wrap the entire sequence:

```typescript
const syncUserToProvider = createWorkflow({ findUser, syncUser, markSynced });

const result = await syncUserToProvider(async (step) => {
  // Retry the whole operation
  const user = await step.retry(
    async () => {
      const user = await step(() => findUser({ userId }, deps));
      await step(() => syncUser({ user }, deps));  // Must be idempotent!
      await step(() => markSynced({ userId }, deps));
      return user;
    },
    {
      attempts: 2,
      backoff: 'exponential',
    }
  );
  return user;
});
```

**Important:** The entire sequence must be idempotent. If `syncUser` is called twice, it should have the same effect as calling it once.

### 9. Circuit Breakers

When a service is down, stop hammering it. Circuit breakers prevent cascade failures:

```typescript
// Circuit breaker states
// CLOSED: Normal operation, requests go through
// OPEN: Service down, fail fast without trying
// HALF_OPEN: Testing if service recovered
```

Circuit breakers are outside the scope of `step.retry()`, but consider libraries like [opossum](https://github.com/nodeshift/opossum) or [cockatiel](https://github.com/connor4312/cockatiel) for production systems where dependencies fail frequently.

**When to use circuit breakers:**
- External APIs that may be down for extended periods
- Services with rate limits that trigger failures
- Downstream dependencies in microservices

**Don't use for:**
- Database calls (usually want retry instead)
- Internal function calls

### 10. Handling Timeout Errors

Use helpers to detect and handle timeouts:

```typescript
import { isStepTimeoutError, getStepTimeoutMeta } from '@jagreehal/workflow';

const result = await workflow(async (step) => {
  const data = await step.withTimeout(
    () => slowOperation(),
    { ms: 5000 }
  );
  return data;
});

if (!result.ok && isStepTimeoutError(result.error)) {
  const meta = getStepTimeoutMeta(result.error);
  deps.logger.warn('Operation timed out', {
    timeoutMs: meta?.timeoutMs,
    attempt: meta?.attempt,
  });
}
```

## The Rules

| Failure Type | Where to Retry |
|-------------|----------------|
| Transport/network | Workflow level |
| Idempotent reads | Workflow level |
| Non-idempotent writes | NEVER (or with idempotency key) |
| Multi-step operation | Workflow level (if idempotent) |

1. **Retry at workflow level only**
2. **Never double-retry across layers**
3. **Only retry transient errors**
4. **Never retry non-idempotent writes without idempotency key**
5. **Always set timeouts**
6. **Always use jitter in production**
7. **Use circuit breakers for external services**
