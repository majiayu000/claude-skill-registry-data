---
name: error-retry-tracking
description: Instrument error handling, retries, fallbacks, and failure patterns
triggers:
  - "error tracking"
  - "retry instrumentation"
  - "failure handling"
  - "fallback tracking"
  - "rate limit handling"
priority: 2
---

# Error and Retry Tracking

Instrument error handling to understand failure patterns and recovery behavior.

## Core Principle

Error observability answers:
1. **What failed** and why?
2. **How many retries** before success/failure?
3. **What fallbacks** were used?
4. **What's the recovery rate**?
5. **Are errors correlated** (rate limits, outages)?

## Error Classification

### Transient vs. Permanent
```python
TRANSIENT_ERRORS = [
    "RateLimitError",
    "TimeoutError",
    "ServiceUnavailable",
    "ConnectionError",
]

PERMANENT_ERRORS = [
    "InvalidRequestError",
    "AuthenticationError",
    "ContentPolicyViolation",
    "ContextLengthExceeded",
]

def classify_error(error: Exception) -> str:
    error_type = type(error).__name__
    if error_type in TRANSIENT_ERRORS:
        return "transient"
    elif error_type in PERMANENT_ERRORS:
        return "permanent"
    return "unknown"
```

## Error Span Attributes

```python
# Error identification (P0)
span.set_attribute("error.type", "RateLimitError")
span.set_attribute("error.message", "Rate limit exceeded")
span.set_attribute("error.category", "transient")
span.set_attribute("error.source", "llm_provider")

# Provider context (P1)
span.set_attribute("error.provider", "anthropic")
span.set_attribute("error.model", "claude-3-opus")
span.set_attribute("error.status_code", 429)
span.set_attribute("error.request_id", "req_abc123")

# Timing context (P1)
span.set_attribute("error.retry_after_ms", 60000)
span.set_attribute("error.occurred_at_step", 3)
span.set_attribute("error.time_into_request_ms", 2500)

# Impact (P2)
span.set_attribute("error.tokens_wasted", 1500)  # Tokens sent before failure
span.set_attribute("error.cost_wasted_usd", 0.015)
```

## Retry Span Attributes

```python
# Retry tracking (P0)
span.set_attribute("retry.attempt", 2)
span.set_attribute("retry.max_attempts", 3)
span.set_attribute("retry.strategy", "exponential_backoff")

# Timing (P1)
span.set_attribute("retry.delay_ms", 2000)
span.set_attribute("retry.total_wait_ms", 3500)
span.set_attribute("retry.jitter_ms", 150)

# Outcome (P0)
span.set_attribute("retry.success", True)
span.set_attribute("retry.final_attempt", 2)
span.set_attribute("retry.exhausted", False)
```

## Retry Wrapper Pattern

```python
from functools import wraps
from langfuse.decorators import observe
import time

def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
):
    def decorator(func):
        @wraps(func)
        @observe(name=f"{func.__name__}.with_retry")
        def wrapper(*args, **kwargs):
            span = get_current_span()
            span.set_attribute("retry.max_attempts", max_attempts)
            span.set_attribute("retry.strategy", "exponential_backoff")

            last_error = None
            total_wait = 0

            for attempt in range(1, max_attempts + 1):
                try:
                    span.set_attribute("retry.attempt", attempt)
                    result = func(*args, **kwargs)
                    span.set_attribute("retry.success", True)
                    span.set_attribute("retry.final_attempt", attempt)
                    return result

                except Exception as e:
                    last_error = e
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.category", classify_error(e))

                    if classify_error(e) == "permanent":
                        span.set_attribute("retry.exhausted", False)
                        span.set_attribute("retry.abort_reason", "permanent_error")
                        raise

                    if attempt < max_attempts:
                        delay = min(
                            base_delay * (exponential_base ** (attempt - 1)),
                            max_delay
                        )
                        total_wait += delay
                        span.add_event("retry.waiting", {"delay_ms": delay * 1000})
                        time.sleep(delay)

            span.set_attribute("retry.success", False)
            span.set_attribute("retry.exhausted", True)
            span.set_attribute("retry.total_wait_ms", total_wait * 1000)
            raise last_error

        return wrapper
    return decorator

@with_retry(max_attempts=3)
def call_llm(messages):
    return client.messages.create(messages=messages)
```

## Fallback Tracking

```python
# Fallback span attributes
span.set_attribute("fallback.triggered", True)
span.set_attribute("fallback.reason", "primary_model_unavailable")
span.set_attribute("fallback.from_model", "claude-3-opus")
span.set_attribute("fallback.to_model", "claude-3-sonnet")
span.set_attribute("fallback.quality_impact", "reduced")

# Fallback chain
span.set_attribute("fallback.chain", ["opus", "sonnet", "haiku"])
span.set_attribute("fallback.chain_position", 2)
```

## Rate Limit Handling

```python
# Rate limit specific attributes
span.set_attribute("rate_limit.type", "tokens_per_minute")
span.set_attribute("rate_limit.limit", 100000)
span.set_attribute("rate_limit.remaining", 0)
span.set_attribute("rate_limit.reset_at", "2024-01-15T10:01:00Z")
span.set_attribute("rate_limit.retry_after_ms", 45000)

# Proactive rate limiting
span.set_attribute("rate_limit.preemptive_wait", True)
span.set_attribute("rate_limit.tokens_queued", 5000)
```

## Circuit Breaker Pattern

```python
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

# Circuit breaker attributes
span.set_attribute("circuit.state", "open")
span.set_attribute("circuit.failure_count", 5)
span.set_attribute("circuit.failure_threshold", 5)
span.set_attribute("circuit.last_failure_at", timestamp)
span.set_attribute("circuit.opens_at", timestamp)
span.set_attribute("circuit.half_open_attempts", 0)
```

## Error Aggregation

Track error patterns:
```python
# Per-session error summary
span.set_attribute("session.total_errors", 3)
span.set_attribute("session.transient_errors", 2)
span.set_attribute("session.permanent_errors", 1)
span.set_attribute("session.retry_success_rate", 0.67)

# Per-provider health
span.set_attribute("provider.health", "degraded")
span.set_attribute("provider.error_rate_1h", 0.05)
span.set_attribute("provider.avg_latency_1h_ms", 2500)
```

## Framework Integration

### LangChain Retry
```python
from langchain.chat_models import ChatAnthropic
from langfuse.callback import CallbackHandler

llm = ChatAnthropic(
    model="claude-3-opus",
    max_retries=3,
    request_timeout=30,
)

# Callbacks capture retry behavior
handler = CallbackHandler()
response = llm.invoke(messages, config={"callbacks": [handler]})
```

### Tenacity Integration
```python
from tenacity import retry, stop_after_attempt, wait_exponential
from langfuse.decorators import observe

@observe(name="llm.call")
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
)
def call_with_tenacity(messages):
    return client.messages.create(messages=messages)
```

## Anti-Patterns

- Catching all exceptions silently (hidden failures)
- No retry tracking (can't optimize retry config)
- Missing error classification (can't distinguish transient vs. permanent)
- No fallback logging (unclear degradation)
- Retrying permanent errors (wasted cost)

## Related Skills
- `llm-call-tracing` - LLM error context
- `tool-call-tracking` - Tool error handling
