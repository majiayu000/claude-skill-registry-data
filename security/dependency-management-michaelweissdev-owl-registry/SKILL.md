---
name: dependency-management
description: >
  Audit, update, lock, and secure third-party open-source dependencies across
  software supply chains. Use when analyzing transitive dependencies, generating
  Software Bill of Materials (SBOM), auditing packages with cargo audit, pip-audit,
  or npm audit, configuring Renovate/Dependabot, or managing deterministic lockfiles.
compatibility: >
  Agent Skills-compatible coding agents managing dependencies across package managers
  (npm, pnpm, uv, pip, cargo, go mod).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "dependencies, security, sbom, supply-chain, lockfiles, dependabot, audit"
  topics: "security, devops, software-development"
---

# Software Dependency Management & Supply Chain Security

Modern applications consist overwhelmingly of third-party open-source libraries. Malicious package takeovers, dependency confusion attacks, typosquatting, and unpatched CVEs in transitive dependencies represent severe supply-chain risks. Disciplined dependency management enforces deterministic lockfiles, automated vulnerability scanning, minimal dependency footprints, and Software Bill of Materials (SBOM) tracking.

## Core Rules

1. **Commit deterministic lockfiles for applications**: Always commit `package-lock.json`, `uv.lock`, `Cargo.lock`, `pnpm-lock.yaml`, or `go.sum` in production services to ensure bit-for-bit reproducible builds.
2. **Automate vulnerability scanning in CI**: Run automated vulnerability scanners (`cargo audit`, `pip-audit`, `npm audit`, `trivy`) to block builds introducing known CVEs.
3. **Scrutinize transitive dependencies**: A direct dependency adding 80 transitive packages multiplies your attack surface by 80. Prefer lightweight libraries with minimal transitive dependencies.
4. **Enforce automated minor/patch updates**: Use Renovate or Dependabot to receive continuous automated dependency pull requests with passing CI tests.
5. **Verify package provenance and checksums**: Ensure package managers verify cryptographic hashes (SHA-256) of downloaded wheels, crates, or npm tarballs.

---

## 1. Vulnerability Auditing Across Ecosystems

Run automated audits regularly:

### Python (`pip-audit` / `uv`)
```bash
# Audit installed virtualenv packages against PyPA Advisory Database
pip-audit --strict

# Or audit directly from lockfile without installing
pip-audit -r requirements.txt
```

### Rust (`cargo audit`)
```bash
# Check dependencies against RustSec Advisory Database
cargo audit
```

### Node.js (`npm` / `pnpm`)
```bash
# Audit production dependencies only (ignoring devDependencies)
npm audit --omit=dev
```

### Go (`govulncheck`)
```bash
# Scan Go module dependencies and analyze if vulnerable functions are actually called
govulncheck ./...
```

---

## 2. Generating a Software Bill of Materials (SBOM)

An SBOM provides an inventory of all software components, licenses, and versions in standard machine-readable formats (CycloneDX or SPDX):

```bash
# Generate CycloneDX JSON SBOM using Syft
syft packages dir:. -o cyclonedx-json=sbom.json

# Scan the generated SBOM for known vulnerabilities using Grype
grype sbom:sbom.json
```

---

## 3. Automated Dependency Updates: Renovate Configuration

Renovate (`renovate.json`) provides automated, scheduled dependency PRs:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    ":semanticCommits"
  ],
  "packageRules": [
    {
      "description": "Automatically merge patch updates if CI passes",
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "pr"
    },
    {
      "description": "Group devDependencies into a single monthly PR",
      "matchDepTypes": ["devDependencies"],
      "groupName": "devDependencies",
      "schedule": ["before 5am on the first day of the month"]
    }
  ]
}
```

---

## 4. Defending Against Supply Chain Attacks

### Typosquatting & Malicious Packages
- Always check the exact package name (`pydantic` vs `pydantc`).
- Inspect repository stars, release history, and publisher verification before adopting new dependencies.

### Dependency Confusion
When an organization uses private internal packages (e.g. `@internal/core`):
- Configure package registries with scoped namespaces.
- Register placeholders on public npm/PyPI registries or configure package managers to never look up internal scopes in public registries.

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Supply Chain Risk | Correct Practice |
| :--- | :--- | :--- |
| Deleting `Cargo.lock` / `package-lock.json` in CI | Builds pull unverified upstream updates that break builds | Always build with `--frozen` or `--immutable` |
| Floating dependency versions (`"requests": "*"`) | Pulls breaking changes or compromised releases automatically | Use SemVer range bounds (`requests>=2.31,<3.0`) |
| Ignoring `npm audit` warnings | Deploys known exploits to production | Update vulnerable packages; investigate overrides |
| Adding massive dependencies for single trivial helper | Unnecessary attack surface expansion | Implement simple helpers in-house (Zero-dependency rule) |

---

## 6. Verification Checklist

- [ ] Lockfile exists, is committed, and is up to date with manifest.
- [ ] Automated security audit (`pip-audit`, `cargo audit`, `npm audit`) passes with 0 known CVEs.
- [ ] Automated dependency updates configured (Renovate or Dependabot).
- [ ] All downloaded packages verified against cryptographic SHA-256 hashes.
