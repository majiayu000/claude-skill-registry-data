---
name: security-owasp
description: 'Secure coding guidelines grounded in the OWASP Top 10 and industry best practices. Covers access control, authentication, injection prevention (SQL, XSS, command), cryptographic failures, SSRF, security misconfiguration, vulnerable dependencies, insecure deserialization, security logging, and secure design patterns. Applies to all languages and file types including C#, JavaScript, TypeScript, Python, Go, Java, YAML, Dockerfiles, Terraform, and Bicep. Use this skill whenever writing, reviewing, or refactoring code that handles user input, authentication, authorization, secrets, passwords, tokens, session management, HTTP headers, CORS, CSP, API endpoints, database queries, file uploads, URL handling, deserialization, cryptography, or dependency management. Also use when performing security reviews, hardening existing code, fixing vulnerabilities, or responding to security audit findings.'
user-invocable: false
---

# Secure Coding and OWASP Guidelines

Ensure all code you generate, review, or refactor is secure by default. When a tradeoff exists between convenience and security, choose the secure path and explain the reasoning so the developer understands the risk being mitigated. The guidelines below are organized around the OWASP Top 10 (2021) categories.

## A01: Broken Access Control

Access control vulnerabilities are the most common web application security risk. When an attacker can act outside their intended permissions, the entire system's trust model breaks down.

- **Deny by default.** Access control decisions should grant access only when an explicit rule allows it -- unauthorized requests are rejected, not silently passed through.
- **Enforce least privilege.** Default to the most restrictive permissions for every role, resource, and operation. Check the user's rights against the specific resource they are accessing, not just whether they are authenticated.
- **Prevent path traversal.** When handling file uploads or accessing files based on user input, sanitize input to prevent directory traversal attacks (e.g., `../../etc/passwd`). Use platform APIs that build paths securely (e.g., `Path.Combine` with validation in C#, `path.resolve` with prefix checking in Node.js).
- **Validate object-level access.** When exposing resources by ID (e.g., `/api/orders/123`), verify the authenticated user owns or has permission to access that specific record. This prevents Insecure Direct Object Reference (IDOR) attacks.

## A02: Cryptographic Failures

Weak or missing cryptography exposes sensitive data. The goal is to make sure data is unreadable to anyone who should not have access, both at rest and in transit.

- **Use strong, modern algorithms.** For password hashing, use Argon2, bcrypt, or scrypt -- these are intentionally slow, which makes brute-force attacks expensive. MD5 and SHA-1 are not suitable for password storage because they are fast to compute.
- **Protect data in transit.** Default to HTTPS for all network requests. When generating HTTP client code, use `https://` URLs and enforce TLS 1.2+.
- **Protect data at rest.** When storing sensitive data (PII, tokens, financial records), recommend encryption using standard algorithms like AES-256. Use platform-provided encryption services where available.
- **Never hardcode secrets.** API keys, passwords, connection strings, and tokens must not appear in source code, configuration files committed to version control, or log output. Generate code that reads secrets from environment variables or a secrets management service (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault) with a clear placeholder and explanatory comment.

## A03: Injection

Injection flaws occur when untrusted data is sent to an interpreter as part of a command or query. The fundamental defense is to keep data separate from commands.

- **Use parameterized queries.** For all database interactions, use parameterized queries or prepared statements. String concatenation or interpolation to build SQL from user input creates SQL injection vulnerabilities regardless of any sanitization attempts.
- **Escape command-line input.** For OS command execution, use built-in functions that handle argument escaping (e.g., `shlex.quote()` in Python, `ProcessStartInfo` with argument list in C#). Avoid passing user input through a shell interpreter.
- **Prevent Cross-Site Scripting (XSS).** When displaying user-controlled data in frontend code, use context-aware output encoding. Prefer methods that treat data as text (`.textContent`, Razor encoding, React JSX auto-escaping) over methods that parse HTML (`.innerHTML`, `@Html.Raw()`). When raw HTML rendering is necessary, sanitize with a trusted library like DOMPurify first.
- **Validate and sanitize all input.** Apply server-side validation at every entry point. Client-side validation improves UX but provides no security because it can be bypassed.

## A04: Insecure Design

Security must be considered during design, not bolted on afterward. Insecure design cannot be fixed by a perfect implementation -- the architecture itself needs to account for threats.

- **Apply threat modeling.** When designing new features that handle sensitive data, authentication, or authorization, consider what an attacker would target and what controls prevent abuse.
- **Use secure design patterns.** Prefer established patterns: the repository pattern isolates data access, the mediator pattern centralizes validation, and the result pattern makes error handling explicit without leaking implementation details.
- **Limit resource consumption.** Design APIs with rate limiting, pagination, and request size limits to prevent abuse and denial of service.
- **Separate trust boundaries.** Keep untrusted input processing isolated from privileged operations. Validate at the boundary before data enters trusted components.

## A05: Security Misconfiguration

Misconfiguration is one of the easiest vulnerabilities to introduce and one of the hardest to detect because the code itself may be correct while the environment is not.

- **Secure defaults for production.** Disable verbose error messages, debug endpoints, and stack traces in production environments. Expose detailed errors only in development.
- **Set security headers.** For web applications, include essential HTTP security headers:
  - `Content-Security-Policy` (CSP) -- restricts resource loading sources to prevent XSS
  - `Strict-Transport-Security` (HSTS) -- forces HTTPS connections
  - `X-Content-Type-Options: nosniff` -- prevents MIME-type sniffing
  - `X-Frame-Options: DENY` or `SAMEORIGIN` -- prevents clickjacking
  - `Referrer-Policy` -- controls information leakage in referrer headers
- **Configure CORS carefully.** Avoid `Access-Control-Allow-Origin: *` for APIs that handle authenticated requests. Restrict allowed origins to known, trusted domains. Reflect the `Origin` header only when it matches an allow-list.
- **Harden container and infrastructure configs.** For Dockerfiles, avoid running as root, minimize image layers, and use multi-stage builds. For Kubernetes/Terraform/Bicep, apply least-privilege service accounts and network policies.

## A06: Vulnerable and Outdated Components

Using libraries with known vulnerabilities is a direct path to exploitation. The fix is straightforward: know what you depend on and keep it current.

- **Use up-to-date dependencies.** When adding a new library, suggest the latest stable version. Recommend running vulnerability scanners regularly: `npm audit`, `pip-audit`, `dotnet list package --vulnerable`, or Snyk/Trivy.
- **Pin dependency versions.** Use lock files (`package-lock.json`, `packages.lock.json`, `poetry.lock`) to ensure reproducible builds and prevent supply chain attacks through unpinned transitive dependencies.
- **Remove unused dependencies.** Unused packages increase attack surface for no benefit.

## A07: Identification and Authentication Failures

Weak authentication allows attackers to assume other users' identities. These controls protect the gateway to everything else in the system.

- **Generate new session identifiers on login.** After successful authentication, create a new session ID to prevent session fixation attacks. Invalidate the old session.
- **Configure session cookies securely.** Set `HttpOnly` (prevents JavaScript access), `Secure` (HTTPS only), and `SameSite=Strict` or `SameSite=Lax` (mitigates CSRF) attributes on session cookies.
- **Protect against brute force.** For authentication and password reset flows, implement rate limiting and progressive delays or account lockout after repeated failed attempts.
- **Validate JWTs properly.** When using JWT-based authentication, validate the signature, issuer (`iss`), audience (`aud`), and expiration (`exp`) on every request. Reject tokens with `alg: none`. Use asymmetric signing (RS256/ES256) when tokens are verified by multiple services.

## A08: Software and Data Integrity Failures

Trusting serialized data or unsigned updates from untrusted sources allows attackers to inject malicious objects or tamper with application state.

- **Avoid insecure deserialization.** Do not deserialize data from untrusted sources without strict type validation. Prefer safe formats: `System.Text.Json` with `JsonSerializerOptions` type restrictions in C#, JSON over Pickle in Python, and `JSON.parse` over `eval` in JavaScript.
- **Verify software integrity.** When downloading dependencies or artifacts in CI/CD pipelines, verify checksums or signatures. Use lock files and enable dependency signature verification where available.

## A09: Security Logging and Monitoring Failures

Without proper logging, attacks go undetected, making incident response impossible. Logging is a detective control that complements the preventive controls above.

- **Log security-relevant events.** Record authentication attempts (success and failure), authorization failures, input validation failures, and changes to sensitive data or configuration.
- **Never log secrets or sensitive data.** Passwords, tokens, API keys, credit card numbers, and PII must not appear in log output. Use structured logging with named placeholders -- this also prevents log injection attacks (e.g., `logger.LogInformation("Login attempt for {UserId}", userId)`).
- **Include correlation context.** Add correlation IDs, user identifiers, and source IP addresses to security log entries to support incident investigation and tracing.
- **Set up monitoring and alerting.** Recommend monitoring for anomalous patterns: spikes in failed login attempts, unusual access patterns, or repeated authorization failures from the same source.

## A10: Server-Side Request Forgery (SSRF)

SSRF attacks trick the server into making requests to unintended destinations, potentially exposing internal services or cloud metadata endpoints.

- **Validate all server-side URLs.** When the server makes requests to URLs provided by users (webhooks, URL previews, file imports), treat those URLs as untrusted. Use strict allow-list validation for protocol, host, port, and path.
- **Block internal network access.** Deny requests to private IP ranges (`10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`, `127.0.0.1`, `169.254.169.254`) and link-local addresses. Cloud metadata endpoints (e.g., `169.254.169.254`) are a particularly high-value SSRF target.
- **Use network-level controls.** Where possible, configure firewalls or network security groups to restrict outbound traffic from application servers to only necessary external destinations.

## General Principles

- **Explain security decisions.** When generating code that mitigates a risk, state what it protects against (e.g., "Using a parameterized query here to prevent SQL injection"). This helps developers learn and maintain the security posture over time.
- **Educate during reviews.** When identifying a vulnerability in existing code, provide the corrected code and explain the risk -- not just "this is insecure" but what an attacker could do and how the fix prevents it.
- **Defense in depth.** No single control is sufficient. Layer multiple defenses so that if one fails, others still protect the system.
- **Fail securely.** When an error occurs, the application should default to a secure state. Error handlers should not expose stack traces, internal paths, or configuration details to users.
