---
name: docker-build-test
description: Docker build and test workflow with mandatory pre-push validation checklist to prevent CI/CD failures
---

# Docker Build & Test

Local Docker testing workflow to prevent CI/CD failures. **CRITICAL**: Always run `make validate` before pushing.

## Pre-Push Checklist (MANDATORY)

Before pushing ANY Docker-related changes:

- [ ] `make validate` passes completely
- [ ] No build errors or warnings
- [ ] Smoke tests pass
- [ ] Image sizes verified
- [ ] Clean validation from scratch

## Quick Start

```bash
# Complete validation (ALWAYS run before push)
make validate

# Build and test everything
make all

# Clean and rebuild
make clean && make validate
```

## Build Commands

```bash
# Build both images
make build

# Build individual images
make build-healthcheck
make build-pgbouncer
```

## Test Commands

```bash
# Test both images
make test

# Test individual images
make test-healthcheck
make test-pgbouncer
```

## Validation Pipeline

```bash
# 1. Complete validation (recommended)
make validate

# 2. Check for errors
make build 2>&1 | grep -i error

# 3. Verify functionality
make test

# 4. Check image sizes
make info

# 5. Clean validation
make clean && make validate
```

## Manual Docker Commands (Fallback)

```bash
# Build
docker build -f Dockerfile.healthcheck -t pgbouncer-healthcheck:latest .
docker build -f Dockerfile.pgbouncer -t pgbouncer:latest .

# Test
docker run --rm pgbouncer-healthcheck:latest /usr/local/bin/healthcheck-unified.py --help
docker run --rm pgbouncer:latest /usr/local/bin/pgbouncer --version

# Check sizes
docker images | grep -E "(pgbouncer-healthcheck|pgbouncer)"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker daemon not running | Start Docker Desktop |
| Permission denied | Verify Docker access: `docker info` |
| Build failures | Use `make debug` for verbose output |
| Disk space | Use `make clean-all` |

### Debug Commands

```bash
# Verbose debugging
make debug

# Check prerequisites
make check

# Build with no cache
docker build --no-cache -f Dockerfile.pgbouncer -t pgbouncer:debug .

# Check layers
docker history pgbouncer:latest
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `make validate` | Complete validation pipeline |
| `make all` | Build and test everything |
| `make build` | Build both images |
| `make test` | Test both images |
| `make info` | Show image information |
| `make clean` | Remove local images |
| `make debug` | Build with verbose output |
| `make check` | Check prerequisites |
| `make push` | Push to ECR (requires AWS auth) |

## Key Principles

- ✅ **Simple and reliable** - standard Docker + Make workflow
- ✅ **No complex tooling** - just Docker + Make (built-in)
- ✅ **Easy debugging** - familiar Docker commands
- ✅ **CI/CD compatible** - same commands locally and in pipelines
