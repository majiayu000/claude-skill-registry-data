---
name: error-handling
description: >
  Architect and implement resilient error handling, custom error hierarchies,
  and recovery strategies across application boundaries. Use when distinguishing
  transient from permanent failures, designing Result types vs exception hierarchies,
  implementing exponential backoff with jitter for retries, or preventing silent
  error swallowing and information leakage.
compatibility: >
  Agent Skills-compatible coding agents designing error handling strategies
  across backend and systems codebases.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "error-handling, exceptions, retry, exponential-backoff, jitter, resilience"
  topics: "software-development, architecture"
---

# Resilient Error Handling and Recovery

Software systems inevitably encounter unexpected states: network outages, corrupted input, timeouts, and resource exhaustion. Robust engineering categorizes errors systematically, propagates context cleanly, applies resilient retry strategies for transient faults, and enforces strict error boundaries to prevent cascading crashes.

## Core Rules

1. **Distinguish transient from permanent failures**: Transient errors (network blips, rate limits, deadlock contention) should be retried with exponential backoff; permanent errors (validation failures, 404 Not Found, bad auth) must fail fast.
2. **Never catch and silently ignore exceptions**: Catching an error without logging, alerting, or re-raising hides bugs and corrupts system state.
3. **Preserve the error cause chain**: In exceptions, always chain the root cause (`raise CustomError from original_err`). In Result types, bundle the underlying error type.
4. **Always use jitter with exponential backoff**: Retrying at exact intervals causes a "thundering herd" effect that overwhelms recovering services. Add randomized jitter.
5. **Sanitize error messages at system boundaries**: Never leak internal database schemas, stack traces, or credentials in client-facing HTTP/API responses.

---

## 1. Error Classification Matrix

| Error Class | Characteristics | Examples | Recommended Action |
| :--- | :--- | :--- | :--- |
| **Transient** | Temporary external condition; likely to succeed on subsequent attempt | HTTP 503, 429 Rate Limit, TCP socket timeout, DB deadlock | Retry with exponential backoff & jitter |
| **Permanent Client** | Bad input or protocol violation; will fail every time with same payload | HTTP 400 Bad Request, validation error, schema mismatch | Fail immediately; return clear diagnostic error to client |
| **Permanent System** | Internal bug or severe infrastructure failure | Out of Memory, missing binary, disk hardware error | Fail fast; log critical alert; abort process if state is corrupted |

---

## 2. Exponential Backoff with Jitter

The industry standard algorithm for retrying network operations safely:

```python
import random
import time
import logging

logger = logging.getLogger(__name__)

def retry_with_backoff(
    func,
    max_retries: int = 4,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
):
    """Execute func with full jitter exponential backoff."""
    attempt = 0
    while True:
        try:
            return func()
        except TransientNetworkError as exc:
            attempt += 1
            if attempt > max_retries:
                logger.error("Operation failed after %d retries: %s", max_retries, exc)
                raise

            # Full jitter formula: sleep = uniform(0, min(max_delay, base_delay * 2^attempt))
            calculated_backoff = min(max_delay, base_delay * (2 ** (attempt - 1)))
            sleep_duration = random.uniform(0, calculated_backoff)

            logger.warning(
                "Transient error on attempt %d/%d: %s. Backing off for %.2fs",
                attempt, max_retries, exc, sleep_duration
            )
            time.sleep(sleep_duration)
```

---

## 3. Exceptions vs Result Types

Choose the error idiom that fits your programming language:

### Result / Either Pattern (Rust, Go, TypeScript)
Used when errors are an expected part of normal domain operations (e.g. parsing, validation):
```typescript
type Result<T, E> =
  | { success: true; value: T }
  | { success: false; error: E };

function parsePort(input: string): Result<number, string> {
  const num = parseInt(input, 10);
  if (isNaN(num) || num < 1 || num > 65535) {
    return { success: false, error: `Invalid port number: ${input}` };
  }
  return { success: true, value: num };
}
```

### Exception Hierarchies (Python, Java, C#)
Used for exceptional conditions, with domain-specific base classes:
```python
class AppDomainError(Exception):
    """Base class for all domain errors."""

class EntityNotFoundError(AppDomainError):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(f"{entity_name} with ID '{entity_id}' not found.")
        self.entity_name = entity_name
        self.entity_id = entity_id
```

---

## 4. Boundary Sanitization (Security)

At API or HTTP boundaries, translate internal exceptions into safe responses:

```python
# FastAPI / Flask middleware boundary example
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_id = str(uuid.uuid4())
    # Log internal details and stack trace privately:
    logger.error("Unhandled error [ID: %s] on %s: %s", error_id, request.url, exc, exc_info=True)

    # Return safe, non-leaking error to client:
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please quote the reference ID.",
            "reference_id": error_id,
        },
    )
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Retrying permanent errors (e.g. HTTP 400 or 401) | Wastes server resources, triggers rate limits | Only retry transient faults (503, 429, timeouts) |
| Retrying without jitter (fixed sleep) | Synchronizes traffic bursts, crashing the database | Always add randomized jitter |
| Catching bare `Exception` without re-raise | Masks syntax errors, keyboard interrupts, OOM | Catch specific exception types |
| Leaking stack traces to HTTP responses | Exposes internal paths, library versions to attackers | Log internally; return generic message with reference ID |

---

## 6. Verification Checklist

- [ ] Transient faults are retried with exponential backoff and randomized jitter.
- [ ] Retries have a strict maximum limit (`max_retries <= 5`).
- [ ] Non-transient client errors fail immediately without retry.
- [ ] Error messages at API boundaries contain no internal stack traces or secrets.
- [ ] All chained exceptions preserve the original `from` cause.
