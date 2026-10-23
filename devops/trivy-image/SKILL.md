---
name: trivy-image
description: "Configures and runs Trivy for container image scanning: Aqua Security's all-in-one scanner combining vuln + secret + misconfiguration + license detection in one pass; `trivy image {image}` with --severity HIGH,CRITICAL filter; --format sarif/json (incl. scan-embedded CycloneDX; for standalone SBOM generation see syft-generation + sbom-formats); .trivyignore CVE suppression file; --ignore-unfixed for actionable filter; --scanners vuln/misconfig/license/secret toggle. Use when the team wants a single tool covering container image security across multiple dimensions, not for producing a standalone CycloneDX SBOM."
---

# trivy-image

## Overview

Per [trivy.dev/latest/docs/target/container_image/][tv-img]:

[tv-img]: https://trivy.dev/latest/docs/target/container_image/

Trivy is Aqua Security's open-source scanner. Distinguishing
feature: **all-in-one** - one CLI invocation covers vuln + secret +
misconfig + license scanning. By contrast, `syft-generation`'s
Grype workflow is a two-step
SBOM-then-scan pattern.

Per [tv-img][tv-img] the scanner toggles:

| Scanner | Default? | Use |
|---|---|---|
| `vuln` | yes | Known CVEs in OS + language packages |
| `secret` | yes | Exposed credentials (env vars, config files) |
| `misconfig` | no | Docker / Kubernetes config best-practices |
| `license` | no | License compliance scanning |

## When to use

- Container-image security in one tool (vs separate tools per
  concern).
- The team uses Aqua Security stack (Trivy is the OSS center of
  it).
- Pre-prod or registry-side scanning (Trivy's image-by-tag mode).
- Layered with the Grype workflow in `syft-generation` for
  cross-DB consensus on vuln findings.

## Step 1 - Install

Common install paths:

```bash
# Homebrew (macOS / Linux)
brew install trivy

# Docker (zero-install for CI)
docker pull aquasec/trivy:latest

# Linux APT
sudo apt-get install trivy

# RPM
sudo dnf install trivy
```

## Step 2 - Basic image scan

Per [tv-img][tv-img]:

```bash
# Default: vuln + secret scan
trivy image python:3.4-alpine
```

Example with multiple toggles:

```bash
# All scanners (vuln + secret + misconfig + license)
trivy image --scanners vuln,secret,misconfig,license python:3.4-alpine

# Vuln-only (fastest, default if --scanners omitted defaults to vuln+secret)
trivy image --scanners vuln python:3.4-alpine
```

## Step 3 - Severity filtering

Per [tv-img][tv-img]:

```bash
trivy image --severity HIGH,CRITICAL python:3.4-alpine
```

Severity levels: `UNKNOWN`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.

Combined with exit-code-on-finding:

```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 python:3.4-alpine
```

Exit code semantics: `0` = no findings at the configured severity;
`1` = findings present.

## Step 4 - Output formats

Per [tv-img][tv-img]:

| Format | Use |
|---|---|
| `json` | For multi-scanner finding prioritization |
| `sarif` | GitHub Code Scanning upload |
| `cyclonedx` | CycloneDX SBOM with vuln annotations |
| `spdx-json` | SPDX SBOM (vuln-only metadata) |
| `template` | Custom Go template |
| (default) | Table format human-readable |

```bash
trivy image --format json --output trivy-image.json my-image:1.0
trivy image --format sarif --output trivy-image.sarif my-image:1.0
trivy image --format cyclonedx --output trivy-cyclonedx.json my-image:1.0
```

## Step 5 - `--ignore-unfixed` for actionable filter

Per [tv-img][tv-img], `--ignore-unfixed` excludes vulnerabilities without an
available fix - the practical first-line filter for actionable findings:

```bash
trivy image --ignore-unfixed python:3.4-alpine
```

Combine with a severity threshold for the recommended PR-blocking config (fail
only on actionable, high-severity vulns):

```bash
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 my-image:1.0
```

## Step 6 - Secret scanning

Per [tv-img][tv-img]:

> "Secret detection runs automatically. The tool scans for exposed
> credentials and sensitive data, particularly in environment
> variables."

Secret findings appear alongside vuln findings in the same report.
For deeper secret-scanning patterns, see `gitleaks-scanning`
+ `trufflehog-scanning`.

## Step 7 - Misconfiguration scanning

Per [tv-img][tv-img]:

```bash
trivy image --scanners misconfig --severity HIGH,CRITICAL my-image:1.0
```

Detects Docker / Kubernetes config patterns matching CIS Benchmarks
+ team-policy issues (e.g., container running as root, missing
HEALTHCHECK, exposed sensitive ports).

For comprehensive IaC scanning (not just image-internal config),
use `checkov-policy`
+ `trivy-config`
from the qa-iac plugin.

## Step 8 - False-positive triage (MANDATORY)

Per [tv-img][tv-img]: "Use a `.trivyignore` file to suppress
specific findings. Place this file in your project directory with
CVE IDs or vulnerability identifiers you wish to exclude."

Suppression mechanisms:

| Mechanism | Use |
|---|---|
| `.trivyignore` file | Per-CVE / per-misconfig-rule ID list |
| `--ignore-unfixed` flag | Filter to actionable findings only |
| `--vex` (VEX file) | Standardized status assertions (CycloneDX-VEX or OpenVEX) |
| `--ignore-policy` Rego policy | Programmatic ignore via OPA Rego |

`.trivyignore` example:

```
# .trivyignore
# Reason: log4j-core 2.14.x bundled but not loaded at runtime
#         (verified via dependency tree analysis)
# Approved-by: alice@example.com
# Re-review-date: 2026-09-15
CVE-2021-44228
CVE-2021-45046

# Misconfiguration ignores
DS013
KSV001
```

**Justification template (mandatory):** every entry in `.trivyignore`
should be preceded by `# Reason: ... # Approved-by: ... # Re-review-date: ...`
comment block.

For richer programmatic suppression, use OpenVEX:

```bash
trivy image --vex sbom.openvex.json --severity HIGH,CRITICAL my-image:1.0
```

The VEX file's per-CVE assertions (`not_affected` etc.) filter the
output.

Cadence: every quarter, audit `.trivyignore`; expired re-review-date
entries removed.

## Step 9 - CI integration

Wrap the CLI with the `aquasecurity/trivy-action` GHA to scan the built image
and upload SARIF to GitHub Code Scanning. The full GitHub Actions workflow is
in [references/ci-and-composition.md](references/ci-and-composition.md).

## Step 10 - Composition with sister tools

Trivy is the all-in-one first line; compose it with `syft-generation` for a
standalone SBOM plus the Grype scan for cross-DB consensus on findings, and
`checkov-policy` for deeper IaC scanning. The full composition table is in
[references/ci-and-composition.md](references/ci-and-composition.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Skip `--ignore-unfixed` | Stuck findings (no fix available) flood report | Always for PR gating (Step 5) |
| `.trivyignore` without justification comment | No audit trail | Mandatory template (Step 8) |
| Run all scanners on every PR | Slow; misconfig + license noise on small changes | Default vuln+secret on PR; full scan nightly |
| Skip severity filter | LOW noise drowns CRITICAL signal | `--severity CRITICAL,HIGH` for PR (Step 3) |
| Pin to `aquasec/trivy:latest` Docker tag | Breaking changes mid-release | Pin specific version |

## Limitations

- DB updates are large (~1 GB cache); pin DB version for CI
  determinism.
- Misconfig + license + secret scanning are less deep than
  dedicated tools (use Trivy as first-line; layer dedicated tools
  for depth).
- Trivy's vuln DB has its own coverage profile; pair with
  Grype (`syft-generation` Step 7) for cross-DB
  consensus.
- License detection is basic; for compliance-grade analysis, use
  ScanCode / FOSSology.

## References

- [tv-img][tv-img] - container image scan reference
- trivy.dev - landing
- aquasecurity.github.io/trivy - full documentation
- github.com/aquasecurity/trivy - repository
- openvex.dev - OpenVEX specification (used by `--vex` flag)
- [references/ci-and-composition.md](references/ci-and-composition.md) - full CI workflow + sister-tool composition
- `syft-generation`,
  `sbom-formats` - sister tools
