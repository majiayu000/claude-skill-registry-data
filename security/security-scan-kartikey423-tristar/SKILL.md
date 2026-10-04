---
name: security-scan
description: Scan TriStar codebase for security vulnerabilities. Checks secrets, dependencies, injection vectors, authentication, Azure configuration, PII handling, and HTTP security. Produces severity-rated findings.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Scan Skill

## Prime Directive

**"Assume the code is insecure until proven otherwise."**

Systematically scan for security vulnerabilities across the full stack. Every finding gets a severity rating and remediation guidance.

## Process

### Step 1: Secrets Detection

Scan all files for hardcoded secrets:
- API keys, passwords, tokens, connection strings, private keys
- Check that `.env` is in `.gitignore`
- Exclude: `.env.example`, documentation files, test fixtures with obviously fake values

### Step 2: Dependency Audit

Run dependency vulnerability scanners:
- Frontend: `npm audit --audit-level=moderate` (if package.json exists)
- Backend: `pip-audit` (if requirements.txt or pyproject.toml exists)
- Flag any high or critical vulnerabilities

### Step 3: Injection Vulnerabilities

Scan for injection vectors:
- **SQL Injection**: string concatenation in SQL queries, missing parameterized statements
- **XSS**: raw HTML injection patterns in React components, unsanitized user input in DOM
- **Command Injection**: unsafe shell invocations, user input reaching system commands
- **Prompt Injection**: user input passed directly into Claude API prompts without sanitization

### Step 4: Authentication and Authorization

Check auth implementation:
- JWT secret strength (not default dev values in production config)
- JWT expiry configured (should be 1 hour)
- JWT verification on all protected routes
- No routes that should be protected but are public

### Step 5: Azure Configuration Review

Check Azure-specific security:
- Key Vault usage for secrets (not environment variables in production)
- CORS restricted (no wildcard origins in production config)
- HTTPS enforced in production
- Managed identity for Azure service access
- No inline secrets in Azure configuration files

### Step 6: PII and Data Privacy (TriStar-Specific)

Scan for PII handling violations:
- Grep log statements for member names, emails, addresses, phone numbers
- Verify only member_id appears in log output
- Check Claude API prompts for member PII inclusion
- Verify GPS coordinates are not logged in plaintext
- Check error responses for PII leakage

### Step 7: CORS and HTTP Security

Check HTTP security headers and configuration:
- CORS origins (should not be wildcard in production)
- Security headers: X-Content-Type-Options, X-Frame-Options, HSTS
- Content-Security-Policy header
- Rate limiting configuration

## Output Format

```markdown
# Security Scan Report

## Summary
- **Date**: <date>
- **Files Scanned**: N
- **Critical**: N | **High**: N | **Medium**: N | **Low**: N | **Info**: N

## Findings

### Critical
1. **[CRITICAL] SEC-001**: <title>
   - **File**: <path:line>
   - **Description**: <what was found>
   - **Impact**: <what could happen>
   - **Remediation**: <how to fix>
   - **OWASP**: <relevant OWASP category>

### High / Medium / Low / Info
...

## Dependency Audit
| Package | Severity | CVE | Fix Version |

## PII Audit
- Log statements checked: N
- PII violations found: N
- GPS data in logs: YES/NO

## Verdict
PASS / FAIL (any Critical or High = FAIL)
```

## Severity Definitions

- **Critical**: Actively exploitable. Immediate fix required.
- **High**: Serious vulnerability. Fix before deployment.
- **Medium**: Requires specific conditions. Fix in current sprint.
- **Low**: Minor concern. Fix when convenient.
- **Info**: Best practice recommendation.

## Reference Files

- `references/owasp-top10.md` - OWASP Top 10 with TriStar remediation patterns
- `references/azure-security-checklist.md` - Azure-specific security checklist
