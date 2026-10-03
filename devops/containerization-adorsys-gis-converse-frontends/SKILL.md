---
name: containerization
description: Builds secure, minimal, and reproducible container images with proper health checks and runtime settings.
---

# Containerization Skill

## Objectives

- Minimal, secure images (non-root, least privilege)
- Reproducible multi-stage builds with caching
- Health checks and graceful shutdown

## Checklist

1. Use multi-stage builds; cache dependency layers
2. Run as non-root; drop capabilities; read-only filesystem if possible
3. Do not bake secrets into images; use env/secret mounts
4. Add `HEALTHCHECK` and proper `CMD`/`ENTRYPOINT`
5. Pin base images by digest or version; verify checksums for downloads
6. Scan images in CI; fail on critical CVEs; maintain SBOM

## Common Tasks

- Convert a Dockerfile to multi-stage with build cache
- Replace root user with unprivileged user and fix permissions
- Add healthcheck compatible with orchestration platform

## Output

- Proposed Dockerfile with annotations
- Security notes (capabilities, file perms, secret handling)
- Scan summary and remediation suggestions
