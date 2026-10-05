---
name: docker-architect
version: 1.2.0
description: Docker standards — multi-stage builds, per-language base defaults (distroless Go, slim Python/Node), BuildKit cache mounts, non-root, multi-arch amd64+arm64, digest-pinned bases, Trivy scanning, Compose v2. Use when writing or reviewing Dockerfiles or Compose files.
---

# Docker Architecture & Container Standards

Targets **Docker Engine 29**, **Compose v2**, **BuildKit** (default). Commands use `docker compose` (v2 plugin, no hyphen). File names use `docker-compose.yaml`. Per-language Dockerfiles and BuildKit/multi-arch/Trivy commands in [RECIPES.md](RECIPES.md); pinned tool versions in [STACK.md](STACK.md).

## 1. Dockerfile fundamentals

- **Always multi-stage.** A build stage (toolchain + sources) and a final runtime stage that copies only the artifacts. Never ship the toolchain in the runtime image.
- **Layer order = least → most volatile.** Pin OS deps first, then language deps, then source. Source code changes invalidate the fewest layers possible.
- **`.dockerignore` is mandatory.** Excludes `.git/`, `node_modules/`, `.venv/`, build outputs, secrets, IDE files. Bad `.dockerignore` is the most common cause of bloated images and accidentally-leaked secrets.
- **Non-root USER.** Final stage runs as a dedicated, non-root user (UID ≥ 10000). Distroless `:nonroot` tag handles this; for Debian-based, `useradd -u 10001 -r app && USER 10001`.
- **`HEALTHCHECK`** on every long-running service. Use the simplest possible probe (HTTP `/healthz`, `pg_isready`, etc.). Compose `depends_on` conditions depend on healthchecks being correct.
- **No `RUN apt-get update` without install + cleanup in the same layer:** `RUN apt-get update && apt-get install -y --no-install-recommends X && rm -rf /var/lib/apt/lists/*`.

## 2. Base image selection

Per-language defaults:

| Language | Default base | Why |
|---|---|---|
| **Go** | `gcr.io/distroless/static-debian12:nonroot` | Static binary, ~2 MB image, non-root by default, no shell (smaller attack surface). Reach for `scratch` only after auditing CA certs + tzdata yourself. |
| **Python** | `python:3.14-slim` (debian slim) | `uv` in a builder stage, copy `.venv` to runtime. Avoid alpine — musl breaks several scientific wheels. |
| **Node** | `node:22-slim` (debian slim) | Alpine breaks too many native modules. LTS only in production. |

**Always pin by digest in production:** `FROM python:3.14-slim@sha256:abc...`. Tags are mutable; digests aren't. Refresh digests via Renovate / Dependabot.

## 3. BuildKit features

BuildKit is the default builder in Docker 29 — use **cache mounts** (survive layer invalidation), **secret mounts** (never `COPY` secrets into layers), **bind mounts** (read source without `COPY`), and **here-docs** (multi-line scripts) deliberately. Snippets in [RECIPES.md](RECIPES.md).

## 4. Image security

- **Digest-pin bases** in production Dockerfiles. Renovate updates them automatically; review the diff.
- **No secrets baked in.** Build-time secrets go through `--mount=type=secret`. Runtime secrets come from the orchestrator (env, mounted file, secrets manager).
- **Drop capabilities** at runtime when possible (`--cap-drop=ALL --cap-add=NET_BIND_SERVICE`).
- **Read-only root filesystem** for stateless services (`--read-only` + tmpfs for `/tmp`).
- **Distroless `:nonroot` or explicit `USER`** — never run as root in the final stage.
- **Single-process containers.** No init system unless the app forks (then use `--init` / `tini`).
- **Scan every image in CI** (see §10).

## 5. Multi-arch builds

Always build `linux/amd64` + `linux/arm64`. Cloud is largely arm64-friendly now (Graviton, Ampere); local dev on Apple Silicon is arm64-native. `docker buildx build --platform linux/amd64,linux/arm64 ...` — full command + cache options in [RECIPES.md](RECIPES.md).

## 6. Compose patterns (v2)

- **File name:** `docker-compose.yaml` (long extension), with `docker-compose.override.yaml` for dev-only additions. Compose auto-merges them.
- **Command:** `docker compose up` (v2 plugin, integrated). The legacy `docker-compose` standalone binary is deprecated — don't use it.
- **No `version:` key.** Compose v2 ignores it; remove from any file you touch.
- **`depends_on` with conditions:**
  ```yaml
  services:
    app:
      depends_on:
        db:
          condition: service_healthy
  ```
  This requires `db` to define a working `healthcheck`. `depends_on` without `condition:` only orders startup — doesn't wait for readiness.
- **Named volumes for stateful data** (`db-data:`), bind mounts only for source-code hot-reload in dev.
- **Networks:** declare them explicitly; don't rely on the default network for anything non-trivial.
- **Secrets and configs:** use `secrets:` and `configs:` top-level blocks for production-shaped local runs.

## 7. Runtime defaults

- **Resource limits** on every service (`deploy.resources.limits.memory`, `cpus`). Unbounded containers eat hosts.
- **Logging driver:** `json-file` with size + count rotation, or `journald` on Linux hosts. Production typically forwards to a log aggregator.
- **Restart policy:** `unless-stopped` for long-running services; `no` for batch jobs.
- **Init process:** add `--init` (or `init: true` in Compose) when the app spawns child processes — prevents zombie processes.
- **TZ:** set `TZ=Etc/UTC` explicitly in the image; never rely on host timezone.

## 8. Dev vs prod

- `docker-compose.yaml` — production-shaped baseline (images by digest, no source bind mounts, prod env defaults).
- `docker-compose.override.yaml` — dev-only additions: bind-mount source for hot reload, expose ports for debuggers, pull secrets from `.env.local`.
- Compose loads both automatically with `docker compose up`. To run *prod-only*, use `docker compose -f docker-compose.yaml up` (skip the override).
- **Never bake dev conveniences into the main file.** That's how mounting `./` into prod ships.

## 9. Registry & tagging

- **Production deploys reference image digests** (`@sha256:...`), not tags. Tags are for humans; digests are for machines.
- **Human-facing tags follow semver** (`1.2.3`) plus a moving `latest` and `1.2` major/minor aliases for local convenience.
- **CI also pushes `:<short-sha>`** for traceability — easy to roll back to a specific commit.
- **Sign images** with Cosign for prod-bound registries. Verify on pull in the deployment platform.

## 10. Vulnerability scanning — Trivy

- **Default scanner: `aquasecurity/trivy`.** Open-source, fast, scans images + filesystems + IaC.
- **CI step on every push** (`trivy image --severity HIGH,CRITICAL --exit-code 1 ...`) — full command in [RECIPES.md](RECIPES.md).
- **Ignore file** (`.trivyignore`) for documented, accepted exceptions — never silent allowlists.
- **SBOM:** `trivy image --format spdx-json --output sbom.json ...` — attach to releases. Required for supply-chain compliance.

## 11. Language-specific recipes

Reference Dockerfiles for **Go (distroless)**, **Python (uv, debian slim)**, and **Node (debian slim)** live in [RECIPES.md](RECIPES.md).

## New project checklist

When scaffolding a new project, use [CHECKLIST.md](CHECKLIST.md) to walk through decisions on restart policies, resource limits, healthchecks, security, and registry setup. The checklist explicitly prompts on **restart policy** (`unless-stopped` for long-running services, `no` for batch jobs).
