---
name: security-baseline
description: Security requirements, threats, and controls that apply across this system.
---

# Security Baseline

## Threat Model (High Level)

- Primary users: [internal / external]
- Assets to protect:
  - [e.g., customer PII, payment data, secrets]
- Primary threats:
  - [e.g., unauthorized access, data exfiltration, data tampering]

## Required Controls

### Authentication

- Use [e.g., OAuth2 / OIDC / SSO] for user identity.
- Never build custom password handling if avoidable.

### Authorization

- Enforce least privilege.
- Centralize authorization decisions when possible.

### Input Validation & Output Encoding

- Validate all untrusted input at boundaries.
- Sanitize or encode output where appropriate (HTML, JSON, SQL, etc.).

### Secrets Management

- Store secrets in [vault / secret manager], never in code or config files.
- Rotate secrets according to policy.

### Logging & Auditing

- Log security-relevant events:
  - Logins, permission changes, critical operations.
- Avoid logging sensitive data.

## Common Vulnerabilities

See `vulnerabilities.md` for patterns to search for and avoid.

## Security Testing Requirements

See `security-testing.md` for:
- Required automated checks
- Manual review steps for critical flows
