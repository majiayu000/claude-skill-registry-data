---
name: do-dockerfile
version: 1.0.0
description: Write or optimize a Dockerfile and compose stack for small, secure, cache-friendly, reproducible images using multi-stage builds and non-root runtime.
author: matrixx0070
tags: [docker, containers, devops, security, build, compose]
capabilities: []
---

# do-dockerfile

## When to use

You need a production Dockerfile, a bloated image slimmed down, a slow build made cache-friendly, or a docker-compose stack for local development and integration testing.

**Not for:** Kubernetes manifests or runtime orchestration (use do-kubernetes), CI wiring that builds the image (use do-ci-pipeline), or host provisioning (use do-terraform).

## Method

1. Pick the base. Decision: use distroless or a digest-pinned slim tag for compiled/static apps; use alpine or slim only when you need a shell/package manager. Never `latest`.
2. Use multi-stage builds: a build stage with compilers and dev dependencies, a final stage that copies only the runtime artifact.
3. Order layers by change frequency — copy the lockfile and install dependencies before copying source, so code edits do not bust the dependency cache.
4. Harden. Decision: run as a non-root `USER`; if the app writes at runtime, mount a writable volume rather than dropping `readOnlyRootFilesystem`. Avoid embedding secrets (use build args or mounts), and add a `HEALTHCHECK`.
5. Trim: combine `RUN` steps, clean package caches in the same layer, and add a `.dockerignore` to keep the build context lean.
6. For compose: declare health-gated `depends_on`, named volumes, and an isolated network; keep dev-only overrides in a separate file.

## Example

```dockerfile
# build stage — has the toolchain
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci                 # cached until lockfile changes
COPY . .
RUN npm run build

# runtime stage — minimal, non-root
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER nonroot
HEALTHCHECK CMD ["node", "dist/healthcheck.js"]
CMD ["dist/server.js"]
```

## Pitfalls

- Copying source before installing dependencies, so every code edit reinstalls everything from scratch.
- Running as root in the runtime image — a container escape becomes host root.
- Using `ADD` with a remote URL or leaving a build-arg secret in an intermediate layer; `docker history` exposes it.
- Cleaning apt/npm caches in a separate `RUN` — the deleted files still live in the earlier layer, so the image never shrinks.

## Output format

```
Dockerfile: multi-stage, commented.
.dockerignore: entries listed.
docker-compose.yml: when relevant (health-gated deps, named volumes).

Before/after:
- image size:   <old> -> <new>
- layer cache:  <what now stays cached on a code-only edit>
- security:     <non-root? secrets removed? healthcheck added?>
```
