---
name: fleet-docker-management
description: How DevOps manages Docker — Dockerfile best practices, multi-stage builds, compose patterns, security. The fleet runs on Docker, this is core domain knowledge.
---

# Docker Management — DevOps Container Discipline

The fleet's MC backend runs in Docker. Agent workspaces depend on containerized services. Docker isn't optional infrastructure — it's the deployment foundation.

## Dockerfile Best Practices

### Multi-Stage Builds
```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (smaller image)
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["python", "-m", "fleet.mcp.server"]
```
Why: build tools stay in stage 1. Runtime image is smaller and has less attack surface.

### Layer Caching
```dockerfile
# GOOD — dependencies cached separately from code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# BAD — every code change reinstalls deps
COPY . .
RUN pip install -r requirements.txt
```

### Non-Root User
```dockerfile
RUN adduser --disabled-password --no-create-home appuser
USER appuser
```
Why: if the container is compromised, the attacker doesn't have root.

### Pin Base Images
```dockerfile
# BAD — changes without you knowing
FROM python:latest

# GOOD — reproducible
FROM python:3.11.7-slim-bookworm
```

## Docker Compose Patterns

### Service Dependencies
```yaml
services:
  mc-backend:
    depends_on:
      mc-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Volume Mounts
```yaml
volumes:
  - ./data/mc:/data          # Persistent data
  - ./config:/config:ro       # Read-only config
  # NEVER: - .:/app          # Don't mount entire project into container
```

### Network Isolation
```yaml
networks:
  fleet-internal:
    driver: bridge
  fleet-external:
    driver: bridge
```
Separate internal (MC ↔ DB) from external (MC ↔ gateway) traffic.

## Security

1. **No secrets in images** — Use env vars or mounted secret files, never COPY secrets into the image
2. **Scan base images** — Use `container-inspector` sub-agent to audit image contents
3. **Pin ALL versions** — base image, package versions, apt packages
4. **Minimal base** — `slim` or `alpine`, not full OS images
5. **No build tools in runtime** — multi-stage keeps compilers out of production

## Fleet-Specific Docker

### MC Backend
```
vendor/openclaw-mission-control/  — Patched source
docker-compose.yaml               — Service definition
patches/                          — Applied by scripts/apply-patches.sh
```

The MC backend Docker image is built from patched vendor source. Patches survive git clone and are applied by IaC scripts.

### Container Inspector Sub-Agent
```
Agent: container-inspector
Prompt: "Inspect the mc-backend container: check resource usage, 
        verify health check is passing, list exposed ports, 
        check for running processes."
```

Use for health audits without loading Docker output into your main context.

## The IaC Principle for Docker

Everything Docker is scripted:
- `docker-compose.yaml` — declarative service definition
- `scripts/setup-mc.sh` — builds and starts MC
- `make mc-up` / `make mc-down` — simple lifecycle commands
- Patches applied by `scripts/apply-patches.sh`

No `docker run` commands in documentation. Everything through compose and scripts.
