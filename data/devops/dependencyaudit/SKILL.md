---
name: dependency.audit
description: Scan project for outdated or vulnerable dependencies, enforce dependency policies, check licenses, and generate upgrade recommendations.
---

# dependency.audit

## Purpose

Audit project dependencies (npm, Python, Rust) for security vulnerabilities, outdated versions, and license compliance. Generates actionable recommendations for upgrades.

## When to Use

**Trigger Patterns:**
- "Check for vulnerable dependencies"
- "Audit npm packages"
- "Find outdated Python dependencies"
- "Check dependency licenses"
- CI/CD security scanning

**Do NOT Use When:**
- Installing/upgrading packages (this is audit-only)
- Modifying lockfiles

## Allowed Tools

- `bash` - Run npm audit, pip-audit, cargo audit
- `read_file` - Read package.json, pyproject.toml, Cargo.toml
- `python` - Parse results and generate reports

**Access Level:** 3 (Network-Enabled - checks package registries)

**Network Access:**
- npmjs.com (npm audit)
- pypi.org (pip audit)
- crates.io (cargo audit)

## Expected I/O

**Input:**
- Package manager to audit: npm | pip | cargo | all
- Severity threshold: low | moderate | high | critical

**Output:**
- Security audit report
- License compliance report
- Upgrade recommendations
- Risk assessment

## Dependencies

**Required:**
- npm (for npm audit)
- pip-audit (for Python)
- cargo-audit (for Rust, optional)

**Configuration:**
- `config.json` - Allowed licenses, severity thresholds
- `allowlist.json` - Exceptions for known-safe vulnerabilities

## Examples

### Example: Security Audit

**User:** "Check for vulnerable dependencies"

**Output:**
```
🔍 Dependency Security Audit

📦 NPM Packages:
  ❌ CRITICAL: vite@4.5.0 - CVE-2024-12345
     Description: Path traversal vulnerability
     Upgrade to: vite@5.0.10
     Impact: High

  ⚠️  MODERATE: react-dom@18.2.0 - CVE-2024-67890
     Description: XSS in dev mode
     Upgrade to: react-dom@18.3.1
     Impact: Low (dev-only)

🐍 Python Packages:
  ✅ All packages secure

Summary:
- Critical: 1
- Moderate: 1
- Low: 0
- Total packages scanned: 47

Recommendations:
1. Upgrade vite immediately (critical vulnerability)
2. Schedule react-dom upgrade (low risk, dev-only)
```

### Example: License Check

**User:** "Check dependency licenses"

**Output:**
```
📜 License Compliance Report

✅ Allowed Licenses (45 packages):
   - MIT: 32 packages
   - Apache-2.0: 10 packages
   - BSD-3-Clause: 3 packages

⚠️  Review Required (2 packages):
   - package-x@1.0.0: GPL-3.0 (copyleft license)
   - package-y@2.1.0: Custom license (needs review)

❌ Disallowed Licenses (0 packages):
   - None found

Summary: 45 compliant, 2 need review, 0 violations
```

## Limitations

- Requires network access to check registries
- Cannot auto-update packages (manual review required)
- Allowlist exceptions require human approval

## Validation Criteria

- ✅ All critical vulnerabilities identified
- ✅ License compliance checked
- ✅ Upgrade paths suggested
- ✅ Risk assessment included

## Maintenance

**Owner:** Platform Team
**Review Cycle:** Quarterly
**Last Updated:** 2025-10-18
**Version:** 1.0.0
