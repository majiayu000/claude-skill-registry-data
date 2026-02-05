---
name: docker-deploy
description: Create Docker configurations and deployment workflows for Scrapy projects when containerizing spiders or deploying to production. Generates Dockerfiles, docker-compose setups, and orchestration configurations.
allowed-tools: Read, Write, Grep
---

You are a Docker and deployment expert for Scrapy projects. You create production-ready containerization configurations with proper resource management, monitoring, and scalability.

## Docker Architecture for Scrapy

### Single Spider Container
```
┌─────────────────────────────────┐
│   Scrapy Spider Container       │
│                                 │
│  ┌──────────────────────────┐  │
│  │  Spider Process          │  │
│  └──────────────────────────┘  │
│                                 │
│  ┌──────────────────────────┐  │
│  │  Output Volume           │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
```

### Distributed Scraping Architecture
```
┌─────────────────────────────────┐
│    Scrapy Cluster               │
│                                 │
│  ┌───────────┐  ┌───────────┐  │
│  │ Spider 1  │  │ Spider 2  │  │
│  └───────────┘  └───────────┘  │
│                                 │
│  ┌─────────────────────────┐   │
│  │   Redis (Queue)         │   │
│  └─────────────────────────┘   │
│                                 │
│  ┌─────────────────────────┐   │
│  │   PostgreSQL (Storage)  │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

## Docker Configuration Files

### 1. Basic Dockerfile

**Purpose**: Single spider containerization

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs

# Set environment variables
ENV SCRAPY_SETTINGS_MODULE=myproject.settings
ENV PYTHONUNBUFFERED=1

# Run spider
CMD ["scrapy", "crawl", "myspider"]
```

### 2. Multi-stage Dockerfile (Optimized)

**Purpose**: Smaller production images

```dockerfile
# Multi-stage Dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libxml2 \
    libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p /app/data /app/logs

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN useradd -m -u 1000 scrapy && \
    chown -R scrapy:scrapy /app

USER scrapy

CMD ["scrapy", "crawl", "myspider"]
```

### 3. Playwright-enabled Dockerfile

**Purpose**: Spiders requiring browser automation

```dockerfile
# Dockerfile.playwright
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Copy project
COPY . .

# Create directories
RUN mkdir -p /app/data /app/logs

ENV SCRAPY_SETTINGS_MODULE=myproject.settings
ENV PYTHONUNBUFFERED=1

# Run with xvfb for headless mode
CMD ["scrapy", "crawl", "playwright_spider"]
```

### 4. Docker Compose - Single Spider

**Purpose**: Simple spider with volume mounts

```yaml
# docker-compose.yml
version: '3.8'

services:
  scrapy:
    build: .
    container_name: scrapy-spider
    environment:
      - SCRAPY_SETTINGS_MODULE=myproject.settings
      - LOG_LEVEL=INFO
    volumes:
      # Mount data directory
      - ./data:/app/data
      # Mount logs directory
      - ./logs:/app/logs
      # Mount source code for development
      - ./myproject:/app/myproject
    command: scrapy crawl myspider
    restart: unless-stopped
    networks:
      - scrapy-network

networks:
  scrapy-network:
    driver: bridge
```

### 5. Docker Compose - Full Stack

**Purpose**: Spider with database and Redis

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: scrapy-postgres
    environment:
      POSTGRES_DB: scrapy_db
      POSTGRES_USER: scrapy
      POSTGRES_PASSWORD: ${DB_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - scrapy-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U scrapy"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis for caching and queuing
  redis:
    image: redis:7-alpine
    container_name: scrapy-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - scrapy-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Scrapy Spider
  scrapy:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: scrapy-spider
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://scrapy:${DB_PASSWORD:-changeme}@postgres:5432/scrapy_db
      - REDIS_URL=redis://redis:6379/0
      - LOG_LEVEL=INFO
      - CONCURRENT_REQUESTS=16
      - DOWNLOAD_DELAY=1
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./myproject:/app/myproject
    command: scrapy crawl myspider
    restart: unless-stopped
    networks:
      - scrapy-network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 512M

  # ScrapyD - Spider Management (optional)
  scrapyd:
    build:
      context: .
      dockerfile: Dockerfile.scrapyd
    container_name: scrapy-scrapyd
    ports:
      - "6800:6800"
    volumes:
      - ./data:/app/data
      - scrapyd_eggs:/app/eggs
    networks:
      - scrapy-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  scrapyd_eggs:

networks:
  scrapy-network:
    driver: bridge
```

### 6. Docker Compose - Distributed Scraping

**Purpose**: Multiple spiders with load balancing

```yaml
# docker-compose.distributed.yml
version: '3.8'

services:
  # Shared Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: scrapy_db
      POSTGRES_USER: scrapy
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - scrapy-network

  # Shared Redis
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - scrapy-network

  # Spider 1 - Product Scraper
  spider-products:
    build: .
    environment:
      - DATABASE_URL=postgresql://scrapy:${DB_PASSWORD}@postgres:5432/scrapy_db
      - REDIS_URL=redis://redis:6379/0
      - SPIDER_NAME=product_spider
    volumes:
      - ./data/products:/app/data
      - ./logs:/app/logs
    command: scrapy crawl product_spider
    depends_on:
      - postgres
      - redis
    networks:
      - scrapy-network
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G

  # Spider 2 - Review Scraper
  spider-reviews:
    build: .
    environment:
      - DATABASE_URL=postgresql://scrapy:${DB_PASSWORD}@postgres:5432/scrapy_db
      - REDIS_URL=redis://redis:6379/0
      - SPIDER_NAME=review_spider
    volumes:
      - ./data/reviews:/app/data
      - ./logs:/app/logs
    command: scrapy crawl review_spider
    depends_on:
      - postgres
      - redis
    networks:
      - scrapy-network
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G

  # Monitoring - Prometheus
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    ports:
      - "9090:9090"
    networks:
      - scrapy-network

  # Monitoring - Grafana
  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    networks:
      - scrapy-network

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  scrapy-network:
    driver: bridge
```

## ScrapyD Deployment

### Dockerfile.scrapyd

```dockerfile
# Dockerfile.scrapyd
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install ScrapyD
RUN pip install scrapyd scrapyd-client

# Copy ScrapyD configuration
COPY scrapyd.conf /etc/scrapyd/scrapyd.conf

# Create directories
RUN mkdir -p /app/eggs /app/logs /app/items

# Expose ScrapyD port
EXPOSE 6800

CMD ["scrapyd"]
```

### scrapyd.conf

```ini
[scrapyd]
eggs_dir    = /app/eggs
logs_dir    = /app/logs
items_dir   = /app/items
dbs_dir     = /app/dbs

http_port   = 6800
bind_address = 0.0.0.0

max_proc    = 4
max_proc_per_cpu = 2

poll_interval = 5.0

[services]
schedule.json = scrapyd.webservice.Schedule
cancel.json   = scrapyd.webservice.Cancel
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
listjobs.json     = scrapyd.webservice.ListJobs
```

## Deployment Scripts

### build-and-deploy.sh

```bash
#!/bin/bash
# Build and deploy Scrapy project

set -e

echo "Building Docker image..."
docker build -t scrapy-spider:latest .

echo "Stopping existing containers..."
docker-compose down

echo "Starting services..."
docker-compose up -d

echo "Waiting for services to be healthy..."
sleep 10

echo "Checking container status..."
docker-compose ps

echo "Deployment complete!"
echo "View logs: docker-compose logs -f scrapy"
```

### deploy-scrapyd.sh

```bash
#!/bin/bash
# Deploy to ScrapyD

set -e

PROJECT_NAME="myproject"
SCRAPYD_URL="http://localhost:6800"

echo "Building egg file..."
python setup.py bdist_egg

echo "Deploying to ScrapyD..."
scrapyd-deploy default -p $PROJECT_NAME

echo "Deployment complete!"
echo "Schedule spider: curl $SCRAPYD_URL/schedule.json -d project=$PROJECT_NAME -d spider=myspider"
```

### run-spider.sh

```bash
#!/bin/bash
# Run spider in Docker with arguments

SPIDER_NAME=$1
SPIDER_ARGS="${@:2}"

if [ -z "$SPIDER_NAME" ]; then
    echo "Usage: ./run-spider.sh <spider_name> [spider_args]"
    exit 1
fi

echo "Running spider: $SPIDER_NAME"
echo "Arguments: $SPIDER_ARGS"

docker-compose run --rm scrapy scrapy crawl $SPIDER_NAME $SPIDER_ARGS
```

## Environment Configuration

### .env.example

```bash
# Database
DB_PASSWORD=your_secure_password
DATABASE_URL=postgresql://scrapy:password@postgres:5432/scrapy_db

# Redis
REDIS_URL=redis://redis:6379/0

# Scrapy Settings
LOG_LEVEL=INFO
CONCURRENT_REQUESTS=16
DOWNLOAD_DELAY=1
AUTOTHROTTLE_ENABLED=True

# Monitoring
GRAFANA_PASSWORD=admin

# ScrapyD
SCRAPYD_URL=http://scrapyd:6800
```

## Kubernetes Deployment (Advanced)

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scrapy-spider
  labels:
    app: scrapy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: scrapy
  template:
    metadata:
      labels:
        app: scrapy
    spec:
      containers:
      - name: scrapy
        image: scrapy-spider:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: scrapy-secrets
              key: database-url
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: scrapy-data-pvc
      - name: logs
        persistentVolumeClaim:
          claimName: scrapy-logs-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: scrapy-service
spec:
  selector:
    app: scrapy
  ports:
  - protocol: TCP
    port: 6800
    targetPort: 6800
```

### cronjob.yaml

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scrapy-daily-crawl
spec:
  schedule: "0 2 * * *"  # Run at 2 AM daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scrapy
            image: scrapy-spider:latest
            command:
            - scrapy
            - crawl
            - myspider
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: scrapy-secrets
                  key: database-url
          restartPolicy: OnFailure
```

## Production Best Practices

### 1. Resource Limits

```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### 2. Health Checks

```dockerfile
# In Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import scrapy; print('healthy')" || exit 1
```

### 3. Logging Configuration

```yaml
# In docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 4. Security Hardening

```dockerfile
# Run as non-root user
RUN useradd -m -u 1000 scrapy && \
    chown -R scrapy:scrapy /app
USER scrapy

# Don't include secrets in image
# Use environment variables or Docker secrets
```

## Monitoring and Alerts

### prometheus.yml

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'scrapy'
    static_configs:
      - targets: ['scrapy:6800']
```

## When to Use This Skill

Use this skill when:
- Containerizing Scrapy spiders
- Setting up production deployments
- Creating distributed scraping systems
- Implementing CI/CD pipelines
- Scaling spider operations
- Deploying to cloud platforms

## Integration with Commands

**Commands**:
- `/dockerize` - Generate Docker configuration
- `/deploy` - Deploy to production
- `/scale <replicas>` - Scale spider instances

This skill ensures production-ready containerization with proper resource management, monitoring, and scalability.
