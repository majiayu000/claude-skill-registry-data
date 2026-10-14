---
name: containers
description: "Containers: minimal images, non-root, pinned digests, secret hygiene, compose security. Apply the production container checklist: minimal image, non-root, pinned digest, no baked-in secrets."
---

# containers

Production container checklist, enforced on every image: minimal, pinned, non-root, secret-free.

## Activate when

- Writing Dockerfiles, reviewing images, or debugging container behavior/size/security.

## Do NOT activate for

- Compose orchestration (see devops/docker-compose); Kubernetes (registry pointers only — no dedicated skill).

## Inspection

Read the Dockerfile(s): base image + tag policy, USER, COPY layers, secret usage, exposed ports, healthcheck, entrypoint.

## Decision rules

- Minimal base (distroless/slim where the runtime allows); pinned digest, not floating tags.
- Non-root USER; no package-manager caches left in layers; `.dockerignore` present.
- Secrets via runtime injection (env files/vault), never `COPY`/`ARG`-baked; multi-stage builds keep build tools out of runtime.
- One concern per container; healthcheck reflects real readiness.

## Procedure

1. Rewrite the Dockerfile to the checklist; order layers by change frequency (stable first for cache hits).
2. Scan the image (IF trivy/grype exists use it, ELSE manual review of packages + base age); fix findings by bumping, not by ignoring.
3. Verify: rebuild from scratch, image size recorded, runs as non-root (exec check), no secrets in layers (`dive` or history inspection), healthcheck green.

## Failure modes

- `:latest` in production; root by default; secrets in ENV baked into layers; 2GB images from untrimmed bases; healthcheck always-true.

## Escalation

Image CVE triage → security/secrets-supply-chain; orchestration → devops/docker-compose.

## References

- Registry: `../../research/documentation-search/references/framework-registry.yaml` (docker).
- Related: `../../devops/docker-compose/`.
