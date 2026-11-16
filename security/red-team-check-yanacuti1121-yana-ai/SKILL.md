---
name: red-team-check
description: >
  Offensive security review of the current local codebase — scan for OWASP Top 10
  vulnerabilities, hardcoded secrets, misconfigurations, and broken access control.
  Use when the user asks to find security issues, audit the codebase for vulnerabilities,
  run a red team check, or scan for security bugs. Requires ownership confirmation via
  security-scope-gate before starting. Only runs against repos the user owns.
origin: yamtam
version: 1.0.0
compatibility: >
  Local codebase only. Requires security-scope-gate.md confirmation before starting.
  Does not make external HTTP requests. Does not exploit live systems.
---

<!-- Concept inspired by Strix (Apache 2.0) — scan mode taxonomy and OWASP framing.
     All content written original for YAMTAM. No code ported. -->

## When to Use

- User asks to "find security issues", "audit for vulnerabilities", "run red team"
- Before a major release or deploy to production
- After adding new auth, API endpoints, or user input handling
- When integrating a third-party library that handles sensitive data

Do NOT use:
- Against systems the user does not own (security-scope-gate will block)
- As a substitute for a full professional pentest on critical infrastructure

## Pre-condition: Security Scope Gate

**STOP. Before scanning, you MUST:**

1. Follow the confirmation flow in `gates/security-scope-gate.md`
2. Get explicit user confirmation of ownership/authorization
3. Log the confirmation to `.claude/state/security-scope-confirmations.log`
4. Only then proceed to Step 1 below

If the user has not confirmed, output the scope confirmation prompt from the gate
and wait. Do not begin scanning.

## Scan Modes

Choose the mode based on user request or context. Default is **quick**.

| Mode | Scope | Time | Output |
|------|-------|------|--------|
| quick | Secrets, obvious injections, config | < 5 min | CRITICAL only |
| targeted | Specific file/module/feature | 5–15 min | CRITICAL + HIGH |
| deep | Full codebase, all 10 OWASP categories | 15–60 min | Full finding list |

See `docs/security-scan-modes.md` for full taxonomy.

## How It Works

### Step 0 — Run Automated Tools (if available)

Before manual review, run the security tools script to get machine-detected findings:

```bash
YAMTAM_SCOPE_CONFIRMED=1 bash core/scripts/run-security-tools.sh --mode <quick|targeted|deep>
```

- If tools are installed: their output becomes **Hard Evidence** in the finding list
- If no tools installed: skip and proceed to Step 1 (manual only)
- Do NOT run this step if the user has said to skip tool execution
- Tool findings should be merged into the Step 3 finding list, not listed separately
- Reference: `docs/security-tools-setup.md` for installation guide

### Step 1 — Reconnaissance

Map the attack surface before scanning:
```
- List all input entry points: forms, API endpoints, CLI args, env vars
- Identify authentication and session handling files
- Identify files handling database queries
- Identify files handling file uploads or external URLs
- Identify dependency manifests (package.json, requirements.txt, go.mod, etc.)
```

Output a surface map before proceeding. Do not skip this step.

### Step 2 — Scan by OWASP Category

Work through each category. For each: check → document → move on.
Do not stop early unless user requests quick mode.

**A01 — Broken Access Control**
- IDOR: can resource IDs in URLs/bodies be manipulated to access other users' data?
- Missing auth checks on admin routes
- Horizontal privilege escalation paths

**A02 — Cryptographic Failures**
- Sensitive data (passwords, tokens, PII) stored or transmitted unencrypted
- Weak hashing (MD5, SHA1 for passwords — must be bcrypt/argon2/scrypt)
- Hardcoded secrets, API keys, connection strings in source

**A03 — Injection**
- SQL: unsanitized user input in queries
- Command injection: user input passed to shell commands
- Template injection: user input in render templates

**A04 — Insecure Design**
- Missing rate limits on auth endpoints (login, OTP, password reset)
- Race conditions in financial or state-changing operations
- Predictable resource identifiers

**A05 — Security Misconfiguration**
- Debug mode enabled in production config
- Default credentials not changed
- Verbose error messages exposing stack traces
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Exposed admin panels without auth

**A06 — Vulnerable and Outdated Components**
- Dependency versions with known CVEs
- Check: npm audit / pip-audit / govulncheck / cargo audit
- Container base images with outdated OS packages

**A07 — Identification and Authentication Failures**
- Weak password policy (no length/complexity minimum)
- Session tokens not invalidated on logout
- JWT: alg:none attack surface, symmetric key reuse

**A08 — Software and Data Integrity Failures**
- Unverified third-party scripts (CDN without SRI hash)
- CI/CD pipeline: can external contributors inject into build?
- Unsigned dependency installs

**A09 — Security Logging and Monitoring Failures**
- Auth failures not logged
- Admin actions not logged
- Logs containing PII or credentials

**A10 — Server-Side Request Forgery (SSRF)**
- User-controlled URLs fetched server-side without allowlist
- Webhook endpoints accepting arbitrary URLs
- Internal metadata endpoints reachable via redirect

### Step 3 — Output Finding List

For each finding:
```
[SEVERITY] Category: Title
  File: path/to/file.ext:line_number
  Description: what is wrong
  Reproduction: how to trigger
  Impact: what an attacker can do
  Recommendation: how to fix
```

Severity levels: CRITICAL / HIGH / MEDIUM / LOW / INFO

Always output a category coverage table even if 0 findings:
```
| Category | Status | Findings |
|----------|--------|---------|
| A01 Broken Access Control | SCANNED | 0 |
| A02 Cryptographic Failures | SCANNED | 2 |
...
```

## Gotchas

- Quick mode skips A04, A06, A08 — note this explicitly in output
- A06 requires running package audit commands — ask user before running `npm audit` if it may modify lock files
- Never suggest exploiting a finding beyond minimal PoC (no destructive payloads)
- If a finding involves credentials, redact the actual value in output

## Anti-Fake-Pass Rules

Before claiming the scan is complete, you MUST show:
- [ ] Category coverage table with SCANNED status for each OWASP category in scope
- [ ] Finding list (can be empty, but must be shown explicitly)
- [ ] Severity counts: X CRITICAL, Y HIGH, Z MEDIUM, W LOW
- [ ] Confirmation log entry (or bypass note)
- [ ] Tool run summary: which tools ran, which were skipped (or note "tools not run")

MUST NOT say "scan passed" or "no issues found" without showing the category table.
