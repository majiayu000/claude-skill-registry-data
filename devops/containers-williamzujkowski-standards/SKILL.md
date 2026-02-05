---
skill_id: cloud-native/containers
version: 1.0.0
category: cloud-native
complexity: intermediate
prerequisites:
- coding-standards/shell
estimated_time: 4-6 hours
standards_alignment:
- CN:container
- SEC:secrets
- DOP:ci-cd
token_cost:
  level_1: ~150
  level_2: ~2000
  level_3: 0 (filesystem)
name: containers
description: 'Core Principles:'
---


# Containers

## Level 1: Quick Start (5 min)

**Core Principles**:

- Immutable infrastructure - containers are disposable, not pets
- Single responsibility - one process per container
- Minimal base images - reduce attack surface and size

**Quick Reference**:

```dockerfile
FROM alpine:3.18
WORKDIR /app
COPY --chown=nobody:nobody . .
USER nobody
EXPOSE 8080
CMD ["./app"]
```

**Essential Checklist**:

- [ ] Use official minimal base images (alpine, distroless)
- [ ] Run containers as non-root user
- [ ] Pin specific image versions (no :latest)
- [ ] Scan images for vulnerabilities
- [ ] Set resource limits (CPU, memory)

**Common Pitfalls**: See [Common Pitfalls](#common-pitfalls)

## Level 2: Implementation (30 min)

### Multi-Stage Builds

Reduce final image size and eliminate build dependencies:

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /build
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o app

# Runtime stage
FROM gcr.io/distroless/static-debian11
COPY --from=builder /build/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

### Image Optimization

**Layer Caching**:

- Order Dockerfile commands from least to most frequently changing
- Copy dependency manifests before source code
- Use .dockerignore to exclude unnecessary files

**Size Reduction**:

- Use distroless or alpine base images
- Clean package manager caches in same RUN command
- Combine commands to reduce layers

```dockerfile
RUN apk add --no-cache ca-certificates \
    && rm -rf /var/cache/apk/*
```

### Security Best Practices

**Non-Root Execution**:

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

**Read-Only Filesystem**:

```dockerfile
FROM alpine:3.18
RUN mkdir -p /tmp /app && chown -R nobody:nobody /tmp /app
USER nobody
WORKDIR /app
# Mount tmpfs for writable dirs
```

**Vulnerability Scanning**:

```bash
# Trivy scan
trivy image --severity HIGH,CRITICAL myapp:latest

# Snyk scan
snyk container test myapp:latest
```

### Container Runtime Configuration

**Resource Limits**:

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M
```

**Health Checks**:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
```

**Integration Points**: See [Integration Points](#integration-points)

## Level 3: Mastery

**Advanced Topics**:

- See `docs/cloud-native/containers/advanced-optimization.md`
- See `docs/cloud-native/containers/security-hardening.md`

**Resources**:

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [OCI Image Specification](https://github.com/opencontainers/image-spec)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

**Templates**:

- `templates/cloud-native/containers/dockerfile-go.template`
- `templates/cloud-native/containers/dockerfile-python.template`
- `templates/cloud-native/containers/dockerfile-node.template`

**Scripts**:

- `scripts/cloud-native/containers/build-optimized.sh`
- `scripts/cloud-native/containers/security-scan.sh`
- `scripts/cloud-native/containers/multi-arch-build.sh`

## Examples

### Basic Web Application

```dockerfile
FROM node:18-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci --only=production
COPY --chown=node:node . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

### Production-Ready Python Service

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir poetry==1.6.1
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd -m -u 1000 appuser
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### CI/CD Integration

```yaml
# .gitlab-ci.yml
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker build --target production -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Integration Points

### Upstream Dependencies

- **Base Images**: Official Docker Hub, Red Hat Quay, Google GCR
- **Build Tools**: Docker BuildKit, Buildah, Kaniko
- **Security Scanners**: Trivy, Snyk, Clair

### Downstream Consumers

- **Container Orchestrators**: Kubernetes, Docker Swarm, Nomad
- **CI/CD Pipelines**: GitLab CI, GitHub Actions, Jenkins
- **Image Registries**: Docker Hub, Harbor, ECR, GCR, ACR

### Related Skills

- [Kubernetes](../kubernetes/SKILL.md)
- [Infrastructure as Code](../../devops/infrastructure-as-code/SKILL.md)
- [Secrets Management](../../security/secrets-management/SKILL.md)
- [CI/CD](../../devops/ci-cd/SKILL.md)

## Common Pitfalls

### Pitfall 1: Running as Root User

**Problem**: Containers running as root pose security risks if compromised
**Solution**: Always create and use a non-root user in Dockerfile
**Prevention**: Add USER directive and scan with hadolint or dockerfile-lint

### Pitfall 2: Using :latest Tag

**Problem**: Non-deterministic builds, inconsistent deployments
**Solution**: Pin specific version tags (e.g., `alpine:3.18`, `node:18.17-alpine`)
**Prevention**: CI/CD pipeline rules to reject :latest tags

### Pitfall 3: Large Image Sizes

**Problem**: Slow deployments, increased storage costs, larger attack surface
**Solution**: Use multi-stage builds, minimal base images, .dockerignore
**Prevention**: Set image size limits in CI/CD (e.g., < 100MB for services)

### Pitfall 4: Secrets in Images

**Problem**: Hardcoded secrets accessible in image layers
**Solution**: Use build secrets, environment variables, or secret management tools
**Prevention**: Scan images for secrets (gitleaks, trufflehog) in CI pipeline

### Pitfall 5: No Health Checks

**Problem**: Orchestrators can't detect unhealthy containers
**Solution**: Implement HEALTHCHECK in Dockerfile or orchestrator config
**Prevention**: Make health endpoints mandatory in service templates
