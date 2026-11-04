---
name: security
description: "Use when Forge performs security review. Security reviewer audits OWASP Top 10, scans for secrets, reviews auth/authz logic."
---

<Purpose>
Phase 5 of the Forge pipeline. The Security Reviewer conducts a comprehensive
security audit covering OWASP Top 10 vulnerabilities, secret/credential scanning,
and authentication/authorization logic review. Security issues are always classified
as blockers and route to the fix loop before delivery. In Autonomous Company Mode,
security is part of the internal delivery-readiness gate, not a passive phase hop.
</Purpose>

<Use_When>
- Automatically invoked after Phase 4 (QA) completes with no blockers
- state.json phase=5
</Use_When>

<Steps>
1. Dispatch security-reviewer agent with context:
   - .forge/spec.md (auth/authz requirements)
   - .forge/design/architecture.md (attack surface overview)
   - .forge/contracts/*.ts (API boundary definitions)
   - Full source code access for scanning

2. OWASP Top 10 Audit:
   a. A01 — Broken Access Control:
      - Verify all endpoints enforce authorization
      - Check for IDOR (Insecure Direct Object References)
      - Verify CORS configuration is restrictive
      - Check for path traversal vulnerabilities
   b. A02 — Cryptographic Failures:
      - Verify sensitive data is encrypted at rest and in transit
      - Check for hardcoded secrets or weak encryption
      - Verify password hashing uses bcrypt/argon2 (not MD5/SHA1)
   c. A03 — Injection:
      - Check for SQL injection in raw queries
      - Check for XSS in user-rendered content
      - Check for command injection in shell calls
      - Verify input sanitization on all user inputs
   d. A04 — Insecure Design:
      - Review rate limiting on auth endpoints
      - Check for missing CSRF protection
      - Verify secure defaults in configuration
   e. A05 — Security Misconfiguration:
      - Check for debug mode in production config
      - Verify security headers (CSP, HSTS, X-Frame-Options)
      - Check for default credentials or open admin panels
   f. A06 — Vulnerable Components:
      - Scan dependencies for known CVEs
      - Check for outdated packages with security patches
   g. A07 — Authentication Failures:
      - Review session management
      - Check token expiration and refresh logic
      - Verify password policies if applicable
   h. A08 — Data Integrity Failures:
      - Check for unsigned/unverified data in critical flows
      - Review CI/CD pipeline for integrity
   i. A09 — Logging Failures:
      - Verify security events are logged
      - Check that sensitive data is NOT logged (passwords, tokens)
   j. A10 — SSRF:
      - Check for unvalidated URL inputs used in server requests
      - Verify allowlists for external API calls

3. Secrets Scan:
   a. Scan entire codebase for:
      - API keys, tokens, passwords in source files
      - .env files committed to git
      - Private keys or certificates in repo
      - Hardcoded connection strings
   b. Verify .gitignore covers: .env*, *.pem, *.key, credentials.*

4. Auth/Authz Logic Review:
   a. Trace every authenticated endpoint:
      - Is the auth check present?
      - Is it the correct auth check (not just "is logged in" but "is authorized")?
      - Can the check be bypassed?
   b. Review role-based access control (if applicable):
      - Are roles enforced server-side?
      - Can role escalation occur?
   c. Review token handling:
      - Are tokens stored securely (httpOnly cookies, not localStorage)?
      - Is token validation happening on every request?

5. Issue Classification:
   For each discovered vulnerability, dispatch the bug-tracker agent to create a hole
   file using the standard format `HOLE-{NNN}-{slug}.md`:
   - Provide the bug-tracker with:
     - Severity: blocker (all security issues are blockers)
     - Category: owasp-{number} | secrets | auth | authz
     - Vulnerability description
     - Attack scenario
     - Recommended fix
     - Affected files
   - The bug-tracker agent writes .forge/holes/HOLE-{NNN}-{slug}.md with the next
     available sequence number and a kebab-case slug derived from the vulnerability summary

6. Gate Decision:
   - If any security issues found → mark delivery readiness blocked and route to phase=6 (fix loop)
   - If clean → mark security clear for delivery readiness and phase=7 (delivery)

7. Update state.json:
   - If issues: phase=6, phase_id="fix", phase_name="fix"
   - If clean: phase=7, phase_id="delivery", phase_name="delivery"

8. Update runtime expectations:
   - Security findings must appear as internal blockers owned by security-reviewer
   - A clean audit must contribute to delivery-readiness rather than only changing phase labels
   - Preferred helper:
     - If issues:
       `node scripts/forge-lane-runtime.mjs set-company-gate --gate implementation_readiness --gate-owner lead-dev --delivery-state blocked --internal-blockers "{security blocker summaries}"`
     - If clean:
       `node scripts/forge-lane-runtime.mjs set-company-gate --gate delivery_readiness --gate-owner ceo --delivery-state ready_for_review`

9. Update session handoff:
   - If issues:
     `node scripts/forge-lane-runtime.mjs write-session-handoff --summary "{security blockers found}" --next-goal "Fix security blockers and rerun security" --next-owner security-reviewer`
   - If clean:
     `node scripts/forge-lane-runtime.mjs write-session-handoff --summary "Security clear; prep delivery review" --next-goal "Prepare customer delivery review" --next-owner ceo`

10. Create git tag: forge/v1-security

11. Transition to next phase (forge:fix or forge:deliver)
</Steps>

<State_Changes>
- Creates: .forge/holes/HOLE-{NNN}-{slug}.md (one per vulnerability, via bug-tracker agent)
- Updates: .forge/state.json (phase=6 or phase=7)
- Updates: .forge/runtime.json (delivery gate result + next session handoff)
- Creates: git tag forge/v1-security
</State_Changes>

<Failure_Modes_To_Avoid>
- Performing only a surface-level scan without tracing auth logic
- Missing hardcoded secrets because they look like config constants
- Not treating all security issues as blockers
- Skipping OWASP categories because the app "seems simple"
- Approving code that stores tokens in localStorage
- Not scanning dependencies for known CVEs
- Logging sensitive data (passwords, tokens) in audit trail
- Treating security as informational instead of a delivery gate
- Moving to delivery with unresolved security issues
</Failure_Modes_To_Avoid>

<Auto_Chain>
When security review completes:
- If security issues found: update state.json phase_id → "fix", IMMEDIATELY invoke Skill: forge:fix
- If no issues: update state.json phase_id → "delivery", IMMEDIATELY invoke Skill: forge:deliver
Do NOT stop, summarize, or ask the user. The pipeline continues autonomously.
</Auto_Chain>
