---
name: security-audit
description: Comprehensive security auditing workflow covering web application testing, API security, penetration testing, vulnerability scanning, and security hardening.
stacks:
  - security
tags:
  - security
  - audit
category: workflow-bundle
risk: safe
source: personal
date_added: 2026-02-27
---

## Use this skill when

- Performing security audits on web applications
- Testing API security (authentication, authorization, rate limiting, input validation)
- Conducting penetration tests
- Scanning for OWASP Top 10 vulnerabilities
- Hardening application security posture
- Compliance-driven security assessments

## Do not use this skill when

- The task is purely code quality or architecture review — use production-code-audit
- The task requires only dependency vulnerability scanning in isolation

## Instructions

Work through phases sequentially. Document findings at each phase before proceeding to the next. Provide remediation steps alongside every finding, not just after all phases complete.

## Capabilities

### Phase 1: Reconnaissance
- Define target scope: domains, IP ranges, endpoints in/out of scope
- Gather intelligence: DNS records, SSL certificate info, HTTP headers, technology fingerprints
- Map attack surface: public endpoints, authentication flows, file upload points, external integrations
- Identify technologies: framework, server, database, CDN, WAF

### Phase 2: Vulnerability Scanning
- Automated scanner execution (OWASP ZAP, Nikto, or Burp Suite active scan)
- Static code analysis (SAST) for injection patterns, hardcoded secrets, insecure crypto
- Software composition analysis: known CVEs in dependencies (npm audit, Snyk, OWASP Dependency-Check)
- Configuration review: security headers, TLS configuration, CORS policy, cookie flags

### Phase 3: Web Application Testing

**Injection Testing**
- SQL injection: error-based, blind boolean, time-based; test all input fields and URL parameters
- NoSQL injection: MongoDB operator injection ($where, $regex in JSON bodies)
- OS command injection: semicolon, pipe, backtick chaining in system call inputs
- LDAP injection in directory service integrations
- XML/XXE injection in XML-accepting endpoints

**Authentication Testing**
- Brute force protection: rate limiting, account lockout, CAPTCHA effectiveness
- Password policy: minimum length, complexity, breach database checks
- Password reset flow: token predictability, expiry, reuse after reset
- Multi-factor authentication bypass attempts
- Default credentials on admin interfaces

**Session Management**
- Session token entropy and predictability
- Session fixation vulnerabilities
- Proper session invalidation on logout
- Cookie attributes: Secure, HttpOnly, SameSite, appropriate Max-Age

**Access Control**
- Horizontal privilege escalation (IDOR): access other users' resources by changing IDs
- Vertical privilege escalation: accessing admin functionality with user-level account
- Forced browsing to authenticated endpoints without session
- JWT token manipulation: algorithm confusion (alg:none), weak secrets, expired token acceptance

**Input Validation**
- Cross-site scripting (XSS): reflected, stored, DOM-based; test all output contexts
- Path traversal: ../../../etc/passwd in file path inputs
- Open redirect: unvalidated redirect targets in login flows
- Business logic: negative quantities, price manipulation, workflow step skipping

**Security Headers**
- Content-Security-Policy presence and strictness
- X-Frame-Options or CSP frame-ancestors to prevent clickjacking
- X-Content-Type-Options: nosniff
- Strict-Transport-Security with appropriate max-age
- Referrer-Policy to prevent information leakage

### Phase 4: API Security Testing
- Endpoint enumeration: discover undocumented or legacy API versions
- Authentication: missing auth on endpoints, token in URL instead of header, weak token formats
- Authorization: BOLA/IDOR (Broken Object Level Authorization) — access other objects by ID manipulation
- Function level authorization: user accessing admin-only operations
- Rate limiting: brute force protection, resource exhaustion prevention
- Input validation: mass assignment (extra fields in request body), type confusion, nested object injection
- Error handling: stack traces, internal paths, database errors in responses

### Phase 5: Penetration Testing
- Plan with defined scope, rules of engagement, and timeline
- Execute attack scenarios in order of likely impact
- Exploit confirmed vulnerabilities with proof-of-concept
- Document exact reproduction steps for each finding
- Assess business impact: data exposure, availability, integrity, compliance

### Phase 6: Security Hardening
- Implement security controls based on findings
- Configure security headers in web server/application layer
- Enforce authentication and authorization on all protected routes
- Implement rate limiting at appropriate granularity
- Configure structured security logging (authentication events, access control failures, anomalies)
- Patch or upgrade vulnerable dependencies

### Phase 7: Reporting
- Executive summary: overall risk posture, critical finding count, recommended timeline
- Technical findings: CVSS score, reproduction steps, affected components, remediation
- Risk ratings: Critical (immediate), High (within 1 week), Medium (within 1 month), Low (next sprint)

## Behavioral Traits
- Documents findings as they are discovered, not at the end of all phases
- Provides concrete remediation code or configuration alongside each finding
- Rates vulnerabilities by exploitability and business impact, not just textbook severity
- Tests authentication bypass before testing authorization issues
- Verifies that reported vulnerabilities are actually exploitable before flagging as confirmed
- Checks for defense-in-depth: one missing control is a finding, but chain of missing controls is critical

## Knowledge Base

### OWASP Top 10 (2021) Coverage
- A01: Broken Access Control — IDOR, privilege escalation, forced browsing, JWT manipulation
- A02: Cryptographic Failures — weak TLS, plaintext data, weak hashing (MD5/SHA1), missing encryption at rest
- A03: Injection — SQL, NoSQL, OS command, LDAP, XXE
- A04: Insecure Design — missing threat modeling, insecure business logic
- A05: Security Misconfiguration — default credentials, verbose errors, unnecessary features enabled
- A06: Vulnerable Components — outdated dependencies with known CVEs
- A07: Authentication Failures — brute force, session fixation, weak passwords, missing MFA
- A08: Integrity Failures — unsigned serialization, insecure CI/CD pipelines
- A09: Logging Failures — missing security event logging, no anomaly detection
- A10: SSRF — server-side requests to internal services via user-controlled URLs

### CVSS Scoring Quick Reference
- Critical (9.0-10.0): unauthenticated remote code execution, data breach of all users
- High (7.0-8.9): authenticated RCE, significant data exposure, complete auth bypass
- Medium (4.0-6.9): limited data exposure, requires user interaction, partial auth bypass
- Low (0.1-3.9): information disclosure, requires local access, limited impact

### Common API Security Findings
- BOLA: change /api/orders/123 to /api/orders/124 to access another user's order
- Mass assignment: POST /users with {"admin": true} sets admin flag if not filtered
- Function level auth: GET /api/admin/users accessible without admin role
- Algorithm confusion: JWT with "alg": "none" accepted by vulnerable implementations
- API versioning: /api/v1/ deprecated but still accessible with less security than /api/v2/

### Security Header Configuration (Required)
- Content-Security-Policy: default-src 'self'; define explicit allowed sources
- Strict-Transport-Security: max-age=31536000; includeSubDomains (HTTPS required first)
- X-Content-Type-Options: nosniff (prevents MIME type sniffing)
- X-Frame-Options: DENY or SAMEORIGIN (prevents clickjacking)
- Referrer-Policy: strict-origin-when-cross-origin (prevents sensitive URL leakage)

### Security Testing Checklist

**OWASP Top 10**
- Injection (SQL, NoSQL, OS, LDAP)
- Broken authentication and session management
- Sensitive data exposure in responses and logs
- XML External Entities (XXE)
- Broken access control (IDOR, privilege escalation)
- Security misconfiguration (headers, defaults, errors)
- Cross-site scripting (XSS) — reflected, stored, DOM
- Insecure deserialization
- Components with known vulnerabilities
- Insufficient logging and monitoring

**API Security**
- Authentication on every endpoint
- Authorization checks at object and function level
- Rate limiting on all public and authenticated endpoints
- Input validation and type enforcement
- Structured error responses (no stack traces or internal details)
- Security headers on all responses

## Constraints
- Never perform security testing on systems without explicit written authorization
- Never exploit vulnerabilities beyond confirming exploitability (no data exfiltration, no persistent access)
- Always document the exact reproduction steps, not just the finding category
- Rate all findings with CVSS or equivalent scoring before reporting
- Provide remediation steps for every finding — a finding without remediation is incomplete
- Validate that fixes actually resolve the vulnerability before closing findings

## Quality Gates
- All planned test phases executed
- Every vulnerability documented with reproduction steps
- Proof-of-concept captured for confirmed findings
- Risk assessments completed with CVSS scores
- Remediation steps provided for every finding
- Executive summary written for non-technical stakeholders
