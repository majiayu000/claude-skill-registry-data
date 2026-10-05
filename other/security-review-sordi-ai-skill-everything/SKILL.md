---
name: security-review
description: Apply when performing a security review, checking for vulnerabilities, or implementing authentication and authorization logic.
license: MIT
version: 1.0.0
tokens_target: 2200
triggers:
  - security review
  - vulnerability check
  - auth implementation
loads_after: [code-quality]
supersedes: []
---

# Sub-Skill: Security Review Depth
<!-- target: tokens_target above. Run `python tools/render_readme_table.py` to update README. -->

**Purpose:** Deep security rules for authentication, authorization, injection, session management, and API hardening. Complements code-quality rules 20–23 with IDOR, SSRF, and access-control depth.

---

## Rules

### Authentication vs. Authorization

1. **AuthN/AuthZ separation.** Always treat authentication (who are you?) and authorization (what can you do?) as distinct checks; never collapse them into a single boolean `is_logged_in` guard.
2. **Resource ownership check.** Always verify resource ownership in addition to role-based access on mutation endpoints — a valid role does not imply ownership of the target record. Reference: ERR-2026-019
3. **IDOR prevention.** Never expose sequential or predictable resource IDs in URLs without a server-side ownership assertion; use opaque UUIDs and always re-fetch the record to confirm the caller owns it.
4. **Privilege escalation guard.** Never allow a user to elevate their own role or grant permissions they do not already hold; enforce privilege changes through a separate admin-only path.
5. **Token scope enforcement.** Always validate that the token's declared scope covers the requested operation before executing it; reject tokens with insufficient scope with 403, not 401.

### Session Management

6. **Session fixation prevention.** Always regenerate the session identifier immediately after a successful login to prevent session fixation attacks.
7. **Idle and absolute timeouts.** Ensure sessions carry both an idle timeout (e.g., 15 min) and an absolute expiry (e.g., 8 h); never issue non-expiring session tokens.
8. **Secure cookie attributes.** Always set `HttpOnly`, `Secure`, and `SameSite=Strict` (or `Lax`) on session cookies; never omit any of these three attributes.
9. **Logout invalidation.** Always invalidate the server-side session record on logout; never rely solely on deleting the client-side cookie.

### Injection and Input Handling

10. **Parameterized queries everywhere.** Never construct database queries by string concatenation with user-supplied values; always use parameterized statements or an ORM that enforces binding.
11. **Output encoding context.** Always encode output in the context where it will be rendered (HTML entity encoding for HTML, JSON encoding for JSON responses, URL encoding for query strings); never apply a single generic escape.
12. **SSRF mitigation.** Before making any server-side HTTP request to a URL derived from user input, validate the resolved IP against an allowlist; block private RFC-1918 ranges and loopback addresses.
13. **File path traversal.** Never concatenate user input into file system paths; always resolve the canonical path and assert it falls within the expected base directory before opening.

### API and Transport Hardening

14. **CORS allowlist.** Avoid wildcard `Access-Control-Allow-Origin: *` on endpoints that return authenticated data; always enumerate trusted origins explicitly.
15. **CSP header.** Ensure every HTML response includes a `Content-Security-Policy` header that restricts `script-src` to known origins; never use `unsafe-inline` without a nonce or hash.
16. **Rate limiting on auth endpoints.** Always apply rate limiting and exponential back-off to login, password-reset, and OTP endpoints; never expose them without request throttling.
17. **Sensitive data in logs.** Never log passwords, tokens, full credit-card numbers, or other PII; mask or omit them before writing to any log sink.

### Secrets and Dependencies

18. **Secret rotation readiness.** Always design secret consumption so that rotating a credential requires only an environment variable update with no code change; never hard-code secrets or embed them in config files committed to version control.
19. **Dependency CVE scan.** Before merging any PR that adds or upgrades a dependency, run a CVE scan (e.g., `pip-audit`, `npm audit`, `trivy`); block merge if high-severity findings are unresolved.
20. **Audit logging on sensitive actions.** Always emit a structured audit log entry (actor, action, resource ID, timestamp, outcome) for every privileged or destructive operation; never skip audit logging for admin endpoints.

---

## See also

- `skills/code-quality/SKILL.md` — rules 20–23 cover sanitization, parameterized queries, and secret hygiene at a general level; this skill deepens those with IDOR, SSRF, and session specifics.
- `skills/error-log/SKILL.md` — ERR-2026-019 motivated rule 2 (resource ownership check).

---
