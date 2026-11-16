---
name: error-handling-patterns
description: Production error handling — typed errors, Result type, error boundaries, structured logging, retry strategies
triggers:
  - error handling
  - exception handling
  - error boundary
  - result type
  - typed errors
  - error handling python
  - error handling typescript
  - retry strategy
  - error logging best practice
  - production error handling
do_not_use_for:
  - validation only — use pydantic for input validation
  - observability/tracing — use langfuse
  - AI-specific anti-patterns — use ai-code-maintainability
see_also:
  - ai-code-maintainability
  - type-safety-patterns
  - testing-strategy
---

# Error Handling Patterns

## Python: Typed Exception Hierarchy

```python
# Define domain-specific exception tree
class AppError(Exception):
    """Base for all application errors."""
    def __init__(self, message: str, code: str, **context):
        super().__init__(message)
        self.code = code
        self.context = context

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(f"{resource} {resource_id} not found",
                         code="NOT_FOUND",
                         resource=resource, resource_id=resource_id)

class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Validation failed: {field} — {reason}",
                         code="VALIDATION_ERROR",
                         field=field, reason=reason)

class ExternalServiceError(AppError):
    def __init__(self, service: str, status: int, detail: str):
        super().__init__(f"{service} returned {status}: {detail}",
                         code="EXTERNAL_ERROR",
                         service=service, status=status)
```

## Python: Result Type (no exceptions for control flow)

```python
from typing import Generic, TypeVar, Union
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E")

@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    ok: bool = True

@dataclass(frozen=True)
class Err(Generic[E]):
    error: E
    ok: bool = False

Result = Union[Ok[T], Err[E]]

# Usage
def parse_age(raw: str) -> Result[int, str]:
    try:
        age = int(raw)
        if not 0 <= age <= 150:
            return Err(f"age {age} out of range [0, 150]")
        return Ok(age)
    except ValueError:
        return Err(f"'{raw}' is not a valid integer")

result = parse_age("25")
match result:
    case Ok(value=age):
        print(f"Valid age: {age}")
    case Err(error=msg):
        print(f"Error: {msg}")
```

## TypeScript: Result Type

```typescript
type Ok<T> = { ok: true; value: T };
type Err<E> = { ok: false; error: E };
type Result<T, E = string> = Ok<T> | Err<E>;

const ok = <T>(value: T): Ok<T> => ({ ok: true, value });
const err = <E>(error: E): Err<E> => ({ ok: false, error });

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.findUser(id);
    if (!user) return err(`User ${id} not found`);
    return ok(user);
  } catch (e) {
    logger.error("fetchUser failed", { id, error: e });
    return err("database error");
  }
}

// Exhaustive handling — TypeScript checks you handled both cases
const result = await fetchUser(id);
if (!result.ok) {
  res.status(404).json({ error: result.error });
  return;
}
const user = result.value; // User — not undefined
```

## Structured Error Logging

```python
import structlog
from typing import Any

log = structlog.get_logger()

def process_payment(order_id: str, amount: float) -> None:
    log_ctx = log.bind(order_id=order_id, amount=amount, action="payment")
    try:
        log_ctx.info("payment_started")
        result = stripe.charge(order_id, amount)
        log_ctx.info("payment_succeeded", charge_id=result.id)
    except stripe.CardError as e:
        log_ctx.warning("payment_declined", code=e.code, message=e.user_message)
        raise
    except stripe.StripeError as e:
        log_ctx.error("payment_stripe_error", error_type=type(e).__name__, detail=str(e))
        raise ExternalServiceError("stripe", 500, str(e)) from e
    except Exception as e:
        log_ctx.exception("payment_unexpected_error")  # includes stack trace
        raise
```

## Retry with Tenacity

```python
from tenacity import (
    retry, stop_after_attempt, wait_exponential,
    retry_if_exception_type, before_sleep_log,
    RetryError,
)
import logging

@retry(
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    before_sleep=before_sleep_log(logging.getLogger(__name__), logging.WARNING),
    reraise=True,
)
async def call_external_api(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()

try:
    data = await call_external_api("https://api.example.com/data")
except RetryError as e:
    # All retries exhausted
    raise ExternalServiceError("example-api", 503, "all retries failed") from e
```

## Error Boundaries (React)

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    logger.error('React error boundary caught', {
      error: error.message,
      component: info.componentStack,
    });
  }

  render(): ReactNode {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorPage message="Something went wrong" />}>
  <RiskyComponent />
</ErrorBoundary>
```

## Anti-Fake-Pass Checks

- `log.exception()` includes stack trace — use for unexpected errors, not expected ones
- `reraise=True` in tenacity means after all retries fail, original exception propagates
- Result type only works if callers check `result.ok` — TypeScript enforces this, Python does not
- `before_sleep_log` requires a Python `logging.Logger`, not structlog logger — use `logging.getLogger()`
- Error boundaries only catch rendering errors — async errors (useEffect, event handlers) need try/catch
- Match statement (Python 3.10+) — use `if/elif` for 3.9 compat
