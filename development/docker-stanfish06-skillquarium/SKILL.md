---
name: docker
description: Containerizing and shipping applications with Docker — writing efficient Dockerfiles (multi-stage builds, layer caching, small/secure images), docker compose for multi-service local stacks, and the core build/run/debug commands. Use when creating a Dockerfile, debugging image builds, slimming images, or composing services (app + db + cache). For Claude Code dev sandboxes use devcontainer-setup; for serverless GPU runs use modal.
---

# Docker — containerizing applications

## Overview

Docker packages an app and its dependencies into a portable image. This skill covers
**writing good Dockerfiles** and **composing services**. For local *development*
environments with Claude Code, prefer [[devcontainer-setup]]; for serverless GPU jobs use
[[modal]]. This is for building/shipping app images.

## Dockerfile — the essentials

```dockerfile
# Pin a specific, slim base. "slim" over full; avoid bare :latest in production.
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# Copy ONLY dependency manifests first so this layer caches across code changes.
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

# Then copy source (changes often -> invalidates only later layers).
COPY . .

# Run as non-root.
RUN useradd -m app && chown -R app /app
USER app

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Layer ordering is the core skill:** put rarely-changing steps (deps) before
frequently-changing ones (source) so the build cache is reused. Use a `.dockerignore`
(`.git`, `__pycache__`, `node_modules`, data, `.venv`) to keep the build context small.

## Multi-stage builds — small final images

Build/compile in a fat stage, copy only artifacts into a slim runtime stage:

```dockerfile
FROM node:22 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build               # produces /app/dist

FROM nginx:1.27-alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
```

The final image contains no toolchain, source, or build caches — smaller and smaller attack
surface. Use `--from=build` to pull exactly what you need.

## Core commands

```bash
docker build -t myapp:1.0 .
docker build --target build -t myapp:dev .       # build a specific stage
docker run --rm -p 8000:8000 --env-file .env myapp:1.0
docker run --rm -it myapp:1.0 sh                 # shell into the image
docker exec -it <container> sh                   # shell into a running container
docker logs -f <container>
docker ps -a;  docker images
docker system prune -af --volumes                # reclaim disk (careful: removes unused)
```

Build cache & speed: enable BuildKit (default on modern Docker). For multi-arch:
`docker buildx build --platform linux/amd64,linux/arm64 -t myapp:1.0 --push .`.

## docker compose — multi-service local stacks

```yaml
# compose.yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:17
    environment:
      POSTGRES_PASSWORD: dev
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

```bash
docker compose up -d --build      # start (rebuild if needed)
docker compose logs -f app
docker compose down -v            # stop and remove volumes
```

Use `depends_on` + `healthcheck` so the app waits for the DB to be *ready*, not just
*started*.

## Gotchas

- **Huge images** → not using `-slim`/`alpine`, missing multi-stage, or a fat build context
  (no `.dockerignore`). Inspect with `docker history myapp:1.0`.
- **Cache never hits** → you `COPY . .` before installing deps. Copy manifests first.
- **Secrets:** never `COPY` secrets or bake them via `ENV`/`ARG` (they persist in layers).
  Use `--secret`/BuildKit mounts or runtime env vars.
- **Runs as root by default** → add a non-root `USER`.
- **`alpine` + Python/C deps:** musl libc breaks many manylinux wheels; prefer
  `*-slim` (Debian) for Python/data work.
- **File watching/perf** on bind mounts (macOS/Windows) is slow — fine for dev, don't ship
  bind mounts to production.

## Related

Dev environments: [[devcontainer-setup]]; serverless/GPU: [[modal]], [[e2b-sandbox]];
build/test in CI with [[github-actions-ci]]; Python setup in [[modern-python]].
