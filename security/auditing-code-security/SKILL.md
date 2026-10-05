---
name: auditing-code-security
description: Audit code against OWASP Top 10 vulnerabilities with structured findings. Use when reviewing code for security issues or conducting security audits.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
  argument-hint: [file-or-directory]
  stability: stable
  content-hash: sha256:ff6c21be83f8cbf0dd2b5abc6e5234ee06f462b4737d1c835c5caf89c048bd12
---

# OWASP Top 10 Code Security Audit

**Scope**: $ARGUMENTS

## When to Use

- Security review before release or merge
- Auditing new features for vulnerability exposure
- Periodic security posture assessment
- Compliance-driven code review

## Workflow

1. **Identify scope** — files, modules, or full codebase
2. **Scan each OWASP category** using the checklist below
3. **Record findings** in the output table
4. **Assign severity** (Critical / High / Medium / Low / Info)
5. **Propose remediation** for each finding

## Workflow Mode (full-codebase scope)

When auditing a **whole codebase or many modules** and the **Workflow tool is
available**, fan the ten OWASP categories out in parallel instead of scanning
them one after another:

```js
Workflow({
  scriptPath: "${CLAUDE_PLUGIN_ROOT}/workflows/audit-owasp.js",
  args: { scope: "<dir>",
          skillPath: "${CLAUDE_PLUGIN_ROOT}/skills/auditing-code-security/SKILL.md" }
})
```

`args` reaches the script as a JSON string (the script parses it). One read-only
agent scans the scope per category (A01–A10) and returns structured findings;
render them with the Output Format below. Fall back to the inline per-category
scan (steps 1–5) when the Workflow tool is unavailable. The agents are
read-only, so the only permission to pre-grant is the Workflow tool.

## OWASP Top 10 Checklist

### A01: Injection

- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] OS command execution uses allowlists, not user input
- [ ] LDAP queries use proper escaping
- [ ] XPath queries parameterized
- [ ] ORM queries avoid raw SQL where possible

### A02: Broken Authentication

- [ ] Passwords hashed with bcrypt/scrypt/argon2 (not MD5/SHA1)
- [ ] Session tokens are cryptographically random
- [ ] Session expiration and rotation implemented
- [ ] Multi-factor authentication available for sensitive operations
- [ ] Account lockout or rate limiting on login

### A03: Cross-Site Scripting (XSS)

- [ ] Output encoding applied for HTML, JS, CSS, URL contexts
- [ ] Reflected input never rendered without sanitization
- [ ] Stored user content sanitized before display
- [ ] DOM manipulation uses safe APIs (textContent, not innerHTML)
- [ ] Content-Security-Policy headers configured

### A04: Insecure Direct Object References

- [ ] Authorization checked before resource access
- [ ] Object IDs not guessable (use UUIDs or indirect references)
- [ ] Horizontal privilege escalation prevented
- [ ] File paths validated (no directory traversal)

### A05: Security Misconfiguration

- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Error messages don't expose stack traces or internals
- [ ] Unnecessary HTTP methods disabled
- [ ] Security headers present (HSTS, X-Frame-Options, etc.)

### A06: Sensitive Data Exposure

- [ ] PII encrypted at rest and in transit
- [ ] TLS 1.2+ enforced for all connections
- [ ] Sensitive data not logged
- [ ] API responses don't over-expose data
- [ ] Cache-Control headers prevent caching of sensitive responses

### A07: Missing Function-Level Access Control

- [ ] Every endpoint checks authentication
- [ ] Role-based authorization enforced server-side
- [ ] Admin functions not accessible to regular users
- [ ] API routes match UI access controls

### A08: Cross-Site Request Forgery (CSRF)

- [ ] Anti-CSRF tokens on state-changing requests
- [ ] SameSite cookie attribute set
- [ ] Origin/Referer header validation
- [ ] State-changing operations require POST/PUT/DELETE (not GET)

### A09: Using Components with Known Vulnerabilities

- [ ] Dependencies up to date
- [ ] No packages with known CVEs
- [ ] Dependency lock files committed
- [ ] Automated vulnerability scanning in CI

### A10: Server-Side Request Forgery (SSRF)

- [ ] User-supplied URLs validated against allowlist
- [ ] Internal network access blocked from user-controlled requests
- [ ] DNS rebinding protections in place
- [ ] Redirect chains limited and validated

## Output Format

Present findings as:

| # | Category | Severity | File:Line | Description | Remediation |
|---|----------|----------|-----------|-------------|-------------|
| 1 | A01 Injection | Critical | `src/db.py:42` | Raw SQL with f-string | Use parameterized query |
| 2 | A03 XSS | High | `templates/profile.html:18` | Unescaped user input | Apply output encoding |

### Severity Definitions

- **Critical** — Exploitable now, data breach or RCE risk
- **High** — Exploitable with moderate effort, significant impact
- **Medium** — Requires specific conditions, limited impact
- **Low** — Minor issue, defense-in-depth concern
- **Info** — Best practice recommendation, no direct risk
