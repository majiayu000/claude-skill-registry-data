---
name: fleet-dependency-audit
description: How DevSecOps audits project dependencies — CVE checking, version pinning, license review, transitive dependency analysis. Maps to sec_dependency_audit group call and nightly-dependency-scan CRON.
---

# Dependency Audit — DevSecOps Systematic Methodology

Every external dependency is an attack surface. Libraries you didn't write contain vulnerabilities you didn't create. Your job is to find them before they reach production.

## The Audit Scope

| Dependency Type | Where to Find | Tool |
|----------------|--------------|------|
| Python packages | requirements.txt, pyproject.toml, setup.py | `pip audit`, semgrep |
| Node packages | package.json, package-lock.json | `npm audit` |
| Docker base images | Dockerfile FROM lines | Image scan, version check |
| GitHub Actions | .github/workflows/*.yml | SHA pinning verification |
| System packages | apt/apk install lines | Version tracking |

## The Audit Protocol

### Step 1: Inventory Dependencies

Before scanning, know what you're scanning:
```
# Python — list all with versions
pip list --format=freeze

# Node — list all including transitive
npm ls --all

# Docker — check base image versions
grep "FROM " Dockerfile
```

### Step 2: CVE Database Check

Run automated scanners:
```
# Python CVEs
pip audit --format=json

# Node CVEs  
npm audit --json

# Semgrep for code patterns that use vulnerable APIs
semgrep --config=auto --json
```

Use your `dependency-scanner` sub-agent for isolated scanning:
```
Agent: dependency-scanner
Prompt: "Audit all Python dependencies in requirements.txt against 
        CVE databases. Classify findings by severity."
```

### Step 3: Classify Findings

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Known exploit exists, RCE/auth bypass, in production deps | Immediate: security_hold + alert + ntfy PO |
| HIGH | Significant vuln, no known exploit, production deps | Same sprint: create fix task |
| MEDIUM | Moderate risk, specific conditions needed, or dev-only deps | Next sprint: track and plan |
| LOW | Theoretical, mitigated by other controls, informational | Backlog: monitor for escalation |

### Step 4: Version Pinning Verification

Unpinned dependencies are time bombs — they change without you knowing.

**Check:**
```python
# BAD — unpinned
requests
flask

# GOOD — pinned to compatible range
requests>=2.31.0,<3.0
flask>=3.0.0,<4.0

# BEST — pinned to exact (for reproducibility)
requests==2.31.0
flask==3.0.3
```

For GitHub Actions, check SHA pinning:
```yaml
# BAD — tag can be overwritten
- uses: actions/checkout@v4

# GOOD — pinned to SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

### Step 5: License Review

Not all open-source licenses are compatible with all uses:

| License | Risk | Fleet Impact |
|---------|------|-------------|
| MIT, Apache 2.0, BSD | Low | Safe for any use |
| LGPL | Medium | OK for dynamic linking, risky for static |
| GPL | High | Copyleft — may require open-sourcing fleet code |
| AGPL | Critical | Network use triggers copyleft — very restrictive |
| No license | Critical | No permission to use at all |

Check: `pip-licenses` for Python, `license-checker` for Node.

### Step 6: Transitive Dependencies

Your direct dependencies pull in transitive dependencies. A vulnerability 3 levels deep is still a vulnerability.

```
# Python — show dependency tree
pipdeptree

# Node — show why a package is installed
npm explain package-name
```

If a transitive dependency has a critical CVE, the fix might be:
1. Update the direct dependency (pulls in fixed transitive)
2. Pin the transitive dependency directly (override)
3. Replace the direct dependency (if unmaintained)

## The Vulnerability Report

Structure findings as a `vulnerability_report` artifact:
```
## Dependency Audit: {project}
Date: {date}
Scanned: {count} direct + {count} transitive dependencies

### Critical (0)
### High (1)
- [H-001] requests 2.28.0: CVE-2023-XXXXX (SSRF via redirect)
  Fix: pin to >= 2.31.0
  Impact: fleet/infra/mc_client.py uses requests for MC API calls

### Medium (2)
- [M-001] ...
- [M-002] ...

### Version Pinning
- {N} unpinned dependencies found
- {N} GitHub Actions not SHA-pinned

### License
- All licenses compatible: {yes/no}
- Flagged: {list if any}
```

## CRON Integration

Your **nightly-dependency-scan** CRON runs this automatically at 01:00:
1. Scan all projects in config/projects.yaml
2. Run pip audit + npm audit
3. Classify findings
4. Post summary to board memory [security, audit]
5. For critical: security_hold + alert + ntfy

Between CRONs, new dependencies introduced by commits won't be caught until the next scan. For high-risk changes (new dependency added), scan manually during your heartbeat.
