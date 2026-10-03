---
name: devsecops
description: DevSecOps skill for securing CI/CD pipelines, infrastructure as code, containers, Kubernetes, cloud deployments, secrets handling, dependency management, SAST/DAST/SCA, release gates, supply-chain controls, SBOMs, policy-as-code, and secure SDLC workflows. Use for pipeline hardening, deployment risk reviews, security automation, and remediation planning.
---

# DevSecOps

## Operating Rules

- Inspect the repo, pipeline files, deployment manifests, and current security tooling before recommending changes.
- Prefer incremental controls that developers can keep using over heavyweight gates that will be bypassed.
- Treat credentials, artifacts, build provenance, and deployment permissions as first-class risks.
- Separate blocking release criteria from advisory findings.

## Workflow

1. Map the path from commit to production: source, build, test, artifact, deploy, runtime.
2. Identify trust boundaries, identities, secrets, third-party actions/images, and artifact storage.
3. Add or improve controls: least privilege, pinned dependencies, scanning, signing, SBOM, policy checks, and audit logging.
4. Tune severity and false-positive handling so the pipeline remains usable.
5. Verify with local checks, CI dry runs, or policy evaluation where available.

## Baseline Controls

- Pin third-party CI actions and container base images.
- Use short-lived credentials or OIDC federation instead of long-lived secrets.
- Run SAST/SCA/container/IaC checks with documented exception handling.
- Generate SBOMs and preserve build provenance for release artifacts.
- Enforce least-privilege deploy roles per environment.

