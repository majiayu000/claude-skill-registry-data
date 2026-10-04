---
name: scbe-docker-workflow
description: Coordinate SCBE Docker workflows from build to runtime. Use for SCBE container commands, docker-compose service startup, health checks, and troubleshooting of image/build failures, port conflicts, and container startup issues in SCBE repos.
---

# SCBE Docker Workflow

## Quick Start

1. Change to repo:
   - `C:\Users\issda\SCBE-AETHERMOORE-working`
2. Verify Docker files:
   - `Dockerfile`
   - `docker-compose.yml`
   - `docker-compose.api.yml`
   - `docker-compose.unified.yml`
3. Run the standard command for your target stack:
   - Single image: `npm run docker:build` then `docker run -it -p 8000:8000 scbe-aethermoore:latest`
   - Single compose: `npm run docker:compose`
   - API compose: `docker-compose -f docker-compose.api.yml up -d`
   - Unified stack: `docker-compose -f docker-compose.unified.yml up -d`

## Standard Operations

- Build image:
  - `docker build -t scbe-aethermoore:latest .`
  - `docker build -t scbe-aethermoore .`
- Run container directly:
  - `docker run -it scbe-aethermoore:latest`
  - Add port mapping when testing API locally, typically `-p 8000:8000`
- Start compose stacks:
  - `docker-compose up -d`
  - `docker-compose -f docker-compose.api.yml up -d`
  - `docker-compose -f docker-compose.unified.yml up -d`

## Health and Runtime Checks

- `docker ps`
- `docker logs <container>`
- Health check endpoints:
  - `http://localhost:8000/v1/health` (API-focused compose)
  - `http://localhost:8080/health` (unified gateway and Dockerfile default health test)
- `docker ps -f health=unhealthy` to spot failing healthchecks

## Troubleshooting Playbook

- Build errors before compile step:
  - Retry with `docker build --no-cache -t scbe-aethermoore:latest .`
  - Check for transient network errors downloading build toolchains (Node/Python/liboqs)
- Container exits immediately:
  - `docker logs <container>`
  - Validate expected env vars from stack file and `.env` usage
- Port conflicts:
  - Check host ports `8000`, `8080`, and `3000` are free before mapping
  - Use compose alternatives or remap ports in a temporary override
- Compose startup stalls:
  - `docker-compose logs -f`
  - Confirm required service health using container logs and `docker ps -f status=running`

## Reference and Deep Context

For full stack maps, service-level expectations, and deeper remediation steps, read:
- [references/docker-stack.md](references/docker-stack.md)

## Automation Assets

Use the troubleshooting script when you need repeatable diagnostics:

- `scripts/scbe_docker_status.ps1`
- `assets/action-summary.template.yaml`

Example usage:

- `.\scripts\scbe_docker_status.ps1 -RepoPath . -InspectStacks -ShowLogs`
- `.\scripts\scbe_docker_status.ps1 -RepoPath . -ContainerName scbe-core -LogTail 120`
- `.\scripts\scbe_docker_status.ps1 -RepoPath . -CleanRestart`
