---
name: cloud-native-checklist
description: Generate CNCF/12-Factor compliance checklists and ADRs for cloud-native applications. Use when reviewing application architecture, planning containerization, or documenting cloud-native decisions.
---

# Cloud-Native Compliance Checklist

Generate Architecture Decision Records (ADRs) and compliance checklists for CNCF and 12-Factor App principles.

## When to Use

- Reviewing application architecture for cloud-native readiness
- Planning containerization of existing applications
- Documenting architectural decisions for cloud deployment
- Auditing applications against industry standards

## Quick Checklist Generation

When asked to generate a checklist, create an ADR at `docs/adr/NNNN-cloud-native-compliance.md`:

```markdown
# ADR-NNNN: Cloud-Native Compliance Assessment

## Status

Proposed | Accepted | Implemented

## Context

[Brief description of the application and why this assessment is needed]

## 12-Factor App Compliance

| Factor | Status | Notes |
|--------|--------|-------|
| I. Codebase | | One codebase tracked in VCS, many deploys |
| II. Dependencies | | Explicitly declare and isolate dependencies |
| III. Config | | Store config in environment variables |
| IV. Backing Services | | Treat backing services as attached resources |
| V. Build, Release, Run | | Strictly separate build and run stages |
| VI. Processes | | Execute app as stateless processes |
| VII. Port Binding | | Export services via port binding |
| VIII. Concurrency | | Scale out via process model |
| IX. Disposability | | Fast startup and graceful shutdown |
| X. Dev/Prod Parity | | Keep development, staging, production similar |
| XI. Logs | | Treat logs as event streams |
| XII. Admin Processes | | Run admin/management tasks as one-off processes |

## Container Standards

| Requirement | Status | Notes |
|-------------|--------|-------|
| `/health` endpoint | | Orchestrator health checks |
| `/ready` endpoint | | Startup readiness (if slow init) |
| Graceful SIGTERM | | Drain connections, finish requests |
| Log to stdout | | No file logging |
| Non-root user | | Container security |
| Environment config | | No hardcoded configuration |
| OCI labels | | Image metadata and linking |

## Supply Chain Security

| Requirement | Status | Notes |
|-------------|--------|-------|
| Image signing (Cosign) | | Cryptographic verification |
| SLSA provenance | | Build attestations |
| Dependency scanning | | Vulnerability detection |
| SBOM generation | | Software bill of materials |

## Observability

| Requirement | Status | Notes |
|-------------|--------|-------|
| Structured logging | | JSON log format |
| OpenTelemetry tracing | | Distributed tracing |
| Prometheus metrics | | `/metrics` endpoint |
| Correlation IDs | | Cross-service request tracking |

## Decision

[Summary of compliance status and recommended actions]

## Consequences

[Impact of implementing/not implementing the recommendations]
```

## The 12 Factors Explained

### I. Codebase
One codebase tracked in revision control, many deploys.
- **Check**: Single repo per deployable unit
- **Anti-pattern**: Multiple apps in one repo, or one app across repos

### II. Dependencies
Explicitly declare and isolate dependencies.
- **Check**: `package.json`, `pyproject.toml`, `go.mod` with lockfiles
- **Anti-pattern**: System-wide packages, implicit dependencies

### III. Config
Store config in the environment.
- **Check**: Environment variables for all config
- **Anti-pattern**: Config files checked into repo, hardcoded values

### IV. Backing Services
Treat backing services as attached resources.
- **Check**: Database URLs from environment, swappable without code changes
- **Anti-pattern**: Hardcoded connection strings, local vs remote distinction

### V. Build, Release, Run
Strictly separate build and run stages.
- **Check**: Immutable releases, CI/CD pipeline
- **Anti-pattern**: Modifying code at runtime, FTP deployments

### VI. Processes
Execute the app as one or more stateless processes.
- **Check**: No sticky sessions, external state storage
- **Anti-pattern**: In-memory session state, local file uploads

### VII. Port Binding
Export services via port binding.
- **Check**: Self-contained HTTP server, configurable port
- **Anti-pattern**: Depends on external webserver injection

### VIII. Concurrency
Scale out via the process model.
- **Check**: Horizontal scaling, process-per-workload-type
- **Anti-pattern**: Single multi-threaded process, vertical-only scaling

### IX. Disposability
Maximize robustness with fast startup and graceful shutdown.
- **Check**: Seconds to start, SIGTERM handling, idempotent operations
- **Anti-pattern**: Long warmup, dropped requests on shutdown

### X. Dev/Prod Parity
Keep development, staging, and production as similar as possible.
- **Check**: Same backing services, containers everywhere
- **Anti-pattern**: SQLite dev / PostgreSQL prod, mock services

### XI. Logs
Treat logs as event streams.
- **Check**: Write to stdout, structured JSON
- **Anti-pattern**: Log files, log rotation in app

### XII. Admin Processes
Run admin/management tasks as one-off processes.
- **Check**: Same codebase, run in identical environment
- **Anti-pattern**: SSH and run scripts, separate admin tools

## Container Runtime Standards

### Health Endpoints

```python
# FastAPI example
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    # Check database, cache, etc.
    if await database.is_connected():
        return {"status": "ready"}
    raise HTTPException(503, "Not ready")
```

### Graceful Shutdown

```python
import signal
import asyncio

async def shutdown(signal, loop):
    logging.info(f"Received {signal.name}, shutting down...")
    # Stop accepting new requests
    # Wait for in-flight requests
    # Close connections
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

loop = asyncio.get_event_loop()
for sig in (signal.SIGTERM, signal.SIGINT):
    loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s, loop)))
```

### Non-Root User

```dockerfile
# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app
```

## CNCF Landscape Categories

When assessing cloud-native readiness, consider:

- **Container Runtime**: Docker, containerd, CRI-O
- **Orchestration**: Kubernetes, Nomad
- **Service Mesh**: Istio, Linkerd, Cilium
- **Observability**: Prometheus, Grafana, Jaeger, OpenTelemetry
- **CI/CD**: Argo, Flux, Tekton
- **Security**: Falco, OPA, Trivy, Cosign

## ADR Template

Store in `docs/adr/` with numeric prefix:

```
docs/adr/
├── 0001-use-postgresql.md
├── 0002-adopt-kubernetes.md
├── 0003-cloud-native-compliance.md
└── template.md
```

## Quick Assessment Script

```bash
#!/bin/bash
# Quick cloud-native assessment

echo "=== Cloud-Native Readiness Check ==="

# Check for Dockerfile
[ -f Dockerfile ] && echo "✓ Dockerfile found" || echo "✗ No Dockerfile"

# Check for health endpoint in code
grep -r "/health" --include="*.py" --include="*.ts" --include="*.go" . >/dev/null && \
  echo "✓ Health endpoint found" || echo "✗ No health endpoint"

# Check for environment config
grep -r "os.environ\|process.env\|os.Getenv" --include="*.py" --include="*.ts" --include="*.go" . >/dev/null && \
  echo "✓ Environment config found" || echo "? Check config handling"

# Check for structured logging
grep -r "structlog\|pino\|zap\|slog" --include="*.py" --include="*.ts" --include="*.go" . >/dev/null && \
  echo "✓ Structured logging found" || echo "? Check logging setup"

# Check for non-root in Dockerfile
grep -i "USER" Dockerfile >/dev/null 2>&1 && \
  echo "✓ Non-root user in Dockerfile" || echo "✗ No USER directive"

echo "=== Assessment Complete ==="
```

## References

- [12-Factor App](https://12factor.net/)
- [CNCF Landscape](https://landscape.cncf.io/)
- [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
