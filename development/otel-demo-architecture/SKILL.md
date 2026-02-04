---
name: otel-demo-architecture
description: OpenTelemetry Demo system architecture reference for debugging service dependencies, port conflicts, memory issues, telemetry gaps, and performance problems. Use when analyzing failures, understanding service topology, troubleshooting communication issues, or investigating system bottlenecks in the OTel demo environment.
---

# OpenTelemetry Demo Architecture

Quick reference for the OpenTelemetry Demo microservices system. Focus on service dependencies, critical paths, and common failure patterns.

**For detailed observability queries**: See the [Observability Query Guides](#observability-query-guides) section below for comprehensive metrics, traces, and logs references.

## Service Dependency Matrix

| Service | Language | Depends On | Protocol | Memory Limit |
|---------|----------|------------|----------|--------------|
| **frontend** | TypeScript | ad, cart, checkout, currency, product-catalog, recommendation, shipping, image-provider | gRPC | 250M |
| **checkout** | Go | cart, currency, email, payment, product-catalog, shipping, kafka | gRPC, HTTP | 20M |
| **cart** | .NET | valkey-cart, flagd | - | 160M |
| **product-catalog** | Go | flagd | - | 20M |
| **recommendation** | Python | product-catalog, flagd | gRPC | 50M |
| **shipping** | Rust | quote | HTTP | 20M |
| **payment** | JavaScript | flagd | - | 120M |
| **ad** | Java | flagd | gRPC | 300M |
| **email** | Ruby | - | - | 100M |
| **currency** | C++ | - | - | 20M |
| **quote** | PHP | - | - | 40M |
| **fraud-detection** | Kotlin | kafka, flagd | TCP | - |
| **product-reviews** | Python | product-catalog, llm, postgresql, flagd | gRPC | - |
| **accounting** | .NET | kafka, postgresql | TCP | - |
| **frontend-proxy** | Envoy | frontend, flagd, flagd-ui, image-provider | HTTP | 65M |
| **image-provider** | nginx | - | - | 120M |
| **load-generator** | Python | frontend-proxy, flagd | HTTP | 120M |

## Critical Service Paths

**User Request Flow:**
```
Internet → frontend-proxy:ENVOY_PORT → frontend → [cart, product-catalog, recommendation, checkout]
```

**Checkout/Order Flow:**
```
checkout → cart (gRPC)
        → currency (gRPC)
        → payment (gRPC)
        → product-catalog (gRPC)
        → shipping (HTTP) → quote (HTTP)
        → email (HTTP)
        → kafka → [accounting, fraud-detection]
```

**Telemetry Flow:**
```
All services → otel-collector:4317(gRPC)/4318(HTTP) → [jaeger, prometheus, tempo, opensearch]
                                                     → grafana (visualization)
```

## Observability Stack Details

### Metrics Pipeline
```
Services → otel-collector (OTLP) → prometheus (scrape/remote-write) → grafana
```

### Traces Pipeline
```
Services → otel-collector (OTLP) → [jaeger, tempo] → grafana
```

### Logs Pipeline
```
Services → docker json-file → alloy → loki → grafana
```

### Log Configuration
All services use json-file driver:
- Max size: 5M
- Max files: 2
- Auto-rotation

## Observability Query Guides

Detailed reference guides for querying observability data:

### Metrics Guide
See [metrics-guide.md](references/metrics-guide.md) for:
- **Complete Prometheus metrics catalog** - All 260+ available metrics organized by category
- **Service-specific metrics** - Application metrics for each demo service
- **HTTP/RPC metrics** - Request rates, latencies, error rates
- **Runtime metrics** - Go, .NET, JVM, Node.js, Python runtime instrumentation
- **Container metrics** - CPU, memory, network, disk I/O
- **Feature flag metrics** - Flag evaluation and impression tracking
- **OTEL Collector metrics** - Pipeline health and throughput
- **Common label patterns** - Service identification, filtering, aggregation
- **Query patterns** - Request rates, error rates, percentiles, top-N

**When to use**: Building dashboards, investigating performance issues, analyzing resource utilization, monitoring service health.

### Traces Guide
See [traces-guide.md](references/traces-guide.md) for:
- **TraceQL syntax and patterns** - Complete query language reference
- **Resource attributes** - Service, host, process, runtime identification (27 attributes)
- **Span attributes** - HTTP, gRPC, database, application-specific (150+ attributes)
- **Event attributes** - Exceptions, feature flags, business events
- **Intrinsic attributes** - Duration, status, kind, instrumentation
- **Service-specific attributes** - Cart, product, payment, shipping, ad service patterns
- **Common query patterns** - Error investigation, performance analysis, feature flag impact

**When to use**: Debugging distributed transactions, investigating latency issues, understanding service dependencies, tracing business transactions.

### Logs Guide
See [logs-guide.md](references/logs-guide.md) for:
- **LogQL syntax and patterns** - Complete query language reference
- **Available labels** - service_name, container, project (5 labels)
- **Service identification** - All 16 application and infrastructure services
- **Common query patterns** - Errors, HTTP requests, performance, business events
- **Log parsing** - JSON parsing, pattern extraction, label filtering
- **Aggregations** - Count, rate, percentiles, error percentages
- **Multi-service analysis** - Cross-service errors, communication tracing

**When to use**: Investigating errors, debugging application logic, analyzing request patterns, root cause analysis.
