---
name: docker-compose-helper
description: Use when the user asks to create, debug, or modify Docker Compose files, compose.yaml, docker-compose.yml, service dependencies, healthchecks, ports, volumes, networks, environment variables, or local multi-container development stacks. Use this skill even if the user says "compose file" or "local stack" instead of "Docker Compose".
---

# Docker Compose Helper

Help users create, review, and repair Docker Compose setups with the smallest
working change that fits their local development workflow.

## Workflow

1. Identify the user's goal:
   - creating a new compose file
   - adding or changing a service
   - debugging startup, networking, volume, or environment issues
   - translating a `docker run` command into compose
2. Inspect existing files before editing:
   - `compose.yaml`
   - `compose.yml`
   - `docker-compose.yaml`
   - `docker-compose.yml`
   - `.env`
   - Dockerfiles referenced by `build`
3. Prefer Docker Compose v2 syntax:
   - omit the obsolete top-level `version`
   - use `compose.yaml` if creating a new file
   - keep service names lowercase and stable
4. Make the smallest useful change. Do not add orchestration, custom networks,
   or named volumes unless the service needs them.

## Compose Defaults

- Use explicit image tags instead of `latest` when a stable tag is obvious.
- Use named volumes for database state.
- Use bind mounts for application source during local development.
- Put secrets and machine-specific values in `.env`, not directly in YAML.
- Add `depends_on` only for startup ordering; add `healthcheck` when readiness
  actually matters.
- Expose only the host ports the user needs.

## Debugging Checklist

When debugging, check these in order:

1. YAML validity and indentation.
2. Whether the service name, image, build context, and Dockerfile path exist.
3. Port conflicts between host ports and already-running services.
4. Volume paths and whether a bind mount hides files built into the image.
5. Environment variable names, `.env` loading, and missing required values.
6. Container-to-container networking: services should use service names as DNS
   hosts, not `localhost`.
7. Readiness problems: add a healthcheck and condition only when the dependent
   service truly must wait.

## Output

When editing files, show the changed compose snippet or file path and explain
the reason for each non-obvious setting in one short sentence.
