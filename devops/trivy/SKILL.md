---
name: trivy
description: "Scan containers, filesystems, repositories, and infrastructure code with Trivy, then triage CVEs and configure CI thresholds."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["trivy", "security", "cve", "container-scan", "iac", "sbom"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Aqua Trivy Vulnerability Scanning AI Skill Guide

## Overview

Trivy scans container images, filesystems, Git repos, Kubernetes manifests, and Terraform/CloudFormation for OS packages, language libraries, secrets, and misconfigurations. It is widely used as a CI gate. Agents should report **actionable** findings (fixable base, upgraded package) and avoid failing builds on unfixed noise without a documented policy.

```
Target (image | fs | repo | k8s)
        |
        v
Trivy DB + checks
        |
        +--> vulnerabilities (CVE)
        +--> misconfig / secrets
        +--> SBOM (optional)
```

## When to use

- Scanning images before registry push or cluster deploy
- Adding CI security gates with severity thresholds
- Generating SBOM artifacts for compliance
- Triaging whether a CVE is reachable / fixed upstream

## Operational directives

1. Pin Trivy version in CI; cache the vulnerability DB between jobs.
2. Fail on `CRITICAL`/`HIGH` by policy; document ignores with expiry reasons.
3. Prefer scanning by image digest, not mutable tags.
4. Separate vuln results from misconfig/secret scanners in reports.
5. Never suppress secrets findings without rotating the leaked credential.

## Concrete examples

### Image and filesystem scans

```bash
trivy image ghcr.io/example/api:1.4.2
trivy image --severity HIGH,CRITICAL --exit-code 1 ghcr.io/example/api@sha256:...
trivy fs --scanners vuln,secret,misconfig .
trivy repo --severity HIGH,CRITICAL https://github.com/example/api
```

### CI-friendly JSON + SARIF

```bash
trivy image -f json -o trivy.json ghcr.io/example/api:1.4.2
trivy image -f sarif -o trivy.sarif ghcr.io/example/api:1.4.2
trivy image --format spdx-json -o sbom.spdx.json ghcr.io/example/api:1.4.2
```

### Ignore file (time-boxed)

```yaml
# .trivyignore.yaml
vulnerabilities:
  - id: CVE-2024-12345
    paths:
      - "usr/lib/libexample.so"
    expired_at: "2026-09-30"
    statement: "Waiting on upstream base image 1.5; tracked in JIRA-100"
```

### Kubernetes / config

```bash
trivy k8s cluster --severity HIGH,CRITICAL --report summary
trivy config ./deploy/k8s
```

## Triage table

| Finding type | Typical remediations |
| :--- | :--- |
| Distro package CVE | Rebuild on newer base (`alpine:3.20`, distroless) |
| App library CVE | Bump lockfile dependency; rebuild |
| Secret in image | Rotate; rewrite history/layers; use BuildKit secrets |
| K8s misconfig | Fix securityContext, capabilities, root FS |

## Best practices

1. Scan both build images and final runtime images (multi-stage).
2. Publish SBOM beside the image digest in the registry/CI artifacts.
3. Track mean-time-to-remediate for CRITICAL separately from informational noise.
4. Combine with admission policy (optional) - Trivy alone is not runtime enforcement.

## Limitations

- Not all CVEs are exploitable in context; still require human risk acceptance.
- DB freshness matters - stale caches miss new advisories.
- IaC checks are heuristics; not a full cloud security posture platform.

## Related skills

- `docker` - rebuild images after base/package bumps
- `kubernetes` - workload hardening after `trivy k8s` findings
- `packer` - scan golden images/AMIs via filesystem export where applicable
- `argocd` / `fluxcd` - block bad digests before sync
