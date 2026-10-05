---
name: docker
description: Apply when writing or reviewing Dockerfiles, docker compose files, or container build pipelines. Covers layer caching, multi-stage builds, security hardening, and compose conventions.
license: MIT
version: 1.0.0
tokens_target: 1700
triggers:
  - dockerfile
  - docker compose
  - container build
loads_after:
  - code-quality
supersedes: []
---

# Sub-Skill: Docker / Container Conventions

**Purpose:** Prevent common container mistakes — busted layer caches, bloated images, insecure defaults, and compose misconfigurations — before they reach CI or production.

---

## Rules

### Layer Ordering & Cache

1. **Dependency layer first.** Always install dependencies in a separate layer before copying application source, so a source change does not invalidate the package cache. Reference: ERR-2026-020
2. **Copy only what's needed early.** Before copying the full source tree, copy only the dependency manifest files (e.g., `requirements.txt`, `package.json`, `pyproject.toml`) so the install layer is cached independently.
3. **Minimise layer count.** Prefer chaining related `RUN` commands with `&&` and `\` continuations rather than issuing one `RUN` per command; each `RUN` creates a new layer.
4. **Order by change frequency.** Always place instructions that change rarely (OS packages, global tools) before instructions that change often (app source, config files).

### Multi-Stage Builds

5. **Use multi-stage for compiled artefacts.** Always use a builder stage to compile or bundle, then copy only the final artefact into a minimal runtime stage; never ship build toolchains in the production image.
6. **Name every stage.** Use `AS <name>` on every `FROM` line so later stages and `docker build --target` calls are readable and stable.
7. **Pin the runtime base image.** Always pin base images to a specific digest or immutable tag (e.g., `python:3.12.3-slim`) in the runtime stage; never use `latest` in production Dockerfiles.

### Security

8. **Run as non-root.** Always create a dedicated non-root user and switch to it with `USER` before the final `CMD`/`ENTRYPOINT`; never run application processes as `root` inside a container.
9. **Never embed secrets in image layers.** Never pass secrets via `ARG` or `ENV` in a Dockerfile; use Docker BuildKit `--secret` mounts or runtime environment injection instead.
10. **Scan images before push.** Before pushing any image to a registry, run an image vulnerability scanner (e.g., `trivy image`, `docker scout`) and fail the pipeline on critical CVEs.
11. **Prefix docker run -v from Git Bash with MSYS_NO_PATHCONV=1.** Always prefix `docker run -v` calls issued from Git Bash or MSYS on Windows with `MSYS_NO_PATHCONV=1` to prevent path mangling. Reference: ERR-2026-013

### .dockerignore & Context

12. **Maintain a .dockerignore.** Always keep a `.dockerignore` at the repo root that excludes `.git`, test fixtures, local env files, and build artefacts; a large build context slows every build and may leak secrets.

### Health Checks & Signal Handling

13. **Declare a HEALTHCHECK.** Always add a `HEALTHCHECK` instruction so orchestrators (Compose, Kubernetes) can detect unhealthy containers without external probes.
14. **Use exec-form ENTRYPOINT.** Always write `ENTRYPOINT` in exec form (`["executable", "arg"]`) rather than shell form so the process receives OS signals directly and `docker stop` terminates it cleanly.

### Compose Conventions

15. **Set resource limits in compose.** Always declare `deploy.resources.limits` (CPU and memory) for every service in `docker-compose.yml` to prevent a runaway container from starving the host.
16. **Use compose profiles for optional services.** Prefer assigning optional services (e.g., observability stacks, seed jobs) to named `profiles` so `docker compose up` starts only the core services by default.
17. **Isolate networks per stack.** Avoid using the default bridge network across unrelated stacks; define explicit named networks and attach only the services that need to communicate.

---

## See also

- `skills/code-quality/SKILL.md` — general layering and change-frequency ordering principles
- `skills/review-deployment/SKILL.md` — deployment checklist that includes image scanning and migration ordering

---

## Notes

- ERR-2026-020 is the canonical reference for layer-cache busting caused by copying source before installing dependencies.
- ERR-2026-013 covers MSYS path mangling on Windows when using `docker run -v`.
