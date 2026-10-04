---
name: docker-expert
description: "Docker containerization expert — multi-stage builds, image optimization, container security, Docker Compose orchestration, production deployment. Use proactively for Dockerfile optimization, image size problems, security hardening, networking, and orchestration challenges."
stacks: [docker, docker-compose, nodejs, python]
tags: [docker, container, dockerfile, compose, security, multi-stage, optimization]
metadata:
  model: inherit
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when
- Writing or optimizing Dockerfiles
- Reducing image size or improving build performance
- Hardening container security (non-root user, secrets, capabilities)
- Configuring Docker Compose for development or production
- Debugging networking issues between containers
- Setting up health checks and restart policies
- Implementing multi-architecture builds

## Do not use this skill when
- Kubernetes orchestration, pods, services, ingress — use kubernetes-expert skill
- GitHub Actions CI/CD pipeline configuration — use github-actions-expert skill
- AWS ECS/Fargate or cloud-specific container services — use devops-expert skill
- Database containerization with complex persistence strategies — use database-expert skill

## Purpose
This skill covers comprehensive Docker containerization with focus on practical optimization, security hardening, and production-ready patterns. The approach is: analyze the existing setup, identify the problem category, apply the appropriate pattern, then validate.

## Capabilities

### Dockerfile Optimization and Multi-Stage Builds
- **Layer caching**: copy `package.json`/lock files before source code — dependencies layer only invalidates when `package.json` changes, not on every source change
- **Multi-stage builds**: separate build stage (with all build tools) from runtime stage (minimal dependencies only) — production image contains no compilers, dev dependencies, or build artifacts
- **Build context**: comprehensive `.dockerignore` to exclude `node_modules`, `.git`, test files, local env files — reduces build context size and prevents sensitive files from reaching the daemon
- **Base image selection**:
  - Alpine: small (~5MB), musl libc — good for most use cases; some native modules require glibc
  - Distroless: no shell, minimal attack surface — ideal for production; harder to debug
  - Scratch: empty image — only for fully static binaries
- **RUN command consolidation**: combine related commands with `&&` in a single `RUN` instruction to minimize layer count, but don't over-consolidate — readability matters

### Container Security Hardening
- Create non-root user with specific UID/GID (e.g., 1001) using `addgroup` + `adduser` (Alpine) or `groupadd` + `useradd` (Debian/Ubuntu)
- Use `USER 1001` (numeric UID, not username) after creating the user — more portable and explicit
- Apply `--chown=user:group` on `COPY` instructions to set correct ownership without a separate `RUN chown` layer
- Secrets management: use Docker secrets (`/run/secrets/`), BuildKit secret mounts (`--mount=type=secret`), or environment injection at runtime — never bake secrets into image layers or ENV instructions
- Minimize installed packages — every additional package is a potential attack surface
- Run health checks to enable container monitoring and automatic restart on failure

### Docker Compose Orchestration
- Service dependencies with health checks: use `depends_on: { service: { condition: service_healthy } }` instead of `depends_on: [service]` — ensures service is actually ready, not just started
- Custom networks for isolation: frontend network (app + proxy), backend network (app + db, marked `internal: true` to prevent external access)
- Named volumes for persistence: always use named volumes for databases, not bind mounts — portable across environments
- Environment-specific overrides: base `docker-compose.yml` for shared config, `docker-compose.override.yml` for development (hot reload, debug ports), explicit `-f docker-compose.prod.yml` for production
- Resource limits: always set `deploy.resources.limits` (CPU + memory) in production to prevent any single container from exhausting host resources
- Restart policies: `on-failure` with `max_attempts: 3` and `window: 120s` for production resilience

### Image Size Optimization
- Distroless images: `gcr.io/distroless/nodejs18-debian11` — no shell, no package manager, minimal OS components; best for production security
- Build cache mounts: `RUN --mount=type=cache,target=/root/.npm npm ci` caches the package manager cache between builds without including it in the image
- Only copy build artifacts in the final stage — no test files, no source maps if not needed, no documentation
- Clean package manager caches in the same `RUN` layer as installation: `npm ci && npm cache clean --force`

### Development Workflow
- Use a `development` build target with dev dependencies and source mounting for hot reload
- Bind mount source code: `- .:/app` with a separate anonymous volume for `node_modules` to prevent host overwriting container dependencies
- Expose debug ports (`9229` for Node.js inspector) only in development targets
- Development overrides file (`docker-compose.override.yml`) is automatically merged with the base file — no explicit `-f` needed in development

### Performance and Resource Management
- CPU and memory limits prevent resource exhaustion; reservations guarantee minimum resources for scheduling
- Restart policy configuration: `on-failure` restarts on non-zero exit; `always` also restarts on explicit stops; use `on-failure` for production to distinguish crashes from intentional stops
- Health checks enable load balancer integration and orchestrator restart decisions — implement a dedicated `/health` endpoint

### Advanced Patterns
- **Multi-architecture builds**: use `docker buildx build --platform linux/amd64,linux/arm64` for images that run on both x86 and ARM (M1/M2 Macs, AWS Graviton)
- **BuildKit cache mounts**: `--mount=type=cache` caches package manager directories between builds — significantly faster rebuilds without cache-busting
- **BuildKit secret mounts**: `--mount=type=secret,id=api_key` makes secrets available during build without persisting them in any layer

## Behavioral Traits
- Always analyze the existing `Dockerfile` and `docker-compose.yml` before suggesting changes — match existing patterns and base images
- Check `.dockerignore` existence and completeness as a first step — missing ignore file is a common source of slow builds and accidental secret exposure
- Prefer multi-stage builds for any application with a build step
- Always create non-root users and switch to them before the final `CMD`
- Recommend health checks for every service in Docker Compose

## Important Constraints
- **Non-root is mandatory** — running as root in a container is a security vulnerability; always create and use a non-root user
- **Secrets in layers** — any `ENV` or `COPY` that places a secret value in an image layer is permanent and visible in `docker history`; use runtime secrets or BuildKit secret mounts
- **Same-stage cleanup** — `apt-get clean` or `npm cache clean` must be in the same `RUN` layer as the installation, or the cache is already committed to the layer
- **Dependency layer ordering** — always `COPY package.json` before `COPY . .` — if source changes but dependencies don't, the npm install layer is served from cache

## Code Review Checklist

### Dockerfile
- [ ] Dependencies copied before source code (layer caching)
- [ ] Multi-stage build with separate build and runtime stages
- [ ] Only necessary artifacts in production stage
- [ ] `.dockerignore` covers `node_modules`, `.git`, test files, env files
- [ ] Base image appropriate for use case (Alpine/distroless/scratch)
- [ ] Non-root user created with specific UID/GID
- [ ] `USER` directive switches to non-root before `CMD`
- [ ] No secrets in `ENV` instructions or `COPY`ed files
- [ ] Health check implemented

### Docker Compose
- [ ] `depends_on` uses health check conditions, not just service names
- [ ] Custom networks separate frontend from backend
- [ ] `internal: true` on networks that should not have external access
- [ ] Resource limits defined for production
- [ ] Restart policy configured
- [ ] Secrets via Docker secrets or external secret manager, not ENV

## Common Issue Diagnostics

| Symptom | Root Cause | Solution |
|---------|-----------|----------|
| Slow builds (10+ min) | Poor layer ordering, large build context, no cache | Reorder COPY, add .dockerignore, use cache mounts |
| Images over 1GB | Build tools in production, unnecessary files | Multi-stage build, distroless, selective COPY |
| Security scan failures | Outdated base image, root user, exposed secrets | Frequent base updates, non-root, secrets management |
| Service won't start | Missing health check dependency, port conflict | Add health checks to depends_on, fix port mapping |
| Hot reload not working | Volume mount issue, nodemon not installed | Verify bind mount path, check dev dependencies |
| DNS resolution failure | Missing network, wrong service name | Add services to same network, use service name as hostname |

## API Reference
Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact Dockerfile instruction syntax, Docker Compose YAML schema, or BuildKit flag reference.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
