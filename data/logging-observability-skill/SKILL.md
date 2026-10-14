---
name: logging-observability-skill
description: >-
  Structured logging and observability — Winston, pino, structlog,
  OpenTelemetry, Sentry, correlation IDs.
license: Apache-2.0
compatibility: opencode
category: DevOps
---

## What I do

I help you implement comprehensive logging and observability:

1. **Structured Logging**: JSON logging with Winston, pino, and structlog
2. **OpenTelemetry**: Distributed tracing and metrics instrumentation
3. **Error Monitoring**: Sentry integration patterns for error tracking
4. **Correlation IDs**: Request tracing across services
5. **Log Levels**: Proper level usage and filtering strategies
6. **Observability Stack**: Setup guidance for ELK, Grafana, Jaeger

## When to use me

Use this skill when:
- Setting up structured logging in a new project
- Integrating OpenTelemetry for distributed tracing
- Configuring Sentry for error monitoring
- Implementing correlation IDs for request tracing
- Designing log aggregation architecture
- Choosing between logging libraries (Winston vs pino, structlog vs logging)
- Setting up log levels and filtering
- Creating observability dashboards and alerts

## Related Skills

- **error-resolver-workflow-skill**: Handles runtime error *diagnosis*. This skill handles *instrumentation setup* (Sentry integration, structured logging configuration). Error-resolver consumes the data this skill produces.
- **docker-containerization-skill**: Container log driver configuration.
- **performance-optimization-skill**: Uses tracing data for performance analysis.

---

## Step 1: Structured Logging

### Node.js (pino - Recommended for performance)

```typescript
import pino from "pino"

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport:
    process.env.NODE_ENV === "development"
      ? { target: "pino-pretty", options: { colorize: true } }
      : undefined,
  formatters: {
    level: (label) => ({ level: label }),
  },
  defaultMeta: {
    service: "my-api",
    version: process.env.APP_VERSION || "1.0.0",
  },
})

export default logger
```

### Node.js (Winston - More configurable)

```typescript
import winston from "winston"

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: "my-api" },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "logs/error.log", level: "error" }),
  ],
})

if (process.env.NODE_ENV !== "production") {
  logger.add(
    new winston.transports.Console({
      format: winston.format.combine(winston.format.colorize(), winston.format.simple()),
    })
  )
}
```

### Python (structlog - Recommended)

```python
import structlog
import logging

def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")),
    )

log = structlog.get_logger()
```

### Usage

```python
log.info("user_created", user_id=user.id, email=user.email)
log.error("database_connection_failed", error=str(e), retry_count=3)
log.warning("slow_query", query=sql, duration_ms=1500, threshold_ms=1000)

with structlog.contextvars.bound_contextvars(request_id=request_id, user_id=user_id):
    log.info("processing_order", order_id=order.id)
```

### Silent Failure in Sequential Async (`silent-failure-sequential-async`)

Helper functions that catch failures with only `console.error` swallow errors silently. Callers proceed with missing or stale data, and the failure becomes invisible in production. Either rethrow (let the caller decide) or return a discriminated union so the caller can handle success/failure explicitly.

```typescript
// BEFORE: Failure swallowed — caller has no way to react
async function fetchSidebarData(userId: string) {
  try {
    return await api.get(`/users/${userId}/sidebar`)
  } catch (error) {
    console.error("Failed to fetch sidebar data", error)
    return null
  }
}

// Caller proceeds with null, showing empty sidebar with no explanation
const sidebar = await fetchSidebarData(userId)
renderSidebar(sidebar) // renders nothing, user sees blank space

// AFTER (option 1): Rethrow — let the caller handle the error
async function fetchSidebarData(userId: string) {
  return api.get(`/users/${userId}/sidebar`) // no try/catch
}

// Caller can show fallback UI
try {
  const sidebar = await fetchSidebarData(userId)
  renderSidebar(sidebar)
} catch (error) {
  renderSidebarFallback(error)
}

// AFTER (option 2): Discriminated union — caller gets structured result
type Result<T> = { ok: true; value: T } | { ok: false; error: Error }

async function fetchSidebarData(userId: string): Promise<Result<Sidebar>> {
  try {
    const data = await api.get(`/users/${userId}/sidebar`)
    return { ok: true, value: data }
  } catch (error) {
    return { ok: false, error: error instanceof Error ? error : new Error(String(error)) }
  }
}

const result = await fetchSidebarData(userId)
if (!result.ok) {
  log.error("sidebar_fetch_failed", { userId, error: result.error.message })
  renderSidebarFallback(result.error)
} else {
  renderSidebar(result.value)
}
```

**Rule**: Never silently swallow errors in async helpers. Either rethrow or return a discriminated union that forces the caller to acknowledge both outcomes.

---

## Step 2: Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| TRACE | Detailed function-level tracing | `trace("cache_lookup", key=cache_key)` |
| DEBUG | Development-time diagnostics | `debug("sql_query", query=sql, params=params)` |
| INFO | Business events, normal operations | `info("user_login", user_id=user.id)` |
| WARN | Unexpected but handled situations | `warning("slow_query", duration_ms=1500)` |
| ERROR | Failures requiring attention | `error("payment_failed", order_id=id, error=str(e))` |
| FATAL | Application cannot continue | `fatal("database_unavailable")` |

### Rules

1. **INFO and above** in production (DEBUG in development)
2. **Never log secrets** — mask tokens, passwords, API keys
3. **Include context** — request_id, user_id, correlation_id
4. **Use structured fields** — not free-form messages
5. **Log at the boundary** — incoming requests, outgoing calls, errors

### Log Masking

```python
def mask_sensitive(data: dict) -> dict:
    SENSITIVE_KEYS = {"password", "token", "secret", "api_key", "credit_card"}
    masked = {}
    for key, value in data.items():
        if any(s in key.lower() for s in SENSITIVE_KEYS):
            masked[key] = "***REDACTED***"
        elif isinstance(value, dict):
            masked[key] = mask_sensitive(value)
        else:
            masked[key] = value
    return masked
```

---

## Step 3: Correlation IDs

### FastAPI Middleware

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        correlation_id = request.headers.get(
            "X-Correlation-ID", str(uuid.uuid4())
        )
        request.state.correlation_id = correlation_id

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id,
            request_id=str(uuid.uuid4()),
        )

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response
```

### Next.js API Route

```typescript
import { NextRequest, NextResponse } from "next/server"
import { v4 as uuidv4 } from "uuid"

export function middleware(request: NextRequest) {
  const correlationId = request.headers.get("x-correlation-id") || uuidv4()
  const response = NextResponse.next()
  response.headers.set("x-correlation-id", correlationId)
  return response
}
```

---

## Step 4: OpenTelemetry

### Python (FastAPI)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def setup_telemetry(app):
    provider = TracerProvider()
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")))
    )
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)
```

### Node.js

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node"
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http"
import { getResourceAttributes } from "@opentelemetry/sdk-node"

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: ["@opentelemetry/instrumentation-http", "@opentelemetry/instrumentation-express"],
})

sdk.start()
```

---

## Step 5: Error Monitoring (Sentry)

### Python

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENVIRONMENT", "development"),
    release=os.environ.get("APP_VERSION", "1.0.0"),
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    before_send=mask_sensitive_data,
)
```

### Next.js

```typescript
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.VERCEL_ENV || "development",
  release: process.env.NEXT_PUBLIC_APP_VERSION,
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0,
  replaysOnErrorSampleRate: 1.0,
})
```

---

## Step 6: Observability Stack Setup

### Recommended Architecture

```
Application → OTel Collector → [Jaeger (traces)]
                            → [Prometheus (metrics)]
                            → [Loki/ELK (logs)]
                            → [Grafana (visualization)]
```

### Docker Compose (Development)

```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "4317:4317"    # OTLP gRPC
    environment:
      COLLECTOR_OTLP_ENABLED: true

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  grafana-data:
```

### Health Check with Observability

```python
@app.get("/health")
async def health():
    checks = {
        "database": await check_db(),
        "redis": await check_redis(),
        "upstream": await check_upstream(),
    }
    healthy = all(checks.values())
    status_code = 200 if healthy else 503

    log.info("health_check", checks=checks, healthy=healthy)
    return JSONResponse(content={"status": "healthy" if healthy else "degraded", "checks": checks}, status_code=status_code)
```
