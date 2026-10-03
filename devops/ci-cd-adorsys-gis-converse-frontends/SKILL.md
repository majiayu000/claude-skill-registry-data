---
name: ci-cd
description: Designs, audits, and debugs continuous integration and delivery pipelines across environments.
---

# CI/CD Skill

Use this when creating or modifying pipelines (e.g., GitHub Actions, GitLab CI, Jenkins, Argo, CircleCI).

## Objectives

- Fast, reliable pipelines with clear stages and caching
- Secure by default (no plaintext secrets, least-privileged credentials)
- Reusable workflows and templates across repos

## Checklist

1. Stages: lint → build → test → security → package → deploy
2. Cache: dependency caches keyed by lockfiles; avoid cache poisoning
3. Matrix: cover supported OS/versions/runtimes where applicable
4. Artifacts: immutable, signed or checksummed; SBOM generated if possible
5. Secrets: sourced from vault/OIDC; never echoed; masked in logs
6. Deploy: blue/green or canary; health checks and automatic rollback
7. Pin actions/plugins by commit SHA or exact version

## Common Tasks

- Create a reusable workflow for Node/TS projects with pnpm cache and Vitest
- Add OIDC-based cloud deployment without long-lived keys
- Integrate SAST/DAST/license scans with thresholds that fail builds

## Output

Provide:

- Proposed pipeline YAML (annotated)
- Risk assessment (secrets exposure, supply-chain)
- Optimization notes (expected minutes saved, cache hits)
