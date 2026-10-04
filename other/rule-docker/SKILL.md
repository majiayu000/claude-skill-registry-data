---
name: rule-docker
description: MANDATORY when editing files matching ["**/Dockerfile", "**/Dockerfile.*", "**/docker-compose*.yml", "**/docker-compose*.yaml"]. Dockerfile and docker-compose conventions for API and frontend images
---

# Docker Rules

## Base Images

ALWAYS pin base images to a specific minor version and digest where possible (e.g., `python:3.12-slim@sha256:...`, `node:20-bookworm-slim`). NEVER use `latest`. ALWAYS use slim or distroless variants for runtime stages. Base images MUST be FedRAMP-approved and scanned in CI.

## Multi-Stage Builds

ALWAYS use multi-stage builds: a `builder` stage with build toolchain and a minimal `runtime` stage. NEVER ship compilers, dev dependencies, or package caches into the runtime image.

Correct (API):
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && poetry export -f requirements.txt > req.txt
RUN pip install --no-cache-dir --prefix=/install -r req.txt

FROM python:3.12-slim AS runtime
COPY --from=builder /install /usr/local
COPY api/src /app/src
WORKDIR /app
USER 10001:10001
CMD ["python", "-m", "src"]
```

## Non-Root User

ALWAYS run as a non-root UID (e.g., `USER 10001:10001`). NEVER run containers as root. ALWAYS `chown` copied application files to the runtime user.

## Layer Hygiene

ALWAYS order layers from least- to most-frequently-changing (dependencies before source). ALWAYS combine related `RUN` commands and clean apt/pip caches in the same layer. NEVER `COPY . .` before installing dependencies.

Incorrect:
```dockerfile
FROM python:latest
COPY . /app
RUN pip install -r /app/requirements.txt
USER root
```

## Secrets and Build Args

NEVER bake secrets, tokens, or credentials into images or `ARG` defaults. ALWAYS mount secrets at runtime via environment variables sourced from SSM or AWS Secrets Manager. ALWAYS use `--secret` BuildKit mounts for build-time credentials.

## Health Checks and Signals

ALWAYS define a `HEALTHCHECK` or rely on the orchestrator's probe. ALWAYS handle SIGTERM for graceful shutdown (use `tini` or `exec` form `CMD`).

## docker-compose

ALWAYS pin service image tags. ALWAYS use named volumes for data. ALWAYS load environment variables from `.env` files that are gitignored. NEVER commit `.env` with real secrets.

---

## Related Rules

- **`infra.mdc`** — ECS/Fargate task definitions consuming images
- **`ci-cd.mdc`** — image build, scan, and push pipeline
- **`security.mdc`** — vulnerability scanning, SBOM, secrets
- **`fedramp.md`** — approved base images and hardening
- **`makefile.mdc`** — developer workflow shortcuts

## Specialist Validation

**Simple (bump pinned version):** None.
**Moderate (new stage, new service in compose):** Invoke `codebase-conventions-reviewer`.
**Complex (new base image, runtime hardening, multi-arch):** Invoke `security-sentinel` and `architecture-strategist`.
