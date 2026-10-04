---
name: fleet-security-contribution
description: How DevSecOps produces security_requirement contributions — specific actionable controls, not generic advice. Threat assessment, auth, input validation, deps, secrets.
user-invocable: false
---

# DevSecOps Security Contribution

## The Principle

Security at EVERY phase, not just review. DevSecOps provides security
requirements BEFORE implementation — the engineer sees them as constraints
during work stage. Not a final checkpoint. A layer that runs alongside.

## When This Applies

The brain creates a `security_requirement` contribution task when:
- A story/epic enters REASONING stage AND touches auth, data, external calls, deps, or permissions
- The contribution is conditional — not every task needs security input
- But when it applies, it's REQUIRED (the brain blocks work without it)

## Step 1: Gather Context

Call `sec_contribution(task_id)` — your group call that gathers:
- Verbatim requirement
- Task description
- Delivery phase
- Architect's design input (if available)

## Step 2: Assess Security Implications

For EACH aspect of the task, ask:

### Authentication & Authorization
- Does this involve auth? What method? (JWT, session, API key, OAuth)
- What signing algorithm? (RS256, not HS256)
- Token storage? (httpOnly cookies, not localStorage)
- Permission model? (RBAC, ABAC, scope-based)
- Session management? (expiry, refresh, revocation)

### Input Validation
- Does this accept user input? Where? What form?
- What sanitization is needed? (HTML encoding, SQL parameterization, path traversal prevention)
- What validation rules? (type, length, range, format, allowlist)
- File uploads? (type validation, size limits, storage location)

### Dependencies
- New dependencies added? Check against CVE databases
- Version pinning? (exact versions in requirements.txt, SHA pinning for GitHub Actions)
- License compatibility?
- Maintenance status? (last commit, open issues, known vulnerabilities)

### Secrets Management
- Does this handle secrets? (API keys, tokens, passwords, connection strings)
- Storage method? (environment variables via .env, never in code or config files)
- Rotation plan? (how to rotate without downtime)
- Access scope? (principle of least privilege)

### Network & External Calls
- External API calls? (allowlist, TLS required, timeout handling)
- Internal service communication? (authentication between services)
- DNS resolution? (trusted resolvers only)
- Rate limiting? (both outbound and inbound)

### File & Permission Security
- File permissions? (no world-writable, no 777)
- Directory access? (no path traversal, sandboxed)
- Temporary files? (secure creation, cleanup)

## Step 3: Produce SPECIFIC Requirements

**This is the critical distinction.** Generic advice is useless.
Specific, actionable controls are requirements.

### BAD (generic — useless)
- "Be secure"
- "Handle auth properly"
- "Validate input"
- "Use best practices for secrets"

### GOOD (specific — actionable)
- "Use JWT with RS256 signing (not HS256). Store tokens in httpOnly cookies with Secure and SameSite=Strict flags."
- "Pin GitHub Actions to SHA, not tags: `uses: actions/checkout@8e5e7e5ab8b370d6c329ec480221332ada57f0ab`"
- "Sanitize all input on /api/search endpoint using parameterized queries. No string concatenation in SQL."
- "Store API keys in .env (gitignored), load via python-dotenv. Never in config.py or YAML."
- "Rate limit the /api/auth/login endpoint to 5 attempts per minute per IP. Return 429 after limit."

## Step 4: Phase-Appropriate Security Depth

| Phase | Security Depth |
|-------|---------------|
| poc | No secrets in code. Basic input validation. That's it. |
| mvp | Auth implemented. Input validated at boundaries. Deps pinned. Secrets in env. |
| staging | Dep audit done. Pen-test mindset applied. Auth hardened. Network boundaries defined. |
| production | Certified. Compliance verified. All findings resolved. Monitoring for security events. |

A POC does NOT need a full threat model. A production feature does NOT
get away with "we'll add auth later."

## Step 5: Deliver

```
fleet_contribute(
  task_id=TARGET_TASK_ID,
  contribution_type="security_requirement",
  content=YOUR_SPECIFIC_REQUIREMENTS
)
```

## Step 6: During Review — Security Review

When the task enters review, call `sec_pr_security_review(task_id)`.
Check the PR against your requirements:
- Did the engineer follow your auth specification?
- Are inputs validated as you specified?
- Are deps pinned as required?

Critical finding → `fleet_alert(category="security", severity="critical")`
→ sets `security_hold` on the task → blocks approval chain.

## The security_hold Mechanism

When you call `fleet_alert` with `category="security"`, the tool automatically
sets `security_hold: "true"` on the task. This blocks the approval chain —
fleet-ops cannot approve until you clear the hold.

Clear it by posting a follow-up comment confirming the issue is resolved,
and updating the custom field.
