---
name: docker-compose
description: Debug and manage ettametta's Docker Compose stack. Use when troubleshooting service orchestration, container networking, volume issues, Traefik routing, healthchecks, or multi-container startup failures.
---

# Docker Compose Debugging

Skill for diagnosing Docker Compose issues in ettametta — service startup, networking, volumes, Traefik routing, healthchecks, and container lifecycle.

## Quick Diagnostics

```bash
docker compose ps
docker compose logs --tail=50 api
docker compose stats --no-stream
docker inspect --format='{{json .State.Health}}' ettametta-api-1 | jq
```

## Service Architecture

| Service | Image | Port | Healthcheck | Restart |
|---|---|---|---|---|
| traefik | traefik:v3.7 | 80, 443 | None | None |
| db | postgres:15-alpine | 7203:5432 | pg_isready | always |
| redis | redis:7-alpine | 7204:6379 | redis-cli ping | always |
| api | api.Dockerfile | 7201:8000 | curl /health | always |
| dashboard | dashboard/Dockerfile | — | None | always |
| celery_worker | api.Dockerfile | — | psutil check | always |
| celery_beat | api.Dockerfile | — | psutil check | always |
| ollama | ollama/ollama:latest | 11434 | None | always |
| nginx | nginx:alpine | 7200:80, 7213:443 | None | None |
| openclaw | openclaw.Dockerfile | 7217-7219 | None | unless-stopped |
| node-skills | node:18-alpine | 3002 | None | None |
| ai-gateway | gatekeeper.Dockerfile | 8133 | None | always |
| video_processor | video_processor.Dockerfile | 7206:8001 | python no-op | unless-stopped |
| qdrant | qdrant/qdrant:latest | 6333, 6334 | None | unless-stopped |

## Common Issues & Fixes

### Service won't start — missing env vars
Compose enforces `:?` on `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, `AI_CLUSTER_SECRET`. Empty/missing = immediate exit.
```bash
docker compose config --format json | jq '.services.api.environment'
```

### Celery starts before DB is ready
`celery_worker` and `celery_beat` use `depends_on: [redis, db]` without `condition: service_healthy`. Fix:
```yaml
celery_worker:
  depends_on:
    redis: { condition: service_healthy }
    db: { condition: service_healthy }
```

### API runs as root (security)
Compose sets `user: "0:0"` on api, celery_worker, celery_beat — overrides `appuser` from Dockerfile.

### Traefik/nginx have no restart policy
If they crash, all ingress stops. Add `restart: always`.

### Port conflict with ollama compose
Both `docker-compose.yml` and `docker-compose.ollama.yml` define ollama. Use `-f` to specify.

### Dockerfile base image mismatch
`api.Dockerfile` defaults to python:3.12-slim but compose passes python:3.11-slim.

## Dockerfiles

| File | Stages | Notes |
|---|---|---|
| infra/docker/api.Dockerfile | Single | ffmpeg, chromium, deno, opencli-rs, yt-dlp |
| infra/docker/video_processor.Dockerfile | 2 (builder/runtime) | torch, moviepy, opencv |
| apps/dashboard/Dockerfile | 2 (builder/runner) | Next.js build |
| infra/docker/openclaw.Dockerfile | Single | playwright, crewai |
| infra/docker/gatekeeper.Dockerfile | Single | minimal fastapi+uvicorn |
| infra/docker/voiceover.Dockerfile | Single | Fish Speech TTS |

## Traefik Routing (via Docker labels)

| Router | Host | Service | Middleware |
|---|---|---|---|
| traefik | traefik.localhost | api@internal | BasicAuth |
| api | api.localhost | api:8000 | — |

## Compose Files

| File | Purpose |
|---|---|
| docker-compose.yml | Primary stack (14 services) |
| docker-compose.ollama.yml | Standalone Ollama (port 11435) |
| docker-compose.dify.yml | Dify AI orchestration (3 services) |

## Debugging Checklist

1. `docker compose ps` — all services running?
2. `docker compose logs --tail=20 <service>` — recent errors?
3. `docker compose config` — validate syntax
4. Check env vars: `docker compose config --format json | jq '.services.<name>.environment'`
5. Check volume permissions: `ls -la data/storage/`
6. Check port conflicts: `ss -tlnp | grep -E '7200|7201|7203|7204'`
