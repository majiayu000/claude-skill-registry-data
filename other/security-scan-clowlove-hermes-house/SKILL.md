---
name: security-scan
description: "Comprehensive security scanning for code, dependencies, and infrastructure. Detects vulnerabilities, misconfigurations, and security risks."
triggers:
  - "security scan"
  - "漏洞扫描"
  - "vulnerability scan"
  - "security audit"
---

# Security Scan

Comprehensive security scanning and vulnerability detection.

## Features

- 🔍 **Code Scan** — Static analysis for security issues
- 📦 **Dependency Scan** — Check for vulnerable packages
- 🌐 **Infrastructure Scan** — Cloud/Docker security
- 🔑 **Secret Scan** — Detect exposed credentials
- 📊 **Compliance** — SOC2, HIPAA, GDPR checks

## Usage

### Scan Project

```bash
# Full scan
hermes security scan /path/to/project

# Fast scan
hermes security scan /path/to/project --mode fast

# Specific checks
hermes security scan --checks secrets,vulns,configs
```

### Dependency Scan

```bash
# Scan dependencies
hermes security deps --file package-lock.json

# Python packages
hermes security deps --file requirements.txt

# Docker images
hermes security scan-image node:18-alpine
```

### Secret Detection

```bash
# Scan for secrets
hermes security secrets --path ./src/

# Git history
hermes security secrets --git-history
```

## Report

```bash
# Generate report
hermes security report --format html --output security-report.html

# Severity filter
hermes security report --severity critical,high
```

## Configuration

```yaml
# security-config.yml
scan:
  exclude: ["node_modules", ".git", "test/**"]
  severity_threshold: medium
  
secrets:
  patterns:
    - "api[_-]?key"
    - "password"
    - "secret"
    
dependencies:
  ignore: ["dev-only-pkg"]
```

## Pitfalls

1. **False Positives** — Always verify reported issues
2. **Performance** — Full scans can be slow on large codebases
3. **Credentials** — Don't commit API keys to scanner