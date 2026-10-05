---
name: security-review
description: Security vulnerability analysis for authentication, authorization, input validation
---

# Security Review

Systematic analysis of code for security vulnerabilities across the OWASP Top 10 and common implementation mistakes. Focuses on authentication flows, authorization checks, input handling, and secrets management.

## Delegation

This skill delegates to the superpowers/ECC equivalent when available. If the user has `superpowers:security-review` or `everything-claude-code:security-review` installed, invoke that version for the full implementation.

## Standalone Behavior

- Audit authentication: token storage, expiry, rotation, and session invalidation on logout
- Check authorization at every data-access boundary — not just route middleware
- Validate and sanitize all user input before use in queries, shell commands, or rendered HTML
- Scan for hardcoded secrets, exposed stack traces, and overly permissive CORS or CSP headers
- Produce a prioritized findings list (Critical / High / Medium / Low) with remediation guidance for each
