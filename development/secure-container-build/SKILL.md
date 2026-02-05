---
name: secure-container-build
description: Build secure container images with Wolfi runtime, non-root users, and multi-stage builds. Templates for Python/uv, Bun, Node.js/pnpm, Golang (static/CGO), and Rust (glibc/musl) with allocator optimization
---

# Secure Container Build Best Practices

Build secure, minimal container images using security-hardened runtime images and multi-stage builds.

## Core Principles

### 1. Security-First Runtime Images

Use **Wolfi glibc-dynamic** as the runtime base image:
- Minimal attack surface (no unnecessary packages)
- Built-in CVE-free by design
- Non-root user by default (UID 65532)
- Regular security updates by Chainguard

**Production vs Development:**
```dockerfile
# ARG for choosing runtime image tag
ARG RUNTIME_TAG=latest
FROM cgr.dev/chainguard/glibc-dynamic:${RUNTIME_TAG}
```

- **`latest`** (default): Production - no shell, most secure
- **`latest-dev`**: Development - includes shell for debugging

**Build for debugging:**
```bash
podman build --build-arg RUNTIME_TAG=latest-dev -t myapp:debug .
podman run -it myapp:debug sh  # Can exec with shell
```

### 2. Multi-stage Builds

Always use multi-stage builds to minimize runtime image size:
- **Builder stage**: Full build environment (Python/Node.js official images)
- **Runtime stage**: Minimal Wolfi image with only runtime artifacts

### 3. Non-root User Configuration

Wolfi images use UID 65532 (nonroot user) by default:

```dockerfile
# No need to create user, already exists in Wolfi
USER 65532:65532

# When copying files from builder, set ownership
COPY --from=builder --chown=65532:65532 /app /app
```

### 4. Init System (tini)

Wolfi images don't include tini. Copy it from builder:

```dockerfile
# Copy tini from builder stage
COPY --from=builder /usr/bin/tini-static /usr/bin/tini

# Use as entrypoint for proper signal handling
ENTRYPOINT ["tini", "--"]
CMD ["your-app"]
```

## Quick Start

### Python + uv Project

1. **Copy Containerfile template**:
   ```bash
   cp assets/Containerfile.python-uv ./Containerfile
   ```

2. **Update application command**:
   ```dockerfile
   CMD ["python", "your_app.py"]  # Change to your entry point
   ```

### Bun Project

1. **Copy Containerfile template**:
   ```bash
   cp assets/Containerfile.bun ./Containerfile
   ```

2. **Update runtime command**:
   ```dockerfile
   CMD ["bun", "run", "start"]  # Change to your script
   ```

### Node.js + pnpm Project

1. **Copy Containerfile template**:
   ```bash
   cp assets/Containerfile.nodejs ./Containerfile
   ```

2. **Update entry point**:
   ```dockerfile
   CMD ["node", "./dist/index.js"]  # Change to your compiled output
   ```

### Golang Project

**First: Do you need CGO?** (packages with C bindings)

Most Go projects don't need CGO. Quick test:
```bash
CGO_ENABLED=0 go build .
# Success → Use Containerfile.golang (static, recommended)
# Fails → Use Containerfile.golang-cgo (CGO)
```

**Common CGO packages:** `mattn/go-sqlite3`, `git2go/git2go`, `h2non/bimg`

**Option A: Pure Go (no CGO) - Recommended**

1. **Copy Containerfile template**:
   ```bash
   cp assets/Containerfile.golang ./Containerfile
   ```

2. **Update binary name**:
   ```dockerfile
   CMD ["/app/server"]  # Change to your binary name
   ```

**Option B: Requires CGO (SQLite, C libraries)**

1. **Copy CGO template**:
   ```bash
   cp assets/Containerfile.golang-cgo ./Containerfile
   ```

### Rust Project

**Default: Use glibc template** (best compatibility)

1. **Copy template**:
   ```bash
   cp assets/Containerfile.rust ./Containerfile
   ```

2. **Update binary name**:
   ```dockerfile
   CMD ["/app/server"]  # Change to your binary name
   ```

3. **Optional: Boost performance with mimalloc**

   Three allocator options (see comments in Containerfile):
   - **(a) Cargo + mimalloc** [Recommended] - Add to Cargo.toml for best performance (50% less memory)
   - **(b) LD_PRELOAD** - Uncomment lines in Containerfile (no code changes, 50% less memory)
   - **(c) Default malloc** - No changes needed (good for most apps)

   **Why mimalloc?** Reduces memory usage by ~50% vs glibc malloc under load. See [allocator comparison](references/allocator-comparison.md) for details vs jemalloc/tcmalloc.

**Advanced: Smallest image with musl**

If you need the smallest possible image and have no C dependencies:

1. **Copy musl template**:
   ```bash
   cp assets/Containerfile.rust-musl ./Containerfile
   ```

**Warning:** musl's allocator is 7-10x slower in multi-threaded workloads. You MUST add mimalloc to Cargo.toml (see Containerfile comments).

## Builder Image Selection

### Python Projects

```dockerfile
FROM docker.io/python:3-slim AS builder
```

Use official Python slim images for building Python applications with uv.

### Bun/Node.js Projects

```dockerfile
FROM docker.io/node:lts-slim AS builder
```

Use official Node.js LTS slim images for building Bun or Node.js applications.

### Golang Projects

```dockerfile
FROM docker.io/golang:1 AS builder
```

Use official Golang images for building Go applications. Includes Go toolchain and gcc for CGO support.

### Rust Projects

```dockerfile
FROM docker.io/rust:slim AS builder
```

Use official Rust slim images for building Rust applications. Includes rustc, cargo, and rustup for target management.

## Build Cache Optimization

Use BuildKit cache mounts to speed up dependency installation:

```dockerfile
# Python/uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Bun
RUN bun install --frozen-lockfile

# pnpm
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile

# Rust/cargo (both registry and target dir)
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release
```

## Runtime Image Options

### glibc-dynamic (Default)

```dockerfile
FROM cgr.dev/chainguard/glibc-dynamic:${RUNTIME_TAG}
```

- For dynamically linked binaries
- Supports LD_PRELOAD for allocator replacement
- Suitable for: Python, Node.js, Bun, Rust (glibc), Go (CGO)

### static (Smallest)

```dockerfile
FROM cgr.dev/chainguard/static:${RUNTIME_TAG}
```

- For statically linked binaries only
- Smallest possible image size (~4MB for Rust)
- No dynamic linker (no LD_PRELOAD)
- Suitable for: Go (pure), Rust (musl)

## Debugging Support

All Containerfile templates support both production and debug builds:

### Production Build (Default)
```bash
podman build -t myapp:latest .
```
- Uses `cgr.dev/chainguard/glibc-dynamic:latest`
- No shell (most secure)
- Minimal attack surface

### Debug Build
```bash
podman build --build-arg RUNTIME_TAG=latest-dev -t myapp:debug .
```
- Uses `cgr.dev/chainguard/glibc-dynamic:latest-dev`
- Includes shell and basic tools
- For development/troubleshooting only

**Never use debug images in production!**

For detailed debugging techniques, see `references/debugging-containers.md`.

## Reference Documentation

For detailed information, consult these reference files:

- **Security practices**: See `references/security-best-practices.md`
- **Dependency management**: See `references/dependency-management.md`
- **Debugging containers**: See `references/debugging-containers.md`
- **Allocator comparison**: See `references/allocator-comparison.md`

## CI/CD Integration

For GitHub Actions workflows to build multi-arch images, see the **github-actions-container-build** plugin which provides:
- Matrix build workflow (native ARM64 runners for public repos)
- QEMU workflow (for private repos)
- Podman-based rootless builds with manifest support

## Troubleshooting

### Common Issues

**Build timeout**:
- Review Containerfile for inefficient layers
- Enable BuildKit cache mounts
- Consider splitting large builds

**Binary not found**:
- Verify the COPY command copies the correct path
- Check binary permissions (should be executable)
- For static builds, ensure correct target triple

**Container starts but exits immediately**:
- Check if tini is properly configured as entrypoint
- Verify the CMD points to the correct binary
- Use debug build to inspect: `podman run -it myapp:debug sh`

### Local Testing

**Test image locally**:
```bash
podman run --rm -it "$IMAGE:$TAG"
```

**Inspect built image**:
```bash
podman inspect "$IMAGE:$TAG"
```

**Check image size**:
```bash
podman images "$IMAGE:$TAG"
```
