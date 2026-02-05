---
name: docker-health
description: Docker health checks and troubleshooting. Use when building Docker images, running containers, or debugging deployment issues. Validates backend API and worker services.
---

# Docker Health Check Workflow

This skill helps with Docker-related development, testing, and deployment.

## When to use this skill

- Building Docker images for backend
- Running backend in containerized environment
- Debugging Docker deployment issues
- Validating Docker health before deployment
- Testing production-like environment locally

## Quick Commands

```bash
make docker-build   # Build backend Docker image
make docker-test    # Run comprehensive Docker health checks
make db-start       # Start PostgreSQL Docker container
make db-stop        # Stop PostgreSQL (keeps data)
```

## Development Database (Docker)

### Start Database
```bash
make db-start
```

This starts PostgreSQL in Docker:
- **Port**: 5432 (main), 5433 (test)
- **User**: postgres
- **Password**: postgres
- **Database**: arive_dev, manageros_test
- **Volume**: `pgdata` (persisted)

### CRITICAL: Database Persistence

The development database uses Docker volumes for data persistence:
- Volume name: `pgdata`
- **NEVER** delete this volume in development
- `make db-stop` stops container but PRESERVES data
- **NEVER** run `docker compose down -v` (destroys data)
- Database state persists across container restarts

### Database Management
```bash
make db-start       # Start PostgreSQL container
make db-stop        # Stop container (keeps data)
make db-upgrade     # Apply migrations
make db-migrate     # Create new migration

# Check database status
docker ps | grep postgres
docker volume ls | grep pgdata
```

## Backend Docker Image

### Build Image
```bash
make docker-build
```

This builds the production backend image:
- Base: Python 3.13 slim
- Package manager: uv
- Entry point: Litestar app
- Includes: Database migrations, compiled email templates
- Tag: `arive-backend:latest`

### What's Included
- Python application code
- uv-managed dependencies
- Alembic migrations
- Compiled email templates (HTML)
- Litestar ASGI server

### What's NOT Included
- Frontend (deployed separately to Vercel)
- Development tools
- Test files
- Source email templates (only compiled HTML)

## Docker Health Check

### Run Health Checks
```bash
make docker-test
```

This performs comprehensive validation:
1. **Build check**: Verifies Docker image builds successfully
2. **Container start**: Starts backend + database containers
3. **Health endpoint**: Checks `/health` returns 200 OK
4. **Database connectivity**: Verifies PostgreSQL connection
5. **Migration check**: Ensures migrations can run
6. **API smoke test**: Validates basic API functionality
7. **Worker check**: Tests SAQ worker process

### Health Check Output

**Success:**
```
✓ Docker image built successfully
✓ Containers started
✓ Health endpoint responding
✓ Database connected
✓ Migrations applied
✓ API responding to requests
✓ Worker process running

All health checks passed!
```

**Failure Example:**
```
✗ Health endpoint not responding
  Error: Connection refused on http://localhost:8000/health

Troubleshooting steps:
1. Check container logs: docker logs <container-id>
2. Verify port mapping: docker ps
3. Check health endpoint code
```

## Troubleshooting Docker Issues

### Container Won't Start

**Check logs:**
```bash
docker compose logs backend
docker logs <container-id>
```

**Common issues:**
- Port 8000 already in use: Stop other backend processes
- Database not ready: Ensure PostgreSQL container is running
- Migration failures: Check Alembic version compatibility
- Missing environment variables: Verify .env or docker-compose.yml

### Build Failures

**Check build output:**
```bash
docker build --progress=plain -t arive-backend -f backend/Dockerfile backend/
```

**Common issues:**
- Python dependency conflicts: Check `pyproject.toml`
- File not found: Ensure files exist in build context
- uv errors: Verify uv version compatibility
- Permission issues: Check file permissions

### Database Connection Issues

**Check database container:**
```bash
docker ps | grep postgres          # Is it running?
docker logs <postgres-container>   # Check logs
```

**Test connection:**
```bash
docker exec -it <postgres-container> psql -U postgres -d arive_dev
```

**Common issues:**
- Container not running: `make db-start`
- Wrong credentials: Check DATABASE_URL
- Port conflict: Ensure 5432/5433 are available
- Network issues: Verify Docker network configuration

### Worker Not Processing Tasks

**Check worker logs:**
```bash
docker compose logs worker
```

**Verify queue configuration:**
```bash
# Access backend shell
docker exec -it <backend-container> python

from app.queue.config import get_queue
queue = await get_queue()
stats = await queue.stats()
print(stats)  # Check queued/processed counts
```

**Common issues:**
- Worker not started: Check docker-compose.yml includes worker service
- Queue table missing: Run migrations to create `saq_*` tables
- Task not registered: Verify task imported in `app/queue/config.py`
- Database connection: Check worker can connect to PostgreSQL

## Local Docker Compose Setup

### docker-compose.yml Example

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: arive_dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/arive_dev
      ENV: local
    depends_on:
      - db

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: litestar workers run
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/arive_dev
      ENV: local
    depends_on:
      - db

volumes:
  pgdata:
```

### Start Full Stack
```bash
docker compose up -d          # Start all services
docker compose logs -f        # Follow logs
docker compose down           # Stop all (keeps volumes)
docker compose down -v        # Stop and DELETE volumes (⚠️ DANGER)
```

## Pre-Deployment Checklist

Before deploying to AWS:

1. **Health checks pass locally:**
   ```bash
   make docker-test
   ```

2. **All tests pass:**
   ```bash
   make test
   make check-all
   ```

3. **Migrations reviewed:**
   - Check `backend/alembic/versions/` for new migrations
   - Test both upgrade and downgrade paths
   - Verify no data loss operations

4. **Environment variables configured:**
   - Check `.env.production` or AWS Secrets Manager
   - Verify DATABASE_URL, API keys, etc.

5. **Email templates compiled:**
   ```bash
   make build-emails
   git status  # Ensure compiled templates committed
   ```

6. **Image size reasonable:**
   ```bash
   docker images arive-backend
   # Should be < 500MB ideally
   ```

## Production Deployment (AWS ECS)

The backend deploys to AWS ECS Fargate:
- **API Service**: Litestar app behind ALB
- **Worker Service**: SAQ background task processor
- **Database**: Aurora Serverless v2 PostgreSQL
- **Images**: Stored in ECR (Elastic Container Registry)

Deployment handled by Terraform in `infra/` directory.

See `infra/CLAUDE.md` for detailed infrastructure guide.
