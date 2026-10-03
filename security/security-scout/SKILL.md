---
name: security-scout
description: Perform practical security review for code, diffs, dependencies, configuration, auth flows, data handling, and deployment changes. Use when the user asks for security audit, threat model, vulnerability review, secret scan, authz/authn check, injection risk, supply-chain risk, or secure implementation guidance. Do not use for exploit development or unrelated style review.
---

# Security Scout

Find realistic security risks and fix paths.

## Workflow

1. Identify assets: secrets, user data, money movement, permissions, tokens, files, network calls, admin surfaces, and logs.
2. Identify trust boundaries: browser/server, user/admin, tenant/tenant, internal/external, CI/runtime.
3. Review the changed code and the closest callers, validators, policies, and tests.
4. Check the risk categories that fit the change.
5. Recommend safe fixes and verification.

## Risk Categories

- Authentication bypass or weak session handling.
- Authorization and tenant-boundary mistakes.
- Injection: SQL, command, template, path, SSRF, XSS, deserialization.
- Secret exposure in code, logs, errors, URLs, screenshots, or build artifacts.
- Unsafe file upload/download or path traversal.
- Dependency, package script, lockfile, and CI supply-chain risk.
- Missing rate limits, replay protection, CSRF, or input limits.
- Insecure defaults in deployment, CORS, cookies, TLS, or cloud IAM.

## Reporting

For each finding include:

- Severity: `Critical`, `High`, `Medium`, or `Low`.
- Preconditions: what an attacker needs.
- Impact: what they gain or break.
- Evidence: exact code path.
- Fix: concrete mitigation.
- Verification: test, scan, or manual check.

If a secret-like value appears, do not print the full value. Show only the file
and a short redacted prefix/suffix.
