---
name: dockerfile-review
description: Review Dockerfiles for best practices, security, and optimization. Use when the user says "review Dockerfile", "optimize image", "Dockerfile best practices", "reduce image size", or asks to audit a container build.
allowed-tools: Read, Glob, Grep
---

# Dockerfile Review

Audit Dockerfiles for security, efficiency, and best practices.

## Instructions

1. Read the Dockerfile
2. Check for issues in each category below
3. Report findings with severity (critical/warning/suggestion)
4. Provide specific fixes with corrected code

## Security checks

- MUST flag `USER root` without switching back
- MUST flag secrets in ENV, ARG, or COPY (API keys, passwords)
- MUST flag `apt-get install` without `--no-install-recommends`
- Flag missing `USER` directive (runs as root by default)
- Flag `COPY . .` (may include secrets, .git, etc.)
- Flag `:latest` tags (unpinned versions)
- Flag `curl | sh` patterns

## Optimization checks

- Multi-stage builds for compiled languages
- Layer ordering (least-changing first)
- Combined RUN statements to reduce layers
- Cache mounts for package managers: `--mount=type=cache`
- `.dockerignore` file exists and covers .git, node_modules, etc.
- `apt-get clean && rm -rf /var/lib/apt/lists/*` in same layer

## Best practices

```dockerfile
# Good: pinned, non-root, minimal
FROM python:3.11-slim@sha256:abc123...
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python", "app.py"]
```

## Output format

```
## Critical
- Line 5: Running as root without USER directive

## Warnings
- Line 12: Using :latest tag - pin to specific version

## Suggestions
- Line 8-10: Combine RUN statements to reduce layers
```

## Rules

- MUST read the Dockerfile before reviewing
- MUST categorize issues by severity
- Never approve Dockerfiles with hardcoded secrets
- Always check for corresponding .dockerignore
