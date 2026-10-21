---
name: security-review
description: Audit actual trust boundaries and abuse paths with current guidance. Triggers on "security review", "安全审查".
---

# Security Review

## When to use

- Audit actual trust boundaries and abuse paths with current guidance.

**Not for:** auth-implementation for building auth; incident-response for compromise.

## Steps

1. Identify assets, inputs, identities and relevant changes; verify authoritative current references.

2. Trace injection, cross-user access, upload, secret and supply-chain abuse paths.

3. For LLM features, inspect enforced tool permissions, untrusted input and output handling rather than relying on prompt instructions.

4. Validate safe reproduction and report impact, severity and remedies at the approved path; retest fixes and state assessment limits.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/security-report.md` when durable findings are requested.

## Verify

- Findings tie attacker-controlled inputs to actual impact; checklist completion is not proof of security.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/owasp-patterns.md](references/owasp-patterns.md) — OWASP Top 10 prevention code examples (injection, auth, XSS, access control, SSRF, validation, rate limiting, LLM output).
- [references/compliance-process.md](references/compliance-process.md) — load when PII/payment assets appear in the threat model; GDPR/CCPA process layer: data inventory, DSR fulfillment, retention, right-to-erasure, privacy-by-design, audit readiness
