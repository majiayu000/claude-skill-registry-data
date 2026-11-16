---
name: dockerfile
description: Write or improve Dockerfiles and compose files with multi-stage builds, pinned base images, cache-friendly layer order, a non-root user, a minimal runtime image, and a .dockerignore, verified by building the image. Use when the user asks to containerize an app, write or fix a Dockerfile or docker-compose file, or make an image smaller, faster to build, or safer. Do not use for Kubernetes manifests (use agent-kit:kubernetes), for CI pipelines (use agent-kit:ci-pipeline), or for running containers in production.
---

# Dockerfile

## 1. Measure the existing image

If a Dockerfile already exists, build it before changing anything (`docker build -t <name>:before .`) and record the image size from `docker images <name>`. Do this first: once you edit the Dockerfile, the original size is lost. If Docker is unavailable, note that and continue.

## 2. Learn the app

Find the runtime and version, package manager and lockfile, build command, start command, port, required environment variables, and files the app needs at runtime. Read any existing Dockerfile, compose file, and `.dockerignore`.

## 3. Write

- **Base images:** official or trusted images pinned to an exact version tag (or digest), matching the project's runtime version; slim or distroless variants for the runtime stage.
- **Multi-stage:** install dependencies and build in a builder stage; copy only the build output and production dependencies into the runtime stage.
- **Caching:** copy the manifest and lockfile first, install with the lockfile (`npm ci`, `pnpm install --frozen-lockfile`, `uv sync --frozen`, `go mod download`), then copy the source. Use BuildKit cache mounts if the project already does.
- **Security:** run as a non-root `USER`; never copy `.env`, credentials, or `.git` into the image or pass secrets as `ARG` or `ENV` (use BuildKit `--secret`); no package manager caches left in the final image.
- **Runtime:** exec-form `CMD` or `ENTRYPOINT` so signals reach the process, `EXPOSE` the port, a `HEALTHCHECK` if the platform uses it (distroless images have no shell or curl, so use the app binary or skip it), and production settings such as `NODE_ENV=production`.
- **.dockerignore:** exclude `node_modules`, `.venv`, build output, `.git`, `.env*`, and test artifacts.
- **Compose:** pinned images, named volumes for data, health-checked `depends_on`, and no secrets inline.

## 4. Verify

Build the new image (`docker build -t <name>:after .`) and, when possible, run it briefly to confirm it starts and answers on its port, then stop it. Report the image size, before and after when there was an earlier image. Never tag and push images to a registry unless the user asks. If Docker is unavailable, say so instead of claiming the build works.

## 5. Report

Summarize the stages, base images and why, security choices, build and run results, and the image size before and after (or why the before size is missing).

## Examples

- Use: "Containerize this FastAPI app." "Make our Node image smaller." "Fix the Dockerfile so it doesn't run as root."
- Skip: "Write the Kubernetes Deployment." (agent-kit:kubernetes) "Add a GitHub Actions job that pushes the image." (agent-kit:ci-pipeline)
