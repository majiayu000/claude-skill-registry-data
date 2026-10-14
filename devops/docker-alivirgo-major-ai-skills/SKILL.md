---
name: docker
description: "Build reproducible container images with BuildKit, wire Compose service graphs with real readiness gates, and debug networking, volumes, and layer-cache failures agents routinely miss."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["docker", "dockerfile", "compose", "buildkit", "containers", "supply-chain", "healthcheck"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Docker Containers & Compose AI Skill Guide (Claude)

## Overview & Engine Architecture

Docker packages apps as **immutable images** and runs them as **ephemeral containers** on a host engine (containerd/Moby). **BuildKit** builds images with cache mounts and multi-stage targets; **Compose** declares multi-container graphs on a single host. Agents should treat images as **versioned artifacts** (digest-pinned bases), Compose as **startup-order contracts** (not “wait forever”), and secrets as **runtime mounts**—never committed layers.

```
┌─────────────────────────────────────────────────────────────┐
│                 Docker build → run loop                       │
│                                                             │
│  Build (BuildKit / buildx)                                  │
│  ├── Multi-stage: deps → build → runner (non-root)          │
│  ├── Cache: lockfiles first; RUN --mount=type=cache         │
│  └── SBOM/scan gate before push (pair with @trivy)           │
│                                                             │
│  Runtime                                                    │
│  ├── Namespaces: net / pid / mnt; USER in final stage       │
│  ├── Volumes: named > bind (UID/GID traps on bind)          │
│  └── HEALTHCHECK + Compose condition: service_healthy       │
│                                                             │
│  Compose orchestration (single host)                        │
│  ├── depends_on + healthcheck (startup only, not runtime)   │
│  └── Internal DNS: <service> on user-defined network       │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when**

- Authoring Dockerfiles, `.dockerignore`, and `compose.yaml` for local/staging parity.
- Debugging “works on my machine” via container logs, healthchecks, and network aliases.
- Optimizing image size, layer cache, and non-root runtime hardening.

**Do not use when**

- You need multi-node scheduling, rolling updates, or cluster RBAC → `@kubernetes` / `@helm`.
- The task is host-level syslog/logging-driver plugins that must exist **before** any container starts on daemon reboot (Compose cannot order daemon-wide plugins) → host OS service instead.
- Someone asks to bake API keys into `ENV` or `ARG` defaults → refuse; use secrets mounts or external secret stores (`@vault`).

---

## Operational Capabilities & Agent Directives

1. **Pin bases by digest** in production Dockerfiles; tag drift (`node:20-alpine` today ≠ tomorrow) breaks reproducibility and CVE response.
2. **Multi-stage by default**: compile in builder; copy only artifacts + prod deps into `runner`; run as non-root with explicit `USER`.
3. **Compose readiness**: use `depends_on.condition: service_healthy` with healthchecks that prove **application readiness** (`pg_isready`, HTTP `/health`), not “process started”.
4. **Tune healthcheck `start_period` + retries**: Compose stops startup if dependency goes `unhealthy` after retries—it does **not** wait indefinitely.
5. **BuildKit secrets**: `RUN --mount=type=secret` for npm/pip tokens; never `COPY .env` or `ENV TOKEN=`.
6. **Idempotent compose**: document `docker compose up --build` vs `pull` policy; use named volumes for stateful data.
7. **Platform builds**: `docker buildx build --platform linux/amd64,linux/arm64` when CI arch ≠ laptop (Apple Silicon → amd64 deploy traps).

---

## Production Example: API + Postgres with real readiness

`Dockerfile` (excerpt):

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine@sha256:<pin-digest> AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci

FROM node:20-alpine@sha256:<pin-digest> AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S app && adduser -S app -G app
COPY --from=deps /app/node_modules ./node_modules
COPY --chown=app:app dist ./dist
USER app
EXPOSE 3000
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

`compose.yaml`:

```yaml
services:
  api:
    build:
      context: .
      target: runner
    ports: ["3000:3000"]
    environment:
      DATABASE_URL: postgres://app@db:5432/app
    secrets: [db_password]
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:3000/health"]
      interval: 10s
      start_period: 30s
      retries: 5
  db:
    image: postgres:16-alpine@sha256:<pin-digest>
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: app
    secrets: [db_password]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 30s
    volumes: [pgdata:/var/lib/postgresql/data]
secrets:
  db_password:
    file: ./secrets/db_password.txt  # gitignored
volumes:
  pgdata:
```

Validation loop:

```bash
docker compose config
docker buildx build -t myorg/api:$(git rev-parse --short HEAD) --target runner .
docker compose up --build -d
docker compose ps
docker inspect --format='{{json .State.Health}}' "$(docker compose ps -q api)"
```

---

## Technical Troubleshooting Matrix

| Signature | Likely cause | Fix path |
| :--- | :--- | :--- |
| Dependency `unhealthy`, compose aborts startup | Healthcheck too aggressive vs slow boot | Increase `start_period`, fix test command, verify port inside container |
| `connection refused` to `db:5432` on first boot only | Short-form `depends_on` without `service_healthy` | Add `condition: service_healthy` |
| After **host reboot**, logging driver / syslog race | Engine starts containers without Compose ordering | Do not model engine plugins as Compose services; use host syslog |
| `permission denied` on bind mount | UID/GID mismatch (`USER app` vs host root-owned dir) | Named volume, or `chown` host path, or align UID |
| Image 2GB+ | Build tools in final stage | Multi-stage; `.dockerignore`; `npm prune --omit=dev` |
| `no matching manifest for linux/amd64` | arm64-only image on amd64 cluster | `buildx --platform` or pin correct base |
| Secrets in `docker history` | `ENV`/`ARG` for credentials | BuildKit secrets; runtime env from orchestrator |
| Nginx/upstream “host not found” at start | Static upstream DNS at boot | Pair with `@nginx` resolver pattern in frontends |

---

## Best Practices

1. `.dockerignore`: `.git`, `node_modules`, `*.pem`, `.env*`, test fixtures.
2. One process per container; use Compose for sidecars on single host only.
3. Tag images with **git SHA**; promote digests to prod manifests (`@kubernetes`, `@github-actions`).
4. Run `docker scout cves` or `@trivy` in CI before push.
5. Prefer `read_only: true` + tmpfs for stateless services when feasible.
6. Document required env vars in README; fail fast in entrypoint if missing.

---

## Limitations

- Compose is not Kubernetes: no PodDisruptionBudgets, no cluster autoscaler, no cross-host networking without Swarm (deprecated path).
- Healthchecks are **startup ordering** helpers; they do not restart failed dependencies after boot—apps need retry/backoff.
- Rootless Docker and file permission edge cases vary by host OS.
- Stop and ask if registry credentials, prod compose files, or data migration steps are missing.

---

## Related Skills

- `@kubernetes` — production orchestration beyond single-host Compose
- `@github-actions` — build/push images with OIDC to cloud registries
- `@nginx` — reverse proxy in front of compose stacks
- `@trivy` — image vulnerability gates
- `@vault` — dynamic secrets instead of compose secret files in prod

---

## Agent Operational Directive

> **MANDATORY**: Pin base image digests for production paths. Never put secrets in image layers or committed compose env. Use `depends_on` with `service_healthy` and healthchecks that reflect real readiness; tune `start_period` so slow deps are not marked unhealthy during boot. Validate with `docker compose config` and `nginx -t`-equivalent (`docker build` + container health) before declaring success.

---

## Source anchors (research)

- [Compose startup order & `service_healthy`](https://docs.docker.com/compose/how-tos/startup-order/)
- [Compose file: `depends_on`, `healthcheck`](https://docs.docker.com/reference/compose-file/services)
- [Compose issue: healthcheck timeout stops startup (not infinite wait)](https://github.com/docker/compose/issues/11474)
- [Compose issue: daemon reboot ignores startup order for logging drivers](https://github.com/docker/compose/issues/12589)
- [Dockerfile HEALTHCHECK reference](https://docs.docker.com/reference/dockerfile/#healthcheck)
