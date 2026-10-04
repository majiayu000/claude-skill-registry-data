---
name: docker-build-strategies
description: Use this skill when writing, reviewing, or optimizing Dockerfiles, even if the user just says their image is too large, their build is slow, or they need to harden a container for production. Covers multi-stage builds, layer caching, .dockerignore, non-root users, and image size optimization.
license: Apache-2.0
compatibility: Requires Docker 23.0+ (BuildKit default). On Docker 20.10–22.x, set DOCKER_BUILDKIT=1 before building.
---

# Docker Build Strategies

## Overview

This skill provides rules and patterns for writing and reviewing production-quality Dockerfiles. Apply it when the main task is image-build quality: multi-stage builds, cache behavior, non-root execution, build context hygiene, and runtime image size.

## When to use this skill

Activate this skill when:

- Creating a new Dockerfile for any language or framework
- Optimizing an existing Dockerfile for size, speed, or security
- Reviewing a Dockerfile for best-practice compliance
- Adding a `.dockerignore` file to a project

## Do not use this skill when

Do not use this skill when:

- The project has no Docker setup yet and the main need is a first-pass scaffold
- The main task is wiring services together in `compose.yaml`
- The main task is debugging Compose startup ordering, networking, or development overrides

## Core guidance

### Multi-stage builds

Use multi-stage builds when the project has a build step or when build-time dependencies differ from runtime. Separate build-time dependencies from the runtime image.

1. Name every stage explicitly (`FROM ... AS build`, `FROM ... AS runtime`).
2. Use the smallest appropriate base for the runtime stage: `distroless`, `alpine`, or `slim` variants.
3. Copy only the final artifact into the runtime stage with `COPY --from=build`.
4. Use `COPY --link` when copying from a prior stage or adding static files — it improves cache reuse by making the COPY independent of previous layers.

See `references/multi-stage-builds.md` for language-specific patterns (Go, Node, Python, Java).

### Layer caching

Order Dockerfile instructions from least-frequently-changed to most-frequently-changed.

1. Place dependency manifests (`package.json`, `go.mod`, `requirements.txt`) and install steps before copying application source code. Bind-mount the manifest into the install step instead of `COPY`-ing it, so it never enters a layer: `RUN --mount=type=bind,source=package.json,target=package.json --mount=type=bind,source=package-lock.json,target=package-lock.json npm ci`. This is safe for install commands that only read the manifest (`npm ci`, `pip install -r`, `go mod download`); if a step also needs to write the manifest back into the image, `COPY` it instead.
2. Use BuildKit cache mounts for package manager caches:
   - Go: `RUN --mount=type=cache,target=/go/pkg/mod go build ...`
   - Node: `RUN --mount=type=cache,target=/root/.npm npm ci`
   - Python: `RUN --mount=type=cache,target=/root/.cache/pip pip install ...`
   - apt: `RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && apt-get install -y ...` — no `rm -rf /var/lib/apt/lists/*` needed, since the cache lives outside the image layer. `sharing=locked` is required because apt needs exclusive access to its cache directories.
   - apk (Alpine — per the Alpine wiki, not a Docker-verified doc; `references/layer-caching.md` links the source): `RUN --mount=type=cache,target=/etc/apk/cache,sharing=locked apk add ...` — drop `--no-cache` so downloaded packages land in the mounted cache directory instead of being discarded.
3. Pin base image tags to a specific version or digest — never use `latest` in production.
4. Combine related `RUN` commands with `&&` to reduce layer count, but keep logically distinct steps separate for cache granularity.

See `references/layer-caching.md` for detailed cache invalidation rules and cache mount patterns.

### Build secrets and SSH access

Never bake credentials into the image. Use BuildKit secrets and SSH mounts so credentials are available only during the specific `RUN` step that needs them, and never persist in any layer or `docker history` output.

1. **Do NOT** pass credentials through `ARG` or `ENV`. Both end up in the image layers and are inspectable via `docker history`.
2. **Do NOT** `COPY` credential files into the build context: `.npmrc`, `.pypirc`, `.netrc`, `pip.conf`, Maven `settings.xml`, `.env`, cloud credentials (`~/.aws/credentials`, `~/.config/gcloud/`, service-account JSON files, `~/.azure/`), secret-manager tokens (`~/.vault-token`), package-registry tokens (`~/.cargo/credentials.toml`), TLS keys (`*.pem`, `*.p12`), `kubeconfig`, SSH keys (`id_rsa`, `id_dsa`, `id_ed25519`, `id_ecdsa`). Even when the final stage does not copy them forward, they live in intermediate layers and the build cache.
3. **Do NOT** echo, write, or expand the secret value inside a `RUN` command in a way that persists it to a layer or emits it to build logs. Access the secret file (e.g., `/run/secrets/<id>`, or directly via the mount `target=`) — never `echo "$(cat /run/secrets/X)"`, never substitute it into a shell argument that will be logged with `--progress=plain`.
4. **Use `RUN --mount=type=secret`** for package manager registry credentials:
   ```dockerfile
   RUN --mount=type=secret,id=npmrc,target=/root/.npmrc,required=false \
       --mount=type=cache,target=/root/.npm \
       npm ci --omit=dev
   ```
   The secret is available only inside that `RUN`, never written to a layer. Use `required=true` when the build will always need the credential (e.g., all packages come from a private registry, so missing the secret should fail the build immediately); use `required=false` only when the secret is optional (the build can succeed with public packages alone).
5. **Use `RUN --mount=type=ssh`** for fetching private Git repositories or modules. The build container has no `known_hosts` by default — populate it inside the same `RUN`:
   ```dockerfile
   RUN --mount=type=ssh \
       mkdir -p -m 0700 /root/.ssh && \
       ssh-keyscan github.com >> /root/.ssh/known_hosts && \
       git clone git@github.com:org/private-repo.git
   ```
   Do NOT use `StrictHostKeyChecking=no` as a shortcut — it disables host-key verification entirely. `ssh-keyscan` accepts whatever host key the server presents each time the step runs; nothing is pinned between builds. For stronger assurance, compare it against the provider's published host key fingerprints, or write the published key into `known_hosts` instead of scanning.
6. **Invoke buildx with the secret and SSH sources:**
   ```bash
   # --ssh default forwards this shell's SSH agent (SSH_AUTH_SOCK); list every key the build can use:
   ssh-add -l

   docker buildx build \
       --secret id=npmrc,src=$HOME/.npmrc \
       --ssh default \
       .
   ```
   The `RUN --mount=type=ssh` step can use every key that `ssh-add -l` lists, so expose only the key this build needs. In an interactive terminal, run `ssh-agent bash` to start a shell with a dedicated agent, then run `ssh-add <key-file>`, confirm that `ssh-add -l` lists only that key, and run the build in that shell. A tool that starts a new shell for each command loses that agent between commands, so ask the user to run these steps. Alternatively, pass an unencrypted key file, such as a dedicated deploy key, directly with `--ssh default=<key-file>`; BuildKit rejects passphrase-protected keys in this form, so load those into an agent instead.
7. `.dockerignore` exclusions of `.env` and credential files are **defense in depth**, not the primary mechanism — keep them, but do not rely on them as your only protection.

See `references/multi-stage-builds.md` for per-language patterns (npm, pip, Maven, Go `GOPRIVATE`).

### .dockerignore

Always generate a `.dockerignore` alongside the Dockerfile. Exclude:

- `.git/`, `.github/`, `.vscode/`, `.idea/`
- `node_modules/`, `__pycache__/`, `.venv/`, `vendor/` (when rebuilt in the build stage)
- `*.md`, `LICENSE`, `docs/`
- Build outputs, test artifacts, and IDE configs
- `.env` files and any secrets

See `assets/dockerignore-example` for a comprehensive template.

### Non-root user

Always configure the final image to run as a non-root user.

1. Create a dedicated user and group in the runtime stage:
   ```dockerfile
   RUN addgroup --system --gid 1001 appgroup && \
       adduser --system --uid 1001 --ingroup appgroup appuser
   ```
2. Set ownership on application files: `COPY --from=build --chown=appuser:appgroup /app /app`
3. When combining `--chown` with `COPY --link`, always use the numeric UID:GID you assigned (e.g., `--chown=1001:1001` if you used `--uid 1001 --gid 1001` above), not named users. `--link` creates an independent layer where named users from prior `RUN` instructions are not available.
4. Place the `USER appuser` instruction after all file operations and before `ENTRYPOINT`/`CMD`.
5. On distroless images, use the built-in nonroot user: `USER nonroot:nonroot`.

### Image size optimization

1. Prefer `FROM scratch` (Go static binaries), distroless, or Alpine-based images for the runtime stage.
2. Install OS packages with a BuildKit cache mount rather than `rm -rf`-ing the cache in the same layer — see "Layer caching" above. The cache mount keeps the package cache out of the image layer entirely, so no cleanup step is needed.
3. Do not install documentation, man pages, or debug tools in the runtime image.
4. Use `.dockerignore` aggressively to minimize the build context.

### General rules

- Always include a `# syntax=docker/dockerfile:1` directive as the first line to enable BuildKit features.
- Set `WORKDIR` before any `COPY` or `RUN` instructions — never rely on the default `/`.
- Prefer `ENTRYPOINT` with exec form (`["binary"]`) over shell form.
- Add `EXPOSE` to document the listening port.
- Add metadata labels: `LABEL org.opencontainers.image.source=...`

## Related skills

- For first-time Docker project scaffolding and deciding which files to create, use `docker-project-foundations`.
- For service dependencies, health checks, overrides, networks, and volume patterns, use `docker-compose-patterns`.
- For destructive Docker CLI commands (`docker system prune`, `docker rm -f`, image/network/builder pruning) and a cross-product index of destructive-command guardrails, use `docker-destructive-guardrails`.

## References

- `references/multi-stage-builds.md` — Language-specific multi-stage patterns for Go, Node.js, Python, and Java
- `references/layer-caching.md` — Deep dive on layer ordering, cache invalidation, and BuildKit cache mounts

## Assets

- `assets/Dockerfile.go` — Multi-stage Go build with distroless runtime and non-root user
- `assets/Dockerfile.nodejs` — Multi-stage Node.js build with proper layer caching and non-root user
- `assets/Dockerfile.python` — Python build with virtual env, layer ordering, and non-root user
- `assets/dockerignore-example` — Comprehensive `.dockerignore` template

## Scripts

- **`scripts/verify-build.sh`** — Builds the Dockerfile in the current directory, then reports image size and configured user. Run it from the project root (the directory that contains the `Dockerfile`), with the script path resolved under this skill's directory:
  ```bash
  bash "<skill-dir>/scripts/verify-build.sh" [--help] [IMAGE_NAME]
  ```
  Replace `<skill-dir>` with the absolute path of the folder that contains this `SKILL.md`; the `scripts/` path is relative to that folder, not to the project. Do not change into the skill directory first: the script builds whatever is in the current directory. If the skill directory cannot be resolved, run `docker build -t verify-build-test .`, then `docker images verify-build-test` and `docker inspect verify-build-test --format '{{.Config.User}}'`. Exit status is `0` when all Docker commands succeed or help is requested, the failing Docker command's non-zero status when verification fails, and `2` for invalid arguments.

## Checks

- `checks/verification.md` — Detailed verification runbook for manual review.
