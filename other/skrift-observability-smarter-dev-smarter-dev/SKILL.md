---
name: skrift-observability
description: "Skrift logging and observability — Pydantic Logfire integration, structured tracing, ASGI/SQL/HTTPX instrumentation, and no-op degradation."
---

# Skrift Observability

Optional structured observability powered by Pydantic Logfire. Provides request tracing, SQL query visibility, HTTP client tracking, and hook execution spans. Gracefully no-ops when logfire is not installed or not enabled.

## Installation

```bash
pip install skrift[logfire]
```

This installs `logfire[asgi,sqlalchemy,httpx]>=3.0.0`. Without this extra, the observability module silently no-ops.

## Configuration

### app.yaml

```yaml
logfire:
  enabled: true
  service_name: my-site       # defaults to "skrift"
  environment: production      # defaults to SKRIFT_ENV
  sample_rate: 1.0             # 0.0–1.0, trace sampling rate
  console: true                # print spans to console (dev convenience)
```

### Environment Variables

```bash
LOGFIRE_TOKEN=your-logfire-token   # Logfire reads this natively
```

The integration uses `send_to_logfire="if-token-present"`, so it works without a token in development (console-only mode).

### Config Model

```python
class LogfireConfig(BaseModel):
    enabled: bool = False
    service_name: str = "skrift"
    environment: str | None = None
    sample_rate: float = 1.0
    console: bool = False
```

Defined in `skrift/config.py`, accessed via `settings.logfire`.

## Architecture

### Facade Module (`skrift/lib/observability.py`)

All observability goes through a thin facade that guards on a module-level `_logfire` variable. When logfire is not installed or not enabled, every function is a no-op.

| Function | Purpose |
|----------|---------|
| `configure(settings)` | Initialize logfire from `LogfireConfig`. Called once in `create_app()`. |
| `instrument_app(app)` | Wrap ASGI app with `logfire.instrument_asgi()`. Returns app unchanged if unavailable. |
| `instrument_sqlalchemy(engine)` | Instrument a SQLAlchemy engine for SQL query tracing. |
| `instrument_httpx()` | Instrument httpx globally for HTTP client tracing. |
| `span(name, **attrs)` | Context manager yielding a logfire span or `None`. |
| `info(msg, **kwargs)` | Structured log at info level, or no-op. |
| `error(msg, **kwargs)` | Structured log at error level, or no-op. |
| `warning(msg, **kwargs)` | Structured log at warning level, or no-op. |
| `get_logfire()` | Return raw `logfire` module or `None` for advanced usage. |
| `is_available()` | `True` if logfire is installed and configured. |

### Instrumentation Points

Wired in `skrift/asgi.py` during `create_app()`:

1. **Early** (before app creation): `configure(settings)`, `instrument_httpx()`
2. **On startup** (after DB ready): `instrument_sqlalchemy(engine)`, fire `logfire_configured` hook
3. **App wrapping**: `instrument_app(app)` wraps the Litestar ASGI app

### Hook Spans

`HookRegistry.do_action()` and `apply_filters()` in `skrift/lib/hooks.py` are wrapped with spans:

```python
with span(f"hook.action:{hook_name}", hook_name=hook_name):
    # execute handlers
```

Only adds overhead when logfire is active.

### OAuth Span

The `_exchange_and_fetch()` function in `skrift/controllers/auth.py` wraps the token exchange + user info fetch:

```python
with span("oauth.exchange:{provider_key}", provider_key=provider_key):
    # token exchange + user info fetch
```

## Using Observability in User Code

### Custom Spans

```python
from skrift.lib.observability import span

with span("my_operation", item_id=str(item.id)):
    result = await do_something()
```

### Structured Logging

```python
from skrift.lib.observability import info, error

info("Page published", page_id=str(page.id), slug=page.slug)
error("Payment failed", order_id=str(order.id), reason=str(e))
```

### Advanced: Raw Logfire Access

```python
from skrift.lib.observability import get_logfire

lf = get_logfire()
if lf:
    # Use any logfire API directly
    lf.instrument_celery()
```

### Extensibility via Hooks

The `logfire_configured` action fires after instrumentation is complete:

```python
from skrift.lib.hooks import action
from skrift.lib.observability import get_logfire

@action("logfire_configured")
async def my_custom_instrumentation():
    lf = get_logfire()
    if lf:
        # Add custom instrumentation
        pass
```

## What Gets Traced

When enabled, you get automatic visibility into:

- **HTTP requests** — ASGI middleware traces every request with method, path, status, duration
- **SQL queries** — Every SQLAlchemy query with statement text and parameters
- **HTTP client calls** — All httpx requests (OAuth exchanges, external APIs)
- **Hook execution** — Every `do_action()` and `apply_filters()` call with hook name
- **OAuth flows** — Token exchange + user info fetch grouped in a single span

## No-Op Behavior

When logfire is not installed or `logfire.enabled` is `false`:

- All facade functions return immediately or yield `None`
- `instrument_app()` returns the app unchanged
- `span()` yields `None`
- Zero import overhead (logfire import is inside `configure()`)
- Existing tests pass without changes

## Hook Constants

```python
from skrift.lib.hooks import LOGFIRE_CONFIGURED

# LOGFIRE_CONFIGURED = "logfire_configured"
```

## Key Files

| File | Purpose |
|------|---------|
| `skrift/lib/observability.py` | Facade module — all observability API |
| `skrift/config.py` | `LogfireConfig` model |
| `skrift/asgi.py` | Wiring: configure, instrument, wrap app |
| `skrift/lib/hooks.py` | Span wrapping on `do_action`/`apply_filters` |
| `skrift/controllers/auth.py` | OAuth exchange span |
