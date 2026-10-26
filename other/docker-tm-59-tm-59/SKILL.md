---
name: docker
description: Use when writing Dockerfiles and Compose files — reproducible builds that run tests for any language without a local toolchain, multi-stage images, pinned base images tracked by dependency bots, caching, non-root runtime, and Compose for app plus database. Also use when deciding whether a low-spec machine should run Docker at all, when builds are slow, or when "works in the container" differs from CI.
---

# Docker

Default: a multi-stage `Dockerfile` whose build stage runs the tests, base images pinned to a version tag (and tracked by a dependency bot), a non-root final stage, Compose only when more than one service is needed.

## The "test in the image" pattern

For learning repositories in many languages, the image is the toolchain:

```dockerfile
FROM rust:1-slim AS build          # pin a concrete tag in real use
WORKDIR /src
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo 'fn main(){}' > src/main.rs && cargo fetch   # cache dependencies
COPY . .
RUN cargo test --locked && cargo build --release --locked

FROM debian:stable-slim
RUN useradd -r app
COPY --from=build /src/target/release/tool /app/tool
USER app
ENTRYPOINT ["/app/tool"]
```

`docker build .` then proves "a clean machine can build and test this" — useful as a light CI gate when the language is not installed anywhere else.

## Caching and size

- Copy dependency manifests first, install dependencies, then copy the source; source changes do not invalidate the dependency layer.
- Use `.dockerignore` (version-control metadata, dependency folders, build output, local configuration and keys) to keep the context small and secrets out.
- Slim or distroless final images; no compilers in the runtime stage.

## Pinning and updates

- Pin `FROM` to a version tag (or a digest for maximum reproducibility). Configure the dependency bot's `docker` ecosystem so base image updates arrive as pull requests.
- For languages whose package manager the bot cannot read, the base image becomes the managed dependency — note that in the repository.

## Compose

- `docker compose up` for app + database; named volumes for data; health checks and `depends_on: condition: service_healthy` so the app waits for the database.
- Configuration through environment variables from a file that is not committed (commit an example file instead).

## When not to run Docker locally

On low-memory or low-disk machines, Docker Desktop and images can cost more than the work itself. Run container builds on CI (as a light PR gate) or another machine, and keep a native path for day-to-day work.

## Verification loop

1. `docker build --progress=plain .` passes, including the test step.
2. `docker run --rm image --help` works as a non-root user.
3. For Compose: `docker compose up -d`, wait for health, run a smoke request, `docker compose down -v`.

## Pitfalls

- **`latest` tags** make builds change under you.
- **`apt-get update` in its own layer** caches stale indexes; combine with `install` and clean lists in one `RUN`.
- **Secrets in build args or layers** stay in the image history; use build secrets (`--secret`) or runtime injection.
- **File ownership:** files copied as root are not writable by the runtime user; use `COPY --chown`.
- **Architecture:** images built on ARM laptops may not run on x86 servers; build with `--platform`.
