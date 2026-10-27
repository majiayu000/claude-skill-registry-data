---
name: docker-optimizer
description: "Multi-stage Docker builds, minimal non-root image packaging, layer caching optimization, and container security."
---

# Docker Container Optimization & Security Protocol

Author secure, lightweight, and fast-building container images for production services.

---

## 1. Multi-Stage Build Architecture

Separate build tooling from production runtime images:
```dockerfile
# Stage 1: Build & Compile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Minimal Production Image
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## 2. Layer Caching & Non-Root Execution

1. Copy dependency manifests and install dependencies BEFORE copying application source code to maximize layer cache hits.
2. Never run containers as root. Use non-root system users.
3. Leverage .dockerignore to exclude .git, node_modules, and local scratch files.
