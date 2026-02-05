---
name: docker-optimization
description: Optimize Docker images for Python applications including multi-stage builds (70%+ size reduction), security scanning with Trivy, layer caching, and distroless base images. Use when creating Dockerfiles, reducing image size, improving build performance, or scanning for vulnerabilities.
allowed-tools:
  - Read
  - Bash
---

# Docker Image Optimization for Python

## Quick Reference

| Optimization | Benefit | Complexity |
|-------------|---------|------------|
| Multi-stage builds | 70-90% size reduction | Low |
| Distroless base | Highest security (no shell) | Medium |
| Layer caching | Faster builds (90%+ cache hits) | Low |
| `.dockerignore` | Smaller context, faster uploads | Low |
| Security scanning | Vulnerability detection | Low |

**Typical Results**: 1.2GB → 300MB (75% reduction) with multi-stage slim builds

---

## 1. Multi-Stage Build Pattern (Primary Optimization)

**Concept**: Separate build stage (compilers, build tools) from runtime stage (only compiled artifacts).

**Benefits**: 70-90% size reduction, faster deployments, cleaner runtime

### Pattern

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**Result**: 1.2GB → 300MB (75% reduction)

---

## 2. Base Image Selection

| Base Image | Size | Use Case | Notes |
|-----------|------|----------|-------|
| `python:3.11-slim` | 45MB | **Start here** | General purpose, good compatibility |
| `python:3.11-alpine` | 15MB | Size-critical | C extension issues (musl vs glibc) |
| `gcr.io/distroless/python3` | 50MB | Production | No shell, highest security |

**Recommendation**: Use `python:3.11-slim` unless you have specific needs.

**Alpine warning**: Breaks packages with C extensions (numpy, scipy, pillow). Use only for pure Python apps.

---

## 3. Distroless Images (2025 Best Practice)

**What**: Minimal images with ONLY runtime dependencies. No shell, package manager, or utilities.

**Security**: Highest - no shell for attackers, fewer CVEs, meets strict compliance requirements.

**Trade-off**: Can't debug with `docker exec`. Use `--target builder` to debug.

### Pattern

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Distroless runtime
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH PYTHONUNBUFFERED=1
CMD ["app.py"]
```

**Debugging**:
```bash
# Debug build (has shell)
docker build --target builder -t myapp:debug .

# Production (no shell)
docker build -t myapp:prod .
```

---

## 4. Layer Caching Optimization

**Key Rule**: Order layers from least-changing to most-changing.

**Optimal order**:
1. System packages (rarely change)
2. `requirements.txt` (occasional changes)
3. Application code (frequent changes)

### Pattern

```dockerfile
FROM python:3.11-slim

# 1. System packages (cached unless Dockerfile changes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && rm -rf /var/lib/apt/lists/*

# 2. Python dependencies (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Application code (rebuilt on every code change)
COPY . .

CMD ["python", "app.py"]
```

**Impact**: Fixing typo in app.py: 5 minutes → 10 seconds (with good layer order)

---

## 5. Dependency Installation Best Practices

### Essential Flags

| Flag | Purpose | Savings |
|------|---------|---------|
| `--no-cache-dir` | Don't cache pip downloads | 100-200MB |
| `--user` | Install to user site-packages | Easier multi-stage COPY |
| `--no-install-recommends` | Skip suggested apt packages | 50-100MB |

### Pattern

```dockerfile
# Install system dependencies + clean cache in SAME command
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
```

**Critical**: Clean apt cache in SAME `RUN` command (separate commands = cache persists in earlier layer)

**Requirements.txt**: Pin exact versions (`flask==2.3.2`, not `flask>=2.3`)

---

## 6. Image Size Reduction Checklist

- [ ] Use multi-stage builds (exclude build tools)
- [ ] Use slim/alpine base images
- [ ] Add `.dockerignore` file
- [ ] Use `--no-cache-dir` with pip
- [ ] Clean apt cache in same RUN command
- [ ] Combine RUN commands to reduce layers

### .dockerignore Essential Patterns

```gitignore
.git/
__pycache__/
*.py[cod]
venv/
.venv/
.pytest_cache/
.coverage
.vscode/
.idea/
*.md
docs/
.github/
*.log
```

**Impact**: 500MB → 50MB build context (10x reduction)

### Size Progression

| Approach | Size | Reduction |
|----------|------|-----------|
| Basic single-stage | 1.2GB | Baseline |
| + slim base | 800MB | 33% |
| + multi-stage | 400MB | 67% |
| + .dockerignore | 350MB | 71% |
| + all optimizations | 280MB | 77% |

---

## 7. Security Scanning with Trivy

### Installation & Basic Usage

```bash
# Install (macOS)
brew install aquasecurity/trivy/trivy

# Scan image
trivy image python:3.11-slim
trivy image --severity HIGH,CRITICAL myapp:latest
```

### Fixing Vulnerabilities

1. **Update base image**: `FROM python:3.11.8-slim` (newer patch)
2. **Update dependencies**: `pip install --upgrade <package>`
3. **Rebuild and rescan**: `docker build . && trivy image myapp:latest`

### Best Practices

- Scan base images before using
- Fail CI/CD on CRITICAL vulnerabilities
- Scheduled scans of deployed images (weekly)
- Use distroless for fewer vulnerabilities

**See reference.md for CI/CD integration examples (GitHub Actions, GitLab CI).**

---

## 8. Build Performance Optimization

### Enable BuildKit

```bash
# Enable globally
export DOCKER_BUILDKIT=1
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc

# Enable per-build
DOCKER_BUILDKIT=1 docker build .
```

### Cache Mounts (BuildKit)

```dockerfile
# Reuse pip cache across builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Benefit**: 2 minute builds → 10 seconds after first build

### Build Performance Checklist

- [ ] Enable BuildKit (`DOCKER_BUILDKIT=1`)
- [ ] Use cache mounts for package managers
- [ ] Order layers for maximum cache hits
- [ ] Use `.dockerignore` to reduce context size

**Typical improvements**: 10 minute builds → 30 seconds (with warm cache)

---

## 9. Python-Specific Optimizations

### Essential Environment Variables

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
```

| Variable | Purpose |
|----------|---------|
| `PYTHONDONTWRITEBYTECODE=1` | Don't create `.pyc` files (smaller, faster) |
| `PYTHONUNBUFFERED=1` | Unbuffered output (better logging) |
| `PIP_NO_CACHE_DIR=1` | Don't cache pip (100-200MB savings) |

### Non-Root User (Security)

```dockerfile
# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser
WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .
```

**Why**: Containers as root = security risk if compromised

---

## 10. Health Checks

### Basic Pattern

```dockerfile
HEALTHCHECK --interval=30s \
            --timeout=3s \
            --start-period=5s \
            --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

### Common Patterns

| Use Case | Pattern |
|----------|---------|
| **Web apps** | `curl --fail http://localhost:8000/health \|\| exit 1` |
| **Non-web apps** | `pgrep -f "python app.py" \|\| exit 1` |
| **Data processing** | `test $(find /tmp/heartbeat -mmin -5) \|\| exit 1` |

**See reference.md for implementation details and app-specific patterns.**

---

## 11. Quick Pattern Reference

| Use Case | Pattern | Size |
|----------|---------|------|
| **Web API** | Multi-stage slim | ~300MB |
| **Data processing** | Multi-stage slim + volumes | ~350MB |
| **Production secure** | Distroless | ~250MB |
| **Size-critical** | Alpine (test thoroughly!) | ~150MB |

**See reference.md for complete Dockerfile examples.**

---

## 12. Anti-Patterns to Avoid

| Anti-Pattern | Problem | Impact |
|-------------|---------|--------|
| **Using `python:latest`** | Non-reproducible builds | Breaks when new Python releases |
| **Build deps in final stage** | Includes gcc, make, headers | 1.2GB vs 300MB images |
| **No .dockerignore** | Copies .git, venv, cache | 10x larger build context |
| **Running as root** | Security risk | Full host access if compromised |
| **Secrets in layers** | Leaked in history | Anyone with image can extract |
| **Poor layer order** | Cache breaks on code change | 5 min vs 10 sec rebuilds |
| **Separate cleanup commands** | Cache persists in earlier layers | 100MB+ wasted space |

---

## 13. Quick Reference Card

### Dockerfile Checklist

```dockerfile
# ✅ Multi-stage build
FROM python:3.11-slim as builder
# ... build stage ...

FROM python:3.11-slim
# ✅ Python env vars
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH

# ✅ Copy only dependencies first (cache-friendly)
COPY --from=builder /root/.local /root/.local

# ✅ Non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# ✅ Copy app last
COPY --chown=appuser:appuser . .

# ✅ Health check
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

# ✅ Explicit CMD
CMD ["python", "app.py"]
```

### Build Commands

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with tag
docker build -t myapp:latest .

# Build specific stage (debugging)
docker build --target builder -t myapp:debug .

# Scan for vulnerabilities
trivy image --severity HIGH,CRITICAL myapp:latest
```

---

## Additional Resources

**Documentation**:
- Docker multi-stage builds: https://docs.docker.com/build/building/multi-stage/
- BuildKit: https://docs.docker.com/build/buildkit/
- Distroless images: https://github.com/GoogleContainerTools/distroless
- Trivy security scanner: https://aquasecurity.github.io/trivy/

**Best Practices**:
- Docker best practices: https://docs.docker.com/develop/dev-best-practices/
- Python Docker guide: https://docs.python.org/3/using/docker.html

**Security**:
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- OWASP Docker Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html

---

**For comprehensive examples and advanced patterns:** See [reference.md](reference.md)

---

**Last Updated**: 2025-10-27
**Version**: 1.1
