---
name: rule-api-logging
description: MANDATORY when editing files matching ["api/src/**/*.py"]. Structured logging conventions for the Python API
---

# API Logging Rules

## Logger Acquisition

ALWAYS obtain loggers via `logger = logging.getLogger(__name__)` at module scope. NEVER use the root logger. NEVER create ad-hoc loggers inside functions.

## Static Messages, Dynamic Extras

ALWAYS use static log message strings. ALWAYS put dynamic values in `extra={}` with flat snake_case keys. NEVER f-string variable data into the message. NEVER use dotted/nested keys.

Correct:
```python
logger.info(
    "User login completed successfully",
    extra={"user_id": user.user_id, "auth_method": "jwt"},
)
```

Incorrect:
```python
logger.info(f"User {user.user_id} logged in via jwt")
logger.info("login", extra={"user.id": user.user_id})  # dotted key
```

## Log Level Discipline

ALWAYS use `logger.info()` for expected 4xx client errors. Reserve `logger.warning()` for actual operational concerns that should trigger alerts. Use `logger.error()` + `exc_info=True` only for failed operations that require investigation. NEVER use `warning` for normal validation failures.

## PII and Secrets

NEVER log PII (names, emails, SSNs, phone numbers), tokens, passwords, API keys, or full request bodies. FedRAMP Moderate boundary requires redacted logs. When in doubt, log the ID only.

## Request-Scoped Context

ALWAYS call `add_extra_data_to_current_request_logs({...})` inside Flask request handlers to attach stable fields (e.g., `application_id`, `opportunity_id`) to every downstream log line from the request. NEVER call `str()` on UUIDs in extras — keep the UUID type.

Correct:
```python
add_extra_data_to_current_request_logs({"application_id": application_id})
```

## Exceptions

ALWAYS use `logger.exception("msg", extra={...})` or `logger.error("msg", exc_info=True, extra={...})` inside `except` blocks. NEVER swallow an exception with `logger.error(str(e))` alone.

## Correlation

ALWAYS propagate correlation IDs through background tasks via `extra={}` fields and task metadata. NEVER start a new trace for downstream async work when a parent trace exists.

---

## Related Rules

- **`cross-domain.mdc`** — cross-cutting logging conventions
- **`api-routes.mdc`** — request log enrichment
- **`api-error-handling.mdc`** — log level alignment with error classification
- **`data-privacy.mdc`** — PII classification driving log redaction
- **`security.mdc`** — secret handling

## Specialist Validation

**Simple (add one log line):** None.
**Moderate (new logging helper, contextvar change):** Invoke `codebase-conventions-reviewer`.
**Complex (new log pipeline, redaction policy):** Invoke `security-sentinel` and `architecture-strategist`.
