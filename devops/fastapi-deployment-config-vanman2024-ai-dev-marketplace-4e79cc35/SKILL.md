---
name: fastapi-deployment-config
description: Configure multi-platform deployment for FastAPI applications including Docker containerization, Railway, DigitalOcean App Platform, and AWS deployment. Use when deploying FastAPI apps, setting up production environments, containerizing applications, configuring cloud platforms, implementing health checks, managing environment variables, setting up reverse proxies, or when user mentions Docker, Railway, DigitalOcean, AWS, deployment configuration, production setup, or container orchestration.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# FastAPI Deployment Configuration

**Purpose:** Autonomously configure and deploy FastAPI applications across multiple platforms with production-ready configurations.

**Activation Triggers:**
- Deployment setup requests
- Docker containerization needs
- Platform-specific configuration (Railway, DigitalOcean, AWS)
- Health check implementation
- Environment variable management
- Reverse proxy setup (Nginx)
- Production optimization
- Multi-stage build configurations

**Key Resources:**
- `scripts/build-docker.sh` - Multi-stage Docker build automation
- `scripts/validate-deployment.sh` - Pre-deployment validation checks
- `scripts/health-check.sh` - Application health verification
- `templates/` - Production-ready Dockerfile, docker-compose.yml, platform configs
- `examples/` - Platform-specific deployment guides (Railway, DigitalOcean, AWS)

## Deployment Workflow

### 1. Pre-Deployment Validation

Run comprehensive checks before deployment:

```bash
./scripts/validate-deployment.sh

# Validates:
# - Python dependencies (requirements.txt)
# - Environment variables (.env.example)
# - FastAPI application structure
# - Database migrations (if using Alembic)
# - Static file configuration
# - CORS settings
# - Security configurations
```

**Common issues detected:**
- Missing required dependencies
- Unset environment variables
- Database connection configuration
- Missing CORS origins
- Insecure secret key defaults

### 2. Docker Containerization

Build optimized Docker image using multi-stage builds:

```bash
./scripts/build-docker.sh [--platform=linux/amd64] [--tag=myapp:latest]

# Features:
# - Multi-stage build (builder + runtime)
# - Layer caching optimization
# - Non-root user for security
# - Health check integration
# - Minimal production image size
```

**Dockerfile template** (`templates/Dockerfile`):
- Python 3.11+ slim base image
- Virtual environment isolation
- Production dependency separation
- Gunicorn/Uvicorn workers
- Security best practices

### 3. Platform-Specific Configuration

#### Railway Deployment

```bash
# Railway uses railway.json for configuration
# See: examples/railway_setup.md

# Key features:
# - Automatic HTTPS
# - Environment variable management
# - Auto-deploy from Git
# - Database provisioning
# - Custom domains
```

**Configuration:** `templates/railway.json`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check endpoint: `/health`

#### DigitalOcean App Platform

```bash
# DigitalOcean uses app.yaml for configuration
# See: examples/digitalocean_setup.md

# Key features:
# - Container registry integration
# - Managed databases
# - Auto-scaling
# - CDN integration
# - Monitoring & alerts
```

**Configuration:** `templates/digitalocean-app.yaml`
- Dockerfile-based deployment
- Health check configuration
- Environment variable secrets
- Database component linking

#### AWS Deployment Options

**ECS (Elastic Container Service):**
```bash
# See: examples/aws_setup.md#ecs-deployment

# Features:
# - Fargate serverless containers
# - Load balancer integration
# - Auto-scaling policies
# - CloudWatch logging
# - VPC networking
```

**App Runner:**
```bash
# Simplified container deployment
# Automatic scaling and load balancing
# See: examples/aws_setup.md#app-runner
```

### 4. Health Check Implementation

Implement comprehensive health checks:

```bash
./scripts/health-check.sh <endpoint-url>

# Checks:
# - HTTP endpoint availability (GET /health)
# - Database connectivity
# - Redis/cache availability
# - External API dependencies
# - Response time monitoring
```

**Health endpoint template:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": check_db(),
        "cache": check_redis()
    }
```

### 5. Environment Variable Management

**Required environment variables:**
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Application secret key
- `CORS_ORIGINS` - Allowed CORS origins
- `ENVIRONMENT` - prod/staging/dev
- `LOG_LEVEL` - Logging verbosity

**Templates provided:**
- `.env.example` - Development template
- `.env.production.example` - Production template

### 6. Reverse Proxy Configuration (Nginx)

For self-hosted deployments:

```bash
# Nginx configuration: templates/nginx.conf

# Features:
# - SSL/TLS termination
# - Rate limiting
# - Request buffering
# - Gzip compression
# - Static file serving
# - WebSocket support
# - Security headers
```

**Configuration highlights:**
- Proxy to Uvicorn on port 8000
- Client max body size: 10M
- Connection timeout: 60s
- Rate limiting: 100 req/min per IP

## Docker Compose Orchestration

For local development and testing:

```bash
docker-compose up -d

# Services configured:
# - FastAPI application
# - PostgreSQL database
# - Redis cache
# - Nginx reverse proxy
```

**Template:** `templates/docker-compose.yml`
- Volume mounts for development
- Network isolation
- Health check dependencies
- Environment variable injection

## Production Optimization

### Multi-Stage Docker Build

**Stage 1: Builder**
- Install all dependencies
- Compile Python packages
- Create virtual environment

**Stage 2: Runtime**
- Copy only runtime dependencies
- Non-root user execution
- Minimal attack surface
- Optimized layer caching

### Worker Configuration

**Gunicorn + Uvicorn:**
```bash
# Recommended workers: (2 x CPU cores) + 1
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Database Connection Pooling

```python
# SQLAlchemy configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

## Security Configurations

**Implemented in templates:**
- ✅ Non-root Docker user
- ✅ Read-only root filesystem (where possible)
- ✅ Security headers (HSTS, X-Frame-Options, CSP)
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ Secret management via environment variables
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation (Pydantic models)

## Platform Comparison

| Feature | Railway | DigitalOcean | AWS ECS | AWS App Runner |
|---------|---------|--------------|---------|----------------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cost (Low Traffic)** | $5-10/mo | $12/mo | $20-30/mo | $15-25/mo |
| **Auto-Scaling** | Limited | Yes | Yes | Yes |
| **Database Included** | Yes (add-on) | Yes (managed) | Separate (RDS) | Separate (RDS) |
| **Custom Domains** | Yes | Yes | Yes | Yes |
| **CI/CD** | Git-based | Container registry | CodePipeline | Git/ECR |

## Common Deployment Scenarios

### Scenario 1: Simple API (No Database)
**Recommended:** Railway or AWS App Runner
- Minimal configuration
- Fast deployment
- Auto-scaling included

### Scenario 2: API + PostgreSQL
**Recommended:** Railway or DigitalOcean
- Integrated database provisioning
- Automatic backups
- Connection pooling

### Scenario 3: Microservices Architecture
**Recommended:** AWS ECS or DigitalOcean App Platform
- Service mesh capabilities
- Container orchestration
- Advanced networking

### Scenario 4: High-Traffic Production
**Recommended:** AWS ECS with RDS
- Advanced monitoring
- Multi-AZ deployment
- Enterprise support

## Troubleshooting

### Build Failures
```bash
# Check Docker build logs
./scripts/build-docker.sh --verbose

# Common fixes:
# - Update requirements.txt versions
# - Check Python version compatibility
# - Verify base image availability
```

### Health Check Failures
```bash
# Debug health endpoint
./scripts/health-check.sh http://localhost:8000/health --debug

# Common issues:
# - Database connection timeout
# - Missing environment variables
# - Port binding conflicts
```

### Performance Issues
```bash
# Monitor worker utilization
# Increase Gunicorn workers
# Enable connection pooling
# Implement caching (Redis)
# Optimize database queries
```

## Resources

**Scripts:** All scripts are executable and include help documentation (`--help`)

**Templates:** Production-ready configurations in `templates/` directory

**Examples:** Detailed platform-specific guides in `examples/` directory
- `railway_setup.md` - Complete Railway deployment walkthrough
- `digitalocean_setup.md` - DigitalOcean App Platform setup
- `aws_setup.md` - AWS ECS and App Runner deployment

---

**Supported Platforms:** Railway, DigitalOcean App Platform, AWS ECS, AWS App Runner, Self-hosted (Docker + Nginx)

**FastAPI Version:** 0.104.0+
**Python Version:** 3.11+
**Docker Version:** 20.10+
