---
name: docker-container-standards
description: >-
  Standard Docker container rules for packaging services securely and with optimized builds.
  Covers HEALTHCHECK, non-root user, multi-stage builds, layer caching, and .dockerignore.
---

# Docker Container Standards

Best practices for containerized applications. Focus on security, size, speed, and reliability.

## Rules

### 1. Security First
- **Non-Root User:** Never run containers as root. Create a dedicated user (`appuser` / `node`) and switch to it using `USER`.
- **Minimal Base Images:** Use small, secure base images (e.g., `python:3.12-slim` or `node:20-alpine` / `distroless`).
- **No Secrets:** Never hardcode secrets in Dockerfiles. Use environment variables.

### 2. Reliability & Health
- **HEALTHCHECK:** Always define a `HEALTHCHECK` instruction using curl/wget or custom health probe.
- **Signal Handling:** Use `exec` form for `CMD` (e.g. `CMD ["python", "app.py"]` instead of shell form `CMD python app.py`) to pass signals (like `SIGTERM`) properly.

### 3. Build Performance (Layer Caching)
- **Separate Dependency Install:** Copy dependency manifests (`package.json`, `pyproject.toml`, `requirements.txt`) and install dependencies *before* copying application code.
- **Multi-Stage Builds:** Separate build dependencies from runtime environment to keep the final image as light as possible.
- **Dockerignore:** Exclude `__pycache__`, `node_modules`, `.git`, `.env`, and local caches in `.dockerignore`.

---

## Code Templates

### Python Slim Dockerfile Example
```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 2: Runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

# Set non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do instead |
|---------|--------------|
| `USER root` or not specifying `USER` | `RUN useradd appuser && USER appuser` |
| `CMD python app.py` (shell form) | `CMD ["python", "app.py"]` (exec form) |
| Missing `HEALTHCHECK` | Add explicit `HEALTHCHECK` statement |
| Copying code before dependency install | Copy lockfiles, run install, then copy source code |
| Including `.git` or `.env` in final image | Define `.dockerignore` containing sensitive/local files |
