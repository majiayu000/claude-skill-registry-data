---
name: flask-docker-deployment
description: Set up Docker deployment for Flask applications with Gunicorn, automated versioning, and container registry publishing. Use when dockerizing a Flask app, containerizing for production, or setting up CI/CD with Docker.
---

# Flask Docker Deployment Pattern

This skill helps you containerize Flask applications using Docker with Gunicorn for production, automated version management, and seamless container registry publishing.

## When to Use This Skill

Use this skill when:
- You have a Flask application ready to deploy
- You want production-grade containerization with Gunicorn
- You need automated version management for builds
- You're publishing to a container registry (Docker Hub, GHCR, ECR, etc.)
- You want a repeatable, idempotent deployment pipeline

## What This Skill Creates

1. **Dockerfile** - Multi-stage production-ready container with security best practices
2. **build-publish.sh** - Automated build script with version management
3. **VERSION** file - Auto-incrementing version tracking (gitignored)
4. **.gitignore** - Entry for VERSION file
5. **Optional .dockerignore** - Exclude unnecessary files from build context

## Prerequisites

Before using this skill, ensure:
1. Flask application is working locally
2. `requirements.txt` exists with all dependencies
3. Docker is installed and running
4. You're authenticated to your container registry (if publishing)

## Step 1: Gather Project Information

**IMPORTANT**: Before creating files, ask the user these questions:

1. **"What is your Flask application entry point?"**
   - Format: `{module_name}:{app_variable}`
   - Example: `hyperopt_daemon:app` or `api_server:create_app()`

2. **"What port does your Flask app use?"**
   - Default: 5000
   - Example: 5678, 8080, 3000

3. **"What is your container registry URL?"**
   - Examples:
     - GitHub: `ghcr.io/{org}/{project}`
     - Docker Hub: `docker.io/{user}/{project}`
     - AWS ECR: `{account}.dkr.ecr.{region}.amazonaws.com/{project}`

4. **"Do you have private Git dependencies?"** (yes/no)
   - If yes: Will need GitHub Personal Access Token (CR_PAT)
   - If no: Can skip git installation step

5. **"How many Gunicorn workers do you want?"**
   - Default: 4
   - Recommendation: 2-4 × CPU cores
   - Note: For background job workers, use 1

## Step 2: Create Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
FROM python:3.13-slim

# Build argument for GitHub Personal Access Token (if needed for private deps)
ARG CR_PAT
ENV CR_PAT=${CR_PAT}

# Install curl (for health checks) and git (for private GitHub dependencies)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

# Configure git to use PAT for GitHub access (if private deps)
RUN git config --global url."https://${CR_PAT}@github.com/".insteadOf "https://github.com/" \
    && pip install --no-cache-dir -r requirements.txt \
    && git config --global --unset url."https://${CR_PAT}@github.com/".insteadOf

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the application port
EXPOSE {port}

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT={port}

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:{port}", "--workers", "{workers}", "{module}:{app}"]
```

**CRITICAL Replacements:**
- `{port}` → Application port (e.g., 5678)
- `{workers}` → Number of workers (e.g., 4, or 1 for background jobs)
- `{module}` → Python module name (e.g., hyperopt_daemon)
- `{app}` → App variable name (e.g., app or create_app())

**If NO private dependencies**, remove these lines:
```dockerfile
# Remove ARG CR_PAT, ENV CR_PAT, git installation, and git config commands
```

Simplified version without private deps:
```dockerfile
FROM python:3.13-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE {port}
ENV PYTHONPATH=/app
ENV PORT={port}

CMD ["gunicorn", "--bind", "0.0.0.0:{port}", "--workers", "{workers}", "{module}:{app}"]
```

## Step 3: Create build-publish.sh Script

Create `build-publish.sh` in the project root:

```bash
#!/bin/sh

# VERSION file path
VERSION_FILE="VERSION"

# Parse command line arguments
NO_CACHE=""
if [ "$1" = "--no-cache" ]; then
    NO_CACHE="--no-cache"
    echo "Building with --no-cache flag"
fi

# Check if VERSION file exists, if not create it with version 1
if [ ! -f "$VERSION_FILE" ]; then
    echo "1" > "$VERSION_FILE"
    echo "Created VERSION file with initial version 1"
fi

# Read current version from file
CURRENT_VERSION=$(cat "$VERSION_FILE" 2>/dev/null)

# Validate that the version is a number
if ! echo "$CURRENT_VERSION" | grep -qE '^[0-9]+$'; then
    echo "Error: Invalid version format in $VERSION_FILE. Expected a number, got: $CURRENT_VERSION"
    exit 1
fi

# Increment version
VERSION=$((CURRENT_VERSION + 1))

echo "Building version $VERSION (incrementing from $CURRENT_VERSION)"

# Build the image with optional --no-cache flag
docker build $NO_CACHE --build-arg CR_PAT=$CR_PAT --platform linux/amd64 -t {registry_url}:$VERSION .

# Tag the same image as latest
docker tag {registry_url}:$VERSION {registry_url}:latest

# Push both tags
docker push {registry_url}:$VERSION
docker push {registry_url}:latest

# Update the VERSION file with the new version
echo "$VERSION" > "$VERSION_FILE"
echo "Updated $VERSION_FILE to version $VERSION"
```

**CRITICAL Replacements:**
- `{registry_url}` → Full container registry URL (e.g., `ghcr.io/mazza-vc/hyperopt-server`)

**If NO private dependencies**, remove `--build-arg CR_PAT=$CR_PAT`:
```bash
docker build $NO_CACHE --platform linux/amd64 -t {registry_url}:$VERSION .
```

Make the script executable:
```bash
chmod +x build-publish.sh
```

## Step 4: Create Environment Configuration

### File: `example.env`

Create or update `example.env` with required environment variables for running the containerized application:

```bash
# Server Configuration
PORT={port}

# Database Configuration (if applicable)
{PROJECT_NAME}_DB_HOST=localhost
{PROJECT_NAME}_DB_NAME={project_name}
{PROJECT_NAME}_DB_USER={project_name}
{PROJECT_NAME}_DB_PASSWORD=your_password_here

# Build Configuration (for private dependencies)
CR_PAT=your_github_personal_access_token

# Optional: Additional app-specific variables
DEBUG=False
LOG_LEVEL=INFO
```

**CRITICAL**: Replace:
- `{port}` → Application port (e.g., 5678)
- `{PROJECT_NAME}` → Uppercase project name (e.g., "HYPEROPT_SERVER")
- `{project_name}` → Snake case project name (e.g., "hyperopt_server")

**Note:** Remove CR_PAT if you don't have private dependencies.

### Update .gitignore

Add VERSION file and .env to `.gitignore`:

```gitignore
# Environment variables
.env

# Version file (used by build system, not tracked)
VERSION
```

This prevents the VERSION file and environment secrets from being committed.

## Step 5: Create .dockerignore (Optional but Recommended)

Create `.dockerignore` to exclude unnecessary files from Docker build context:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment files (secrets should not be in image)
.env
*.env
!example.env

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Git
.git/
.gitignore

# CI/CD
.github/

# Documentation
*.md
docs/

# Build artifacts
VERSION
*.log

# OS
.DS_Store
Thumbs.db
```

## Step 6: Usage Instructions

### Setup

```bash
# Copy example environment file and configure
cp example.env .env
# Edit .env and fill in actual values
```

### Building and Publishing

**Load environment variables** (if using .env):
```bash
# Export variables from .env for build process
set -a
source .env
set +a
```

**Standard build** (increments version, uses cache):
```bash
./build-publish.sh
```

**Fresh build** (no cache, pulls latest dependencies):
```bash
./build-publish.sh --no-cache
```

### Running the Container

**Using environment file:**
```bash
docker run -p {port}:{port} \
  --env-file .env \
  {registry_url}:latest
```

**Using explicit environment variables:**
```bash
docker run -p {port}:{port} \
  -e PORT={port} \
  -e {PROJECT_NAME}_DB_PASSWORD=secret \
  -e {PROJECT_NAME}_DB_HOST=db.example.com \
  {registry_url}:latest
```

### Local Testing

Test the container locally before publishing:
```bash
# Build without pushing
docker build --platform linux/amd64 -t {project}:test .

# Run locally
docker run -p {port}:{port} {project}:test

# Test the endpoint
curl http://localhost:{port}/health
```

## Design Principles

This pattern follows these principles:

### Security:
1. **Non-root user** - Container runs as unprivileged user
2. **Minimal base image** - python:3.11-slim reduces attack surface
3. **Build-time secrets** - CR_PAT only available during build, not in final image
4. **Explicit permissions** - chown ensures correct file ownership

### Reliability:
1. **Gunicorn workers** - Production-grade WSGI server with process management
2. **Platform specification** - `--platform linux/amd64` ensures compatibility
3. **Version tracking** - Auto-incrementing versions for rollback capability
4. **Immutable builds** - Each version is reproducible

### Performance:
1. **Layer caching** - Dependencies cached separately from code
2. **No-cache option** - Force fresh builds when needed
3. **Slim base image** - Faster pulls and smaller storage
4. **Multi-worker** - Concurrent request handling

### DevOps:
1. **Automated versioning** - No manual version management
2. **Dual tagging** - Both version and latest tags for flexibility
3. **Idempotent builds** - Safe to run multiple times
4. **Simple CLI** - Single script handles build and publish

## Common Patterns

### Pattern 1: Standard Web API
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]
```
- Multiple workers for concurrent requests
- Factory pattern with `create_app()`

### Pattern 2: Background Job Worker
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5678", "--workers", "1", "daemon:app"]
```
- Single worker to avoid job conflicts
- Direct app instance

### Pattern 3: High-Traffic API
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "8", "--timeout", "120", "api:app"]
```
- More workers for higher concurrency
- Increased timeout for long-running requests

## Integration with Other Skills

### flask-smorest-api Skill
Create the API first, then dockerize:
```
1. User: "Set up Flask API server"
2. [flask-smorest-api skill runs]
3. User: "Now dockerize it"
4. [flask-docker-deployment skill runs]
```

### postgres-setup Skill
For database-dependent apps:
```dockerfile
# Add psycopg2-binary to requirements.txt
# Set database env vars in docker run:
docker run -e DB_HOST=db.example.com -e DB_PASSWORD=secret ...
```

## Container Registry Setup

### GitHub Container Registry (GHCR)

**Login:**
```bash
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
```

**Registry URL format:**
```
ghcr.io/{org}/{project}
```

### Docker Hub

**Login:**
```bash
docker login docker.io
```

**Registry URL format:**
```
docker.io/{username}/{project}
```

### AWS ECR

**Login:**
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  {account}.dkr.ecr.us-east-1.amazonaws.com
```

**Registry URL format:**
```
{account}.dkr.ecr.{region}.amazonaws.com/{project}
```

## Troubleshooting

### Build fails with "permission denied"
```bash
chmod +x build-publish.sh
```

### Private dependency installation fails
```bash
# Verify CR_PAT is set
echo $CR_PAT

# Test GitHub access
curl -H "Authorization: token $CR_PAT" https://api.github.com/user
```

### Container won't start
```bash
# Check logs
docker logs {container_id}

# Run interactively to debug
docker run -it {registry_url}:latest /bin/bash
```

### Version file conflicts
```bash
# If VERSION file gets corrupted, delete and rebuild
rm VERSION
./build-publish.sh
```

## Example: Complete Workflow

**User:** "Dockerize my Flask hyperopt server"

**Claude asks:**
- Entry point? → `hyperopt_daemon:app`
- Port? → `5678`
- Registry? → `ghcr.io/mazza-vc/hyperopt-server`
- Private deps? → `yes` (arcana-core)
- Workers? → `1` (background job processor)

**Claude creates:**
1. `Dockerfile` with gunicorn, 1 worker, port 5678
2. `build-publish.sh` with GHCR registry URL
3. Adds `VERSION` to `.gitignore`
4. Creates `.dockerignore`

**User runs:**
```bash
export CR_PAT=ghp_abc123
./build-publish.sh
```

**Result:**
- ✅ Builds `ghcr.io/mazza-vc/hyperopt-server:1`
- ✅ Tags as `ghcr.io/mazza-vc/hyperopt-server:latest`
- ✅ Pushes both tags
- ✅ Updates VERSION to `1`

**Subsequent builds:**
```bash
./build-publish.sh          # Builds version 2
./build-publish.sh          # Builds version 3
./build-publish.sh --no-cache  # Builds version 4 (fresh)
```

## Best Practices

1. **Use --no-cache strategically** - Only when dependencies updated or debugging
2. **Test locally first** - Build and run locally before pushing
3. **Keep VERSION in .gitignore** - Let build system manage it
4. **Use explicit versions** - Don't rely only on `latest` tag for production
5. **Document env vars** - List all required environment variables in README
6. **Health checks** - Add `/health` endpoint for container orchestration
7. **Logging** - Configure logging to stdout for container logs
8. **Resource limits** - Set memory/CPU limits in production deployment

## Advanced: Multi-Stage Builds

For smaller images, use multi-stage builds:

```dockerfile
# Build stage
FROM python:3.13-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.13-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

This pattern:
- Installs dependencies in builder stage
- Copies only installed packages to runtime
- Results in smaller final image
- Includes curl for health checks
