---
name: docker
description: Docker containerization best practices — writing lean Dockerfiles, multi-stage builds, image security, and docker-compose patterns for local development.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# docker

Docker containerization best practices — writing lean Dockerfiles, multi-stage builds, image security, and docker-compose patterns for local development.

## Instructions

Apply these Docker practices when containerizing applications:

### Dockerfile Best Practices

**Use multi-stage builds** to keep production images small:
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Runtime
FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

**Layer caching** — order instructions from least to most frequently changing:
1. Base image
2. System dependencies (`apt-get`, `apk add`)
3. Dependency manifests (`package.json`, `requirements.txt`)
4. Install dependencies
5. Application source code

**Always pin base image versions:**
```dockerfile
# Bad
FROM node:latest
# Good
FROM node:20.11.1-alpine3.19
```

### Security Hardening

- **Run as non-root:** add `USER node` / `USER nobody` before `CMD`
- **Read-only filesystem:** mount volumes where writes are needed; use `--read-only` flag
- **No secrets in layers:** use build args only for non-sensitive values; use runtime secrets or env vars for sensitive data
- **Scan images:** run `docker scout cves <image>` or `trivy image <image>` before pushing
- **Minimise surface area:** use distroless or alpine base images; remove build tools in final stage

### .dockerignore

Always create a `.dockerignore` to exclude unnecessary files:
```
.git
.env*
node_modules
dist
*.log
*.md
coverage
.DS_Store
```

### docker-compose for Local Development

```yaml
services:
  app:
    build:
      context: .
      target: runtime
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules   # anonymous volume to prevent host override
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: appdb
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  db_data:
```

### Image Tagging Strategy

- `latest` – only for local dev, never push to production registry
- `<semver>` – e.g., `1.2.3` for releases
- `<git-sha>` – immutable tag for traceability in CI/CD
- `<branch>-<sha>` – e.g., `main-a1b2c3d` for staging

## Examples

```bash
# Build with a specific target
docker build --target runtime -t myapp:1.0.0 .

# Run a container with a read-only filesystem
docker run --read-only -p 3000:3000 myapp:1.0.0

# Scan for vulnerabilities
trivy image myapp:1.0.0

# Check image size and layers
docker history myapp:1.0.0

# Prune dangling images and stopped containers
docker system prune -f
```

## References

- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Trivy scanner](https://github.com/aquasecurity/trivy)
- [Distroless images](https://github.com/GoogleContainerTools/distroless)
