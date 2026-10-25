---
name: docker-image-management
description: Guide for creating, building, and managing Docker images and containers. Use this skill when working with Dockerfiles, containerization, image building, registry operations, container runtime, storage mounts, image security, Docker Compose, or any Docker-related task including optimization, debugging, and best practices.
---

# Docker Image Management Skill

This skill covers the full lifecycle of Docker container images: authoring Dockerfiles, building with BuildKit, running containers, managing storage, pushing to registries, and scanning for vulnerabilities.

## Quick Decision Guide

| Task | Load |
|---|---|
| Writing or optimizing a Dockerfile, multi-stage builds, build cache, build secrets | `references/build.md` |
| Running containers, networking, mounts, resource limits, capabilities | `references/run.md` |
| Tagging, pushing/pulling, Docker Hub auth, image scanning (Scout) | `references/registry.md` |
| Multi-container apps | `references/docker-compose-examples.yml` |
| Dockerfile templates for Node, Python, Go, Java, etc. | `references/dockerfile-templates.md` |

Always load the relevant reference file before giving guidance on that topic.

## Core Principles

### Security first
- Run as a non-root `USER` — always. Docker Scout flags containers running as root.
- Never embed secrets in image layers. Use build-time `--secret` mounts or runtime env vars.
- Use official or verified publisher base images. Pin to a specific tag (e.g. `node:22-alpine`) or digest for reproducibility.

### Layer efficiency
- Order `COPY`/`RUN` instructions from least-to-most frequently changed to maximize cache reuse.
- Install dependencies before copying app code.
- Combine `apt-get update && apt-get install` in a single `RUN`; clean up in the same layer.
- Use multi-stage builds to keep production images free of build tools.

### BuildKit is the default
BuildKit is enabled by default in Docker Engine 23.0+ and Docker Desktop. It provides:
- Parallel stage execution
- Efficient layer caching
- Secret mounts (`--secret`)
- SSH forwarding (`--ssh`)
- Inline cache export

Use `docker buildx build` for advanced features (multi-platform, custom builders). `docker build` wraps Buildx.

## Standard Workflow

### 1. Analyze requirements
Before writing a Dockerfile, identify:
- Runtime vs. build-only dependencies
- Exposed ports
- Required env vars and config
- Persistent data (volumes)
- Security context (user, capabilities)

### 2. Write the Dockerfile
Read `references/build.md` for Dockerfile instruction guidance and patterns.
Copy a starter from `references/dockerfile-templates.md` and customize.

### 3. Create `.dockerignore`
Exclude `node_modules/`, `.git/`, `.env`, `*.log`, build output dirs, and test files.
See `references/dockerignore-template` for language-specific patterns.

### 4. Build the image
```bash
# Standard build
docker build -t myapp:1.0 .

# Build + push in one step
docker build --push -t registry.example.com/myapp:1.0 .

# Pull fresh base, bypass cache
docker build --pull --no-cache -t myapp:1.0 .

# Pass a build secret (never use --build-arg for secrets)
docker build --secret id=mysecret,src=.env -t myapp:1.0 .
```

### 5. Run and test
```bash
docker run --rm -p 3000:3000 myapp:1.0
docker logs <container>
docker exec -it <container> sh
```
Read `references/run.md` for full runtime options.

### 6. Tag and push
```bash
docker tag myapp:1.0 myorg/myapp:1.0
docker push myorg/myapp:1.0
```
Read `references/registry.md` for authentication, tagging strategy, and vulnerability scanning.

## Debugging Checklist

| Symptom | Action |
|---|---|
| Container exits immediately | `docker logs <container>` |
| Port not reachable | Check `-p HOST:CONTAINER`, verify `EXPOSE` |
| File not found in container | Check `.dockerignore`, verify `COPY` paths |
| Permission denied | Check `USER` and file ownership |
| Large image size | Use multi-stage build, alpine base, `.dockerignore` |
| Build cache not working | Verify COPY order; check if files changed |
| Secret exposed in layer | Use `--secret` mount, not `--build-arg` |