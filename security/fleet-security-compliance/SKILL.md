---
name: fleet-security-compliance
description: How DevSecOps verifies compliance with security standards — not finding new vulnerabilities, but verifying that established security controls are still in place and functioning.
---

# Security Compliance Verification — DevSecOps Standards Assurance

Vulnerability scanning finds NEW problems. Compliance verification checks that EXISTING controls are still working. Authentication still enforced? Secrets still managed? Dependencies still pinned? Controls that were implemented don't erode silently.

## The Security Controls Checklist

### 1. Authentication Controls

| Control | How to Verify | Where |
|---------|-------------|-------|
| JWT tokens used (not session cookies) | Check auth middleware | fleet/infra/ auth code |
| Token expiry configured | Check config | .env, fleet.yaml |
| Refresh token rotation | Check auth flow | auth daemon |
| API endpoints require auth | Check middleware attachment | all route files |
| No hardcoded credentials | Scan for patterns | all source files |

### 2. Input Validation Controls

| Control | How to Verify | Where |
|---------|-------------|-------|
| Request size limits | Check middleware/config | API entry points |
| Content-type validation | Check request handling | API handlers |
| SQL/command injection prevention | Check query construction | database queries, subprocess calls |
| Path traversal prevention | Check file operations | any file read/write |

### 3. Secret Management Controls

| Control | How to Verify | Where |
|---------|-------------|-------|
| .env gitignored | Check .gitignore | .gitignore |
| No secrets in code | Secret scan | all source files |
| API keys from env vars | Check config loading | config_loader.py |
| Secrets not logged | Check log statements | all logger.* calls |
| Example files have placeholders | Check .env.example | .env.example, *.example |

### 4. Dependency Controls

| Control | How to Verify | Where |
|---------|-------------|-------|
| Python deps pinned | Check requirements.txt | requirements.txt, pyproject.toml |
| GitHub Actions SHA-pinned | Check workflow files | .github/workflows/*.yml |
| Docker base images pinned | Check Dockerfiles | Dockerfile, docker-compose |
| No known critical CVEs | Run pip audit | dependencies |

### 5. Infrastructure Controls

| Control | How to Verify | Where |
|---------|-------------|-------|
| MC backend not exposed externally | Check port bindings | docker-compose.yaml |
| IRC not accessible externally | Check miniircd config | scripts/setup-irc.sh |
| Gateway auth enabled | Check gateway config | gateway config |
| File permissions appropriate | Check sensitive files | .env, keys, certs |

## The Compliance Verification Process

### Step 1: Run Automated Checks

Your sub-agents handle the mechanical scanning:
```
Agent: secret-detector — scan for exposed credentials
Agent: security-auditor — OWASP-based code audit
Agent: dependency-scanner — CVE database check
```

### Step 2: Verify Control Categories

For each category above, check: is the control STILL in place?
- Was it removed by a recent commit?
- Was it weakened by a configuration change?
- Was it bypassed by a new code path?

### Step 3: Produce Compliance Report

```
## Security Compliance Report — {date}

### Authentication: {COMPLIANT / NON-COMPLIANT}
- JWT auth: ✓ enforced
- Token expiry: ✓ configured (1h access, 7d refresh)
- Hardcoded creds: ✓ none found

### Input Validation: {COMPLIANT / NON-COMPLIANT}
- Request limits: ✓ configured
- Injection prevention: ⚠ 1 finding (fleet/infra/db.py:142 — string interpolation)

### Secret Management: {COMPLIANT / NON-COMPLIANT}
- .env gitignored: ✓
- No secrets in code: ✓
- Example files clean: ✓

### Dependencies: {COMPLIANT / NON-COMPLIANT}
- Pinned: ✓
- CVEs: ⚠ 1 medium (requests 2.28.0)
- SHA-pinned actions: ✓

### Infrastructure: {COMPLIANT / NON-COMPLIANT}
- Ports: ✓ internal only
- Auth: ✓ enabled

### Overall: COMPLIANT WITH WARNINGS (2 findings)
```

### Step 4: Act on Findings

- **Non-compliant controls:** `fleet_alert(severity="high", category="security")` + create fix task
- **Warnings:** Board memory `[security, compliance]` + track in next scan
- **All compliant:** Board memory confirmation + trail

## Integration With CRONs

Your compliance verification integrates with:
- **nightly-dependency-scan:** Covers dependency controls automatically
- **secret-scan (weekly):** Covers secret management controls
- **infrastructure-security-check:** Covers infrastructure controls

The compliance verification is the AGGREGATE view — combining findings from all your CRONs into a unified compliance posture.

## What Compliance Verification is NOT

- NOT vulnerability scanning (that's fleet-vulnerability-assessment)
- NOT incident response (that's fleet-incident-response)
- NOT threat modeling (that's fleet-threat-modeling)

This is ASSURANCE — verifying that controls already implemented are still functioning. The immune system for security.
