---
name: security
description: >
  Apply security best practices to code, architecture, and workflows. Trigger whenever
  the user mentions authentication, authorization, API keys, secrets, encryption,
  vulnerabilities, OWASP, SQL injection, XSS, CSRF, data exposure, penetration testing,
  security review, or asks "is this secure?". Also trigger proactively when reviewing
  code that handles user data, passwords, tokens, or network requests. When to trigger:
  during any code review pass when the diff touches auth, payments, user input, or API
  endpoints; proactively whenever secrets, tokens, or credentials appear in code; when
  the user explicitly asks for a security review or names a security concern; and when
  setting up new services, databases, or network-exposed components. Key capabilities:
  OWASP Top 10 coverage, secrets-in-code detection, JWT/session validation checks, BOLA/
  IDOR vulnerability screening, parameterized query enforcement, CORS and HTTPS audit,
  dependency CVE scanning via npm audit/pip-audit/snyk, and PII handling review.
  Findings are always reported by severity (Critical/High/Medium/Low) with concrete
  recommended fixes. Ideal for any developer who handles auth, payments, user data, or
  external APIs. Also useful for pre-commit hooks, CI security gates, and compliance-
  adjacent reviews (SOC2, GDPR) where attack surface must be documented.
---

# Security Skill

## When reviewing code or architecture, always check:

### Secrets & Credentials
- No hardcoded API keys, passwords, or tokens in source code
- Secrets loaded from environment variables or secret managers (Vault, AWS Secrets Manager, etc.)
- `.env` files in `.gitignore`

### Authentication & Authorization
- Verify JWT/session token validation on every protected route
- Check for broken object-level authorization (BOLA/IDOR)
- Enforce least-privilege principles
- MFA recommended for sensitive operations

### Input Validation
- Sanitize and validate all user inputs server-side
- Parameterized queries / ORM to prevent SQL injection
- Encode outputs to prevent XSS
- CSRF tokens on state-changing requests

### API Security
- Rate limiting on all public endpoints
- CORS configured restrictively
- HTTPS enforced everywhere
- Sensitive data not exposed in URLs or logs

### Dependency Security
- Flag outdated or CVE-listed packages
- Recommend `npm audit`, `pip-audit`, `snyk`, or equivalent

### Data Protection
- PII encrypted at rest and in transit
- Minimal data collection principle
- Proper error messages (no stack traces to users)

## Output Format
Always provide:
1. **Findings** — list of issues by severity (Critical / High / Medium / Low)
2. **Recommended Fix** — concrete code or config change for each finding
3. **Quick Wins** — top 3 things to fix immediately