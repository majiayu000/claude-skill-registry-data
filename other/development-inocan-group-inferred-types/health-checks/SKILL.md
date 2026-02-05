---
name: health-checks
description: "Implement liveness, readiness, and dependency health checks"
triggers:
  - "health check endpoints"
  - "liveness probe"
  - "readiness probe"
  - "kubernetes health checks"
priority: 1
---

# Health Checks

Different checks serve different purposes. Don't conflate them.

## Check Types

| Endpoint | Purpose | On Failure | Should Check |
|----------|---------|------------|--------------|
| `/health/live` | Process alive? | K8s restarts pod | **Only** process responsiveness |
| `/health/ready` | Can handle traffic? | K8s removes from LB | DB, cache, critical deps |
| `/health/startup` | Init complete? | K8s waits | Initialization status |

## Liveness (Simple)

```
Return 200 OK immediately. Never check dependencies.
```

Checking DB in liveness = pod restarts when DB is down = cascading failure.

## Readiness (Dependency Checks)

```
For each dependency:
  → Check with timeout (1-2s)
  → Record healthy/unhealthy status
Return 503 if any critical dependency unhealthy
```

## Response Format

```json
{
  "status": "healthy|unhealthy",
  "version": "1.2.3",
  "dependencies": {
    "database": "healthy",
    "cache": "unhealthy: connection refused"
  }
}
```

## Kubernetes Config

```yaml
livenessProbe:
  httpGet: { path: /health/live, port: 8080 }
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet: { path: /health/ready, port: 8080 }
  periodSeconds: 5
  failureThreshold: 3

startupProbe:
  httpGet: { path: /health/startup, port: 8080 }
  periodSeconds: 5
  failureThreshold: 30  # 150s max startup
```

## Anti-Patterns

- **Liveness checks dependencies** → Cascading restarts
- **No timeout on checks** → Health endpoint hangs
- **No caching** → Thundering herd on health endpoints

## References

- `references/platforms/{platform}/health-checks.md`
