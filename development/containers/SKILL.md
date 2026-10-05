---
name: containers
description: Use when building or debugging container images. Covers multi-stage builds, layer caching, image size, non-root users, signal handling, and the security defaults most Dockerfiles get wrong.
metadata:
  category: devops
  version: 1.0.0
  tags: [docker, containers, dockerfile, security, build]
---

# Containers

## Purpose

Build container images that are small, cached effectively, and safe to run — not a 1.2 GB image running as root that rebuilds from scratch every time a source file changes.

## When to Use

- Writing or reviewing a Dockerfile.
- Reducing image size or build time.
- Debugging a container that exits, hangs, or behaves differently from local development.
- Hardening images before a security review.

## Capabilities

- Multi-stage builds and build-cache optimization.
- Base-image selection: distroless, Alpine, slim, and their trade-offs.
- Non-root users, read-only filesystems, and dropped capabilities.
- Signal handling and PID 1 semantics.
- Image scanning and SBOM generation.

## Inputs

- The application, its runtime, and its build steps.
- The target platform (including whether ARM builds are required).
- Security and compliance requirements.

## Outputs

- A multi-stage Dockerfile with an ordered, cache-friendly layer sequence.
- An image running as a non-root user, with no build tooling inside.
- A scan report with no critical vulnerabilities in the final image.

## Workflow

1. **Order layers by change frequency** — Dependency manifests first, dependency install second, source code last. Copying the source before installing dependencies invalidates the cache on every code change.
2. **Build in stages** — A build stage with compilers and dev dependencies; a runtime stage containing only the artifact and its runtime. The compiler must not ship to production.
3. **Run as non-root** — Create a user in the image and `USER` it. A container running as root that is compromised is a root process on the node.
4. **Handle signals** — Use exec form (`CMD ["node", "server.js"]`), not shell form. Shell form makes `/bin/sh` PID 1, which does not forward SIGTERM, so your graceful shutdown never runs.
5. **Scan and pin** — Pin the base image by digest, scan the final image, and rebuild regularly to pick up base-image patches.

## Best Practices

- `COPY package*.json ./` then `RUN npm ci` then `COPY . .` — in that order. This is the single most impactful Dockerfile optimization and it is routinely written backwards.
- Shell-form `CMD` means your process is not PID 1 and will not receive SIGTERM. Every "why doesn't my container shut down gracefully" question has this answer.
- Distroless or `scratch` images have no shell, which is excellent for security and inconvenient for debugging. Use `kubectl debug` or a debug variant tag.
- A `.dockerignore` that excludes `.git`, `node_modules`, and build output can cut the build context from hundreds of megabytes to a few.
- `latest` is not a version. Pin by digest for reproducibility, or at minimum by an immutable tag.
- Secrets passed as build args are baked into the image layers and recoverable. Use BuildKit secret mounts.

## Examples

**Multi-stage build with correct caching, a non-root user, and exec-form CMD:**

```dockerfile
# syntax=docker/dockerfile:1

# ---- build stage: has the toolchain, ships nothing ----
FROM node:22-bookworm-slim AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci                                   # cached unless the lockfile changes

COPY . .                                     # source last: code changes do not
RUN npm run build                            # invalidate the dependency layer

# ---- runtime stage: no compiler, no dev dependencies, no shell needed ----
FROM gcr.io/distroless/nodejs22-debian12@sha256:4c2e...
WORKDIR /app

COPY --from=build --chown=nonroot:nonroot /app/dist ./dist
COPY --from=build --chown=nonroot:nonroot /app/node_modules ./node_modules

USER nonroot                                 # never root
EXPOSE 8080
CMD ["dist/server.js"]                       # exec form: the process is PID 1
```

**Secret at build time without baking it into a layer:**

```dockerfile
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
```

The token is available during the command and absent from the resulting layer. A `ARG NPM_TOKEN` would be permanently recoverable with `docker history`.

## Notes

- `docker history <image>` shows every layer and the command that created it. Anything a build arg touched is visible there — which is why build args are not a secrets mechanism.
- Alpine uses musl instead of glibc. It is smaller, but it has caused real production bugs with DNS resolution and with native Node modules. `slim` variants are usually the safer default.
- A read-only root filesystem (`readOnlyRootFilesystem: true`) with an explicit writable `emptyDir` for temp files eliminates an entire class of container escape and persistence techniques.
