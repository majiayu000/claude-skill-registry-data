---
name: ci_cd_pipeline
description: Maintain the 13-workflow GitHub Actions CI/CD system with security gates, integrity checks, and deployment automation.
when_to_use:
  - Editing any .github/workflows/ file
  - Adding CI checks or gates
  - Debugging pipeline failures
  - Hardening deployments
---

# CI/CD Pipeline (RESTO BOT)

## CI Diamond

```text
integrity-gate
  |
  +---> lint
  +---> python-tests
  +---> integration-tests
  +---> docker-build
  +---> security-scan
  +---> frontend-lint
  +---> test-harness
  |
  v
ci-summary
```

## CD Diamond

```text
validate -> preflight -> security-gate -> staging -> smoke
  -> approve -> backup -> deploy -> smoke -> dora -> cleanup
```

## Workflow files

Location: `project/.github/workflows/`

| Workflow | Purpose |
| --- | --- |
| ci.yml | Main CI diamond |
| cd-deploy.yml | CD deployment pipeline |
| build-push-artifacts.yml | Docker build + push to GHCR |
| security-scan.yml | Trivy + secret scanning |
| integrity-gate.yml | Workflow JSON validation |
| test-harness.yml | End-to-end test battery |
| And more... | 12 total workflows |

## Composite actions

Location: `project/.github/actions/` (4 composite actions)

## Supply-chain security policies

- All GitHub Actions must be **SHA-pinned** (no `@v3`, use `@sha256:...`)
- N8N_VERSION must match across `.env`, `ci.yml`, `security-scan.yml`
- Docker images signed with Cosign
- SBOM generated per build
- SLSA provenance attestation

## Required stages for any pipeline change

1. Validate (lint/format/typecheck)
2. Test (unit + integration)
3. Security (secret scan + dependency scan + Trivy)
4. Build (deterministic, reproducible)
5. Deploy (gated for prod, requires approval)
6. Post-deploy smoke (curl health endpoints)
7. Cleanup (safe prune; never delete volumes)

## Key files

- `project/.github/workflows/` (all workflow YAML files)
- `project/.github/actions/` (composite actions)
- `project/.env` (N8N_VERSION must be consistent)
- `project/scripts/validate_cicd.sh` (CI/CD validation script)

## Required output

- Pipeline diff with rationale
- Smoke script used in post-deploy stage
- Rollback instructions
- Version consistency check (N8N_VERSION across files)
