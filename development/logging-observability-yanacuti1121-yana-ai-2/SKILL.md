---
name: logging-observability
description: Production logging — structlog, structured JSON logs, correlation IDs, log levels, OpenTelemetry traces, no print()
triggers:
  - logging best practice
  - structlog
  - structured logging
  - correlation id logging
  - log levels
  - no print logging
  - production logging python
  - observability logging
  - log context
  - opentelemetry traces
do_not_use_for:
  - LLM-specific observability — use langfuse
  - metrics/dashboards — use prometheus/grafana
  - error handling — use error-handling-patterns
see_also:
  - ai-code-maintainability
  - error-handling-patterns
---

# Logging & Observability

## Setup: structlog (Recommended)

```python
import logging
import structlog

def configure_logging(env: str = "production") -> None:
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if env == "development":
        # Human-readable in dev
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer()
        ]
    else:
        # JSON in prod — parseable by Loki/CloudWatch/Datadog
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

log = structlog.get_logger()
```

## Correlation ID Middleware

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import structlog

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id,
            path=request.url.path,
            method=request.method,
        )
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

# All log calls in this request now automatically include correlation_id
```

## Log Levels Guide

```python
log = structlog.get_logger(__name__)

# DEBUG — detailed diagnostic, only in dev
log.debug("processing_chunk", chunk_index=3, chunk_size=512)

# INFO — normal operations, business events
log.info("user_registered", user_id=user.id, plan="free")
log.info("payment_completed", order_id=order.id, amount=99.0, currency="USD")

# WARNING — unexpected but recoverable
log.warning("retry_attempt", attempt=2, max=3, service="stripe")
log.warning("cache_miss", key="user:123", fallback="db")

# ERROR — operation failed, action needed
log.error("payment_failed", order_id=order.id, error=str(e), code=e.code)

# CRITICAL — system-level failure, immediate attention
log.critical("database_unreachable", host=db_host, elapsed_ms=5000)
```

## Structured Log Fields (Standard)

```python
# Always include in service logs
log.info(
    "event_name",                   # snake_case event
    user_id="u-123",               # who
    resource_type="order",          # what
    resource_id="o-456",           # which one
    action="create",               # what action
    duration_ms=42,                # how long
    status="success",              # outcome
    environment="production",      # where
)
# → {"event": "event_name", "user_id": "u-123", ...}
```

## OpenTelemetry Traces

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Setup
provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-service", "1.0.0")

# Instrument code
def process_order(order_id: str) -> None:
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        try:
            result = _do_work(order_id)
            span.set_attribute("order.status", result.status)
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.StatusCode.ERROR, str(e))
            raise
```

## Log Sampling (high-volume)

```python
import structlog

# Don't log every request at INFO in prod — sample at 10%
import random

def log_if_sample(log, rate: float = 0.1, **kwargs) -> None:
    if random.random() < rate:
        log.info(**kwargs)

# Or use structured sampling based on user
def should_log_detailed(user_id: str) -> bool:
    return int(user_id[-4:], 16) % 100 < 5   # 5% of users get detailed logs
```

## Anti-Fake-Pass Checks

- `print()` in server code = invisible in prod log aggregators (CloudWatch, Loki)
- Logging PII (emails, passwords, tokens) = GDPR/compliance violation
- `log.exception()` includes stack trace — use only for unexpected errors
- `structlog.contextvars` is thread-local + async-safe — don't bind to regular dict
- OpenTelemetry `BatchSpanProcessor` is async — call `provider.shutdown()` on app exit
- Log the error, not the exception message alone — include context (user_id, resource_id)
- `logging.DEBUG` level in production = performance hit and log flooding
