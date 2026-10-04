---
name: litestar-deployment
description: "Auto-activate for Dockerfile, compose, Railway, Cloud Run, GKE, systemd, Kubernetes, Terraform, deploy scripts, or granian/litestar run at runtime. Not for packaging artifacts."
---

# Litestar Deployment

Production deployment patterns for Litestar ASGI applications across Docker, Railway, Kubernetes/GKE, Cloud Run, and systemd. Covers multi-stage Dockerfiles, distroless images, asset pipelines, worker containers, and health-check integration.

All deployment paths use **Granian** (via `litestar-granian`) as the ASGI server, **uv** for Python package management, and **Bun** for frontend asset builds.

**Build vs. deploy split:** this skill is about **running** Litestar artifacts in production. For **producing** those artifacts — wheel bundling with embedded Vite assets, PyApp onefile binaries, GitHub Actions CI/release pipelines — see [litestar-build](../litestar-build/SKILL.md).

## Code Style Rules

- `from __future__ import annotations` is allowed in consumer-app modules (Dockerfiles, deploy scripts, settings).
- All Python samples use PEP 604 unions (`T | None`).
- Granian over uvicorn in every CMD/entrypoint. Use `litestar run` (which delegates to Granian when `litestar-granian` is installed).
- Environment-driven configuration via `@dataclass` settings — never hardcode secrets or connection strings.
- Shell scripts follow Google Shell Style Guide (set -euo pipefail, quoted variables).

## Quick Reference

| Target | Reference | Key File |
| --- | --- | --- |
| Litestar App & Cloud IAP | [references/litestar-app.md](references/litestar-app.md) | `asgi.py`, IAP middleware |
| Docker (standard multi-stage) | [references/docker-standard.md](references/docker-standard.md) | `Dockerfile` |
| Docker (distroless production) | [references/docker-distroless.md](references/docker-distroless.md) | `Dockerfile.distroless` |
| Background worker container (`litestar-saq` / `litestar-queues`) | [references/docker-workers.md](references/docker-workers.md) | `Dockerfile.worker` |
| Docker Compose (app + infra) | [references/docker-compose.md](references/docker-compose.md) | `docker-compose.yml` |
| Railway | [references/railway.md](references/railway.md) | `railway.app.json` |
| Kubernetes / GKE | [references/kubernetes.md](references/kubernetes.md) | `deploy.py`, templates/ |
| Cloud Run (Services & Jobs) | [references/cloud-run.md](references/cloud-run.md) | `service.yaml` |
| systemd native | [references/systemd.md](references/systemd.md) | `litestar.service` |

### Dockerfile CMD (all variants)

```dockerfile
# Web server (Granian via litestar-granian)
ENTRYPOINT ["tini", "--"]
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]

# Background worker — Option A: litestar-saq (separate container)
ENTRYPOINT ["tini", "--"]
CMD ["litestar", "workers", "run"]

# Background worker — Option B: litestar-queues (separate container)
ENTRYPOINT ["tini", "--"]
CMD ["litestar", "queues", "run", "--max-concurrency", "10", "--drain-timeout", "30.0"]
```

### Environment variables (required in every target)

```bash
LITESTAR_APP="app.server.asgi:create_app"   # app discovery
DATABASE_URL="postgresql+asyncpg://..."       # async driver
SAQ_REDIS_URL="redis://cache:6379/0"         # worker queue (when using litestar-saq)
LITESTAR_TRUSTED_PROXIES="*"                 # proxy header trust behind Cloud Run / Railway / ingress
SECRET_KEY="..."                              # session signing
```

<workflow>

## Workflow

### Step 1: Choose deployment target

Docker Compose for local/staging. Railway for rapid PaaS. GKE/K8s for production at scale. Cloud Run for serverless containers (and Cloud Run Jobs for `litestar-queues` one-shot tasks). systemd for bare-metal.

### Step 2: Write the Dockerfile

Start from `Dockerfile.distroless` for production (preferred). Use standard multi-stage for environments that need a shell. Use `Dockerfile.dev` for local Docker development. Always pin `ARG PYTHON_VERSION=3.13`.

### Step 3: Build frontend assets inside Docker

Copy Bun lockfiles first (layer caching), install JS deps, then `bun run build` and `uv run app assets build`. Assets must be in the wheel before `uv build --wheel --clear`.

### Step 4: Create separate worker image (Match-Your-Stack)

Background workers use the same build stages as the web image but a different `CMD`, no exposed HTTP port, and a longer termination grace period (`120s`):

- **`litestar-saq`**: run `litestar workers run` (or `app workers run`) with `SAQ_USE_SERVER_LIFESPAN=false`.
- **`litestar-queues`**: run `litestar queues run --max-concurrency 10 --drain-timeout 30.0` for SQLSpec/SQLAlchemy task queues, `litestar queues run-consumer --backend <kafka|pubsub|rabbitmq|sqs>` for stream consumers, or `litestar queues run-task` inside serverless Cloud Run Jobs.

### Step 5: Set up CI/CD

Build images in CI, push to registry, deploy via `railway up`, `gcloud run deploy`, or `kubectl apply`. Tag images with git SHA for production — never deploy `latest` to prod.

### Step 6: Configure health checks and monitoring

Expose `/health` on the API container. K8s uses startupProbe + livenessProbe + readinessProbe on `/health:8000`. Cloud Run and Railway use the same endpoint for readiness.

</workflow>

<guardrails>

## Guardrails

- **Distroless for production, slim for dev.** Distroless (`gcr.io/distroless/cc-debian12:nonroot`) has no shell, no apt, minimal CVE surface. Use slim only when you need a shell for debugging.
- **Non-root user (UID 65532).** Match the distroless `nonroot` user. Create with `useradd --system --uid 65532` in standard images.
- **uv for all package installs.** No pip, no pip-tools. `uv sync --frozen --no-dev` in builder, `uv pip install` wheel in runner.
- **UV_COMPILE_BYTECODE=1.** Pre-compile .pyc in the builder — saves 200-500ms cold-start in containers.
- **UV_LINK_MODE=copy.** Hardlinks break on overlay filesystems. Always copy.
- **Tini as PID 1.** Containers need an init process for signal forwarding and zombie reaping. `ENTRYPOINT ["tini", "--"]`.
- **Granian signal supervision (`STOPSIGNAL SIGINT`).** `litestar-granian` v0.16+ runs Granian in a supervised process group that forwards `SIGINT`, `SIGTERM`, and `SIGHUP` and enforces `--workers-kill-timeout` (default 30s, plus a 5s parent deadline). Keeping `STOPSIGNAL SIGINT` ensures clean shutdown across both standalone Granian and `litestar run`.
- **Multi-architecture support.** Use `docker buildx` with `--platform linux/amd64,linux/arm64`. Distroless Dockerfile handles arch-specific lib paths via `TARGETARCH`.
- **Asset build inside Docker.** Vite/Bun builds run in the builder stage. Never mount host `node_modules` into production images.
- **Health check endpoints.** Every API container must expose `/health`. K8s probes hit this path. Cloud Run and Railway use it for readiness.
- **LITESTAR_APP env var.** Both Litestar CLI and Granian read this for app discovery. Set it in Dockerfile and override per-environment.
- **Never run as root.** `USER nonroot` in Dockerfile. `runAsNonRoot: true` in K8s pod security context.
- **Pin Python version.** `ARG PYTHON_VERSION=3.13` at the top. Never use `python:latest`.
- **Separate worker containers from web containers.** `litestar-saq` (`litestar workers run`) and `litestar-queues` (`litestar queues run` / `run-consumer`) poll queues or brokers, not HTTP. They need a dedicated CMD, separate scaling, and no exposed port.
- **Build-time env vars to prevent connection attempts.** Set `DATABASE_POOL_DISABLED=true`, `SAQ_USE_SERVER_LIFESPAN=false`, `SAQ_WEB_ENABLED=false` during build to prevent the app from trying to connect to databases during asset compilation.

</guardrails>

<validation>

### Validation Checkpoint

Before shipping a Litestar deployment, verify:

- [ ] Dockerfile uses multi-stage build (python-base -> builder -> runner)
- [ ] `ARG PYTHON_VERSION` is pinned (not `latest`)
- [ ] `COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/` present
- [ ] `UV_COMPILE_BYTECODE=1` and `UV_LINK_MODE=copy` set in builder
- [ ] Frontend assets built inside Docker (not copied from host)
- [ ] `uv build` creates wheel; runner installs wheel (not editable)
- [ ] Runner uses non-root user (UID 65532)
- [ ] `ENTRYPOINT ["tini", "--"]` set
- [ ] `STOPSIGNAL SIGINT` set (for Granian graceful shutdown)
- [ ] `LITESTAR_APP` env var set
- [ ] `/health` endpoint exists and is used by probes/readiness checks
- [ ] Background worker (`litestar-saq` or `litestar-queues`) is a separate container/job with dedicated CMD and no EXPOSE
- [ ] No secrets in Dockerfile (use env vars or mounted secrets)
- [ ] Production image is distroless or has documented justification for slim
- [ ] Docker Compose `depends_on` uses `condition: service_healthy`

</validation>

<example>

## Example

See [references/docker-distroless.md](references/docker-distroless.md) for a complete 4-stage distroless Dockerfile with multi-arch support, Vite asset build, and non-root execution.

For a full local stack (app + worker + migrator + PostgreSQL + Valkey), see [references/docker-compose.md](references/docker-compose.md).

For Kubernetes production deployment with HPA, Ingress, and GKE Workload Identity, see [references/kubernetes.md](references/kubernetes.md).

</example>

---

## References Index

- [Litestar App Deployment & Cloud IAP](references/litestar-app.md) — Granian CLI flags, proxy headers, and Cloud IAP JWT authentication
- [Docker Standard Multi-Stage](references/docker-standard.md) — slim-based Dockerfile with cache mounts
- [Docker Distroless (Production)](references/docker-distroless.md) — preferred production image
- [Docker Workers (`litestar-saq` & `litestar-queues`)](references/docker-workers.md) — background task and consumer containers
- [Docker Compose](references/docker-compose.md) — full local/staging stack
- [Railway](references/railway.md) — PaaS deployment with PostgreSQL/Redis provisioning
- [Kubernetes / GKE](references/kubernetes.md) — Deployment, Service, HPA, Ingress
- [Cloud Run](references/cloud-run.md) — serverless container and Cloud Run Job deployment
- [systemd Native](references/systemd.md) — bare-metal service unit

## Official References

- <https://docs.litestar.dev/latest/usage/cli.html> — Litestar CLI and `litestar run`
- <https://docs.litestar.dev/latest/topics/deployment/index.html> — Official deployment guide
- <https://docs.railway.com/> — Railway platform docs
- <https://cloud.google.com/run/docs> — Cloud Run documentation
- <https://cloud.google.com/kubernetes-engine/docs> — GKE documentation
- <https://www.freedesktop.org/software/systemd/man/systemd.service.html> — systemd service units
- <https://github.com/GoogleContainerTools/distroless> — Distroless container images

## Cross-References

- [litestar-build](../litestar-build/SKILL.md) — how the wheel and PyApp onefile artifacts this skill deploys are produced (Hatchling config, Vite-in-package bundling, GitHub release pipelines)
- [litestar-granian](../litestar-granian/SKILL.md) — ASGI server tuning (workers, threads, HTTP/2, backpressure)
- [litestar-queues](../litestar-queues/SKILL.md) — database/broker task queues, stream consumers, and Cloud Run Jobs
- [litestar-saq](../litestar-saq/SKILL.md) — SAQ Redis worker configuration and task definitions
- [litestar-vite](../litestar-vite/SKILL.md) — Vite asset build pipeline and TypeGen
- [litestar settings](../litestar/references/settings.md) — env-driven `@dataclass` settings pattern

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
