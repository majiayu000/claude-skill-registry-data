---
name: "logging-monitoring"
description: 'Implement observability patterns including structured logging, log levels, correlation IDs, metrics, and distributed tracing. Use when adding structured logging, implementing correlation IDs for request tracing, configuring metrics collection, setting up distributed tracing, or designing alerting rules.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Logging & Monitoring

> **Purpose**: Implement observability for production systems. 
> **Goal**: Structured logs, correlation across requests, actionable metrics. 
> **Note**: For implementation, see [C# Development](../csharp/SKILL.md) or [Python Development](../python/SKILL.md).

---

## When to Use This Skill

- Adding structured logging to applications
- Implementing request correlation IDs
- Configuring metrics collection
- Setting up distributed tracing (OpenTelemetry)
- Designing alerting rules and health checks

## Prerequisites

- Logging framework installed
- Monitoring platform access

## Decision Tree

```
Observability concern?
+- What to log?
| +- Request start/end -> INFO with correlation ID
| +- Expected errors -> WARN (validation, not-found)
| +- Unexpected errors -> ERROR with stack trace
| - Debug details -> DEBUG (disabled in production)
+- What NOT to log?
| - PII, passwords, tokens, credit cards -> NEVER
+- Metrics needed?
| +- RED metrics: Rate, Errors, Duration (for services)
| - USE metrics: Utilization, Saturation, Errors (for resources)
+- Distributed tracing?
| - OpenTelemetry for cross-service correlation
- Alerting?
 +- SLO-based: alert on error budget burn rate
 - Avoid alert fatigue: page only for actionable issues
```

## Structured Logging

### Concept

Log structured data (key-value pairs) instead of plain text for better searchability and analysis.

```
[FAIL] Unstructured (hard to parse):
 "User john@example.com logged in from 192.168.1.1 at 2024-01-15 10:30:00"

[PASS] Structured (machine-readable):
 {
 "event": "user_login",
 "user_email": "john@example.com",
 "ip_address": "192.168.1.1",
 "timestamp": "2024-01-15T10:30:00Z",
 "level": "INFO"
 }
```

### Benefits

- **Searchable**: Query by any field
- **Filterable**: Show only errors, specific users, etc.
- **Aggregatable**: Count events, calculate averages
- **Parseable**: Tools can process automatically

---

## Log Levels

### Standard Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| **TRACE** | Very detailed debugging | "Entering function with params: {x: 1, y: 2}" |
| **DEBUG** | Debugging information | "Cache hit for key: user_123" |
| **INFO** | Normal operations | "User logged in", "Order created" |
| **WARN** | Unexpected but recoverable | "Retry attempt 2 of 3", "Rate limit approaching" |
| **ERROR** | Failures requiring attention | "Payment failed", "Database connection lost" |
| **FATAL** | Application cannot continue | "Out of memory", "Configuration invalid" |

### Level Configuration by Environment

```
Development: DEBUG or TRACE
 - See detailed information for debugging

Staging: INFO
 - Normal operations plus warnings/errors

Production: INFO (or WARN)
 - Reduce noise, focus on significant events
 - Keep ERROR/FATAL always enabled
```

---

## Best Practices Summary

| Practice | Description |
|----------|-------------|
| **Structured logging** | JSON format with key-value pairs |
| **Correlation IDs** | Trace requests across services |
| **Appropriate levels** | DEBUG in dev, INFO+ in prod |
| **No sensitive data** | Never log passwords, tokens, PII |
| **Context in errors** | Include what, why, and how to fix |
| **Meaningful metrics** | Track rate, errors, duration |
| **Health checks** | Liveness + readiness endpoints |
| **Actionable alerts** | Include runbooks, reduce noise |

---

## Observability Tools

| Category | Tools |
|----------|-------|
| **Logging** | ELK Stack, Splunk, Datadog Logs, CloudWatch Logs |
| **Metrics** | Prometheus + Grafana, Datadog, New Relic, CloudWatch |
| **Tracing** | Jaeger, Zipkin, Datadog APM, Application Insights |
| **All-in-One** | Datadog, New Relic, Dynatrace, Elastic Observability |

---

**See Also**: [Error Handling](../error-handling/SKILL.md) - [C# Development](../csharp/SKILL.md) - [Python Development](../python/SKILL.md)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in monitoring platform | Check log level configuration, verify sink/exporter endpoint |
| Correlation IDs missing across services | Propagate W3C trace context headers in all HTTP calls |
| Alert fatigue from too many notifications | Set meaningful thresholds, group related alerts, add alert suppression windows |

## References

- [Logging Correlation Metrics](references/logging-correlation-metrics.md)
- [Tracing Health Alerting](references/tracing-health-alerting.md)