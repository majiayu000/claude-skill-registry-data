---
name: security-audit
description: Run a security audit of a module or PR. Use when asked to check security or before merging sensitive changes.
context: fork
agent: Explore
---

# Security Audit

Audit the code for security vulnerabilities: $ARGUMENTS

## OWASP Top 10 Checks

See [owasp-checklist.md](./owasp-checklist.md) for full checklist.

## Process

1. Read all files in the target path
2. Check against each OWASP category
3. Look for hardcoded secrets (grep for KEY, SECRET, PASSWORD, TOKEN)
4. Check for SQL injection vectors
5. Check for XSS vectors
6. Check for broken access control
7. Report findings with severity: Critical/High/Medium/Low
