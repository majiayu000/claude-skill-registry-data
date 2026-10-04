---
name: security
description: "Implements security-sensitive changes with conservative trust boundaries, secret protection, tests, and verification."
---

# Skill: security

## Purpose

Handle security-sensitive work with explicit verification and conservative assumptions.

## Security Invariants

Never hardcode or expose:

- passwords;
- tokens;
- private keys;
- API secrets;
- Wi-Fi credentials;
- database credentials;
- personal data;
- internal-only infrastructure details.

Never log secrets.

Never expose internal exception details in public responses.

## Inspect Before Security Changes

Before changing security-sensitive behavior, inspect:

- existing auth/authz patterns;
- middleware;
- configuration;
- secret handling;
- input validation;
- serialization/deserialization;
- dependency versions if relevant;
- existing tests;
- official documentation when needed.

Do not implement security-sensitive behavior from unverified memory.

## Threat Areas

Be careful with:

- authentication;
- authorization;
- session handling;
- CSRF/CORS;
- SSRF;
- SQL/NoSQL injection;
- shell injection;
- path traversal;
- unsafe deserialization;
- XML/entity expansion;
- template injection;
- user-controlled URLs;
- file uploads;
- dependency/supply-chain risks;
- secrets in logs, traces, fixtures, snapshots;
- insecure randomness;
- replay risks;
- rate limits and abuse paths.

## Authorization Rule

Authentication answers "who are you?"

Authorization answers "are you allowed to do this?"

Do not confuse them, unless the goal is to create tomorrow's incident report.

## Input Handling

Validate untrusted input at boundaries.

Rules:

- parse explicitly;
- reject invalid states;
- normalize only when safe;
- preserve original input when needed for audit/debugging;
- avoid blacklist-only validation for security decisions;
- avoid shell/string concatenation for commands and queries.

## Error Handling

Public errors should be safe and consistent.

Internal logs may include diagnostic context but must not include secrets or personal data.

Do not swallow security-relevant errors silently.

## Security Review Output

Report:

- threat or vulnerability;
- affected code path;
- exploitability conditions;
- impact;
- fix;
- validation;
- residual risk.
## Extended References


For deeper work, read:

- `../../engineering/16_security_philosophy.md`
