---
name: security-review
description: When the user needs a security assessment — threat modeling, vulnerability review, auth flow audit, dependency scanning, or says "is this secure", "review for vulnerabilities", "threat model", "security audit", "pen test prep".
related: [code-review, architecture-design, soc2-prep]
reads: [startup-context]
origin: "startup"
---

# Security Review

## When to Use
- The user wants a security audit of their application, infrastructure, or specific feature
- They need a threat model before launching or a penetration test preparation review
- They have a dependency vulnerability alert and need remediation guidance
- They are handling sensitive data (PII, payment, health) and need verification
- Code audit, secrets detection, or compliance assessment is requested

## Context Required
From `startup-context`: tech stack, deployment environment, compliance requirements, data types. Also ask:
- **Scope** — Full app, feature, auth system, single PR, infrastructure, or cloud environment
- **Data types** — PII, payment, health, credentials, or other sensitive data handled
- **Compliance requirements** — SOC 2, HIPAA, PCI-DSS, GDPR, ISO 27001
- **Authorization** — Confirm written authorization exists before any active testing

## Workflow
Follow a five-phase methodology. Automated scanning precedes manual review. Authorization verification is mandatory before active testing.

1. **Scope definition** — Establish attack surface boundaries. Identify all components, data flows, and trust boundaries. Confirm authorization. Define in-scope and out-of-scope.
2. **Automated scanning** — Execute tooling before manual review:
   - **SAST:** `semgrep --config=auto` across the codebase
   - **Dependency audit:** `npm audit` / `pip-audit` / `govulncheck` / `trivy fs .`
   - **Secrets detection:** Scan for hardcoded credentials, API keys, tokens in source
   - **Container scanning:** `trivy image` for containerized deployments
   - Record all automated findings for validation in the next phase.
3. **Manual code review** — Conduct contextual analysis that automated tools miss:
   - Authentication and authorization flow tracing end-to-end
   - Business logic vulnerabilities (price manipulation, race conditions, privilege escalation)
   - Data flow analysis for sensitive information (where does PII enter, transit, and persist?)
   - STRIDE threat modeling against each component and data flow
4. **Validation and classification** — Test findings and assign severity:
   - Validate automated findings to eliminate false positives
   - Assign CVSS v3.1 scores; assess exploitability in context
   - Classify by business impact, not just technical severity
5. **Reporting** — Document vulnerabilities with precise locations, business impact, and corrective actions. Deliver a prioritized remediation roadmap.

## Output Format

```markdown
# Security Review: [Scope Description]

## Executive Summary
Overall risk posture (Critical / High / Medium / Low), top findings count, and business impact summary.

## Threat Model (STRIDE)
| Threat | Category | Asset | Impact | Likelihood | Risk |

## Findings
### Critical / High / Medium / Low
- **[SEC-N] Title** — CVSS X.X — file:line — description, business impact, remediation with code example

## Auth Flow Assessment
End-to-end trace of authentication and authorization with findings.

## Dependency Vulnerabilities
| Package | Current Version | CVSS | Fix Version | Exploitable in Context? |

## Remediation Roadmap
Prioritized action list with timelines.
```

## Frameworks & Best Practices

### STRIDE Threat Modeling
Apply to every component and data flow:
- **Spoofing** — Can attackers forge tokens or impersonate users? Are API keys rotatable?
- **Tampering** — Can requests be modified in transit? Are webhooks signed? Is data integrity verified?
- **Repudiation** — Are critical actions logged? Are logs tamper-evident?
- **Information Disclosure** — Stack traces in error responses? PII encrypted at rest and in transit?
- **Denial of Service** — Rate limits in place? Can one user exhaust resources for all?
- **Elevation of Privilege** — Can regular users access admin functions? Are role checks server-side?

### OWASP Top 10 Checks
1. **Injection** — Parameterize SQL/NoSQL; check OS commands, SSTI, LDAP
2. **Broken Auth** — argon2id/bcrypt, session timeout, rate limiting on login
3. **Data Exposure** — TLS 1.2+, PII encrypted at rest, HSTS headers
4. **XXE** — Disable DTD processing, prefer JSON over XML
5. **Access Control** — Server-side authz on every endpoint, no IDOR, CORS whitelist
6. **Misconfig** — Debug mode off, default credentials removed, security headers present
7. **XSS** — Output encoding, Content Security Policy, HTTP-only cookies
8. **Deserialization** — Validate schema, prefer JSON, reject untrusted serialized objects
9. **Vulnerable Deps** — `npm audit`, `pip-audit`, `trivy`, `govulncheck`
10. **Logging** — Auth events, admin actions, access violations logged with alerts

### CVSS v3.1 Scoring Guide
- **Critical (9.0-10.0):** RCE, auth bypass, full data breach, complete system compromise
- **High (7.0-8.9):** Privilege escalation, significant data exposure, SSRF to internal services
- **Medium (4.0-6.9):** Stored XSS, CSRF, limited IDOR, information disclosure
- **Low (0.1-3.9):** Missing security headers, minor info disclosure, verbose errors

### Auth Flow Checklist
- [ ] Passwords: argon2id or bcrypt (cost >= 10)
- [ ] JWT: 15-min access tokens, 7-day refresh tokens rotated on use
- [ ] Rate limiting: 5 attempts / 15 min on auth endpoints
- [ ] Sessions invalidated on password change
- [ ] OAuth state parameter validated, scoped API keys
- [ ] MFA enforced for admin accounts
- [ ] Password reset tokens are single-use and time-limited

### Scanning Tools
- **SAST:** `semgrep --config=auto` (all stacks), `bandit` (Python), `gosec` (Go), `eslint-plugin-security` (Node)
- **Dependencies:** `npm audit` / `pip-audit` / `govulncheck` / `trivy fs .`
- **Containers:** `trivy image`

### Mandatory Constraints
- Never test production without explicit written authorization
- Never exploit beyond proof-of-concept demonstration
- Always sequence automated scanning before manual review

### Remediation Priority
1. Actively exploitable + critical data — immediately
2. Auth/authz bypass — 24 hours
3. Injection — 48 hours
4. Data exposure / critical CVEs — 1 week
5. Config hardening — 2 weeks
6. Defense-in-depth — next sprint

## Related Skills
- `code-review` — chain when findings require code-level fixes and review
- `architecture-design` — chain when findings reveal architectural security flaws
- `soc2-prep` — chain when review is part of compliance preparation

## Examples

**Example prompt:** "Review the security of our user authentication system. We use JWT with Express."

**Good output snippet:**
```
# Security Review: JWT Authentication System

## Executive Summary
Risk posture: **Critical**. Hardcoded JWT secret and non-expiring tokens.

## Findings
### Critical (CVSS 9.8)
- **[SEC-1] Hardcoded JWT secret** — auth/config.js:3 — Secret is
  "supersecret123". Attacker can forge any token.
  **Fix:** Move to env var, generate with `openssl rand -base64 64`.

### Critical (CVSS 9.1)
- **[SEC-2] Tokens never expire** — auth/jwt.js:12 — No `expiresIn`.
  **Fix:** Set `expiresIn: '15m'`, implement refresh token rotation.
```
