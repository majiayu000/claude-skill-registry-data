---
name: fleet-monitoring-setup
description: How DevOps sets up monitoring — health checks, alerting, metrics, dashboards. Phase-appropriate observability from POC (console logs) to production (full monitoring suite).
---

# Monitoring Setup — DevOps Observability Skill

You can't fix what you can't see. Monitoring makes the invisible visible — service health, error rates, performance, resource usage. The level of monitoring matches the delivery phase.

## Phase-Appropriate Monitoring

| Phase | What to Monitor | How |
|-------|----------------|-----|
| poc | Is it running? | Console logs, manual health check |
| mvp | Is it healthy? | Health endpoint, structured file logs, basic alerting |
| staging | Is it performing? | Health checks + response time + error rate + resource usage |
| production | Is it reliable? | Full suite: health + metrics + dashboards + alerting + on-call |

Don't over-monitor a POC. Don't under-monitor production.

## The 4 Monitoring Layers

### Layer 1: Health Checks

The simplest and most critical — is the service UP?

**For the fleet:**
```
MC Backend:   curl -sf http://localhost:8000/api/v1/agents > /dev/null
Gateway:      WebSocket ping to ws://localhost:18789
IRC:          nc -z localhost 6667
The Lounge:   curl -sf http://localhost:9000 > /dev/null
LocalAI:      curl -sf http://localhost:8090/healthz > /dev/null
```

Your `devops_infrastructure_health` group call checks these. Your `infrastructure-health-check` CRON runs it every 4 hours.

**For deployed services:**
- Add a `/health` endpoint that returns 200 when service is operational
- Check dependencies: if the service needs a database, health check includes DB ping
- Return structured JSON: `{"status": "healthy", "checks": {"db": "ok", "cache": "ok"}}`

### Layer 2: Structured Logging

Logs are the first thing you read when something goes wrong.

**Standards:**
```python
# BAD — unstructured
print(f"Error processing task {task_id}")

# GOOD — structured, grep-friendly, context included
logger.error("Task processing failed", extra={
    "task_id": task_id,
    "agent": agent_name,
    "error": str(e),
    "stage": task_stage,
})
```

**Log levels:**
| Level | When | Example |
|-------|------|---------|
| DEBUG | Detailed flow tracing (dev only) | "Checking contribution completeness for task:abc" |
| INFO | Normal operations worth noting | "Dispatched task:abc to software-engineer (opus, high)" |
| WARNING | Unexpected but handled | "Budget at 85%, approaching dispatch threshold" |
| ERROR | Failed operation, needs attention | "MC API call failed: connection refused" |
| CRITICAL | Service-level failure | "Gateway process died, agents disconnected" |

### Layer 3: Metrics

Quantitative data over time. Numbers, not events.

**Key metrics for the fleet:**
- **Dispatch rate:** tasks dispatched per hour
- **Completion rate:** tasks completed per day
- **Rejection rate:** approvals rejected / total approvals
- **Budget burn rate:** % of quota used per hour
- **Agent uptime:** % of time each agent is ACTIVE vs IDLE/SLEEPING
- **Storm indicators:** void session rate, circuit breaker state

**Collection:** The fleet records metrics in board memory events and dispatch records. A monitoring dashboard would read these.

### Layer 4: Alerting

Automated notification when thresholds are breached.

**Alert rules for the fleet:**
| Condition | Severity | Channel |
|-----------|----------|---------|
| MC backend down | CRITICAL | ntfy PO + IRC #alerts |
| Budget > 90% | HIGH | ntfy PO + IRC #alerts |
| Agent offline > 2h with assigned work | MEDIUM | IRC #fleet |
| Rejection rate > 50% this sprint | MEDIUM | Board memory [quality] |
| Storm severity >= WARNING | HIGH | ntfy PO + IRC #alerts |

The fleet's existing systems handle most alerting:
- `fleet_alert()` tool → IRC + ntfy for high/critical
- Storm monitor → orchestrator dispatch limiting + PO notification
- Budget monitor → dispatch blocking at 90%

## Setting Up Monitoring for New Services

When devops contributes a `deployment_manifest`, include monitoring:

```
## Monitoring Plan

### Health Check
Endpoint: /health
Interval: 30s
Timeout: 5s
Unhealthy threshold: 3 consecutive failures

### Logging
Format: structured JSON
Level: INFO in production, DEBUG in staging
Retention: 7 days in staging, 30 days in production

### Metrics
- Request count (per endpoint, per status code)
- Response time (p50, p95, p99)
- Error rate (5xx / total)
- Resource usage (CPU, memory, connections)

### Alerts
- Health check fails → PagerDuty/ntfy
- Error rate > 5% for 5min → WARNING
- p99 latency > 2s for 10min → WARNING
- Resource usage > 80% → WARNING
```

## The IaC Principle

Monitoring configuration is CODE, not clicks:
- Health check scripts in `scripts/`
- Alert rules in config files
- Dashboard definitions as code (Grafana JSON, etc.)
- Log configuration in application config

If you can't reproduce the monitoring setup from a script, it's not infrastructure — it's a wish.
