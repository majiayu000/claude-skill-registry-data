---
name: observability-setup
description: Observability implementation including structured logging, metrics collection, distributed tracing, and alerting. Use when setting up monitoring.
---

# Observability Setup

Comprehensive guidance on implementing the three pillars of observability (logs, metrics, traces) with OpenTelemetry, structured logging, Prometheus metrics, distributed tracing, SLO-based alerting, and dashboard design.

## When to Use This Skill

Use this skill for:

- Setting up OpenTelemetry instrumentation (auto and manual)
- Implementing structured logging with correlation IDs
- Designing Prometheus metrics (counters, gauges, histograms)
- Configuring distributed tracing with span propagation
- Defining SLOs, SLIs, and error budgets
- Building Grafana dashboards
- Setting up alerting rules (Prometheus, PagerDuty)
- Deploying log aggregation (ELK stack, Grafana Loki)

**Trigger phrases**: "observability", "monitoring", "logging", "metrics", "tracing", "OpenTelemetry", "Prometheus", "Grafana", "dashboard", "alerting", "SLO", "SLI", "structured logging", "distributed tracing", "ELK", "Loki"

## What This Skill Does

Provides production-ready observability patterns including:

- **Structured Logging**: JSON log output, log levels, correlation IDs, context propagation
- **Metrics Collection**: RED and USE methods, counter/gauge/histogram instrumentation
- **Distributed Tracing**: OpenTelemetry SDK setup, span creation, context propagation, sampling
- **Alerting**: SLO-based alerts, error budgets, multi-window burn-rate alerts
- **Dashboards**: Grafana dashboard JSON, service overview panels, RED metrics
- **Log Aggregation**: ELK and Loki pipeline configuration

## Instructions

### Step 1: Understand the Three Pillars

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         OBSERVABILITY                                   │
├──────────────────┬──────────────────────┬────────────────────────────────┤
│       LOGS       │       METRICS        │          TRACES               │
│                  │                      │                                │
│  What happened   │  How the system      │  How a request flows          │
│  (discrete       │  behaves over time   │  through services             │
│   events)        │  (aggregated numbers)│  (causal chain)               │
│                  │                      │                                │
│  - Error details │  - Request rate      │  - Latency breakdown          │
│  - Audit trail   │  - Error percentage  │  - Service dependencies       │
│  - Debug context │  - Duration P50/P99  │  - Root cause analysis        │
│                  │  - CPU / memory      │  - Cross-service context      │
│                  │                      │                                │
│  Tools:          │  Tools:              │  Tools:                        │
│  ELK, Loki,      │  Prometheus, DD,     │  Jaeger, Tempo, Zipkin,       │
│  CloudWatch Logs │  CloudWatch Metrics  │  Datadog APM, X-Ray           │
└──────────────────┴──────────────────────┴────────────────────────────────┘
```

### Step 2: Set Up OpenTelemetry (Python)

**Install Dependencies**:

```bash
pip install opentelemetry-api \
            opentelemetry-sdk \
            opentelemetry-exporter-otlp \
            opentelemetry-instrumentation-flask \
            opentelemetry-instrumentation-requests \
            opentelemetry-instrumentation-sqlalchemy
```

**SDK Initialization**:

```python
# otel_setup.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def init_telemetry(service_name: str, service_version: str, otlp_endpoint: str):
    """Initialize OpenTelemetry with traces and metrics export."""
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "deployment.environment": "production",
    })

    # Tracing
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=otlp_endpoint),
            max_queue_size=2048,
            max_export_batch_size=512,
            schedule_delay_millis=5000,
        )
    )
    trace.set_tracer_provider(trace_provider)

    # Metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=otlp_endpoint),
        export_interval_millis=15000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Auto-instrumentation
    FlaskInstrumentor().instrument()
    RequestsInstrumentor().instrument()

    return trace.get_tracer(service_name), metrics.get_meter(service_name)
```

**Manual Instrumentation**:

```python
from opentelemetry import trace
from opentelemetry.trace import StatusCode

tracer = trace.get_tracer("order-service")

async def create_order(order_data: dict) -> dict:
    with tracer.start_as_current_span(
        "create_order",
        attributes={
            "order.customer_id": order_data["customer_id"],
            "order.item_count": len(order_data["items"]),
        },
    ) as span:
        try:
            # Validate
            with tracer.start_as_current_span("validate_order"):
                validated = validate(order_data)

            # Persist
            with tracer.start_as_current_span("persist_order"):
                order = await db.orders.insert(validated)
                span.set_attribute("order.id", order["id"])

            # Publish event
            with tracer.start_as_current_span("publish_order_event"):
                await event_bus.publish("order.created", order)

            span.set_status(StatusCode.OK)
            return order

        except ValidationError as e:
            span.set_status(StatusCode.ERROR, str(e))
            span.record_exception(e)
            raise
```

### Step 3: Set Up OpenTelemetry (Node.js)

```javascript
// tracing.js - Load BEFORE any other imports
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-grpc");
const { OTLPMetricExporter } = require("@opentelemetry/exporter-metrics-otlp-grpc");
const { PeriodicExportingMetricReader } = require("@opentelemetry/sdk-metrics");
const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");
const { Resource } = require("@opentelemetry/resources");
const { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } = require("@opentelemetry/semantic-conventions");

const sdk = new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: process.env.SERVICE_NAME || "my-service",
    [ATTR_SERVICE_VERSION]: process.env.SERVICE_VERSION || "1.0.0",
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4317",
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4317",
    }),
    exportIntervalMillis: 15000,
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      "@opentelemetry/instrumentation-http": {
        ignoreIncomingPaths: ["/health", "/ready"],
      },
      "@opentelemetry/instrumentation-fs": { enabled: false },
    }),
  ],
});

sdk.start();

process.on("SIGTERM", () => {
  sdk.shutdown().then(() => process.exit(0));
});
```

### Step 4: Implement Structured Logging

**Python (structlog)**:

```python
import structlog
import logging
import sys
from opentelemetry import trace

def add_trace_context(logger, method_name, event_dict):
    """Inject current trace/span IDs into every log record."""
    span = trace.get_current_span()
    ctx = span.get_span_context()
    if ctx.is_valid:
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict

def configure_logging(service_name: str, log_level: str = "INFO"):
    """Configure structured JSON logging with trace correlation."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            add_trace_context,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    )

    return structlog.get_logger(service=service_name)

# Usage
log = configure_logging("order-service")
log.info("order_created", order_id="abc-123", customer_id="cust-456", total=99.99)

# Output (single JSON line):
# {"service": "order-service", "event": "order_created",
#  "order_id": "abc-123", "customer_id": "cust-456", "total": 99.99,
#  "level": "info", "timestamp": "2026-03-03T10:30:00Z",
#  "trace_id": "abcdef1234567890abcdef1234567890",
#  "span_id": "1234567890abcdef"}
```

**Log Level Guidelines**:

```
LEVEL     | Use For                                | Example
----------|----------------------------------------|--------------------------------
DEBUG     | Detailed diagnostic info for devs      | "Executing SQL: SELECT ..."
INFO      | Normal operations, business events     | "Order created", "User login"
WARNING   | Unexpected but recoverable conditions  | "Retrying failed request (2/3)"
ERROR     | Failures requiring attention            | "Payment gateway timeout"
CRITICAL  | System-level failures, data corruption  | "Database connection pool exhausted"
```

### Step 5: Instrument Prometheus Metrics

**RED Method (Request-oriented services)**:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Rate: request throughput
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

# Errors: request failure rate
http_errors_total = Counter(
    "http_errors_total",
    "Total HTTP errors (4xx and 5xx)",
    ["method", "endpoint", "status_code"],
)

# Duration: request latency distribution
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Middleware
import time
from functools import wraps

def instrument_endpoint(method, endpoint):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                status = getattr(result, "status_code", 200)
                http_requests_total.labels(method, endpoint, status).inc()
                if status >= 400:
                    http_errors_total.labels(method, endpoint, status).inc()
                return result
            except Exception as e:
                http_requests_total.labels(method, endpoint, 500).inc()
                http_errors_total.labels(method, endpoint, 500).inc()
                raise
            finally:
                duration = time.perf_counter() - start
                http_request_duration_seconds.labels(method, endpoint).observe(duration)
        return wrapper
    return decorator
```

**USE Method (Infrastructure resources)**:

```python
# Utilization: how busy is the resource
cpu_utilization = Gauge(
    "cpu_utilization_ratio",
    "CPU utilization (0.0 to 1.0)",
)

# Saturation: how much work is queued
queue_depth = Gauge(
    "task_queue_depth",
    "Number of tasks waiting in the queue",
    ["queue_name"],
)

# Errors: resource-level errors
connection_errors_total = Counter(
    "db_connection_errors_total",
    "Database connection errors",
    ["database", "error_type"],
)

# Connection pool metrics
db_pool_active = Gauge("db_pool_active_connections", "Active DB connections")
db_pool_idle = Gauge("db_pool_idle_connections", "Idle DB connections")
db_pool_max = Gauge("db_pool_max_connections", "Max DB connections")
```

### Step 6: Configure Alerting (SLO-Based)

**Define SLOs and SLIs**:

```yaml
# slo-definitions.yaml
slos:
  - name: api-availability
    description: "API returns non-5xx responses"
    sli:
      type: request-based
      good: 'http_requests_total{status_code!~"5.."}'
      total: 'http_requests_total'
    target: 99.9       # 99.9% availability
    window: 30d        # Rolling 30-day window
    error_budget: 0.1  # 0.1% of requests can fail (43.2 min/month)

  - name: api-latency
    description: "API P99 latency under 500ms"
    sli:
      type: request-based
      good: 'http_request_duration_seconds_bucket{le="0.5"}'
      total: 'http_request_duration_seconds_count'
    target: 99.0
    window: 30d
```

**Prometheus Alerting Rules**:

```yaml
# alerts/slo-alerts.yaml
groups:
  - name: slo-alerts
    rules:
      # Multi-window burn-rate alert (fast burn)
      - alert: HighErrorBurnRate_Fast
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > (14.4 * 0.001)
          and
          (
            sum(rate(http_requests_total{status_code=~"5.."}[1h]))
            /
            sum(rate(http_requests_total[1h]))
          ) > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
          slo: api-availability
        annotations:
          summary: "High error burn rate: consuming error budget 14.4x faster than normal"
          description: "At current rate, the 30-day error budget will be exhausted in {{ $value | humanizeDuration }}"

      # Slow burn
      - alert: HighErrorBurnRate_Slow
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5.."}[6h]))
            /
            sum(rate(http_requests_total[6h]))
          ) > (1.0 * 0.001)
        for: 30m
        labels:
          severity: warning
          slo: api-availability
        annotations:
          summary: "Elevated error rate: consuming error budget faster than sustainable"

      # Latency SLO
      - alert: HighP99Latency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 0.5
        for: 10m
        labels:
          severity: warning
          slo: api-latency
        annotations:
          summary: "P99 latency exceeds 500ms SLO target"
```

### Step 7: Build Grafana Dashboards

**Service Overview Dashboard (JSON model)**:

```json
{
  "dashboard": {
    "title": "Service Overview - Order Service",
    "tags": ["service", "slo"],
    "panels": [
      {
        "title": "Request Rate",
        "type": "timeseries",
        "gridPos": { "h": 8, "w": 8, "x": 0, "y": 0 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"order-service\"}[5m]))",
            "legendFormat": "Total RPS"
          },
          {
            "expr": "sum(rate(http_requests_total{service=\"order-service\",status_code=~\"5..\"}[5m]))",
            "legendFormat": "Error RPS"
          }
        ]
      },
      {
        "title": "Latency Distribution",
        "type": "timeseries",
        "gridPos": { "h": 8, "w": 8, "x": 8, "y": 0 },
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{service=\"order-service\"}[5m])) by (le))",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service=\"order-service\"}[5m])) by (le))",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service=\"order-service\"}[5m])) by (le))",
            "legendFormat": "P99"
          }
        ]
      },
      {
        "title": "Error Budget Remaining (30d)",
        "type": "gauge",
        "gridPos": { "h": 8, "w": 8, "x": 16, "y": 0 },
        "targets": [
          {
            "expr": "1 - (sum(increase(http_requests_total{service=\"order-service\",status_code=~\"5..\"}[30d])) / sum(increase(http_requests_total{service=\"order-service\"}[30d])) / 0.001)",
            "legendFormat": "Budget Remaining"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                { "color": "red", "value": 0 },
                { "color": "yellow", "value": 0.25 },
                { "color": "green", "value": 0.5 }
              ]
            },
            "max": 1, "min": 0, "unit": "percentunit"
          }
        }
      }
    ]
  }
}
```

### Step 8: Deploy Log Aggregation

**Grafana Loki with Promtail**:

```yaml
# docker-compose.observability.yaml
services:
  loki:
    image: grafana/loki:2.9.0
    command: -config.file=/etc/loki/config.yaml
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yaml:/etc/loki/config.yaml
      - loki-data:/loki

  promtail:
    image: grafana/promtail:2.9.0
    command: -config.file=/etc/promtail/config.yaml
    volumes:
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./promtail-config.yaml:/etc/promtail/config.yaml

  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.95.0
    command: ["--config", "/etc/otel/config.yaml"]
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8888:8888"   # Prometheus metrics (self)
    volumes:
      - ./otel-collector-config.yaml:/etc/otel/config.yaml

  prometheus:
    image: prom/prometheus:v2.49.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yaml:/etc/prometheus/prometheus.yml
      - ./alerts:/etc/prometheus/alerts
      - prometheus-data:/prometheus

  grafana:
    image: grafana/grafana:10.3.0
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  tempo:
    image: grafana/tempo:2.3.0
    command: ["-config.file=/etc/tempo/config.yaml"]
    ports:
      - "3200:3200"   # Tempo HTTP
      - "4319:4317"   # OTLP gRPC (mapped to avoid conflict)
    volumes:
      - ./tempo-config.yaml:/etc/tempo/config.yaml

volumes:
  loki-data:
  prometheus-data:
  grafana-data:
```

**OpenTelemetry Collector Configuration**:

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
  attributes:
    actions:
      - key: environment
        value: production
        action: upsert

exporters:
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true
  prometheusremotewrite:
    endpoint: http://prometheus:9090/api/v1/write
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlp/tempo]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheusremotewrite]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [loki]
```

## Best Practices

- **Correlate all three pillars** by injecting trace IDs into logs and linking metrics to traces
- **Use structured JSON logs**; never use unstructured text in production
- **Define SLOs before building dashboards**; SLOs drive what you alert on
- **Alert on symptoms, not causes**; alert on high error rate, not on a single pod restart
- **Use multi-window burn-rate alerts** instead of static threshold alerts; they reduce false positives
- **Sample traces** in production (head-based for throughput, tail-based for errors)
- **Keep cardinality low** for metric labels; avoid user IDs, request IDs, or unbounded values
- **Set retention policies** by data tier (hot for recent, warm for weeks, cold for archival)
- **Instrument at service boundaries** as a starting point before adding method-level spans
- **Include a runbook link** in every alert annotation

## Common Patterns

### Pattern 1: Correlation ID Propagation

```python
import uuid
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

def middleware(request, call_next):
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    correlation_id.set(cid)
    response = call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response
```

### Pattern 2: Health Check Endpoints

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/health")
async def health():
    """Liveness probe: is the process running?"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/ready")
async def ready():
    """Readiness probe: can the service handle traffic?"""
    checks = {
        "database": await check_db(),
        "cache": await check_redis(),
    }
    all_ok = all(v["status"] == "ok" for v in checks.values())
    return {"status": "ok" if all_ok else "degraded", "checks": checks}
```

### Pattern 3: Custom Business Metrics

```python
from prometheus_client import Counter, Histogram

orders_created = Counter("orders_created_total", "Total orders created", ["payment_method"])
order_value = Histogram(
    "order_value_dollars", "Order value in dollars",
    buckets=[10, 25, 50, 100, 250, 500, 1000],
)

def on_order_created(order):
    orders_created.labels(payment_method=order.payment_method).inc()
    order_value.observe(order.total)
```

## Quality Checklist

- [ ] OpenTelemetry SDK initialized before any application code runs
- [ ] Structured JSON logging configured with trace ID correlation
- [ ] RED metrics (Rate, Errors, Duration) instrumented for all HTTP endpoints
- [ ] USE metrics (Utilization, Saturation, Errors) instrumented for infrastructure resources
- [ ] SLOs defined for critical user journeys
- [ ] Multi-window burn-rate alerting rules deployed
- [ ] Grafana dashboards display request rate, latency percentiles, and error budget
- [ ] Health and readiness endpoints exposed (excluded from tracing)
- [ ] Log retention and sampling policies documented
- [ ] Metric label cardinality reviewed (no unbounded labels)
- [ ] Runbook links included in all alert annotations
- [ ] Traces propagate across service boundaries via W3C Trace Context headers

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We'll add monitoring after launch when we see what breaks" | The first outage without observability in place is diagnosed by guesswork; the Facebook 2021 outage demonstrated that without distributed tracing, engineers spent hours identifying a BGP configuration change as the root cause of a 6-hour global outage. |
| "Logs are enough — we don't need metrics or traces" | Logs answer "what happened"; metrics answer "how often and how bad"; traces answer "where in the call chain"; any one of the three alone leaves a class of incidents undiagnosable. The 2020 SolarWinds response required all three pillars to understand blast radius. |
| "High-cardinality labels are fine; storage is cheap" | High-cardinality metric labels (user IDs, request IDs as label values) cause Prometheus cardinality explosions that have taken down monitoring infrastructure at scale; the observability layer fails exactly when it is most needed. |
| "Alerts on every metric prevent incidents" | Alert fatigue from over-alerting causes on-call engineers to mute or ignore alerts, which was a contributing factor in the 2017 Equifax breach where critical alerts went unnoticed; alert only on SLO breaches and actionable conditions. |
| "Health check endpoints are optional if the service is up" | Liveness and readiness probes are how orchestrators (Kubernetes, ECS) distinguish "running but broken" from "healthy"; without them, a deadlocked process continues to receive traffic because the orchestrator believes it is healthy. |
| "We don't need runbooks if the alerts are self-explanatory" | Alert annotations without runbook links require on-call engineers to reconstruct diagnostic steps from memory under pressure; runbooks reduce mean-time-to-resolve even for experienced engineers by eliminating recall errors. |

## Verification

- [ ] Structured logs emitted for every request with correlation ID, service name, and log level (verified by running a request and checking log output)
- [ ] Prometheus metrics endpoint (`/metrics`) returns data for request rate, error rate, and latency (p50, p95, p99)
- [ ] At least one Grafana dashboard exists displaying the four golden signals (latency, traffic, errors, saturation)
- [ ] Distributed traces propagate across service boundaries: a single user request produces a linked trace visible in the tracing backend
- [ ] SLO-based alerts are configured with runbook links in annotations; no alert fires without a linked runbook
- [ ] Metric label cardinality reviewed and no label uses user ID, request ID, or other unbounded values

## Related Skills

- `cicd-architect` - Integrating observability into CI/CD pipelines
- `kubernetes-expert` - Kubernetes-specific monitoring (kube-state-metrics, cAdvisor)
- `cloud-architect` - Cloud-native monitoring services (CloudWatch, Stackdriver)
- `async-patterns` - Tracing asynchronous and concurrent workflows

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
