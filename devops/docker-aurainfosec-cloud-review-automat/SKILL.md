---
type: skill
name: docker
description: Docker container platform for building, running, securing, and deploying containers. Use when creating Dockerfiles, building images, orchestrating services with Compose, optimizing performance, securing containers, integrating with CI/CD, or troubleshooting runtime issues.
last_updated: "2026-02-18"
doc_source: https://docs.docker.com/
---

# Docker

Docker is a containerization platform that packages applications and their dependencies into portable, lightweight containers that run consistently across environments.

---

## Table of Contents

- [Core Concepts](#core-concepts)
- [Common Workflows](#common-workflows)
- [Dockerfile Reference](#dockerfile-reference)
- [Multi-Stage Builds](#multi-stage-builds)
- [Docker Compose](#docker-compose)
- [Networking & Volumes](#networking--volumes)
- [Security Hardening](#security-hardening)
- [CI/CD Integration](#cicd-integration)
- [Kubernetes Bridge Concepts](#kubernetes-bridge-concepts)
- [CLI Reference](#cli-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

# Core Concepts

| Concept | Description |
|----------|-------------|
| **Image** | Immutable template used to create containers |
| **Container** | Running instance of an image |
| **Dockerfile** | Build instructions for an image |
| **Layer** | Each instruction creates a cached filesystem layer |
| **Volume** | Persistent storage outside container lifecycle |
| **Network** | Enables container-to-container communication |
| **Registry** | Stores images (Docker Hub, ECR, GCR, GHCR) |

---

# Common Workflows

## Build an Image

```bash
docker build -t myapp:latest .
```

Specific Dockerfile:

```bash
docker build -f Dockerfile.prod -t myapp:prod .
```

---

## Run a Container

```bash
docker run -d -p 8080:80 --name myapp myapp:latest
```

With environment variables:

```bash
docker run -d \
  -e NODE_ENV=production \
  -e DB_HOST=database \
  -p 8080:3000 \
  myapp:latest
```

Interactive shell:

```bash
docker run -it myapp bash
```

---

## Manage Containers

```bash
docker ps
docker ps -a
docker logs myapp
docker exec -it myapp bash
docker stop myapp
docker rm myapp
```

---

## Push to Registry

```bash
docker login
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest
```

---

# Dockerfile Reference

## Basic Example

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

---

## Environment Variables

```dockerfile
ENV NODE_ENV=production
```

---

## Non-Root User

```dockerfile
RUN addgroup -S app && adduser -S app -G app
USER app
```

---

# Multi-Stage Builds

Reduces final image size.

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

Benefits:
- Smaller attack surface
- Reduced image size
- Production-only artifacts

---

# Docker Compose

For multi-container applications.

## docker-compose.yml

```yaml
version: "3.9"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

Run:

```bash
docker compose up -d
docker compose down
```

---

# Networking & Volumes

## Networks

```bash
docker network create mynetwork
docker run --network mynetwork myapp
```

Inspect:

```bash
docker network inspect mynetwork
```

---

## Volumes

Create:

```bash
docker volume create myvolume
```

Mount:

```bash
docker run -v myvolume:/data myapp
```

Bind mount:

```bash
docker run -v $(pwd)/data:/app/data myapp
```

---

# Security Hardening

## Image Security

- Pin image versions (`node:20.11-alpine`)
- Avoid `latest`
- Use minimal base images (Alpine, distroless)
- Remove build tools from production image

---

## Drop Privileges

```bash
docker run --user 1000:1000 myapp
```

---

## Read-Only Filesystem

```bash
docker run --read-only myapp
```

---

## Limit Resources

```bash
docker run --memory="512m" --cpus="1.0" myapp
```

---

## Scan Images

```bash
docker scan myapp
```

---

# CI/CD Integration

## Build in CI

```bash
docker build -t myapp:${GIT_SHA} .
```

Tag & push:

```bash
docker tag myapp:${GIT_SHA} registry/myapp:${GIT_SHA}
docker push registry/myapp:${GIT_SHA}
```

---

## Example GitHub Actions Snippet

```yaml
- name: Build image
  run: docker build -t myapp:${{ github.sha }} .

- name: Push image
  run: |
    docker tag myapp:${{ github.sha }} myrepo/myapp:${{ github.sha }}
    docker push myrepo/myapp:${{ github.sha }}
```

---

# Kubernetes Bridge Concepts

| Docker | Kubernetes Equivalent |
|--------|-----------------------|
| Container | Pod |
| docker run | kubectl apply |
| docker-compose | Helm / K8s manifests |
| Network | Service |
| Volume | PersistentVolume |

Image built via Docker is deployed to Kubernetes cluster via:

```bash
kubectl apply -f deployment.yaml
```

---

# CLI Reference

## Image Commands

| Command | Description |
|----------|-------------|
| docker build | Build image |
| docker images | List images |
| docker rmi | Remove image |
| docker pull | Pull image |
| docker push | Push image |

---

## Container Commands

| Command | Description |
|----------|-------------|
| docker run | Run container |
| docker start | Start container |
| docker stop | Stop container |
| docker rm | Remove container |
| docker logs | View logs |
| docker exec | Execute command |

---

## System Commands

| Command | Description |
|----------|-------------|
| docker system df | Disk usage |
| docker system prune | Remove unused data |
| docker inspect | Detailed JSON metadata |

---

# Best Practices

## Image Optimization

- Use multi-stage builds
- Use `.dockerignore`
- Copy dependency files first (cache leverage)
- Keep images under ~200MB if possible
- Minimize layers

---

## Performance

- Avoid large build context
- Use build cache properly
- Avoid unnecessary package installs
- Remove temporary files

---

## Reliability

- Add HEALTHCHECK:

```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:3000 || exit 1
```

- Use restart policies:

```bash
docker run --restart unless-stopped myapp
```

---

# Troubleshooting

## Container Exits Immediately

Check logs:

```bash
docker logs container_name
```

Common causes:
- Wrong CMD
- Crash on startup
- Missing env variable
- Port misconfiguration

---

## Port Not Accessible

Verify:

- App listening on 0.0.0.0
- Correct port mapping (`-p host:container`)
- Firewall not blocking port

---

## Disk Space Issues

Check:

```bash
docker system df
```

Cleanup:

```bash
docker system prune -a
```

---

## Permission Errors (Linux)

If volume mount fails:

```bash
sudo chown -R 1000:1000 ./data
```

Or match container UID.

---

# References

- https://docs.docker.com/
- https://docs.docker.com/engine/reference/commandline/cli/
- https://docs.docker.com/compose/
- https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

---

# End of Skill
