---
name: logging-observability
description: >
  Implement structured JSON logging, distributed tracing context, and observability
  metrics across services. Use when configuring structured logging frameworks,
  injecting correlation/trace IDs across asynchronous boundaries, assigning appropriate
  log levels (DEBUG, INFO, WARN, ERROR), or redacting sensitive PII and secrets.
compatibility: >
  Agent Skills-compatible coding agents implementing logging and telemetry
  across backend services.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "logging, observability, metrics, tracing, structured-logging, pii-redaction"
  topics: "software-development, devops"
---

# Structured Logging and Observability

Modern distributed systems require observability to diagnose production issues, track request flows, and monitor service health. Structured logging (JSON), distributed correlation IDs (`trace_id`, `request_id`), standardized log levels, and rigorous PII redaction ensure logs are machine-searchable and security-compliant.

## Core Rules

1. **Log in structured JSON format in production**: Free-form text strings are difficult to parse, query, and aggregate. Emit newline-delimited JSON with consistent field keys.
2. **Propagate correlation IDs (`trace_id`, `request_id`)**: Every incoming request must be assigned an ID that is injected into every log entry emitted during that request lifecycle.
3. **Never log sensitive data (PII, Credentials)**: Passwords, bearer tokens, API keys, credit card numbers, and national IDs must be scrubbed before emitting log entries.
4. **Choose the correct log level**:
   - `DEBUG`: High-volume diagnostic information useful only in development or deep troubleshooting.
   - `INFO`: Normal operational events (e.g. service started, payment processed, user registered).
   - `WARN`: Unexpected situations that did not halt execution (e.g. transient retry, deprecated API used).
   - `ERROR`: Operations that failed to complete (e.g. unhandled exception, database connection loss).
5. **Never use string concatenation for log formatting**: Pass parameters to the logger so parameter interpolation only occurs if the log level is enabled (`logger.info("User %s logged in", user_id)`).

---

## 1. Canonical Structured JSON Log Format

```json
{
  "timestamp": "2026-10-15T15:30:00.123Z",
  "level": "INFO",
  "logger": "app.services.payment",
  "message": "Payment transaction processed successfully",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "request_id": "req_88127391",
  "user_id": "usr_99182",
  "duration_ms": 142.5,
  "service": "payment-api",
  "environment": "production"
}
```

---

## 2. Implementing Contextual Logging with Correlation IDs

Using Python's modern `contextvars` to propagate trace context across async tasks:

```python
import contextvars
import json
import logging
from datetime import datetime, timezone

# Context variable holds trace_id for current execution flow
current_trace_id = contextvars.ContextVar("trace_id", default=None)

class JsonFormatter(logging.Formatter):
    """Custom logging formatter outputting single-line JSON."""
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": current_trace_id.get(),
        }

        # Include stack trace if exception was recorded
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        # Merge custom extra fields
        if hasattr(record, "extra_fields"):
            log_obj.update(record.extra_fields)

        return json.dumps(log_obj)

# Usage in request middleware:
def handle_request(req):
    trace_id = req.headers.get("X-Trace-ID") or generate_uuid()
    token = current_trace_id.set(trace_id)
    try:
        logger.info("Handling order checkout", extra={"extra_fields": {"cart_size": 3}})
    finally:
        current_trace_id.reset(token)
```

---

## 3. Scrubbing and Redacting Sensitive Data

Implement automated log sanitization filters for sensitive fields:

```python
SENSITIVE_KEYS = {"password", "secret", "token", "authorization", "api_key", "credit_card"}

def redact_payload(data: dict) -> dict:
    """Recursively scrub sensitive keys from log dictionaries."""
    sanitized = {}
    for k, v in data.items():
        if k.lower() in SENSITIVE_KEYS:
            sanitized[k] = "[REDACTED]"
        elif isinstance(v, dict):
            sanitized[k] = redact_payload(v)
        else:
            sanitized[k] = v
    return sanitized
```

---

## 4. The Three Pillars of Observability

1. **Logs**: Discrete, timestamped records of events with rich context.
2. **Metrics**: Aggregated numerical counters and gauges over time (e.g. `http_requests_total`, `cpu_usage_percentage`, `db_pool_idle_connections`).
3. **Traces**: End-to-end request latency journeys across microservice boundaries (OpenTelemetry / W3C TraceContext).

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Logging full HTTP headers containing `Authorization: Bearer ...` | Security breach: credentials leaked into log management | Redact `Authorization` and `Cookie` headers |
| Excessive DEBUG logging in production | Massive log storage costs, degraded I/O performance | Default to INFO in production; enable DEBUG selectively |
| Logging sensitive PII (customer SSN, credit cards) | Regulatory violation (GDPR, PCI-DSS) | Redact or tokenize before logging |
| Swallowing exceptions and logging generic text | Lost root cause stack trace | Use `logger.error("Failed", exc_info=True)` |
| Inconsistent timestamp formats across services | Logs cannot be ordered chronologically in Datadog/Elastic | Always use ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SS.sssZ`) |

---

## 6. Verification Checklist

- [ ] Logs are emitted as valid, single-line JSON.
- [ ] Timestamps are formatted in ISO 8601 UTC.
- [ ] Every request includes a unique `trace_id` / `request_id`.
- [ ] Automated filters redact passwords, tokens, and authorization headers.
- [ ] Unhandled errors log full exception stack traces (`exc_info=True`).
