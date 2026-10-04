---
name: docker
description: Containerization guidance for multi-stage builds, non-root execution, dockerignore hygiene, layer caching, healthchecks, and secret handling. Use when writing or reviewing Dockerfiles and container images.
---

# Docker

Build minimal, reproducible images that start fast, run as non-root, and separate build-time concerns from runtime behavior.

## When to Activate

- Write or refactor a Dockerfile
- Split build and runtime concerns
- Harden a container for production
- Improve Docker build cache performance
- Add container healthchecks
- Review secret handling in image builds
- Shrink image size and attack surface

## Base Images and Layering

| Use Case | Preferred | Avoid |
| --- | --- | --- |
| Production service | Distroless or slim runtime | Full distro with build toolchain |
| Build stage | Language-specific SDK image | Installing compilers in runtime image |
| Tiny static binary | `scratch` when feasible | Heavy general-purpose images |

| Order | Reason |
| --- | --- |
| Copy lockfiles first | Maximizes dependency cache hits |
| Install dependencies | Expensive step stays cached |
| Copy source later | Code changes do not bust dependency layer |

## Runtime Hardening

BAD

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
```

GOOD

```dockerfile
FROM python:3.12-slim AS runtime
WORKDIR /app
RUN useradd --create-home appuser
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python", "main.py"]
```

| Scenario | Rule |
| --- | --- |
| Build-time private dependency access | Use ephemeral build secrets if available |
| Runtime credentials | Inject via environment or secret store |
| Static secret in Dockerfile | Never do it |

| Preferred | Avoid |
| --- | --- |
| Application-level readiness endpoint | Checking only whether PID exists |
| Fast, dependency-light command | Heavy scripts that change container state |

## Ignore List

| Always Ignore |
| --- |
| `.git` |
| `node_modules` |
| `.venv` |
| test artifacts |
| local secrets and `.env` files |

BAD

```dockerfile
COPY . .
RUN npm install
```

GOOD

```dockerfile
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
```

## Checklist

- [ ] Dockerfile uses multi-stage builds when build tooling is required
- [ ] Dependency layers are copied before application source
- [ ] Runtime image uses a non-root user
- [ ] `.dockerignore` excludes local junk and secrets
- [ ] Secrets are injected at runtime or via build secret facilities
- [ ] Healthcheck verifies real service readiness
- [ ] Base image is minimal for the workload
