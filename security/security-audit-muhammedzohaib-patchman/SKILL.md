---
name: security-audit
description: Conduct authorized defensive security audits of codebases and web applications. Use for broad appsec review across OWASP, authz, business logic, SSRF, XSS, CSRF, injection, file upload, secrets, logging, and tenant isolation. Produces structured findings with severity, confidence, evidence, and safe remediation guidance.
---

# Security Audit

## When to use

Use this skill when the user wants a full security review of a repository, service, or application slice.

## Default behavior

- stay in read-first mode unless the user explicitly asks for a patch
- reason from framework and architecture conventions
- flag likely vulnerabilities and insecure defaults
- explain exploitability in safe, non-weaponized language
- ask for missing deployment or authorization context when needed

## Coverage map

- broken access control and IDOR
- authentication, session, cookie, token, and reset flaws
- business logic abuse paths
- XSS, CSRF, SSRF, injection, unsafe deserialization
- file upload and document processing risks
- unsafe crypto and secret management
- headers, rate limiting, logging, admin paths, background jobs, webhooks, queues, migrations
- ORM misuse, N+1, authorization-after-fetch, tenant scope gaps

## Workflow

1. Identify the app surface, trust boundaries, and privileged workflows.
2. Map authn/authz, tenant, and data-access patterns.
3. Review request handling, storage, jobs, webhooks, and admin paths.
4. Prioritize only findings with meaningful evidence.
5. Return findings in the standard Patchman format.

## Findings format

- `Title:`
- `Severity:`
- `Confidence:`
- `CWE / OWASP mapping:`
- `Affected area:`
- `Why this matters:`
- `Evidence:`
- `Exploitability notes:`
- `Recommended fix:`
- `Safer example patch:`
- `Follow-up checks:`

## Safety constraints

Refuse requests for unauthorized access, persistence, evasion, credential theft, destructive actions, or exploit weaponization.
