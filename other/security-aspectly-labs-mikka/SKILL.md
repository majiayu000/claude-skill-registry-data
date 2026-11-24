---
name: security
description: Security review for code, APIs, and system designs. Always use this skill when reviewing code for vulnerabilities, auditing authentication or authorization, evaluating input handling, checking for secrets or hardcoded credentials, reviewing dependencies, or threat modeling. Use when the user says "is this secure", "review this for security issues", "could this be exploited", "check for vulnerabilities", "threat model this", "review for SQL injection", "is this JWT implementation safe", or "is my auth correct". Also use proactively when implementing auth, handling untrusted input, or storing sensitive data.
---

# Security

Security review is not a checklist to tick: it's a way of thinking about trust. For every piece of code, ask: what can an attacker control here, and what can they make the system do with it?

## Threat modeling first

Before reviewing specific code, understand the threat surface:

1. **What are the trust boundaries?** Where does untrusted data enter the system? (HTTP requests, file uploads, message queue messages, webhooks, config files loaded from disk)
2. **What are the high-value targets?** (Authentication tokens, PII, financial data, admin functions, ability to execute code)
3. **Who are the threat actors?** Unauthenticated external users, authenticated-but-low-privilege users, internal users with legitimate access, compromised third-party services
4. **What's the worst case?** Data exfiltration, privilege escalation, remote code execution, denial of service, data corruption

Use STRIDE to check you haven't missed a category:

- **S**poofing: can an attacker impersonate another user or system?
- **T**ampering: can an attacker modify data in transit or at rest?
- **R**epudiation: can an attacker perform actions that can't be traced back to them?
- **I**nformation Disclosure: can an attacker read data they shouldn't?
- **D**enial of Service: can an attacker degrade or disable the service?
- **E**levation of Privilege: can an attacker gain permissions they shouldn't have?

## Input validation and injection

**Never trust external input.** Anything that arrives from outside the process (HTTP parameters, headers, bodies, file contents, environment variables read at runtime, database values that were originally user-supplied) is untrusted until validated.

**SQL injection**: use parameterized queries (prepared statements) everywhere. Never concatenate user input into SQL strings. This applies to every database library in every language.

```
// Vulnerable
query = "SELECT * FROM users WHERE email = '" + email + "'"

// Safe
query = "SELECT * FROM users WHERE email = ?"  // with email as a bound parameter
```

**Command injection**: never pass user input to shell commands. If you must invoke a subprocess, use argument arrays (not string interpolation) and validate input strictly before passing it.

**XSS (Cross-Site Scripting)**: escape output at the rendering layer, not at the input layer. Input sanitization loses information and is hard to get right. Output encoding (HTML-encode when rendering in HTML, JS-encode when rendering in JS) is the correct defense. Modern templating frameworks (React, Vue, Angular) do this by default; don't bypass their escaping.

**Path traversal**: if constructing a file path from user input, canonicalize the resulting path and verify it's within the expected directory before opening. `../../../etc/passwd` is a path traversal attack.

**SSRF (Server-Side Request Forgery)**: if your application fetches a URL supplied by a user, an attacker can use it to reach internal services, cloud metadata endpoints, or loop back addresses. Validate and allowlist URLs; block private IP ranges.

**Deserialization**: deserializing untrusted data in languages/formats that support polymorphic deserialization (Java's `ObjectInputStream`, Python's `pickle`, PHP's `unserialize`) can lead to remote code execution. Prefer JSON/protobuf with explicit schemas over binary or language-native serialization for untrusted data.

## Authentication

**Session tokens must be unpredictable.** Use a cryptographically secure random generator for session IDs, CSRF tokens, and password reset tokens. Never use sequential IDs or deterministic values (timestamps, user IDs).

**Passwords**:

- Store with a slow adaptive hash: bcrypt, Argon2, or scrypt. Never MD5, SHA-1, or SHA-256 for passwords.
- Enforce a minimum length (12+ characters); don't impose maximum length or character restrictions.
- Check against breached password lists (Have I Been Pwned API) at registration and reset.

**JWT**:

- Verify the signature on every request; don't just decode and trust the payload.
- Reject the `alg: none` algorithm explicitly.
- Validate `exp`, `iss`, and `aud` claims.
- Keep tokens short-lived; use refresh tokens for longer sessions.
- Don't store sensitive data in the payload: it's base64-encoded, not encrypted.

**OAuth / OIDC**:

- Validate the `state` parameter to prevent CSRF against the authorization flow.
- Validate `redirect_uri` strictly; don't allow open redirects.
- Validate the ID token's `nonce` to prevent replay attacks.

**Multi-factor authentication**: for any system handling sensitive data or admin functions, MFA should be available and enforced for privileged accounts.

## Authorization

Authentication answers "who are you?" Authorization answers "what are you allowed to do?" They're separate concerns and must both be checked.

**Check authorization at every operation, not just at login.** A user authenticated as User A should not be able to read User B's data by changing an ID in the URL. Verify ownership or permission on every resource access.

**Principle of least privilege**: grant the minimum permissions needed to do the job. Service accounts, API keys, and database users should not have admin-level access unless they specifically need it.

**IDOR (Insecure Direct Object Reference)**: when an endpoint accepts a resource ID (order ID, user ID, document ID), verify the requesting user has permission to access that specific resource; don't just check that they're authenticated.

**Horizontal vs vertical privilege escalation**:

- Horizontal: User A accessing User B's data (same privilege level, different account)
- Vertical: a regular user accessing admin functionality

Both must be prevented. Horizontal is easy to overlook because the authorization check pattern seems correct but the ownership check is missing.

## Secrets management

**Secrets don't belong in code.** API keys, database credentials, tokens, private keys: none of these belong in source files, even in private repos. Use environment variables for local development, and a secrets manager (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager) in production.

**Audit for secrets in the codebase.** Tools: `trufflehog`, `gitleaks`, `detect-secrets`. Run these in CI and before open-sourcing any repository.

**Rotate credentials regularly.** Leaked credentials from a breach 18 months ago are still valid if they've never been rotated. Automate rotation where possible.

**Don't log secrets.** Audit log statements that include request objects, headers, or full environment dumps; credentials often end up in logs this way.

**Short-lived over long-lived.** Prefer short-lived tokens (minutes to hours) with refresh over long-lived static credentials. A leaked short-lived token has a bounded impact window.

## Dependencies

Your application's attack surface includes every library it imports. A well-written application with a vulnerable dependency is still vulnerable.

**Audit dependencies for known CVEs.** Tools: `npm audit`, `pip-audit`, `Dependabot`, `Snyk`, `OWASP Dependency-Check`. Run in CI; fail the build on critical vulnerabilities.

**Pin dependency versions.** Unpinned dependencies (`^1.0.0`, `>=2.0`) can pull in a malicious or vulnerable version on the next install. Pin transitive dependencies via a lockfile (`package-lock.json`, `poetry.lock`, `go.sum`).

**Minimize the dependency tree.** Every dependency is a potential supply chain attack vector. Evaluate whether a dependency is necessary; prefer smaller, focused packages over large frameworks when only a fraction of the functionality is needed.

**Vet new dependencies before adding them.** Check the maintainer, download count, recent activity, and whether the package has a history of malicious versions.

## Web security headers

For any HTTP service, set these headers:

| Header                      | Value                                 | Purpose                                                        |
| --------------------------- | ------------------------------------- | -------------------------------------------------------------- |
| `Content-Security-Policy`   | Restrictive allowlist                 | Limits what scripts/resources can load; primary XSS mitigation |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` | Forces HTTPS                                                   |
| `X-Content-Type-Options`    | `nosniff`                             | Prevents MIME-type sniffing                                    |
| `X-Frame-Options`           | `DENY` or `SAMEORIGIN`                | Prevents clickjacking                                          |
| `Referrer-Policy`           | `strict-origin-when-cross-origin`     | Limits referrer leakage                                        |
| `Permissions-Policy`        | Restrict unused browser APIs          | Limits exposure if XSS occurs                                  |

**CORS**: only allow origins you control. Don't reflect the `Origin` header back without validation. Never use `Access-Control-Allow-Origin: *` for endpoints that return authenticated data.

**CSRF**: for any state-changing operation from a browser client, use a CSRF token (or rely on SameSite cookie semantics). `SameSite=Lax` on session cookies prevents CSRF for most attack patterns; `SameSite=Strict` is more restrictive.

## Cryptography

**Don't roll your own crypto.** Use well-audited libraries (libsodium, Bouncy Castle, Web Crypto API). The primitives matter too: use AES-GCM or ChaCha20-Poly1305 for symmetric encryption; use Ed25519 or RSA-OAEP for asymmetric. Don't use ECB mode, MD5, SHA-1, or DES.

**Keys and nonces**: encryption keys must be random and never reused across contexts. Nonces in authenticated encryption must never repeat for a given key: a single nonce reuse can completely break confidentiality.

**TLS**: use TLS 1.2 or 1.3. Disable older versions (SSL, TLS 1.0, 1.1). Verify certificates; don't disable certificate validation in production code, even "temporarily."

## Error handling and information disclosure

**Don't leak implementation details in errors.** Stack traces, database schema names, internal hostnames, and library versions in error responses give attackers a map of your system. Log the detail internally; return a generic message externally.

**Don't leak existence through timing or response.** "That email is not registered" vs "incorrect password" tells an attacker whether an account exists. Use uniform responses and constant-time comparison for credentials.

**Log security events**: authentication failures, authorization failures, privilege changes, account lockouts. These are the events that matter during an incident or forensic investigation.
