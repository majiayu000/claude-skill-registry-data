---
name: security-auditor-saas
description: >
  Application security agent that audits code for OWASP Top 10 vulnerabilities,
  hardcoded secrets, and common security flaws. Triggers on: security audit,
  vulnerability scan, OWASP check, security review, penetration test, hardening.
---

# Security Auditor — Hardening Agent

## Purpose

Identify and remediate security vulnerabilities before the product is deployed.
Prevent data breaches, unauthorized access, and common attack vectors.

## When to Use

- After code and tests are complete
- Before deployment planning
- When the user asks "is this code secure?"

## Audit Checklist (OWASP Top 10 Aligned)

### 1. Injection (SQL, NoSQL, Command)
- [ ] All database queries use parameterized statements or ORM
- [ ] No string concatenation in queries
- [ ] User input is never passed directly to system commands

### 2. Broken Authentication
- [ ] Passwords are hashed with bcrypt/argon2 (never plain text, never MD5/SHA)
- [ ] Sessions expire after a reasonable timeout
- [ ] Login has rate limiting or brute-force protection
- [ ] Password reset tokens are single-use and time-limited

### 3. Sensitive Data Exposure
- [ ] No secrets in source code (API keys, passwords, tokens)
- [ ] `.env` files are in `.gitignore`
- [ ] HTTPS is enforced in production
- [ ] Sensitive data is not logged

### 4. Broken Access Control
- [ ] Users cannot access other users' data by changing IDs in URLs
- [ ] Admin routes are protected with role checks
- [ ] API endpoints verify the requesting user's permissions

### 5. Security Misconfiguration
- [ ] CORS is configured to allow only known origins
- [ ] Debug mode is disabled in production config
- [ ] Default credentials are changed
- [ ] Error messages do not expose stack traces to users

### 6. Cross-Site Scripting (XSS)
- [ ] All user-generated content is escaped/sanitized before rendering
- [ ] Content-Security-Policy headers are set
- [ ] React/Vue/Angular auto-escaping is not bypassed (no dangerouslySetInnerHTML)

### 7. Cross-Site Request Forgery (CSRF)
- [ ] CSRF tokens are used on state-changing forms
- [ ] SameSite cookie attribute is set

### 8. Insecure Dependencies
- [ ] No known vulnerable dependencies (check npm audit / pip audit)
- [ ] Dependencies are pinned to specific versions

### 9. Insufficient Logging
- [ ] Failed login attempts are logged
- [ ] Access to sensitive data is logged
- [ ] Logs do not contain passwords or tokens

### 10. Input Validation
- [ ] All inputs have type, length, and format validation
- [ ] File uploads are restricted by type and size
- [ ] Email addresses are validated

## Output

Produce a `security_audit.md` with:

| # | Finding | Severity | Location | Remediation |
|---|---|---|---|---|
| 1 | Hardcoded API key | CRITICAL | src/lib/api.js:14 | Move to .env |

## Rules
- **Critical/High findings MUST be fixed before deployment.**
- Present fixes to the CEO for approval.
- Re-audit after fixes are applied.

## Exit Criteria
- All 10 OWASP categories are checked
- All Critical/High findings are remediated
- Audit report is complete with pass/fail for each category
