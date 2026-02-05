---
name: FastAPI Observability
description: This skill should be used when the user asks to "add logging", "implement metrics", "add tracing", "configure Prometheus", "setup OpenTelemetry", "add health checks", "monitor API", or mentions observability, APM, monitoring, structured logging, distributed tracing, or Grafana. Provides comprehensive observability patterns.
version: 0.1.0
---

# FastAPI Observability

This skill provides production-ready observability patterns including structured logging, Prometheus metrics, and OpenTelemetry tracing.

## Structured Logging

### Configuration with structlog

```python
# app/core/logging.py
import structlog
import logging
import sys
from typing import Any

def setup_logging(log_level: str = "INFO", json_logs: bool = True):
    """Configure structured logging."""

    # Shared processors
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if json_logs:
        # JSON format for production
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ]
    else:
        # Console format for development
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer()
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name: str = None) -> structlog.BoundLogger:
    return structlog.get_logger(name)
```

### Request Logging Middleware

```python
# app/middleware/logging.py
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import structlog

logger = structlog.get_logger()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Bind context for all logs in this request
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None
        )

        # Add request ID to response headers
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Log request completion
        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            content_length=response.headers.get("content-length")
        )

        return response
```

### Application Logging

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

async def create_user(data: UserCreate) -> User:
    logger.info("creating_user", email=data.email)

    try:
        user = await User(**data.model_dump()).insert()
        logger.info("user_created", user_id=str(user.id))
        return user
    except Exception as e:
        logger.error("user_creation_failed", error=str(e), email=data.email)
        raise
```

## Prometheus Metrics

### Setup with prometheus-fastapi-instrumentator

```python
# app/core/metrics.py
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
from functools import wraps

# Custom metrics
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total request count",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ACTIVE_REQUESTS = Gauge(
    "app_active_requests",
    "Number of active requests"
)

DB_QUERY_LATENCY = Histogram(
    "app_db_query_latency_seconds",
    "Database query latency",
    ["operation", "collection"]
)

CACHE_HITS = Counter(
    "app_cache_hits_total",
    "Cache hit count",
    ["cache_name"]
)

CACHE_MISSES = Counter(
    "app_cache_misses_total",
    "Cache miss count",
    ["cache_name"]
)

def setup_metrics(app):
    """Setup Prometheus metrics instrumentation."""
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
```

### Custom Metric Decorators

```python
import time
from functools import wraps

def track_db_query(operation: str, collection: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                DB_QUERY_LATENCY.labels(
                    operation=operation,
                    collection=collection
                ).observe(duration)
        return wrapper
    return decorator

def track_cache(cache_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            if result is not None:
                CACHE_HITS.labels(cache_name=cache_name).inc()
            else:
                CACHE_MISSES.labels(cache_name=cache_name).inc()
            return result
        return wrapper
    return decorator

# Usage
class UserRepository:
    @track_db_query("find", "users")
    async def find_by_id(self, user_id: str):
        return await User.get(user_id)

    @track_cache("users")
    async def get_cached(self, user_id: str):
        return await cache.get(f"user:{user_id}")
```

## OpenTelemetry Tracing

### Setup

```python
# app/core/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

def setup_tracing(app, service_name: str, otlp_endpoint: str):
    """Setup OpenTelemetry tracing."""

    # Create resource
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0.0",
    })

    # Setup tracer provider
    provider = TracerProvider(resource=resource)

    # Add OTLP exporter
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Instrument HTTP client
    HTTPXClientInstrumentor().instrument()

    # Instrument Redis
    RedisInstrumentor().instrument()

def get_tracer(name: str) -> trace.Tracer:
    return trace.get_tracer(name)
```

### Custom Spans

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

async def process_order(order_id: str):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        try:
            # Validate order
            with tracer.start_as_current_span("validate_order"):
                order = await validate_order(order_id)
                span.set_attribute("order.total", order.total)

            # Process payment
            with tracer.start_as_current_span("process_payment"):
                payment = await process_payment(order)
                span.set_attribute("payment.id", payment.id)

            # Update inventory
            with tracer.start_as_current_span("update_inventory"):
                await update_inventory(order.items)

            span.set_status(Status(StatusCode.OK))
            return order

        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
```

## Health Check Endpoints

```python
# app/routes/health.py
from fastapi import APIRouter, Response
from typing import Dict, Any
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health() -> Dict[str, str]:
    """Kubernetes liveness probe."""
    return {"status": "ok"}

@router.get("/health/ready")
async def ready(
    db: Database = Depends(get_db),
    cache: RedisCache = Depends(get_cache)
) -> Response:
    """Kubernetes readiness probe with dependency checks."""
    checks = {}
    status = HealthStatus.HEALTHY

    # MongoDB check
    try:
        await db.command("ping")
        checks["mongodb"] = {"status": "ok", "latency_ms": 0}
    except Exception as e:
        checks["mongodb"] = {"status": "error", "error": str(e)}
        status = HealthStatus.UNHEALTHY

    # Redis check
    try:
        start = time.perf_counter()
        await cache.client.ping()
        latency = (time.perf_counter() - start) * 1000
        checks["redis"] = {"status": "ok", "latency_ms": round(latency, 2)}
    except Exception as e:
        checks["redis"] = {"status": "error", "error": str(e)}
        status = HealthStatus.DEGRADED  # Cache failure = degraded

    response_data = {
        "status": status.value,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }

    status_code = 200 if status != HealthStatus.UNHEALTHY else 503
    return Response(
        content=json.dumps(response_data),
        status_code=status_code,
        media_type="application/json"
    )

@router.get("/health/live")
async def live() -> Dict[str, str]:
    """Simple liveness check."""
    return {"status": "alive"}
```

## Application Integration

```python
from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.metrics import setup_metrics
from app.core.tracing import setup_tracing

def create_app() -> FastAPI:
    # Setup logging first
    setup_logging(
        log_level=settings.log_level,
        json_logs=settings.environment == "production"
    )

    app = FastAPI(title="API Service")

    # Setup metrics
    setup_metrics(app)

    # Setup tracing
    if settings.otlp_endpoint:
        setup_tracing(
            app,
            service_name="api-service",
            otlp_endpoint=settings.otlp_endpoint
        )

    # Add middleware
    app.add_middleware(RequestLoggingMiddleware)

    return app
```

## Additional Resources

### Reference Files

For detailed configuration:
- **`references/grafana-dashboards.md`** - Grafana dashboard JSON
- **`references/alerting.md`** - Prometheus alerting rules
- **`references/elk-setup.md`** - Elasticsearch/Kibana log aggregation

### Example Files

Working examples in `examples/`:
- **`examples/logging_config.py`** - Complete logging setup
- **`examples/metrics_middleware.py`** - Custom metrics middleware
- **`examples/tracing_service.py`** - Service with tracing
