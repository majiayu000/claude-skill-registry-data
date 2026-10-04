---
name: docker-specialist
description: Docker containerization, Dockerfile writing and optimization, multi-stage
  builds, and Docker Compose configuration for development and production. Use when
  asked to write a Dockerfile, optimize an existing Dockerfile, reduce image size,
  set up Docker Compose for a multi-service app, add health checks to a container,
  secure a container configuration, debug a Docker build error, or containerize an
  application before deploying it.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure
  tags:
  - docker
  - containerization
  - dockerfile
  - docker-compose
  - multi-stage-builds
  - container-security
---

# Docker Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `write a Dockerfile`, `optimize my Docker image`, `Docker Compose`.
- The requested work fits this skill's lane: Writing Dockerfiles, multi-stage builds, reducing image size, Docker Compose, container security.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Kubernetes manifest writing (use kubernetes-specialist); cloud registry setup (use cloud specialist).

## First actions
1. `Glob('**/Dockerfile*', '**/docker-compose*.yml', '**/.dockerignore')` — find existing Docker files
2. `Read` any existing Dockerfile to understand current base image, layers, and patterns in use
3. Identify: application language/runtime, whether this is dev or production, target registry, and whether orchestration (Kubernetes, ECS) is the eventual destination

## Decision rules
- If the app has a build step (Node.js build, Go compile, etc.): use a multi-stage build — builder stage + minimal runtime stage
- Base image selection:
  - Python: `python:3.x-slim` (not full python:3.x)
  - Node.js: `node:lx-alpine` for prod, `node:lx` for dev
  - Go: compile to static binary → `FROM scratch` or `gcr.io/distroless/static`
  - General Linux: `debian:bookworm-slim` over `ubuntu` for size
- Always run as non-root: create a dedicated user with `useradd` or use `USER` directive
- If the image will go to Kubernetes: include SIGTERM handling and graceful shutdown
- If `.dockerignore` is missing: create it before writing the Dockerfile

## Steps

### Step 1: Assess the application
Identify: language, build tool, runtime dependencies, config/secrets approach, port(s) exposed, and health check endpoint if any.

### Step 2: Write .dockerignore
Exclude: `node_modules/`, `.git/`, `*.log`, `.env`, `dist/` (if built inside container), test files, local config.

### Step 3: Write the Dockerfile
Layer order for cache efficiency: base image → system dependencies → copy dependency manifests → install dependencies → copy source → build → final stage (if multi-stage) → USER → EXPOSE → HEALTHCHECK → CMD/ENTRYPOINT.

### Step 4: Write docker-compose.yml (if needed)
Include: named volumes for persistence, environment variable references (not hardcoded values), health check depends_on, named networks.

### Step 5: Validate
```bash
docker build -t test-image .
docker run --rm test-image echo "build ok"
# Check image size:
docker images test-image
# Check for root process:
docker run --rm test-image whoami  # should NOT be root
```

## Output contract
- Primary artifact: `Dockerfile` (and `docker-compose.yml` + `.dockerignore` if applicable)
- Required: non-root USER directive; HEALTHCHECK instruction; .dockerignore file
- Security: no secrets baked into image layers; no `--privileged` flag without explicit justification

## Constraints
- NEVER use `latest` tag for base images in production Dockerfiles - pin to a specific version
- NEVER store secrets (API keys, passwords) in ENV instructions in the Dockerfile
- NEVER install `sudo` in a container
- Scope boundary: Kubernetes manifest writing belongs to kubernetes-specialist; cloud registry setup belongs to aws/azure/gcp-specialist

## Examples

### Example 1: Node.js production Dockerfile
User says: "Write a production Dockerfile for my Node.js Express app"
Actions:
1. Glob for existing Dockerfile and package.json
2. Read package.json for node version and start script
3. Write multi-stage Dockerfile: node:20-alpine builder -> node:20-alpine runtime
4. Write .dockerignore excluding node_modules and .env
Result: Optimized Dockerfile with non-root user, HEALTHCHECK, and .dockerignore

### Example 2: Optimize existing Dockerfile
User says: "My Docker image is 2GB, help me reduce the size"
Actions:
1. Read existing Dockerfile
2. Identify: wrong base image, missing multi-stage build, unnecessary packages, missing .dockerignore
3. Rewrite with multi-stage build and slim base image
4. Show before/after size comparison commands
Result: Refactored Dockerfile with explanation of each optimization

## Troubleshooting
**Build fails: "COPY failed: file not found"**
Cause: File path in COPY instruction doesn't match actual file location, or .dockerignore is excluding the file
Fix: Check build context with `docker build --no-cache .` and verify path; review .dockerignore

**Container exits immediately**
Cause: CMD/ENTRYPOINT produces an error, or process runs in background (daemon mode)
Fix: Run `docker run --rm -it image-name /bin/sh` to inspect; ensure CMD runs process in foreground (no `&` or daemon flags)

**"permission denied" errors at runtime**
Cause: Files owned by root, container running as non-root user
Fix: Add `chown` in Dockerfile: `COPY --chown=appuser:appuser . .`

## Reference
- `references/legacy-agent.md`: Dockerfile patterns by language, security hardening checklist, Docker Compose patterns, container networking, volume management
