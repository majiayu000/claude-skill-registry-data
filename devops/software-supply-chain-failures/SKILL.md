---
name: software-supply-chain-failures
description: >
  Expert guidance on detecting, assessing, and remediating Software Supply Chain Failures
  (OWASP A03:2025) in Python applications — the highest-exploit-score category in the 2025 OWASP
  Top 10. Use this skill whenever the user mentions dependency scanning, vulnerable packages,
  SBOMs, pip-audit, safety check, lockfile integrity, hash pinning, transitive dependencies,
  CI/CD pipeline security, compromised packages, supply chain attacks (SolarWinds, Log4Shell,
  typosquatting), or requests a security review of requirements.txt / pyproject.toml.
  Also trigger for any question about CWE-1104, CWE-1395, or CWE-1329.
---

# Software Supply Chain Failures — OWASP A03:2025

## Overview

**A03:2025 is the #1 community-voted concern** and the **highest-risk category by exploit score**
in the entire OWASP Top 10:2025, despite having only 6 CWEs and limited test data:

| Metric | Value |
|--------|-------|
| OWASP Rank | #3 (new — expands A06:2021 "Vulnerable & Outdated Components") |
| Average Incidence | 5.72% |
| Avg Exploit Score | **8.17** (highest of any category) |
| Avg Impact Score | **5.23** (highest of any category) |
| Key CWEs | CWE-1104, CWE-1395, CWE-1329 |

**Key CWEs:**
- **CWE-1104** — Use of Unmaintained Third-Party Components
- **CWE-1395** — Dependency on Vulnerable Third-Party Component
- **CWE-1329** — Reliance on Component That is Not Updateable

---

## What This Category Covers

Supply chain failures span the full lifecycle — from sourcing packages to building, distributing,
and deploying them:

1. **Untracked / unmonitored dependencies** — direct and transitive
2. **Vulnerable or unsupported components** — unpatched known CVEs
3. **Absence of SBOM management** — no Software Bill of Materials
4. **Unhardened CI/CD pipelines** — no separation of duty, unsigned builds
5. **Untrusted or typosquatted package sources**
6. **Delayed or absent patching cadence**
7. **Build system compromise** (e.g. SolarWinds 2019, Log4Shell 2021, npm worms)

> **Python-specific surface:** Flask alone pulls 7+ transitive packages (Jinja2, Werkzeug,
> MarkupSafe, itsdangerous, click, blinker, packaging). FastAPI pulls Starlette + Pydantic +
> their dependencies. Every transitive package is an attack surface.

---

## Detecting Vulnerabilities — Tool Runbook

### 1. `pip-audit` (recommended — scans against OSV + PyPI Advisory DB)

```bash
# Install
pip install pip-audit

# Scan current environment
pip-audit

# Scan a requirements file
pip-audit -r requirements.txt

# Output JSON for CI
pip-audit -r requirements.txt -f json -o audit-results.json

# Fix automatically where possible
pip-audit --fix
```

### 2. `safety` (scans against Safety DB / PyUp)

```bash
pip install safety

# Basic scan
safety check

# Scan requirements file
safety check -r requirements.txt

# Full JSON output
safety check --json
```

### 3. `osv-scanner` (Google OSV — broadest database)

```bash
# Install via Go or download binary
go install github.com/google/osv-scanner/cmd/osv-scanner@latest

# Scan a project directory
osv-scanner --lockfile=requirements.txt .
```

### 4. `Trivy` (containers + filesystem)

```bash
# Scan Python project
trivy fs --scanners vuln .

# Scan a Docker image
trivy image myapp:latest
```

> **CI/CD Integration:** Run `pip-audit` + `safety` on every PR. Fail the build on HIGH/CRITICAL
> severity findings. See `references/ci-cd-templates.md` for GitHub Actions and GitLab CI examples.

---

## Generating & Managing SBOMs

An SBOM (Software Bill of Materials) is now a compliance requirement (US Executive Order 14028)
and an operational necessity.

### Using `cyclonedx-py`

```bash
pip install cyclonedx-bom

# Generate CycloneDX SBOM from current environment
cyclonedx-py environment -o sbom.json --format json

# From a requirements file
cyclonedx-py requirements requirements.txt -o sbom.json --format json

# From poetry
cyclonedx-py poetry -o sbom.json
```

### Using `pip-licenses` for license compliance

```bash
pip install pip-licenses
pip-licenses --format=json --output-file=licenses.json
```

**SBOM should include:**
- Package name + version + hashes
- License identifiers
- Known vulnerabilities at time of generation
- Transitive dependency tree

---

## Hash Pinning & Lockfiles

### Hash Pinning in `requirements.txt`

```
# BAD — unpinned, vulnerable to substitution attacks
flask==3.0.0

# GOOD — hash-pinned, tamper-evident
flask==3.0.0 \
    --hash=sha256:34a14a9e9ea... \
    --hash=sha256:a9b5cf1a...
```

Generate hash-pinned requirements:

```bash
pip install pip-tools
pip-compile --generate-hashes requirements.in -o requirements.txt
```

### Lockfiles (preferred for applications)

| Tool | Lockfile | Command |
|------|----------|---------|
| Poetry | `poetry.lock` | `poetry install --no-root` |
| uv | `uv.lock` | `uv sync` |
| pip-tools | `requirements.txt` (compiled) | `pip-sync requirements.txt` |
| Pipenv | `Pipfile.lock` | `pipenv install --ignore-pipfile` |

**Critical checks:**
- [ ] Lockfile is committed to source control
- [ ] CI installs from lockfile, not loose `requirements.txt`
- [ ] Lockfile is regenerated on a schedule (weekly minimum)
- [ ] Dependabot / Renovate Bot is configured for automated PRs

---

## Transitive Dependency Auditing

### Visualize the full dependency tree

```bash
pip install pipdeptree
pipdeptree --json-tree > deptree.json

# Find who requires a specific package
pipdeptree --reverse --packages flask
```

### Check for known malicious packages

```bash
# guarddog — detects malicious behavior in packages
pip install guarddog
guarddog pypi scan flask
guarddog pypi verify flask 3.0.0
```

### Flag dangerous import patterns in source code

```python
# Bandit catches these automatically:
import sys
sys.path.insert(0, '/untrusted/path')  # CWE-426: Untrusted Search Path
sys.path.append('/local/unverified')   # Same risk
```

```bash
bandit -r . -t B322,B323,B411  # sys.path manipulation checks
```

---

## CI/CD Pipeline Hardening

Unhardened pipelines are a primary supply chain vector (SolarWinds attack model).

### Minimum pipeline security requirements

| Control | Implementation |
|---------|---------------|
| MFA on pipeline auth | Require OIDC tokens, not static secrets |
| Signed builds | `sigstore` / `cosign` for container images |
| Tamper-evident logs | Immutable audit logs (e.g. Rekor) |
| Dependency pinning | Pin action versions by SHA, not tag |
| Least-privilege | Separate read/write tokens per stage |
| Staged rollouts | Canary deploy before full rollout |

### GitHub Actions — pin by commit SHA

```yaml
# BAD — tag can be moved by attacker
- uses: actions/checkout@v4

# GOOD — immutable SHA
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
```

### SLSA Framework compliance levels

- **SLSA Level 1:** Build process documented, basic provenance
- **SLSA Level 2:** Build service generates signed provenance
- **SLSA Level 3:** Hardened build platform, non-falsifiable provenance

```bash
# Generate SLSA provenance with slsa-verifier
pip install slsa-verifier
slsa-verifier verify-artifact mypackage.tar.gz \
  --provenance-path provenance.json \
  --source-uri github.com/myorg/myrepo
```

---

## FastAPI & Flask — Specific Testing Targets

### Dependency files to audit

| Framework | Direct deps | Key transitives to monitor |
|-----------|------------|---------------------------|
| Flask | flask, flask-login, flask-wtf, sqlalchemy | Jinja2, Werkzeug, MarkupSafe, itsdangerous |
| FastAPI | fastapi, uvicorn, sqlalchemy, pydantic | Starlette, anyio, httpx, h11 |

### Static analysis with Bandit

```bash
pip install bandit

# Full scan with supply-chain relevant rules
bandit -r . -t B301,B302,B303,B324,B411,B412 --format json -o bandit-report.json
```

Key Bandit rules for supply chain:
- `B301` — `pickle` usage (deserialization risk)
- `B302` — `marshal` (similar risk)
- `B411` — `xmlrpc` imports
- `B412` — `httpoxy` detection

### Check for typosquatted / suspicious packages

```bash
# Use pip-audit with strict mode
pip-audit --strict -r requirements.txt

# guarddog behavior analysis
guarddog pypi scan <package>
```

---

## Remediation Priority Matrix

| Finding | Severity | Action |
|---------|----------|--------|
| CVE with CVSS ≥ 9.0 in direct dep | Critical | Patch immediately, block deploy |
| CVE with CVSS 7.0–8.9 in direct dep | High | Patch within 48h |
| CVE in transitive dep only | Medium | Patch within 2 weeks |
| Unpinned dependency | Medium | Add to lockfile in next sprint |
| No SBOM | Medium | Generate and automate in CI |
| Missing `--hash` on requirements | Low | Migrate to lockfile tool |
| Outdated lockfile (>30 days) | Low | Regenerate + review changes |
| No automated dep update bot | Low | Enable Dependabot/Renovate |

---

## Quick-Start Checklist

```
[ ] pip-audit and safety check passing in CI (no HIGH/CRITICAL)
[ ] All dependencies pinned in lockfile (poetry.lock / uv.lock)
[ ] Lockfile committed to source control and used in CI installs
[ ] SBOM generated (cyclonedx-py) and stored as CI artifact
[ ] Dependabot or Renovate Bot enabled on repository
[ ] GitHub Actions pinned by commit SHA
[ ] No sys.path.insert() / sys.path.append() on unverified paths
[ ] SLSA Level 2+ for published packages
[ ] Weekly lockfile refresh scheduled
```

---

## Reference Files

- `references/ci-cd-templates.md` — GitHub Actions + GitLab CI pipeline templates with
  pip-audit, safety, SBOM generation, and SLSA provenance steps
- `references/cwe-mapping.md` — Full CWE-to-detection-tool mapping for audit reporting