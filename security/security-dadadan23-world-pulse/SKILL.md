---
name: "security"
description: 'Implement production security practices covering OWASP Top 10, input validation, injection prevention, and secrets management. Use when hardening applications against vulnerabilities, implementing authentication/authorization, managing secrets, configuring HTTPS/TLS, or conducting security audits.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Security

> **Purpose**: Language-agnostic security practices to protect against common vulnerabilities. 
> **Focus**: Input validation, injection prevention, authentication, secrets management. 
> **Note**: For language-specific implementations, see [C# Development](../../development/csharp/SKILL.md) or [Python Development](../../development/python/SKILL.md).

---

## When to Use This Skill

- Hardening applications against OWASP Top 10
- Implementing authentication and authorization
- Managing secrets and credentials securely
- Configuring HTTPS/TLS
- Conducting security audits

## Prerequisites

- OWASP Top 10 awareness
- Understanding of HTTP security headers

## Decision Tree

```
Security concern?
+- User input? -> VALIDATE + SANITIZE (see Input Validation)
| +- Goes into SQL? -> Parameterized queries ONLY
| +- Goes into HTML? -> Encode output (XSS prevention)
| - Goes into shell? -> Avoid; use SDK/API instead
+- Authentication?
| +- New system? -> Use established provider (OAuth2/OIDC)
| - Existing? -> Verify token validation, session management
+- Secrets/credentials?
| +- In code? -> REMOVE -> use env vars or vault
| - In config? -> Move to secrets manager
| - Run: scripts/scan-secrets.ps1 to verify
+- Dependencies?
| - Run: scripts/scan-security.ps1 -> update vulnerable packages
- Deployment?
 - HTTPS only, security headers, CORS configured
```

## OWASP Top 10 (2025)

1. **Broken Access Control** - Authorization failures, privilege escalation
2. **Cryptographic Failures** - Weak encryption, exposed secrets
3. **Injection** - SQL, NoSQL, command, LDAP injection
4. **Insecure Design** - Missing security controls in architecture
5. **Security Misconfiguration** - Default configs, unnecessary features enabled
6. **Vulnerable Components** - Outdated dependencies with known CVEs
7. **Authentication Failures** - Weak passwords, broken session management
8. **Software/Data Integrity** - Unsigned updates, insecure CI/CD
9. **Logging/Monitoring Failures** - Missing audit logs, delayed detection
10. **Server-Side Request Forgery (SSRF)** - Unvalidated URLs, internal network access

---

## Security Checklist

**Before Production:**
- [ ] All user input validated and sanitized
- [ ] SQL queries use parameterized statements
- [ ] Passwords hashed with bcrypt/Argon2
- [ ] Secrets in environment variables or vault
- [ ] HTTPS enforced with HSTS
- [ ] Security headers configured
- [ ] Authentication and authorization implemented
- [ ] Rate limiting on authentication endpoints
- [ ] CORS configured restrictively
- [ ] Dependencies scanned for vulnerabilities
- [ ] Sensitive data encrypted at rest
- [ ] Security audit logs enabled
- [ ] Error messages don't leak sensitive info
- [ ] File uploads validated and scanned
- [ ] API endpoints have input size limits

---

## Resources

**Security Standards:**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org)
- [CWE Top 25](https://cwe.mitre.org/top25/)

**Tools:**
- **Dependency Scanning**: Snyk, Dependabot, OWASP Dependency-Check
- **SAST**: SonarQube, CodeQL, Semgrep
- **DAST**: OWASP ZAP, Burp Suite
- **Secrets Scanning**: GitGuardian, TruffleHog, git-secrets

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md)

**Last Updated**: January 27, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`scan-secrets.ps1`](scripts/scan-secrets.ps1) | Scan repo for hardcoded secrets, API keys, credentials | `./scripts/scan-secrets.ps1 [-Path ./src]` |
| [`scan-secrets.sh`](scripts/scan-secrets.sh) | Cross-platform secrets scanner (bash) | `./scripts/scan-secrets.sh --path ./src` |
| [`scan-security.ps1`](scripts/scan-security.ps1) | Scan dependencies for known vulnerabilities | `./scripts/scan-security.ps1 [-FailOn critical]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| SQL injection detected | Use parameterized queries, never concatenate user input into SQL |
| JWT token expired errors | Implement token refresh flow, check clock skew between services |
| Secrets exposed in logs | Use structured logging with secret redaction, never log request bodies with credentials |

## References

- [Input Validation Injection](references/input-validation-injection.md)
- [Auth Patterns](references/auth-patterns.md)
- [Secrets Tls Vulnerabilities](references/secrets-tls-vulnerabilities.md)