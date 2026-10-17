---
name: aiwf-application-api-security
description: Use for application and API threat review, authentication, authorization, sessions, cookies, CORS, CSRF, input validation, injection, uploads, SSRF, deserialization, browser security, webhooks, rate limits, LLM tool boundaries, and secure-code remediation.
---

# AIWF Application And API Security

## Core Rule

Trace trust boundaries and server-enforced authorization before proposing controls. Client checks, hidden UI, model instructions, and possession of an identifier are not authorization.

## Workflow

1. Identify assets, actors, entry points, trust boundaries, data flows, roles, and abuse cases.
2. Inspect framework versions, auth/session design, permission checks, validation, parsing, storage, logging, and deployment assumptions.
3. Test object-level and function-level authorization separately from authentication.
4. Review input/output encoding, query construction, file/archive handling, outbound requests, redirects, serialization, subprocesses, secrets, and error behavior.
5. For LLM/RAG/tool systems, treat retrieved content and model output as untrusted; enforce tool allowlists, scoped credentials, validation, human gates, and data boundaries outside the prompt.
6. Rank findings by evidence, affected asset, realistic impact, reachability, and confidence. Do not invent CVSS or exploitability.
7. Patch one bounded finding at a time and run focused regression and negative tests.

Read `references/source-register.json` before versioned control claims.

## Bounded Defensive Authority

- Passive review and non-destructive checks against local code, tests, fixtures, localhost, and user-owned development environments are allowed.
- Obtain explicit target and authorization before scanning remote hosts, testing real accounts, fuzzing production, replaying webhooks, or using exploit payloads.
- Never perform credential attacks, persistence, stealth, exfiltration, destructive testing, or protection bypass.
- Do not weaken auth, TLS, CORS, CSRF, CSP, validation, logging, or permissions as a fix.
- Add `aiwf-data-privacy-protection` for personal data and `aiwf-online-infrastructure-security` for deployment controls.

## Output

Use the shared security finding contract: ID, asset/boundary, evidence, confidence, severity rationale, impact, remediation, validation, owner/status, and residual risk.
