---
name: docker-pro
description: Create, edit, and modernize Dockerfiles, .dockerignore, Docker Bake files, and Compose files using Bret Fisher's strongly opinionated modern Docker + BuildKit rules. Use this skill whenever the user asks about a Dockerfile, containerizing or "dockerizing" an app, base image choice, digest/SHA pinning of image tags, multi-stage builds, BuildKit, build caching or secrets, .dockerignore, docker-bake.hcl / `docker buildx bake`, hardened or distroless images (Chainguard, Docker Hardened Images / DHI), a compose.yaml / docker-compose file, or local dev environments with Compose — even for a small change to any of these files.
license: MIT
---

# Modern Docker & BuildKit Rules

Use this skill when creating, editing, reviewing, or modernizing any Docker build or run files: `Dockerfile`, `.dockerignore`, `docker-bake.hcl`, and `compose.yaml`. Be strongly opinionated and apply these defaults proactively, unless the repository already has clear conflicting conventions or the user explicitly asks for a different tradeoff.

These rules assume **BuildKit** is the builder (the default in modern Docker Engine and in `docker buildx`). That assumption is what lets us use every modern frontend feature below without guarding for legacy builders.

## Working Style

1. Inspect the repo before writing. Detect the language/runtime, package manager, lockfiles, build output dir, and any existing Docker files so your output matches reality instead of a generic template.
2. Prefer the smallest correct change, but don't preserve legacy patterns (no `version:` in compose, secrets baked into layers, `apt-get` without cache mounts) when you're already editing that file.
3. Never invent base image tags, package names, ports, or build commands as facts. If the repo doesn't reveal a value, use a clearly-marked placeholder and say so. Image tags in particular drift — when you're unsure a tag exists, tell the user to confirm against the registry's catalog rather than asserting it.
4. Complete the hand-back checklist below so the user can maintain each change.

## Dockerfile Layout

A Dockerfile is easier to maintain when the things people change most often — versions and config — live at the top in predictable places, and the build logic reads top-to-bottom. Follow this order:

```dockerfile
# syntax=docker/dockerfile:1          # 1. frontend directive — MUST be the very first line
ARG NODE_VERSION=22                   # 2. global version ARGs — one place to bump bases
ARG ALPINE_VERSION=3.22

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS deps   # 3. all FROM stages, each named AS
FROM deps AS build
FROM cgr.dev/chainguard/node:latest AS runtime
# ... stage bodies follow, in build order ...
```

### 1. Frontend directive, first line

Start every Dockerfile with:

```dockerfile
# syntax=docker/dockerfile:1
```

This pulls the latest stable **1.x** Dockerfile frontend from Docker Hub at build time, which decouples Dockerfile features from the engine version — even an older Docker Engine then understands the newest syntax. Pinning to `:1` (not `:1.0` or a full version) is deliberate: the v1 line guarantees no breaking changes, so you get new features and fixes for free. Only hard-pin a minor (e.g. `:1.7`) when a user explicitly needs byte-for-byte reproducibility of the frontend itself.

It must be the **first line** — before comments, before `ARG`. If it isn't first, BuildKit ignores it and silently falls back to the built-in frontend.

### 2. Centralize versions in global ARGs

Declare base-image versions as `ARG`s in the global scope (before the first `FROM`) so every version lives in one block at the top:

```dockerfile
ARG NODE_VERSION=22
ARG ALPINE_VERSION=3.22
```

A global `ARG` is in scope for `FROM` lines. To also use it _inside_ a stage (e.g. in a `RUN`), redeclare a bare `ARG NODE_VERSION` (no default) inside that stage — global args don't automatically cross into stage bodies. The payoff: bumping a version is a one-line edit at the top, and any value is overridable at build time with `--build-arg NODE_VERSION=20` without touching the file.

### 3. All FROM stages at the top, each named with AS

List every build stage's `FROM` near the top of the file with an explicit `AS <name>`, before the long stage bodies. Co-locating the `FROM` lines makes the image graph readable at a glance and keeps all base-image references in one neighborhood, which pairs with the version ARGs above. Named stages also give you stable `COPY --from=<name>` targets and let users build a single stage with `--target <name>`.

### 4. ENV near the top of its stage

Put a stage's `ENV` declarations together near the top of that stage, not scattered between `RUN`s. Env vars are config people reach for first; grouping them makes them findable and keeps cache busting predictable (an `ENV` change invalidates everything below it).

### 5. Use BuildKit frontend features

Because BuildKit is assumed, prefer these over legacy equivalents — they're faster, safer, or both:

```dockerfile
# Cache mounts: persist package-manager caches across builds (don't bloat layers)
RUN --mount=type=cache,target=/root/.npm npm ci

# Secret mounts: secrets are available during RUN but never written to a layer
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci

# Bind mounts: read context/another stage during RUN without COPYing it in
RUN --mount=type=bind,source=package.json,target=package.json npm ci

# COPY --link: layer is independent of its parent chain → better cache reuse
COPY --link ./dist /app/dist

# Heredocs: multi-line RUN without trailing backslashes
RUN <<EOF
set -eux
apt-get update
apt-get install -y --no-install-recommends curl
rm -rf /var/lib/apt/lists/*
EOF

# ADD --checksum: verify a remote artifact's integrity
ADD --checksum=sha256:24454f8...d68d https://example.com/app.tar.gz /opt/
```

## Base Images: Hardened by Default

Default to minimal, hardened base images. They ship with a far smaller package set, which means a smaller attack surface, fewer CVEs to patch, and smaller images. Reach for a full general-purpose base (Debian/Ubuntu/official-`alpine`) only when the app genuinely needs the extra tooling at runtime and a hardened variant won't do — and say why when you do.

Two free, recommended sources:

- **Chainguard Images** — `cgr.dev/chainguard/<name>`. The public catalog pulls with **no authentication**, which makes it the lowest-friction default. Most images come in two flavors:
  - `:latest-dev` — includes a shell and the `apk` package manager. Use in **build stages** where you need to install things.
  - `:latest` (and `static`) — **distroless**: no shell, no package manager. Use in the **final runtime stage**.
- **Docker Hardened Images (DHI)** — `dhi.io/<name>`. Free, but pulls require a one-time `docker login dhi.io` with a Docker account. Tags look like `dhi.io/python:3.13` or `dhi.io/python:3.12-alpine3.22`, with `-dev` variants that add a shell + package manager for build stages. Prefer DHI when the user is already in the Docker ecosystem or wants Docker's signed SBOM/VEX supply-chain metadata.

The multi-stage pattern that makes hardened images practical: do the messy work (compilers, package installs) in a `-dev` build stage, then `COPY --from` only the built artifacts into a distroless final stage that has no shell or package manager to exploit.

```dockerfile
# syntax=docker/dockerfile:1
ARG GO_VERSION=1.24

FROM cgr.dev/chainguard/go:latest-dev AS build
FROM cgr.dev/chainguard/static:latest AS runtime

FROM build AS compile
WORKDIR /src
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    CGO_ENABLED=0 go build -o /app ./cmd

FROM runtime
COPY --from=compile /app /app
ENTRYPOINT ["/app"]
```

Distroless final stages have no shell, so `ENTRYPOINT`/`CMD` must use exec form (`["/app"]`, not `/app`), and `RUN`/`apt`/`apk` won't work there — that's the point. Because exact tags vary per image and over time, treat the tags above as the shape, not gospel; tell the user to confirm against the catalog when it matters.

## Pin Every External Image by Digest

Pin every external image reference — both `FROM` lines and `COPY --from=<image>` that pull a registry image — to a **tag _and_ a digest**. A tag like `node:24` or `:latest` is mutable: the registry can repoint it to new content at any time, so two builds of the "same" Dockerfile can produce different images. The `@sha256:...` digest is immutable content-addressing, so it makes the build reproducible and closes a supply-chain hole (you get exactly the bytes you reviewed, not whatever was pushed since). Keep the human-readable tag alongside the digest so a reader can still see _what_ the image is:

```dockerfile
FROM node:24.11.1@sha256:9a2ed90cd91b1f3412affe080b62e69b057ba8661d9844e143a6bbd76a23260f
```

To get the digest, prefer `regctl` if it's installed — it queries the registry without pulling the whole image:

```bash
regctl manifest head node:24.11.1     # prints the digest for the current tag
```

If `regctl` isn't available, fall back to `docker buildx imagetools inspect <image>:<tag>` (also no full pull), or pull and read `docker inspect --format '{{index .RepoDigests 0}}' <image>:<tag>`. Don't invent a digest — if you can't resolve a real one, leave a clearly-marked `@sha256:<PIN-ME>` placeholder and tell the user the exact command to fill it in.

This composes with the centralized version ARGs: keep the tag in an ARG for readability and put the digest in a sibling ARG, so the whole reference still lives in one place at the top:

```dockerfile
ARG NODE_VERSION=24.11.1
ARG NODE_DIGEST=sha256:9a2ed90cd91b1f3412affe080b62e69b057ba8661d9844e143a6bbd76a23260f
FROM node:${NODE_VERSION}@${NODE_DIGEST} AS build
```

Two clarifications so this doesn't backfire:

- It applies only to **external image URIs**. A `COPY --from=build` that references a _named internal stage_ needs no digest — it's resolved within the build, not pulled from a registry.
- A digest pin freezes the image, which is the point — but it also means you stop getting upstream security patches until the pin is refreshed. Tell the user to let automation (Dependabot/Renovate's Docker support) bump these digests on a schedule, the same way they'd update any dependency, rather than hand-editing hashes or, worse, reverting to bare tags to "stay current."

## Always Create a .dockerignore

Every build context should have a `.dockerignore`. It shrinks what gets sent to the builder (faster builds, better cache), and — more importantly — it's a real security control: the whole context is shipped to the daemon, so excluding `.git`, `.env`, and keys prevents secrets and history from leaking into images.

Build it by starting from the repo's `.gitignore` (if present, copy its entries so already-ignored junk like `node_modules`, build output, and `dist` is excluded too), then add the Docker-specific entries that `.gitignore` won't have:

```gitignore
# --- copied from .gitignore ---
# (paste the project's .gitignore contents here)

# --- Docker additions ---
.git
.gitignore
.dockerignore
Dockerfile*
compose*.yaml
docker-compose*.yml
docker-bake.hcl

# secrets & local env
.env
.env.*
*.pem
secrets/

# CI / docs / editor / OS cruft
.github/
README.md
.vscode/
.idea/
.DS_Store
```

`.git` is the headline addition: it's often huge and carries full history (including any secrets ever committed), and it's almost never needed inside an image.

## Always Add a Bake File

Add a `docker-bake.hcl` so builds are defined as reproducible, version-controlled config instead of long, drifting `docker build` command lines. Bake (`docker buildx bake`) reads it to build one or many targets with consistent tags, platforms, and args — and it's what CI should call so local and CI builds stay identical.

```hcl
variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["app"]
}

target "app" {
  context    = "."
  dockerfile = "Dockerfile"
  tags       = ["myapp:${TAG}"]
  # platforms = ["linux/amd64", "linux/arm64"]   # uncomment for multi-arch
}
```

Build with `docker buildx bake` (the `default` group) or `docker buildx bake app`. Override variables at runtime (`TAG=v2 docker buildx bake`) or per-target (`--set app.platforms=linux/arm64`). Use `inherits` to share a base target's settings and `matrix` to fan one target into variants. Note that `docker buildx bake` with no `-f` auto-discovers `compose.yaml` _before_ `docker-bake.hcl` and turns service `build:` blocks into targets — so if a repo has both, point CI at the file you mean with `-f docker-bake.hcl`.

## Compose for Local Dev

For first-time setup without a Compose file, finish the requested build files and offer to add `compose.yaml` in the final answer. Leave Compose creation pending approval so the user controls local-development scope. When the user is unavailable, include the offer for their next response. If a Compose file already exists, modernize it in place.

Conventions:

- **Name it `compose.yaml`** (the canonical Compose Spec filename), not `docker-compose.yml`.
- **No top-level `version:` key.** It's obsolete in Compose V2 and now emits a warning — remove it from any file you touch.
- **Prefer file sync over bind mounts for source code.** A classic bind mount (`./src:/app/src`) couples container paths to host layout and can be slow or permission-fraught. The modern `develop.watch` mechanism instead _syncs_ changed files into the container, which is faster, cross-platform, and lets you choose what each path change should do.

```yaml
services:
  web:
    build: .
    ports:
      - "3000:3000"
    develop:
      watch:
        # sync: push live source changes into the running container (hot reload)
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - node_modules/
        # rebuild: dependency manifests / compiled languages need a fresh image
        - action: rebuild
          path: package.json
        # sync+restart: config the process only reads at startup
        - action: sync+restart
          path: ./config.yml
          target: /app/config.yml
```

Start it with `docker compose watch`. Pick the action by what the change requires: `sync` for hot-reloadable source, `rebuild` for lockfiles/compiled code, `sync+restart` for startup-only config.

## When You Finish

Complete these checks in the final user-facing answer so the user can maintain the files without opening another document:

- Give each applied default or modernization its own `change — reason` line. Cover the frontend, base image, digest pin, cache mounts, runtime user, `.dockerignore`, Bake, and each Compose change when used. Reasons explain the benefit; a list of settings alone is incomplete.
- Include exact build and run commands, plus validation results and unresolved placeholders, so the user can reproduce the work.
- For first-time setup, include the Compose offer described above so the user can approve the next step.
