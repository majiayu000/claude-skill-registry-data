---
name: security-review
model: reasoning
description: Meta-skill that orchestrates a comprehensive security review by coordinating auth, input validation, secrets management, API security, and infrastructure hardening skills. Use before releases, after auth changes, during audits, or when adding new API endpoints.
---

# Security Review (Meta-Skill)

Comprehensive security review by orchestrating multiple security-related skills into a single, repeatable workflow. This skill does not implement security controls itself — it routes each concern to the specialist skill best equipped to handle it.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install security-review
```


---

## Purpose

Most security gaps emerge at the seams between domains: auth is solid but input validation is missing, APIs are locked down but container images run as root. This skill ensures nothing falls through the cracks by systematically invoking every relevant security skill in a coordinated sequence.

| Does | Does NOT |
|------|----------|
| Defines a fixed review order so every area is covered | Implement fixes (delegates to the relevant skill) |
| Routes each concern to the specialist skill that owns it | Replace automated scanning tools (complements them) |
| Provides a unified checklist spanning OWASP Top 10 and beyond | Serve as a standalone security audit certification |
| Produces a severity-classified report with response-time expectations | |

---

## When to Use

- **Before release** — final security gate before code ships
- **After auth changes** — auth regressions are high-severity by default
- **During security audit** — structured walkthrough for auditors
- **New API endpoints** — every new surface area needs review
- **Handling user input** — input validation is the #1 attack vector
- **Dependency updates** — new deps may introduce vulnerabilities
- **Infrastructure changes** — container, K8s, or network config changes

---

## Orchestration Flow

Execute each area in order. Skip an area only if the project provably does not use that domain (e.g., skip step 5 if there are no smart contracts).

| Step | Skill to Read | Key Focus Areas |
|------|--------------|-----------------|
| **1. Auth & Authz** | auth-patterns | Session management, password hashing, MFA, RBAC/ABAC, OAuth/OIDC token validation |
| **2. Input & Errors** | error-handling-patterns | Server-side validation, parameterized queries, output encoding, safe error messages, file upload restrictions |
| **3. Dependencies** | quality-gates (security gates) | Known CVEs, lock file integrity, license compliance, pinned versions, base-image provenance |
| **4. API Security** | api-design-principles | Auth on every endpoint, rate limiting, request size limits, CORS policy, sensitive data in responses |
| **5. Smart Contracts** | solidity-security | Reentrancy, integer overflow, access control, oracle manipulation, upgrade proxies. *Skip if no contracts.* |
| **6. Infrastructure** | docker-expert, k8s-manifest-generator | Non-root users, minimal base images, no build-time secrets, network policies, resource limits, TLS |

---

## Skill Routing Table

| Security Concern | Skill | Path |
|-----------------|-------|------|
| Authentication & authorization | auth-patterns | `ai/skills/backend/auth-patterns/SKILL.md` |
| Input validation & error handling | error-handling-patterns | `ai/skills/backend/error-handling-patterns/SKILL.md` |
| Dependency scanning & security gates | quality-gates | `ai/skills/testing/quality-gates/SKILL.md` |
| API security & endpoint hardening | api-design-principles | `ai/skills/backend/api-design-principles/SKILL.md` |
| Smart contract vulnerabilities | solidity-security | `ai/skills/devops/solidity-security/SKILL.md` |
| Container security | docker-expert | `ai/skills/devops/docker/SKILL.md` |
| Kubernetes security | k8s-manifest-generator | `ai/skills/devops/kubernetes/k8s-manifest-generator/SKILL.md` |

---

## Security Checklist

Work through every item. Mark each as **Pass**, **Fail**, or **N/A**.

### OWASP Top 10

- [ ] **A01 Broken Access Control** — least-privilege enforced, deny by default
- [ ] **A02 Cryptographic Failures** — strong algorithms, no hard-coded keys
- [ ] **A03 Injection** — parameterized queries, no eval/exec on user input
- [ ] **A04 Insecure Design** — threat modeling performed, abuse cases considered
- [ ] **A05 Security Misconfiguration** — defaults changed, debug off in prod
- [ ] **A06 Vulnerable Components** — no known CVEs in dependency tree
- [ ] **A07 Auth Failures** — brute-force protection, secure password storage
- [ ] **A08 Data Integrity Failures** — signed updates, CI/CD pipeline integrity
- [ ] **A09 Logging Failures** — security events logged, no sensitive data in logs
- [ ] **A10 SSRF** — outbound requests validated, allowlist enforced

### Input Validation & Output Encoding

- [ ] All user input validated server-side (never trust client-only validation)
- [ ] Input length limits enforced
- [ ] File uploads restricted by type, size, and stored outside webroot
- [ ] HTML output encoded to prevent XSS
- [ ] No sensitive data in URLs or query parameters
- [ ] Security headers set (CSP, X-Frame-Options, HSTS, etc.)

### Authentication, Authorization & Sessions

- [ ] Passwords hashed with bcrypt/scrypt/argon2 (not MD5/SHA1)
- [ ] Session tokens regenerated after login, invalidated on logout
- [ ] Token expiry enforced (access tokens short-lived)
- [ ] Principle of least privilege applied to every role
- [ ] Failed login attempts rate-limited and logged
- [ ] Cookies marked Secure, HttpOnly, SameSite

### Cryptography

- [ ] TLS 1.2+ enforced for all connections
- [ ] No deprecated algorithms (DES, RC4, MD5 for integrity)
- [ ] Keys and certificates stored in secrets manager
- [ ] Key rotation schedule documented

### Error Handling & Logging

- [ ] Generic error messages returned to clients (no stack traces in prod)
- [ ] Security events logged with sufficient context
- [ ] Logs do not contain passwords, tokens, or PII

### Data Protection & Communication

- [ ] Sensitive data encrypted at rest
- [ ] PII access logged and auditable
- [ ] Data retention policies enforced
- [ ] All external communication over TLS
- [ ] Webhook endpoints validate signatures
- [ ] Internal service-to-service communication authenticated

---

## Severity Classification

| Severity | Definition | Response Time | Examples |
|----------|-----------|---------------|----------|
| **Critical** | Actively exploitable, data breach imminent | **Immediate** — stop release | RCE, SQL injection, auth bypass, exposed secrets |
| **High** | Exploitable with moderate effort | **24 hours** | Privilege escalation, XSS (stored), CSRF on state-changing ops |
| **Medium** | Exploitable under specific conditions | **1 week** | Information disclosure, missing rate limiting, verbose errors |
| **Low** | Minimal impact, defense-in-depth | **Next sprint** | Missing security headers, outdated non-vulnerable deps |

> **Rule:** Any **Critical** finding blocks the release. No exceptions, no waivers without CISO sign-off.

---

## Report Template

```markdown
# Security Review Report

**Project:** [name] | **Reviewer:** [name] | **Date:** YYYY-MM-DD
**Scope:** [components reviewed] | **Overall Risk:** Critical | High | Medium | Low

## Executive Summary
[2-3 sentence summary of findings and overall posture]

## Findings

### [FINDING-001] Title
- **Severity:** Critical | High | Medium | Low
- **Category:** OWASP A01-A10 | Input | Auth | Infra | ...
- **Location:** `path/to/file:line`
- **Description:** What the issue is
- **Impact:** What could happen if exploited
- **Remediation:** How to fix it — **Skill:** [which skill to apply]

## Checklist Summary

| Area | Pass | Fail | N/A |
|------|------|------|-----|
| OWASP Top 10 | | | |
| Input & Output | | | |
| Auth, Authz & Sessions | | | |
| Cryptography | | | |
| Error Handling & Logging | | | |
| Data & Communication | | | |

## Recommendations
1. [Priority-ordered actions]

## Sign-Off
- [ ] All Critical/High findings remediated
- [ ] Re-review scheduled for [date]
```

---

## NEVER Do

1. **NEVER skip a review area** — mark it N/A with justification, but never silently skip
2. **NEVER downgrade severity to unblock a release** — if it's Critical, it blocks
3. **NEVER store secrets in code, config files, or environment variables at build time** — use a secrets manager
4. **NEVER trust client-side validation alone** — always validate server-side
5. **NEVER expose stack traces, internal paths, or debug info in production** — generic errors only
6. **NEVER use deprecated cryptographic algorithms** — no MD5 for integrity, no SHA1 for signatures, no DES/RC4
7. **NEVER assume a dependency is safe because it is popular** — check CVE databases, audit lock files, pin versions
