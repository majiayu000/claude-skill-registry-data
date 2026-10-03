---
name: monitoring
description: Implement observability with metrics, logs, and traces. Set up alerting, dashboards, and SLIs/SLOs for system reliability.
triggers:
- /monitoring
- /observability
- /alerting
---

# Observability and Monitoring

This skill covers implementing comprehensive observability through metrics, logs, traces, and alerts to ensure system reliability and performance.

## When to use this skill

Use this skill when you need to:
- Set up monitoring for applications and infrastructure
- Define and track SLIs and SLOs
- Create meaningful dashboards
- Configure intelligent alerting
- Implement distributed tracing

## Prerequisites

- Monitoring stack (Prometheus, Grafana, Datadog, New Relic)
- Log aggregation (ELK, Loki, Splunk)
- Application instrumentation libraries
- Alerting channels (PagerDuty, Slack, email)

## Guidelines

### Observability Pillars

**Metrics**
- Numeric measurements over time
- Used for: trends, capacity planning, alerting
- Tools: Prometheus, InfluxDB, CloudWatch

**Logs**
- Discrete event records
- Used for: debugging, auditing, forensics
- Tools: ELK Stack, Loki, Splunk

**Traces**
- Request flow across services
- Used for: latency analysis, dependency mapping
- Tools: Jaeger, Zipkin, OpenTelemetry

### Metrics Strategy

**Metric Types**
- **Counters**: Always increasing (requests, errors)
- **Gauges**: Current value (temperature, queue size)
- **Histograms**: Distribution of values (response times)
- **Summaries**: Percentile calculations (p95, p99)

**Prometheus Example**
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
request_count = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds', 'Request duration')
active_connections = Gauge('active_connections', 'Current active connections')

# Instrument code
@request_duration.time()
def handle_request(request):
    request_count.labels(method=request.method, endpoint=request.path).inc()
    active_connections.inc()
    try:
        return process_request(request)
    finally:
        active_connections.dec()
```

**Key Metrics to Track**
- RED metrics (Rate, Errors, Duration) for services
- USE metrics (Utilization, Saturation, Errors) for resources
- Business metrics (transactions, revenue)
- Infrastructure metrics (CPU, memory, disk, network)

### SLIs and SLOs

**Service Level Indicators (SLIs)**
Quantifiable measures of service quality:
- Availability: percentage of successful requests
- Latency: response time percentiles
- Throughput: requests per second
- Error rate: failed requests percentage

**Service Level Objectives (SLOs)**
Target reliability levels:
```yaml
# Example SLOs
availability_slo: 99.9%  # Three nines
latency_p95_slo: 200ms   # 95% of requests under 200ms
error_rate_slo: 0.1%     # Less than 0.1% errors
```

**Error Budgets**
- SLO of 99.9% = 0.1% error budget
- 43.8 minutes of downtime per month
- Use for: feature launch decisions, maintenance windows

### Alerting

**Alerting Principles**
- Alert on symptoms, not causes
- Use multiple severity levels
- Include runbook links
- Prevent alert fatigue

**Prometheus Alerting Rules**
```yaml
# alerts.yml
groups:
  - name: service_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook_url: "https://wiki.internal/runbooks/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
```

### Dashboards

**Grafana Dashboard Guidelines**
- Use template variables for reusability
- Group related panels
- Include RED metrics for each service
- Add documentation links
- Use consistent color schemes

**Dashboard Structure**
```
Overview Dashboard
├── Service Health (availability, latency, errors)
├── Infrastructure (CPU, memory, disk)
├── Business Metrics (transactions, revenue)
└── Alerts Status

Service Detail Dashboard
├── Request Rate
├── Error Rate
├── Latency Distribution
├── Top Endpoints
└── Dependencies
```

### Distributed Tracing

**OpenTelemetry Setup**
```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add exporter
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument code
with tracer.start_as_current_span("process_order") as span:
    span.set_attribute("order.id", order_id)
    span.set_attribute("customer.id", customer_id)
    
    with tracer.start_as_current_span("validate_payment"):
        validate_payment(payment_info)
    
    with tracer.start_as_current_span("update_inventory"):
        update_inventory(items)
```

### Log Management

**Structured Logging**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "order_processed",
    order_id=order_id,
    customer_id=customer_id,
    amount=amount,
    duration_ms=processing_time,
)
```

**Log Levels**
- ERROR: Action required immediately
- WARN: Attention needed soon
- INFO: Normal operation visibility
- DEBUG: Detailed troubleshooting

## Examples

See the `examples/` directory for:
- `prometheus-configs/` - Prometheus configuration examples
- `grafana-dashboards/` - Dashboard JSON models
- `alert-rules/` - Alerting rule definitions
- `opentelemetry-setup/` - Tracing configuration

## References

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Prometheus documentation](https://prometheus.io/docs/)
- [Grafana documentation](https://grafana.com/docs/)
- [OpenTelemetry](https://opentelemetry.io/docs/)
- [Distributed Systems Observability](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/)
