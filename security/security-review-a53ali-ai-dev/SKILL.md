---
name: security-review
description: Conduct an OWASP-aligned security review of a feature, pull request, or system design. Identify threats using STRIDE, check OWASP Top 10 risks, and produce a prioritized remediation checklist. Designed to be embedded in the PR and design review workflow.
triggers:
  - "security review"
  - "threat model"
  - "OWASP"
  - "security audit"
  - "pen test"
  - "auth vulnerability"
  - "is this secure"
audience:
  - engineer
  - manager
---

# Security Review

Systematically identify and remediate security vulnerabilities in code, APIs, and system designs.

---

## STRIDE Threat Model

Apply STRIDE to any new feature or system boundary:

| Threat | Question to Ask | Example |
|---|---|---|
| **S**poofing | Can an attacker impersonate a user or service? | Weak auth tokens, no service-to-service mTLS |
| **T**ampering | Can data be modified in transit or at rest? | No HTTPS, unverified JWT signatures |
| **R**epudiation | Can a user deny performing an action? | No audit log, no tamper-evident logging |
| **I**nformation Disclosure | Can an attacker read data they shouldn't? | Verbose error messages, misconfigured S3 buckets |
| **D**enial of Service | Can the system be made unavailable? | No rate limiting, unbounded query results |
| **E**levation of Privilege | Can an attacker gain more permissions? | Broken authorization, IDOR vulnerabilities |

---

## OWASP Top 10 Checklist (2021)

For each item, check: **Does this feature or change touch this risk area?**

### A01 — Broken Access Control
- [ ] Every endpoint enforces authorization (not just authentication)
- [ ] Object-level authorization: can User A access User B's resource?
- [ ] Function-level authorization: can a regular user call admin endpoints?
- [ ] No direct object references expose internal IDs without access check

### A02 — Cryptographic Failures
- [ ] Sensitive data encrypted at rest (PII, credentials, health data)
- [ ] TLS 1.2+ enforced; no HTTP fallback in prod
- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] Secrets not hardcoded in source or environment variables in CI logs

### A03 — Injection
- [ ] All SQL uses parameterized queries / ORM (no string concatenation)
- [ ] User input validated and sanitized before use in queries, commands, templates
- [ ] NoSQL queries protected (MongoDB `$where`, etc.)
- [ ] XML/HTML output encoded to prevent XSS

### A04 — Insecure Design
- [ ] Threat model done before feature shipped (this document)
- [ ] No security-sensitive logic on client side only
- [ ] Rate limiting designed in, not bolted on

### A05 — Security Misconfiguration
- [ ] Default credentials changed / disabled
- [ ] Error messages don't expose stack traces or system info to users
- [ ] CORS policy is restrictive (not `*`)
- [ ] HTTP security headers set (CSP, HSTS, X-Frame-Options)

### A06 — Vulnerable and Outdated Components
- [ ] Dependencies scanned (Dependabot, Snyk, or equivalent)
- [ ] No known CVEs in direct dependencies
- [ ] License compliance checked for new packages

### A07 — Identification and Authentication Failures
- [ ] Session tokens are random, long, invalidated on logout
- [ ] MFA available for sensitive operations
- [ ] Account lockout / rate limiting on login endpoints
- [ ] Password reset flow uses time-limited, single-use tokens

### A08 — Software and Data Integrity Failures
- [ ] CI/CD pipeline integrity: no arbitrary code execution in build steps
- [ ] Dependency checksums verified (lock files committed)
- [ ] Deserialization of untrusted data avoided or validated

### A09 — Security Logging and Monitoring Failures
- [ ] Authentication events logged (success and failure)
- [ ] Access control failures logged with user context
- [ ] Logs are structured, tamper-resistant, and retained per policy
- [ ] Alerts exist for anomalous patterns (brute force, mass data access)

### A10 — Server-Side Request Forgery (SSRF)
- [ ] URL inputs validated against allowlist (not blocklist)
- [ ] Internal metadata endpoints (AWS 169.254.x.x) protected
- [ ] HTTP redirects validated before following

---

## PR Security Review Template

Add to PR description or review comment:

```markdown
## Security Review

**Feature**: [name]
**Reviewer**: [name]
**Date**: [date]

### STRIDE Summary
| Threat | Risk | Mitigated? |
|---|---|---|
| Spoofing | [Low/Med/High] | [Yes/No/Partial] |
| Tampering | | |
| Repudiation | | |
| Info Disclosure | | |
| DoS | | |
| Elevation of Privilege | | |

### OWASP Top 10 Flags
- [ ] A01 Access Control — [finding or "clear"]
- [ ] A02 Crypto — [finding or "clear"]
- [ ] A03 Injection — [finding or "clear"]
- [ ] A07 Auth — [finding or "clear"]

### Findings
| Severity | Finding | Recommendation |
|---|---|---|
| Critical | [description] | [fix] |
| High | | |
| Medium | | |

### Sign-off
[ ] No critical or high findings unresolved before merge
```

---

## Severity Definitions

| Severity | Definition | SLA |
|---|---|---|
| **Critical** | Direct data breach or account takeover possible | Block merge; fix immediately |
| **High** | Significant security risk, likely exploitable | Fix before release |
| **Medium** | Security weakness, not immediately exploitable | Fix within sprint |
| **Low** | Defense-in-depth improvement | Track in backlog |
| **Info** | Best practice recommendation | Optional |

---

## Common Vulnerabilities by Stack

### REST APIs
- Missing auth on internal endpoints ("it's internal" is not a security control)
- Returning full DB objects instead of filtered projections (mass assignment)
- No pagination limits on list endpoints (DoS via large page size)

### Frontend / Web
- `dangerouslySetInnerHTML` or `innerHTML` with user content
- Storing tokens in `localStorage` (prefer `httpOnly` cookies)
- Overly permissive CSP (`unsafe-inline`, `unsafe-eval`)

### Infrastructure / Cloud
- Public S3 buckets or storage blobs
- Overly permissive IAM roles (star permissions)
- Secrets in environment variables visible in process list or CI logs

### Authentication
- JWTs not validated on every request (trusting claims without verifying signature)
- `alg: none` accepted in JWT verification
- Long-lived tokens without refresh

---

## References
- [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [STRIDE Threat Modeling](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- Martin Fowler: [Security in Software Development](https://martinfowler.com/tags/security.html)
