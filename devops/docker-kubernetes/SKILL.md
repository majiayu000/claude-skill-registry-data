---
name: Docker & Kubernetes
description: Dockerfile best practices, multi-stage builds, docker-compose patterns, and Kubernetes concepts
keywords:
  - docker
  - kubernetes
  - containers
  - orchestration
  - devops
  - deployment
---

# Docker & Kubernetes

## When to Use

**Perfect for:**
- Containerizing applications for consistent deployment
- Microservices architecture
- CI/CD pipelines with reproducible builds
- Local development environments matching production
- Scaling applications across multiple machines

**Not ideal for:**
- GUI desktop applications (limited container benefits)
- Real-time high-performance computing (overhead)
- Single-server monoliths (overkill unless scaling needs exist)

## Quick Reference

### Dockerfile Best Practices
```dockerfile
# Bad - large final image, hard to debug
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 python3-pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]

# Good - multi-stage, minimal final image, clear layers
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

# Use non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser app.py .

USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000
CMD ["python", "app.py"]
```

### Multi-Stage Build Pattern
```dockerfile
# Stage 1: Build
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine

RUN apk add --no-cache dumb-init
RUN addgroup -g 1000 app && adduser -u 1000 -G app -s /bin/sh -D app

WORKDIR /app

# Copy only runtime dependencies and built app
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --chown=app:app package.json .

USER app

EXPOSE 3000
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

### Docker Image Optimization
```dockerfile
# Layer caching - order matters (least to most frequently changed)
FROM python:3.11-slim

# Stable dependency installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code (changes frequently)
COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
```

### Environment Configuration
```dockerfile
# Build arguments (build-time)
FROM python:3.11-slim

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=1.0.0

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version=$VERSION

# Runtime environment variables
ENV APP_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

EXPOSE $PORT
```

### Docker Compose Pattern
```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: myapp_web
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/myapp
      REDIS_URL: redis://cache:6379/0
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - ./app:/app  # Development only
    networks:
      - app_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  db:
    image: postgres:15-alpine
    container_name: myapp_db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    container_name: myapp_cache
    ports:
      - "6379:6379"
    volumes:
      - cache_data:/data
    networks:
      - app_network
    restart: unless-stopped
    command: redis-server --appendonly yes

volumes:
  db_data:
  cache_data:

networks:
  app_network:
    driver: bridge
```

### Security Best Practices
```dockerfile
# Use official base images
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Minimize layer count and image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Use specific image tags (never "latest")
FROM postgres:15.1-alpine

# Set read-only filesystem where possible
RUN chmod -R 755 /app

# Use secrets management for sensitive data (Docker Swarm/Kubernetes)
# Never hardcode secrets in Dockerfile
```

## Deep Dive

### Health Checks
```dockerfile
# HTTP-based health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command-based health check
HEALTHCHECK --interval=30s --timeout=10s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Shell command health check
HEALTHCHECK --interval=10s --timeout=5s \
    CMD ["CMD-SHELL", "pg_isready -U postgres || exit 1"]
```

### Docker Networking
```yaml
# Bridge network (default, containers can communicate by name)
version: '3.8'

services:
  web:
    image: myapp
    networks:
      - backend

  db:
    image: postgres
    networks:
      - backend

networks:
  backend:
    driver: bridge

# Host network (container shares host's network - performance critical)
services:
  high_perf:
    image: myapp
    network_mode: host  # Performance, but less isolated

# Overlay network (for Swarm mode)
networks:
  distributed:
    driver: overlay
    driver_opts:
      com.docker.network.driver.overlay.vxlan_list: "4789"
```

### Volume Management
```yaml
# Named volumes (managed by Docker, persistent)
services:
  db:
    image: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    driver: local

# Bind mounts (host directory mounted into container)
services:
  web:
    image: myapp
    volumes:
      - /host/path:/container/path:ro  # Read-only

# Tmpfs volumes (in-memory, lost on container restart)
services:
  app:
    image: myapp
    tmpfs:
      - /tmp
      - /run
```

### Container Logging
```yaml
services:
  app:
    image: myapp
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service=myapp,env=production"

  # Alternative: Log to syslog
  app_syslog:
    image: myapp
    logging:
      driver: syslog
      options:
        syslog-address: "udp://localhost:514"
        syslog-facility: "daemon"

  # Alternative: Log to ELK stack
  app_elk:
    image: myapp
    logging:
      driver: splunk
      options:
        splunk-token: ${SPLUNK_TOKEN}
        splunk-url: https://localhost:8088
```

### Kubernetes Basics

#### Pod (Smallest Kubernetes Unit)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: web
    image: myapp:1.0.0
    ports:
    - containerPort: 8000
    env:
    - name: APP_ENV
      value: "production"
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 10
      periodSeconds: 30
    readinessProbe:
      httpGet:
        path: /ready
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 10
```

#### Deployment (Stateless Application)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: web
        image: myapp:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname
```

#### Service (Network Access)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer  # or ClusterIP, NodePort
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8000
    protocol: TCP
  sessionAffinity: ClientIP
```

#### ConfigMap & Secret
```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  config.json: |
    {
      "timeout": 30,
      "retries": 3
    }

---
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAZGI6NTQzMi9teWFwcA==  # base64 encoded
```

## Anti-Patterns

### DON'T: Use "latest" Tag
```dockerfile
# Bad - unpredictable, breaks reproducibility
FROM node:latest
FROM python:latest

# Good - specific version
FROM node:18.17.0-alpine
FROM python:3.11.5-slim
```

### DON'T: Run as Root
```dockerfile
# Bad - security vulnerability
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y myapp
CMD ["myapp"]

# Good - use non-root user
FROM ubuntu:22.04
RUN useradd -m -u 1000 appuser
USER appuser
CMD ["myapp"]
```

### DON'T: Layer Multiple Commands
```dockerfile
# Bad - creates extra layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get clean

# Good - single RUN with && chains
RUN apt-get update && \
    apt-get install -y curl vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### DON'T: Copy Everything
```dockerfile
# Bad - includes unnecessary files
COPY . /app

# Good - be selective
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY config/ ./config/
```

### DON'T: Ignore Resource Limits
```yaml
# Bad - no resource limits, can consume entire node
spec:
  containers:
  - name: app
    image: myapp

# Good - set requests and limits
spec:
  containers:
  - name: app
    image: myapp
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

### DON'T: Skip Health Checks
```dockerfile
# Bad - no way to detect failing app
FROM mybase
COPY app /app
CMD ["app"]

# Good - include health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["app"]
```

### DON'T: Hardcode Configuration
```dockerfile
# Bad - configuration baked into image
ENV DATABASE_URL=postgresql://prod-db:5432/myapp
ENV API_KEY=sk_live_xxx

# Good - use environment variables and secrets
# Leave empty or use defaults for development
ENV DATABASE_URL=postgresql://localhost:5432/myapp
# Use Kubernetes Secrets or docker-compose .env file
```

### DON'T: Combine Multiple Applications
```dockerfile
# Bad - violates single responsibility
FROM ubuntu
RUN apt-get install -y nginx python flask
COPY . /app
CMD ["supervisord"]  # Running multiple services

# Good - one container per concern
FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
---
FROM python:3.11
COPY app.py /app/
CMD ["python", "app.py"]
```
