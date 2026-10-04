---
name: security
description: Application security practices — OWASP Top 10 mitigations, secret management, dependency scanning, and secure coding patterns for web and API projects.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# security

Application security practices — OWASP Top 10 mitigations, secret management, dependency scanning, and secure coding patterns for web and API projects.

## Instructions

Apply these security practices when writing, reviewing, or auditing code:

### OWASP Top 10 Mitigations

**A01 – Broken Access Control**
- Enforce authorisation on every server-side route/endpoint, not just the UI
- Use deny-by-default: explicitly grant permissions, never assume
- Validate that the requesting user owns the resource they're accessing

**A02 – Cryptographic Failures**
- Never roll your own crypto — use established libraries (`bcrypt`, `argon2`, `libsodium`)
- Minimum password hashing: bcrypt with cost ≥ 12 or argon2id
- TLS 1.2+ for all connections; enforce HSTS
- Encrypt sensitive data at rest (PII, payment data, health records)

**A03 – Injection**
- Use parameterised queries / prepared statements — never string-concatenate SQL
- Validate and sanitise all user input at the boundary
- Use an allowlist for input validation, not a denylist
- Escape output context-appropriately (HTML, JSON, shell, URL)

**A05 – Security Misconfiguration**
- Remove default credentials and unused features/endpoints
- Set security headers: `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`
- Disable directory listing and server version disclosure
- Use environment-specific configs; never commit `.env` files

**A06 – Vulnerable and Outdated Components**
- Run `npm audit` / `pip-audit` / `trivy fs .` regularly
- Enable Dependabot or Renovate for automated dependency updates
- Pin dependency versions in lockfiles

**A07 – Identification and Authentication Failures**
- Enforce MFA for admin accounts
- Use secure session tokens (≥ 128 bits of entropy); regenerate after login
- Implement rate limiting and account lockout on login endpoints
- Use `HttpOnly`, `Secure`, `SameSite=Strict` on session cookies

**A09 – Security Logging and Monitoring Failures**
- Log authentication events (success, failure, lockout)
- Log access control failures
- Never log passwords, tokens, or PII
- Alert on anomalous patterns (multiple failures, unusual hours)

### Secret Management

- **Never** hardcode secrets in source code
- Use environment variables for local development (`.env` in `.gitignore`)
- Use a secrets manager in production: AWS Secrets Manager, HashiCorp Vault, GitHub Actions secrets
- Rotate secrets regularly; revoke immediately if exposed
- Use `git-secrets`, `gitleaks`, or `trufflehog` in pre-commit hooks to catch leaks

```bash
# Scan repo history for secrets
trufflehog git file://. --only-verified

# Scan staged changes
gitleaks detect --staged
```

### Dependency Scanning

Run dependency audits as part of CI:

```bash
# Node.js
npm audit --audit-level=high

# Python
pip-audit

# Docker images
trivy image myapp:latest

# Filesystem (any language)
trivy fs --security-checks vuln .
```

### Secure Coding Patterns

**Rate limiting (Express.js example):**
```js
import rateLimit from 'express-rate-limit';
const loginLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 10 });
app.post('/login', loginLimiter, loginHandler);
```

**Parameterised queries:**
```python
# Bad
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
# Good
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Security headers (Helmet.js):**
```js
import helmet from 'helmet';
app.use(helmet());
```

## Examples

```bash
# Run full vulnerability scan
trivy fs --exit-code 1 --severity HIGH,CRITICAL .

# Check npm dependencies
npm audit --audit-level=moderate

# Detect secrets in git history
trufflehog git file://. --only-verified --fail

# Generate SBOM for compliance
syft . -o spdx-json > sbom.json
```

## References

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Trivy](https://github.com/aquasecurity/trivy)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
