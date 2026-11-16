---
name: kit-security-audit
description: Audit a codebase or component for security vulnerabilities, including injection, broken access control, secrets, unsafe deserialization, and vulnerable dependencies, and report evidence-based findings with severity and file locations. Use when the user asks for a security audit, security review of a project or component, or a dependency vulnerability check. Do not use for reviewing an ordinary diff for general correctness (use kit-code-review) or for fixing a specific known bug; this skill reports and does not edit code.
---

# Security audit

Report findings without modifying code unless the user explicitly asks for fixes. Do not run exploits against shared, staging, or production systems, and do not send code or data to external services without permission.

## 1. Scope and map the attack surface

- Confirm the scope: the whole repository, a component, or dependencies only.
- Identify entry points: HTTP routes, CLI arguments, message consumers, file uploads, webhooks, and scheduled jobs. Identify trust boundaries and where untrusted data enters.
- Note authentication and authorization mechanisms, data stores, secrets handling, and external calls.

## 2. Check the code

Trace untrusted input from each entry point to where it is used. Look for:

- **Injection:** SQL or NoSQL built from strings, shell commands with interpolated input, template injection, LDAP or XPath injection.
- **Access control:** missing authentication or authorization checks, insecure direct object references, privilege escalation, missing ownership checks.
- **Paths and files:** path traversal, unsafe archive extraction, unrestricted uploads.
- **Secrets and data:** hardcoded credentials or keys, secrets in logs or error messages, sensitive data exposure, weak hashing for passwords.
- **Unsafe processing:** deserialization of untrusted data, `eval`, server-side request forgery, XML external entities, open redirects.
- **Web concerns:** cross-site scripting, CSRF on state-changing requests, permissive CORS, missing security headers where the project manages them.
- **Cryptography and randomness:** homemade crypto, weak algorithms, predictable tokens.

## 3. Check dependencies and configuration

- Run the ecosystem's audit tool when it is available and does not change files, such as `npm audit`, `pnpm audit`, `pip-audit`, `cargo audit`, `govulncheck`, or `bundle audit`. If none can run, inspect lockfiles and report known-vulnerable versions you can identify, stating how you identified them.
- Review configuration for debug modes, default credentials, overly broad permissions, and secrets committed to the repository.

## 4. Verify and rate

For each candidate, confirm the data flow by reading the code; discard what you cannot support. Rate by impact and exploitability:

- **Critical:** remote compromise, authentication bypass, or broad data exposure reachable by unauthenticated users.
- **High:** exploitable by authenticated users or with modest preconditions.
- **Medium:** requires unusual conditions, or limited impact.
- **Low:** defense-in-depth improvements.

## 5. Report

Order findings by severity. For each, give the title, severity, `file:line`, the vulnerable data flow, a concrete attack scenario, and a remediation. Then list what was audited, what was out of scope, and what could not be verified. If nothing significant was found, say so and describe what was checked.

## Examples

- Use: "Do a security audit of this API." "Check our dependencies for known vulnerabilities." "Is the upload handler safe?"
- Skip: "Review my PR." (use kit-code-review) "Fix the SQL injection in users.ts." (a known fix; implement it directly)
