---
name: docker-compose
description: "Define local and small-prod stacks with Docker Compose: minimal images, non-root, pinned digests, secret hygiene. Use when containerizing services or dependencies."
---

# docker-compose

One command to a working stack; production habits from the first file.
## Inspection

Inventory services, dependency images + pins, env/secret wiring, volumes, networks, and healthcheck coverage.

## Decision rules

One command to a working stack; pinned digests; env from files/vault never committed; healthchecks gating dependents.


## Activate when

- Adding Dockerfiles, compose files, or local Postgres/Redis/queue dependencies.

## Do NOT activate for

- Kubernetes or cloud-managed deploys (see cloud/aws-foundations).

## Procedure

1. Images: minimal base, pinned digest, non-root user, no secrets baked in; `.dockerignore` present.
2. Compose: versioned services, healthchecks, named volumes, explicit networks; env from files/vault, never committed.
3. Dependencies: Postgres/Redis as versioned services with seed + migrate steps documented.
4. Security: apply the container checklist in `../../tooling/containers/`: minimal images, non-root, pinned digests, secret hygiene.
5. Verify: cold `up --build`, healthchecks green, app connects, teardown leaves no stray volumes.

## References
- Related: `../../tooling/containers/`, `../../databases/postgres-operations/`.

## Failure modes

Floating tags; secrets committed in env files; no healthchecks so dependents race; volumes wiping data on recreate.

## Escalation

Image hardening → tooling/containers; production orchestration → cloud/*.
