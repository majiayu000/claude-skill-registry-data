---
name: Production Deployment
description: Expert guidance for deploying Agno AGI agents and AI applications to production using Docker, FastAPI, monitoring, CI/CD, and cloud platforms
version: 1.0.0
---

# Production Deployment for AI Agents

Complete guide for deploying Agno agents and AI applications to production environments.

## Project Structure

### Recommended Layout

```
project/
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── specialized.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── health.py
│   │   └── models/
│   │       ├── __init__.py
│   │       └── schemas.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── custom_tools.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── monitoring.py
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_api.py
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
├── scripts/
│   ├── build.sh
│   ├── deploy.sh
│   └── migrate.sh
├── .env.example
├── .dockerignore
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## FastAPI Production Application

### Main Application

```python
# src/api/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import logging
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.api.routes import chat, health
from src.utils.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting application...")
    # Startup: Load models, initialize agents
    yield
    # Shutdown: Cleanup resources
    logger.info("Shutting down application...")

app = FastAPI(
    title="AI Agent API",
    description="Production AI Agent Service",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.environment != "production" else None,
    redoc_url="/api/redoc" if settings.environment != "production" else None
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI Agent API",
        "version": "1.0.0",
        "status": "running"
    }
```

### Configuration Management

```python
# src/config/settings.py
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""

    # Environment
    environment: str = "development"
    debug: bool = False

    # API Keys
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    # Database
    database_url: str = "postgresql://localhost:5432/agno"
    db_pool_size: int = 20
    db_max_overflow: int = 40

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    allowed_origins: List[str] = ["*"]

    # Agent Settings
    default_model: str = "claude-3-7-sonnet-latest"
    max_tokens: int = 4096
    temperature: float = 0.7
    request_timeout: int = 30

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Monitoring
    sentry_dsn: Optional[str] = None
    enable_metrics: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()

settings = get_settings()
```

### API Routes

```python
# src/api/routes/chat.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from src.agents.base import create_agent
from src.api.models.schemas import ChatRequest, ChatResponse
from src.utils.monitoring import track_request

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse)
@track_request("chat_endpoint")
async def chat(request: ChatRequest):
    """Chat with AI agent"""
    try:
        # Create or get agent
        agent = create_agent(
            model=request.model or "claude-3-7-sonnet-latest",
            session_id=request.session_id
        )

        # Get response
        response = agent.run(
            request.message,
            stream=False
        )

        return ChatResponse(
            response=response.content,
            session_id=agent.session_id,
            model=request.model,
            tokens_used=response.metrics.get("tokens", 0)
        )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint"""
    from fastapi.responses import StreamingResponse

    async def generate():
        try:
            agent = create_agent(
                model=request.model or "claude-3-7-sonnet-latest",
                session_id=request.session_id
            )

            response = agent.run(request.message, stream=True)

            for chunk in response:
                if chunk.content:
                    yield f"data: {chunk.content}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Streaming error: {e}", exc_info=True)
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

```python
# src/api/routes/health.py
from fastapi import APIRouter, Response, status
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def health_check():
    """Basic health check"""
    return {"status": "healthy"}

@router.get("/ready")
async def readiness_check(response: Response):
    """Readiness check for K8s"""
    try:
        # Check database connection
        # Check Redis connection
        # Check model availability
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready", "error": str(e)}

@router.get("/live")
async def liveness_check():
    """Liveness check for K8s"""
    return {"status": "alive"}
```

### Data Models

```python
# src/api/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=10000)
    session_id: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0, le=2)
    max_tokens: Optional[int] = Field(None, ge=1, le=100000)

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    session_id: str
    model: str
    tokens_used: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## Docker Configuration

### Production Dockerfile

```dockerfile
# docker/Dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://agno:agno@db:5432/agno
      - REDIS_URL=redis://redis:6379/0
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - agno-network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  db:
    image: pgvector/pgvector:pg17
    environment:
      - POSTGRES_DB=agno
      - POSTGRES_USER=agno
      - POSTGRES_PASSWORD=agno
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agno"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - agno-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - agno-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - agno-network

volumes:
  postgres_data:
  redis_data:

networks:
  agno-network:
    driver: bridge
```

### Nginx Configuration

```nginx
# docker/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream api {
        least_conn;
        server api:8000 max_fails=3 fail_timeout=30s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name api.example.com;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Gzip compression
        gzip on;
        gzip_types text/plain application/json;

        location / {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        location /api/v1/chat/stream {
            proxy_pass http://api;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_buffering off;
            proxy_cache off;
        }
    }
}
```

## Kubernetes Deployment

### Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-api
  labels:
    app: ai-agent-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-agent-api
  template:
    metadata:
      labels:
        app: ai-agent-api
    spec:
      containers:
      - name: api
        image: your-registry/ai-agent-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-agent-secrets
              key: database-url
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-agent-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Service

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-agent-api
spec:
  selector:
    app: ai-agent-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Horizontal Pod Autoscaler

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-agent-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-agent-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Monitoring and Logging

### Structured Logging

```python
# src/utils/logging.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Setup structured JSON logging"""

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        timestamp=True
    )

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
```

### Prometheus Metrics

```python
# src/utils/monitoring.py
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Define metrics
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['endpoint', 'method', 'status']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'Request duration',
    ['endpoint']
)

active_requests = Gauge(
    'api_active_requests',
    'Active requests',
    ['endpoint']
)

token_usage = Counter(
    'ai_tokens_used_total',
    'Total tokens used',
    ['model', 'type']
)

def track_request(endpoint: str):
    """Decorator to track request metrics"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            active_requests.labels(endpoint=endpoint).inc()
            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                request_count.labels(
                    endpoint=endpoint,
                    method='POST',
                    status='200'
                ).inc()
                return result
            except Exception as e:
                request_count.labels(
                    endpoint=endpoint,
                    method='POST',
                    status='500'
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                request_duration.labels(endpoint=endpoint).observe(duration)
                active_requests.labels(endpoint=endpoint).dec()

        return wrapper
    return decorator
```

### Sentry Integration

```python
# src/utils/sentry.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from src.config.settings import settings

def init_sentry():
    """Initialize Sentry error tracking"""
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.environment,
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
            ]
        )
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=src tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/Dockerfile
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Kubernetes
        run: |
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig
          export KUBECONFIG=kubeconfig
          kubectl set image deployment/ai-agent-api \
            api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/ai-agent-api
```

## Best Practices

### 1. Security
```python
# API key rotation
# Rate limiting
# Input validation
# SQL injection prevention
# CORS configuration
# HTTPS only
```

### 2. Scalability
```python
# Horizontal pod autoscaling
# Database connection pooling
# Redis caching
# Async operations
# Load balancing
```

### 3. Reliability
```python
# Health checks
# Graceful shutdown
# Retry logic
# Circuit breakers
# Fallback responses
```

### 4. Observability
```python
# Structured logging
# Metrics collection
# Distributed tracing
# Error tracking
# Cost monitoring
```

### 5. Performance
```python
# Response caching
# Prompt caching
# Database query optimization
# Connection pooling
# Compression
```

## Environment Variables

```bash
# .env.example
ENVIRONMENT=production
DEBUG=false

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/agno
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40

# Redis
REDIS_URL=redis://localhost:6379/0

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
ALLOWED_ORIGINS=https://app.example.com

# Monitoring
SENTRY_DSN=https://...
ENABLE_METRICS=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Deployment Checklist

- [ ] Environment variables configured
- [ ] API keys secured
- [ ] Database migrations run
- [ ] Health checks working
- [ ] Monitoring configured
- [ ] Logging enabled
- [ ] Rate limiting set up
- [ ] CORS configured
- [ ] HTTPS enabled
- [ ] Backups configured
- [ ] Auto-scaling enabled
- [ ] CI/CD pipeline working
- [ ] Error tracking active
- [ ] Documentation updated
- [ ] Load testing completed

## Resources

- FastAPI: https://fastapi.tiangolo.com/
- Docker: https://docs.docker.com/
- Kubernetes: https://kubernetes.io/docs/
- Prometheus: https://prometheus.io/docs/
- Sentry: https://docs.sentry.io/
- Nginx: https://nginx.org/en/docs/
