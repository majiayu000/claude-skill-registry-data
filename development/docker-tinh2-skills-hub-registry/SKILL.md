---
name: docker
description: "Detect project stack and generate production-ready multi-stage Dockerfiles with compose services, .dockerignore, non-root users, health checks, layer caching, and optional dev hot-reload profiles"
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- `--compose` — also generate docker-compose.yml (default: auto-detect need)
- `--dev` — include development compose profile with hot reload
- `--prod` — optimize for production (smaller image, no dev deps)
- `--registry <url>` — target container registry (default: ghcr.io)
- A specific service name to Dockerize (for monorepos)
- `--slim` — use Alpine/distroless base images for minimal size

If no arguments, generate both Dockerfile and docker-compose.yml if the project has dependencies (database, cache, etc.).

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the application stack by reading manifest files:

**Node.js**:
- Read `package.json` for: `engines.node`, `scripts.start`, `scripts.build`, framework
- Lock file determines package manager: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm)
- Framework detection: Next.js (`next.config.*`), Fastify, Express, NestJS, Remix, Astro
- Check for `tsconfig.json` — TypeScript build step needed

**Python**:
- Read `pyproject.toml`, `requirements.txt`, `Pipfile`, `setup.py`
- Framework: Django (`manage.py`), Flask, FastAPI (`uvicorn`/`gunicorn`)
- Python version from `.python-version`, `pyproject.toml`, or `runtime.txt`

**Go**:
- Read `go.mod` for module name and Go version
- Check for `cmd/main.go` or `main.go` entry point
- Static binary — ideal for scratch/distroless final stage

**Rust**:
- Read `Cargo.toml` for binary name
- Static binary with musl target — ideal for scratch/distroless

**Java**:
- Read `pom.xml` (Maven) or `build.gradle` (Gradle)
- Check for Spring Boot, Quarkus, Micronaut
- JRE-only final stage

**Ruby**:
- Read `Gemfile` for Ruby version and framework (Rails, Sinatra)
- Check for `config.ru` (Rack app)

Also detect dependencies that need compose services:
- **Database**: Prisma schema, SQLAlchemy, GORM, ActiveRecord, TypeORM — note the DB engine
- **Cache**: Redis references in config/code
- **Message queue**: RabbitMQ, Kafka references
- **Search**: Elasticsearch references
- **Object storage**: S3/MinIO references

============================================================
PHASE 2 — GENERATE DOCKERFILE
============================================================

Create a multi-stage `Dockerfile` following these principles:

**Stage 1 — Dependencies** (`deps` or `builder`):
- Use specific version tags, never `latest` (e.g., `node:22-alpine`, `python:3.12-slim`)
- Copy lock file BEFORE source code (layer caching optimization)
- Install only production dependencies first
- Use `--mount=type=cache` for package manager caches where supported

**Stage 2 — Build** (if applicable):
- Copy source code after dependency install
- Run build command (`npm run build`, `go build`, `cargo build --release`)
- For compiled languages, produce a static binary if possible

**Stage 3 — Production**:
- Use smallest appropriate base image:
  - Node.js: `node:22-alpine` (or `distroless` if `--slim`)
  - Python: `python:3.12-slim`
  - Go: `gcr.io/distroless/static-debian12` or `scratch`
  - Rust: `gcr.io/distroless/cc-debian12` or `scratch`
  - Java: `eclipse-temurin:21-jre-alpine`
  - Ruby: `ruby:3.3-slim`
- Copy only built artifacts and production deps from previous stages
- Set `WORKDIR /app`

**Security hardening** (always apply):
- Create non-root user with fixed UID/GID 1001
- `USER appuser` before CMD
- No `apt-get upgrade` — pin base image version instead

**Health check** (always include):
- `HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3`
- Node.js: `wget --no-verbose --tries=1 --spider http://localhost:${PORT}/health || exit 1`
- Python: `curl -f http://localhost:${PORT}/health || exit 1`
- Go: built-in health endpoint check
- For apps without a health endpoint, note that one should be created

**Labels** (OCI standard):
```dockerfile
LABEL org.opencontainers.image.source="https://github.com/OWNER/REPO"
LABEL org.opencontainers.image.description="Description"
```

**Environment**:
- Set `NODE_ENV=production` or equivalent
- Set default `PORT` and `EXPOSE` it
- Never bake secrets into the image

============================================================
PHASE 3 — GENERATE .dockerignore
============================================================

Create `.dockerignore` to minimize build context. Always exclude:
- `.git` directory
- IDE config (`.vscode`, `.idea`)
- Test coverage output (`coverage`, `.nyc_output`, `.pytest_cache`)
- Environment files (`.env*`)
- Build artifacts that will be regenerated in the container
- `node_modules` (rebuilt inside container)
- Documentation files (`*.md`)

Adjust patterns based on detected stack.

============================================================
PHASE 4 — GENERATE DOCKER COMPOSE
============================================================

Create `docker-compose.yml` if the application has external dependencies or `--compose` is set.

**Structure requirements**:
- Omit `version:` field (Docker Compose V2+ does not need it)
- Use `depends_on` with `condition: service_healthy` for startup ordering
- Use named volumes for data persistence
- Use a named bridge network for service communication
- Use environment variable references `${VAR:-default}` for configurable values
- Set `restart: unless-stopped` on all services

**Database services**: Include proper health checks:
- PostgreSQL: `pg_isready -U postgres`
- MySQL: `mysqladmin ping -h localhost`
- MongoDB: `mongosh --eval "db.runCommand('ping')"`

**Cache services**: Include memory limits and eviction policy configuration.

**Development profile** (if `--dev`):
Create a `docker-compose.dev.yml` override with:
- Source code mounted as volume for hot reload
- Development build target in Dockerfile
- Debug ports exposed
- `NODE_ENV=development` or equivalent

============================================================
PHASE 5 — VALIDATION
============================================================

After generating files, verify:

1. **Layer ordering** — dependency install comes before source copy
2. **No secrets** — no hardcoded passwords, API keys, or tokens in Dockerfile or compose
3. **Port consistency** — EXPOSE matches the app's actual listen port
4. **Health check** — endpoint referenced in HEALTHCHECK actually exists (or note to create it)
5. **Base image tags** — all pinned to specific versions, no `latest`
6. **Non-root user** — USER directive is present and set before CMD


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

Print a summary:

```
## Docker Setup Complete

### Files Created
- Dockerfile — Multi-stage build ({base image}, {final size estimate})
- .dockerignore — {N} patterns to minimize build context
- docker-compose.yml — Services: {list}
- docker-compose.dev.yml — Development overrides (if generated)

### Build Commands
- Production: docker compose up --build -d
- Development: docker compose -f docker-compose.yml -f docker-compose.dev.yml up
- Image only: docker build -t {name}:latest .

### Image Details
- Base: {base image}
- Estimated size: {size estimate}
- User: appuser (non-root, UID 1001)
- Health check: {endpoint}
- Exposed port: {port}

### Services
| Service | Image | Port | Volume |
|---------|-------|------|--------|
| app | built | {port} | -- |
| db | postgres:16 | 5432 | db-data |
```

============================================================
NEXT STEPS
============================================================

1. Build and test locally: `docker compose up --build`
2. Add a `/health` endpoint to the application if one does not exist
3. Configure CI/CD to build and push the Docker image (run `deploy/github-actions`)
4. Set real database credentials via environment variables or secrets manager (run `deploy/secrets`)


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /docker — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT use `latest` tag for base images — pin to specific versions
- Do NOT run containers as root — always create and switch to a non-root user
- Do NOT copy `.env` files into the image — use environment variables at runtime
- Do NOT install development dependencies in the production stage
- Do NOT use `ADD` when `COPY` suffices (ADD has implicit tar extraction and URL fetch)
- Do NOT include `apt-get upgrade` — use a pinned base image instead
- Do NOT leave package manager caches in final image (use `--mount=type=cache` or clean up)
- Do NOT overwrite an existing Dockerfile without reading it first and preserving custom configuration
- Do NOT hardcode database passwords — use environment variable references
