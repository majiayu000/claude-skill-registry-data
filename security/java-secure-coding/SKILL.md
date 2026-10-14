---
name: java-secure-coding
description: "Trigger: Java secure coding, Oracle Secure Coding Guidelines, input validation, trust boundaries, deserialization, least privilege, sensitive data. Review Java code for secure implementation practices."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.0.4"
---

# Skill: java-secure-coding

## Activation Contract

Use this skill when reviewing or designing Java code for secure coding practices: input validation, trust boundaries, injection, serialization/deserialization, sensitive data, resource exhaustion, mutability, access control, and third-party code risk.

Do **not** use this skill for full threat modeling, compliance audits, cryptography design, infrastructure hardening, or non-Java security work.

## Responsibility

This skill teaches Java secure-coding review based on Java platform concerns and Oracle Secure Coding Guidelines. It does not call other skills, certify security, or replace a formal security review.

## Required Context

- Data sources and trust boundaries.
- Inputs accepted and outputs generated.
- Sensitive data handled.
- Resource-intensive operations.
- Serialization, reflection, XML, SQL, command execution, or third-party dependencies involved.

## Context Budget

- Keep this `SKILL.md` focused on secure-coding decisions.
- Use `references/java-secure-coding-guidance.md` for checklist details.

## Hard Rules

- Establish trust boundaries before judging input safety.
- Validate and canonicalize untrusted input before use.
- Avoid dynamic SQL; use parameterized statements or safe higher-level APIs.
- Do not log secrets or expose sensitive data in exceptions.
- Release resources and defend against resource exhaustion.
- Treat deserialization, XML, reflection, JNDI, command execution, and third-party code as high-risk areas.
- Prefer least privilege and minimal accessibility.

## Decision Gates

| Condition | Action |
|---|---|
| Untrusted input crosses boundary | Validate type, range, size, format, and canonical form. |
| SQL uses string concatenation | Replace with parameterized query shape. |
| XML or deserialization is involved | Require restrictive parser/filter configuration. |
| Sensitive data appears in logs/exceptions | Remove, redact, or sanitize. |
| Resource size depends on input | Add limits and overflow-safe checks. |
| Public/extensible surface exposes internals | Reduce accessibility or document/guard contract. |

## Execution Steps

1. Identify trust boundaries and untrusted data.
2. Check injection, inclusion, deserialization, and resource risks.
3. Check sensitive-data exposure.
4. Check mutability, access, and privilege boundaries.
5. Return findings with severity and remediation.

## Output Contract

Return:

- Secure-coding verdict: `low_risk`, `needs_hardening`, or `high_risk`.
- Findings with severity and evidence.
- Recommended remediation.
- Residual risks and assumptions.
- Areas requiring formal security review, if any.

## References

- `references/java-secure-coding-guidance.md` — Java secure-coding checklist based on official guidance themes.

## Assets

- None.
