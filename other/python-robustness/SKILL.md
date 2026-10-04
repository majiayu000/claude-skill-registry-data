---
name: python-robustness
description: Python robustness patterns including input validation, exception hierarchies, retry logic, timeouts, and fault-tolerant decorators. Use when implementing validation, designing exception strategies, adding retry logic, handling transient failures, handling batch partial failures, or building fault-tolerant services.
---

# Python Robustness Patterns

Build robust Python applications that validate inputs early, fail with meaningful errors, and recover gracefully from transient failures. Good robustness patterns make debugging easier and keep systems running when dependencies are unreliable.

## When to Use This Skill

- Validating user input and API parameters
- Designing exception hierarchies for applications
- Handling partial failures in batch operations
- Converting external data to domain types
- Building user-friendly error messages
- Implementing fail-fast validation patterns
- Adding retry logic to external service calls
- Implementing timeouts for network operations
- Building fault-tolerant microservices
- Handling rate limiting and backpressure
- Creating infrastructure decorators
- Designing circuit breakers

## Core Concepts

### Error Handling

**1. Fail Fast** — Validate inputs early, before expensive operations. Report all validation errors at once when possible.

**2. Meaningful Exceptions** — Use appropriate exception types with context. Messages should explain what failed, why, and how to fix it.

**3. Partial Failures** — In batch operations, don't let one failure abort everything. Track successes and failures separately.

**4. Preserve Context** — Chain exceptions to maintain the full error trail for debugging.

### Resilience

**5. Transient vs Permanent Failures** — Retry transient errors (network timeouts, temporary service issues). Don't retry permanent errors (invalid credentials, bad requests).

**6. Exponential Backoff** — Increase wait time between retries to avoid overwhelming recovering services.

**7. Jitter** — Add randomness to backoff to prevent thundering herd when many clients retry simultaneously.

**8. Bounded Retries** — Cap both attempt count and total duration to prevent infinite retry loops.

## Quick Start

```python
# Error handling: validate early
def fetch_page(url: str, page_size: int) -> Page:
    if not url:
        raise ValueError("'url' is required")
    if not 1 <= page_size <= 100:
        raise ValueError(f"'page_size' must be 1-100, got {page_size}")
    # Now safe to proceed...

# Resilience: retry transient failures
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def call_external_service(request: dict) -> dict:
    return httpx.post("https://api.example.com", json=request).json()
```

---

## Error Handling Patterns

### Pattern 1: Early Input Validation

Validate all inputs at API boundaries before any processing begins.

```python
def process_order(
    order_id: str,
    quantity: int,
    discount_percent: float,
) -> OrderResult:
    """Process an order with validation."""
    # Validate required fields
    if not order_id:
        raise ValueError("'order_id' is required")

    # Validate ranges
    if quantity <= 0:
        raise ValueError(f"'quantity' must be positive, got {quantity}")

    if not 0 <= discount_percent <= 100:
        raise ValueError(
            f"'discount_percent' must be 0-100, got {discount_percent}"
        )

    # Validation passed, proceed with processing
    return _process_validated_order(order_id, quantity, discount_percent)
```

### Pattern 2: Convert to Domain Types Early

Parse strings and external data into typed domain objects at system boundaries.

```python
from enum import Enum

class OutputFormat(Enum):
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"

def parse_output_format(value: str) -> OutputFormat:
    """Parse string to OutputFormat enum."""
    try:
        return OutputFormat(value.lower())
    except ValueError:
        valid_formats = [f.value for f in OutputFormat]
        raise ValueError(
            f"Invalid format '{value}'. "
            f"Valid options: {', '.join(valid_formats)}"
        )

# Usage at API boundary
def export_data(data: list[dict], format_str: str) -> bytes:
    output_format = parse_output_format(format_str)  # Fail fast
    # Rest of function uses typed OutputFormat
    ...
```

### Pattern 3: Pydantic for Complex Validation

Use Pydantic models for structured input validation with automatic error messages.

```python
from pydantic import BaseModel, Field, field_validator

class CreateUserInput(BaseModel):
    """Input model for user creation."""

    email: str = Field(..., min_length=5, max_length=255)
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().title()

# Usage
try:
    user_input = CreateUserInput(email="user@example.com", name="john doe", age=25)
except ValidationError as e:
    print(e.errors())
```

### Pattern 4: Map Errors to Standard Exceptions

Use Python's built-in exception types appropriately, adding context as needed.

| Failure Type | Exception | Example |
|--------------|-----------|---------|
| Invalid input | `ValueError` | Bad parameter values |
| Wrong type | `TypeError` | Expected string, got int |
| Missing item | `KeyError` | Dict key not found |
| Operational failure | `RuntimeError` | Service unavailable |
| Timeout | `TimeoutError` | Operation took too long |
| File not found | `FileNotFoundError` | Path doesn't exist |
| Permission denied | `PermissionError` | Access forbidden |

```python
# Good: Specific exception with context
raise ValueError(f"'page_size' must be 1-100, got {page_size}")

# Avoid: Generic exception, no context
raise Exception("Invalid parameter")
```

### Pattern 5: Custom Exceptions with Context

Create domain-specific exceptions that carry structured information.

```python
class ApiError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)

class RateLimitError(ApiError):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: int) -> None:
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit exceeded. Retry after {retry_after}s",
            status_code=429,
        )

# Usage
def handle_response(response: Response) -> dict:
    match response.status_code:
        case 200:
            return response.json()
        case 401:
            raise ApiError("Invalid credentials", 401)
        case 404:
            raise ApiError(f"Resource not found: {response.url}", 404)
        case 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(retry_after)
        case code if 400 <= code < 500:
            raise ApiError(f"Client error: {response.text}", code)
        case code if code >= 500:
            raise ApiError(f"Server error: {response.text}", code)
```

### Pattern 6: Exception Chaining

Preserve the original exception when re-raising to maintain the debug trail.

```python
import httpx

class ServiceError(Exception):
    """High-level service operation failed."""
    pass

def upload_file(path: str) -> str:
    """Upload file and return URL."""
    try:
        with open(path, "rb") as f:
            response = httpx.post("https://upload.example.com", files={"file": f})
            response.raise_for_status()
            return response.json()["url"]
    except FileNotFoundError as e:
        raise ServiceError(f"Upload failed: file not found at '{path}'") from e
    except httpx.HTTPStatusError as e:
        raise ServiceError(
            f"Upload failed: server returned {e.response.status_code}"
        ) from e
    except httpx.RequestError as e:
        raise ServiceError(f"Upload failed: network error") from e
```

### Pattern 7: Batch Processing with Partial Failures

Never let one bad item abort an entire batch. Track results per item.

```python
from dataclasses import dataclass

@dataclass
class BatchResult[T]:
    """Results from batch processing."""

    succeeded: dict[int, T]  # index -> result
    failed: dict[int, Exception]  # index -> error

    @property
    def success_count(self) -> int:
        return len(self.succeeded)

    @property
    def failure_count(self) -> int:
        return len(self.failed)

    @property
    def all_succeeded(self) -> bool:
        return len(self.failed) == 0

def process_batch(items: list[Item]) -> BatchResult[ProcessedItem]:
    """Process items, capturing individual failures."""
    succeeded: dict[int, ProcessedItem] = {}
    failed: dict[int, Exception] = {}

    for idx, item in enumerate(items):
        try:
            result = process_single_item(item)
            succeeded[idx] = result
        except Exception as e:
            failed[idx] = e

    return BatchResult(succeeded=succeeded, failed=failed)

# Caller handles partial results
result = process_batch(items)
if not result.all_succeeded:
    logger.warning(
        f"Batch completed with {result.failure_count} failures",
        failed_indices=list(result.failed.keys()),
    )
```

### Pattern 8: Progress Reporting for Long Operations

Provide visibility into batch progress without coupling business logic to UI.

```python
from collections.abc import Callable

ProgressCallback = Callable[[int, int, str], None]  # current, total, status

def process_large_batch(
    items: list[Item],
    on_progress: ProgressCallback | None = None,
) -> BatchResult:
    """Process batch with optional progress reporting."""
    total = len(items)
    succeeded = {}
    failed = {}

    for idx, item in enumerate(items):
        if on_progress:
            on_progress(idx, total, f"Processing {item.id}")

        try:
            succeeded[idx] = process_single_item(item)
        except Exception as e:
            failed[idx] = e

    if on_progress:
        on_progress(total, total, "Complete")

    return BatchResult(succeeded=succeeded, failed=failed)
```

---

## Resilience Patterns

### Pattern 9: Basic Retry with Tenacity

Use the `tenacity` library for production-grade retry logic.

```python
from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential_jitter,
    retry_if_exception_type,
)

TRANSIENT_ERRORS = (ConnectionError, TimeoutError, OSError)

@retry(
    retry=retry_if_exception_type(TRANSIENT_ERRORS),
    stop=stop_after_attempt(5) | stop_after_delay(60),
    wait=wait_exponential_jitter(initial=1, max=30),
)
def fetch_data(url: str) -> dict:
    """Fetch data with automatic retry on transient failures."""
    response = httpx.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

### Pattern 10: Retry Only Appropriate Errors

Whitelist specific transient exceptions. Never retry:

- `ValueError`, `TypeError` — These are bugs, not transient issues
- `AuthenticationError` — Invalid credentials won't become valid
- HTTP 4xx errors (except 429) — Client errors are permanent

```python
RETRYABLE_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
)

@retry(
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def resilient_api_call(endpoint: str) -> dict:
    return httpx.get(endpoint, timeout=10).json()
```

### Pattern 11: HTTP Status Code Retries

Retry specific HTTP status codes that indicate transient issues.

```python
from tenacity import retry, retry_if_result, stop_after_attempt
import httpx

RETRY_STATUS_CODES = {429, 502, 503, 504}

def should_retry_response(response: httpx.Response) -> bool:
    return response.status_code in RETRY_STATUS_CODES

@retry(
    retry=retry_if_result(should_retry_response),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def http_request(method: str, url: str, **kwargs) -> httpx.Response:
    return httpx.request(method, url, timeout=30, **kwargs)
```

### Pattern 12: Combined Exception and Status Retry

Handle both network exceptions and HTTP status codes, with logging.

```python
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential_jitter,
    before_sleep_log,
)
import logging

logger = logging.getLogger(__name__)

TRANSIENT_EXCEPTIONS = (ConnectionError, TimeoutError, httpx.ConnectError, httpx.ReadTimeout)
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

def is_retryable_response(response: httpx.Response) -> bool:
    return response.status_code in RETRY_STATUS_CODES

@retry(
    retry=(
        retry_if_exception_type(TRANSIENT_EXCEPTIONS) |
        retry_if_result(is_retryable_response)
    ),
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def robust_http_call(method: str, url: str, **kwargs) -> httpx.Response:
    return httpx.request(method, url, timeout=30, **kwargs)
```

### Pattern 13: Timeout Decorator

Create reusable timeout decorators for consistent timeout handling.

```python
import asyncio
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar("T")

def with_timeout(seconds: float):
    """Decorator to add timeout to async functions."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=seconds,
            )
        return wrapper
    return decorator

@with_timeout(30)
async def fetch_with_timeout(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Pattern 14: Cross-Cutting Concerns via Decorators

Stack decorators to separate infrastructure from business logic.

```python
from functools import wraps
import structlog

logger = structlog.get_logger()

def traced(name: str | None = None):
    """Add tracing to function calls."""
    def decorator(func):
        span_name = name or func.__name__

        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info("Operation started", operation=span_name)
            try:
                result = await func(*args, **kwargs)
                logger.info("Operation completed", operation=span_name)
                return result
            except Exception as e:
                logger.error("Operation failed", operation=span_name, error=str(e))
                raise
        return wrapper
    return decorator

# Stack multiple concerns
@traced("fetch_user_data")
@with_timeout(30)
@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter())
async def fetch_user_data(user_id: str) -> dict:
    """Fetch user with tracing, timeout, and retry."""
    ...
```

### Pattern 15: Fail-Safe Defaults

Degrade gracefully when non-critical operations fail.

```python
from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")

def fail_safe(default: T, log_failure: bool = True):
    """Return default value on failure instead of raising."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_failure:
                    logger.warning(
                        "Operation failed, using default",
                        function=func.__name__,
                        error=str(e),
                    )
                return default
        return wrapper
    return decorator

@fail_safe(default=[])
async def get_recommendations(user_id: str) -> list[str]:
    """Get recommendations, return empty list on failure."""
    ...
```

### Pattern 16: Dependency Injection for Testability

Pass infrastructure components through constructors for easy testing.

```python
from dataclasses import dataclass
from typing import Protocol

class Logger(Protocol):
    def info(self, msg: str, **kwargs) -> None: ...
    def error(self, msg: str, **kwargs) -> None: ...

class MetricsClient(Protocol):
    def increment(self, metric: str, tags: dict | None = None) -> None: ...
    def timing(self, metric: str, value: float) -> None: ...

@dataclass
class UserService:
    repository: UserRepository
    logger: Logger
    metrics: MetricsClient

    async def get_user(self, user_id: str) -> User:
        self.logger.info("Fetching user", user_id=user_id)
        start = time.perf_counter()

        try:
            user = await self.repository.get(user_id)
            self.metrics.increment("user.fetch.success")
            return user
        except Exception as e:
            self.metrics.increment("user.fetch.error")
            self.logger.error("Failed to fetch user", user_id=user_id, error=str(e))
            raise
        finally:
            elapsed = time.perf_counter() - start
            self.metrics.timing("user.fetch.duration", elapsed)

# Easy to test with fakes
service = UserService(
    repository=FakeRepository(),
    logger=FakeLogger(),
    metrics=FakeMetrics(),
)
```

---

## Best Practices Summary

**Error Handling**
1. **Validate early** — Check inputs before expensive operations
2. **Use specific exceptions** — `ValueError`, `TypeError`, not generic `Exception`
3. **Include context** — Messages should explain what, why, and how to fix
4. **Convert types at boundaries** — Parse strings to enums/domain types early
5. **Chain exceptions** — Use `raise ... from e` to preserve debug info
6. **Handle partial failures** — Don't abort batches on single item errors
7. **Use Pydantic** — For complex input validation with structured errors
8. **Test error paths** — Verify exceptions are raised correctly

**Resilience**
9. **Retry only transient errors** — Don't retry bugs or authentication failures
10. **Use exponential backoff** — Give services time to recover
11. **Add jitter** — Prevent thundering herd from synchronized retries
12. **Cap total duration** — `stop_after_attempt(5) | stop_after_delay(60)`
13. **Log every retry** — Silent retries hide systemic problems
14. **Use decorators** — Keep retry logic separate from business logic
15. **Inject dependencies** — Make infrastructure testable
16. **Set timeouts everywhere** — Every network call needs a timeout
17. **Fail gracefully** — Return cached/default values for non-critical paths
18. **Monitor retry rates** — High retry rates indicate underlying issues
