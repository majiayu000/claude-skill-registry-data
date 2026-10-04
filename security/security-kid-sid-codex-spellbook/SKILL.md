---
name: security
description: Application security guidance covering OWASP Top 10 mitigations, secrets handling, boundary validation, SQL injection prevention, JWT usage, dependency scanning, and STRIDE threat modeling. Use for audits, auth changes, or any security-sensitive code.
---

# Security

Secure the system at boundaries, minimize trust, and make risky behavior explicit in code, configuration, and review.

## When to Activate

- Add a new auth or authorization flow
- Handle user input at an external boundary
- Write database queries or ORM filters
- Review secrets, tokens, or credential handling
- Audit dependencies for known vulnerabilities
- Threat-model a new feature or integration
- Review logging for security-critical events

## OWASP Quick Reference

| Risk | Default Mitigation |
| --- | --- |
| Broken access control | Enforce authorization on every sensitive action |
| Cryptographic failures | Use standard libs and managed secrets |
| Injection | Parameterized queries, escaped templates |
| Insecure design | Threat-model before shipping privileged flows |
| Security misconfiguration | Harden defaults, disable debug in production |
| Vulnerable components | Scan dependencies continuously |
| Identification/auth failures | Strong session rotation and token expiry |
| Integrity failures | Verify signed artifacts and trusted inputs |
| Logging/monitoring failures | Emit actionable audit logs |
| SSRF | Restrict outbound targets and metadata access |

## Secrets and Boundary Validation

| Preferred | Avoid |
| --- | --- |
| Runtime environment variables or secret managers | Hardcoded tokens in source |
| `.env.example` placeholders | Real secrets in sample files |
| Secret rotation playbooks | Long-lived shared credentials |

Rules:

- Validate at request, message, CLI, and job-input boundaries.
- Convert external data into typed internal models once.
- Do not scatter ad hoc validation deep inside core logic unless it enforces domain invariants.

## SQL Injection and JWTs

BAD

```python
query = f"SELECT * FROM users WHERE email = '{email}'"
cursor.execute(query)
```

GOOD

```python
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

GOOD

```ts
await db.query("SELECT * FROM users WHERE email = $1", [email]);
```

| Rule | Why |
| --- | --- |
| Keep JWT lifetimes short | Limits replay window |
| Validate `iss`, `aud`, `exp`, `nbf` | Prevents token confusion |
| Prefer asymmetric signing for distributed verification | Better key separation |
| Store refresh tokens securely and revoke on reuse | Limits session theft |
| Never put secrets or mutable authorization state in JWT payloads | Tokens are bearer artifacts |

## Dependency Scanning and STRIDE

| Frequency | Action |
| --- | --- |
| On every PR | Scan manifests and lockfiles |
| Weekly | Review new advisories for production dependencies |
| Before release | Confirm no unresolved critical issues |

| Threat | Ask |
| --- | --- |
| Spoofing | Can an attacker impersonate a principal? |
| Tampering | Can data be altered without detection? |
| Repudiation | Is there enough audit evidence? |
| Information Disclosure | Can sensitive data leak? |
| Denial of Service | Can work queues or endpoints be exhausted? |
| Elevation of Privilege | Can low-privilege actors cross boundaries? |

BAD

```ts
const token = process.env.JWT_SECRET || "dev-secret";
```

GOOD

```ts
const token = env.JWT_SECRET;
```

## Checklist

- [ ] Secrets are loaded from runtime configuration, not source
- [ ] External input is validated once at the boundary
- [ ] Queries use parameters rather than string interpolation
- [ ] JWTs validate issuer, audience, and expiry claims
- [ ] Sensitive operations emit audit-grade logs
- [ ] Dependency scanning is part of CI or release checks
- [ ] STRIDE risks were considered for new privileged flows
