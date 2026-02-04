---
name: LAYER_11_APM
description: Expert knowledge for APM (Observability) Layer modeling in Documentation Robotics
triggers:
  [
    "APM",
    "observability",
    "monitoring",
    "metrics",
    "spans",
    "traces",
    "logs",
    "OpenTelemetry",
    "telemetry",
  ]
version: 0.7.0
---

# APM Layer Skill

**Layer Number:** 11
**Specification:** Metadata Model Spec v0.7.0
**Purpose:** Defines observability using OpenTelemetry 1.0+, specifying traces, metrics, logs, and instrumentation.

---

## Layer Overview

The APM Layer captures **application performance monitoring**:

- **TRACES** - Distributed tracing with spans
- **METRICS** - Performance and business metrics
- **LOGS** - Structured logging
- **INSTRUMENTATION** - Code instrumentation configuration
- **RESOURCES** - Telemetry resource attributes
- **SLOs/SLAs** - Service level objectives and agreements

This layer uses **OpenTelemetry 1.0+** (industry standard for observability).

**Central Entity:** The **Span** (unit of work in trace) is the core modeling unit.

---

## Entity Types

### Core APM Entities (14 entities)

| Entity Type              | Description                                   |
| ------------------------ | --------------------------------------------- |
| **APMConfiguration**     | Root configuration for observability          |
| **TraceConfiguration**   | Distributed tracing configuration             |
| **Span**                 | Unit of work in distributed trace             |
| **SpanEvent**            | Timestamped event within span                 |
| **MetricConfiguration**  | Metrics collection configuration              |
| **MeterConfig**          | Meter for metric instruments                  |
| **InstrumentConfig**     | Metric instrument (counter, gauge, histogram) |
| **LogConfiguration**     | Structured logging configuration              |
| **LogRecord**            | Individual log record                         |
| **Resource**             | Telemetry resource attributes                 |
| **Attribute**            | Key-value telemetry attribute                 |
| **InstrumentationScope** | Scope of instrumentation                      |
| **DataQualityMetric**    | Data quality metrics                          |
| **DataQualityMetrics**   | Collection of data quality metrics            |

---

## When to Use This Skill

Activate when the user:

- Mentions "APM", "observability", "monitoring", "telemetry"
- Wants to add tracing, metrics, or logging
- Asks about performance monitoring or SLOs
- Needs to instrument code or track business metrics
- Wants to link observability to application services

---

## Cross-Layer Relationships

**Outgoing (APM → Other Layers):**

- `instrumented-service` → Application Layer (which service is being monitored?)
- `business-metrics` → Business Layer (business KPIs)

**Incoming (Other Layers → APM):**

- Application Layer → APM (services reference metrics)
- API Layer → APM (operations set SLA targets)
- Business Layer → APM (processes reference business metrics)
- Data Model Layer → APM (data quality metrics)
- Datastore Layer → APM (query performance metrics)

---

## Observability Best Practices

1. **Traces** - Add spans for critical operations
2. **Metrics** - Track both technical and business metrics
3. **Logs** - Use structured logging (JSON)
4. **Context** - Propagate trace context across services
5. **Sampling** - Configure appropriate sampling rates
6. **SLOs** - Define service level objectives
7. **Alerting** - Set up alerts for critical metrics
8. **Cardinality** - Avoid high-cardinality attributes

---

## Common Commands

```bash
# Add span
dr add apm span --name "Process Order"

# Add metric
dr add apm instrument-config --name "order_rate" --property type=counter

# Add log record
dr add apm log-record --name "Error Log"

# List APM elements
dr list apm span

# Validate APM layer
dr validate --layer apm

# Export APM configuration
dr export --layer apm --format json
```

---

## Example: Order Processing Span

```yaml
id: apm.span.process-order
name: "Process Order Span"
type: span
properties:
  spanKind: INTERNAL
  operationName: process_order
  attributes:
    - key: order.id
      type: string
    - key: order.total
      type: double
    - key: customer.id
      type: string
  events:
    - name: order_validated
      timestamp: relative
    - name: payment_processed
      timestamp: relative
    - name: inventory_reserved
      timestamp: relative
  instrumented-service: application.service.order-processing
  business-metrics:
    - apm.metric.orders-processed
    - apm.metric.order-processing-time
  sla-target-latency: 500ms
  sla-target-availability: 99.9%
```

---

## Example: Business Metrics

```yaml
id: apm.metric.order-rate
name: "Order Rate Metric"
type: instrument-config
properties:
  instrumentType: counter
  unit: orders
  description: "Number of orders processed"
  attributes:
    - key: order.type
      type: string
      values: [standard, express, subscription]
    - key: payment.method
      type: string
      values: [credit_card, paypal, bank_transfer]
  business-context:
    kpi: true
    dashboard: revenue-dashboard
    alerts:
      - threshold: 100
        condition: less-than
        severity: warning
        message: "Order rate below threshold"
```

---

## Example: Data Quality Metrics

```yaml
id: apm.data-quality-metrics.user-data
name: "User Data Quality Metrics"
type: data-quality-metrics
properties:
  entity: data_model.object-schema.user
  metrics:
    - name: completeness
      type: gauge
      description: "Percentage of non-null required fields"
      target: 95%
    - name: validity
      type: gauge
      description: "Percentage of records passing validation"
      target: 99%
    - name: uniqueness
      type: gauge
      description: "Percentage of unique email addresses"
      target: 100%
    - name: freshness
      type: histogram
      description: "Time since last update"
      target: 24h
```

---

## Pitfalls to Avoid

- ❌ Not propagating trace context across services
- ❌ High-cardinality attributes (e.g., unique IDs in tags)
- ❌ Missing business metrics (only technical metrics)
- ❌ Not setting SLOs/SLAs
- ❌ Over-instrumentation (too many spans)
- ❌ Missing cross-layer links to instrumented services
