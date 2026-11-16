---
name: threat-model
description: Build a threat model for a planned feature, design, or component by identifying assets, actors, entry points, and trust boundaries, enumerating threats with STRIDE, and ranking mitigations, before or alongside implementation. Use when the user asks for a threat model, a security design review, abuse cases, or "what could go wrong" security analysis of a design or feature. Do not use for auditing existing code for vulnerabilities (use agent-kit:security-audit), for mapping the entry points of existing code (use agent-kit:attack-surface), or for general design trade-offs without a security focus; this skill reports and does not edit code.
---

# Threat model

Report the model without modifying code unless the user asks.

## 1. Describe the system

- From the design, the code, and the user, list the assets worth protecting (user data, credentials, money, availability, integrity of records), the actors (anonymous users, customers, admins, internal services, third parties), and the components and data stores involved.
- Draw the data flow in text: each entry point, what crosses it, and where trust boundaries are (browser to server, service to service, tenant to tenant, user input to an interpreter such as SQL or a shell). Mark assumptions the design does not state.

## 2. Enumerate threats

For each boundary and data flow, consider STRIDE and keep only threats that apply:

- **Spoofing:** weak or missing authentication, forgeable tokens, webhook callers that are not verified.
- **Tampering:** unvalidated input, mass assignment, client-controlled prices or IDs, unsigned data.
- **Repudiation:** missing audit logs for sensitive actions.
- **Information disclosure:** cross-tenant reads (IDOR), verbose errors, secrets in logs, over-broad API responses.
- **Denial of service:** unbounded queries, uploads, or fan-out; missing rate limits.
- **Elevation of privilege:** missing authorization checks, role changes by the user themselves, SSRF to internal services, injection.

For file uploads, also check malware scanning, content-type and size validation, and isolated processing of untrusted files.

Write each threat as an abuse case: who does what, through which entry point, to which asset.

## 3. Rank and mitigate

- Rate each threat by likelihood and impact (high, medium, low) and note existing controls.
- Propose specific mitigations tied to the design (where the check goes, which component enforces it), and say which are required before launch and which can follow.

## 4. Report

Give the system summary, the data flow with trust boundaries, a ranked threat table (threat, STRIDE category, likelihood, impact, mitigation), assumptions, and open questions for the user.

## Examples

- Use: "Threat model the new file upload feature." "What could go wrong with this webhook design?"
- Skip: "Audit src/ for SQL injection." (agent-kit:security-audit) "Which endpoints does this service expose?" (agent-kit:attack-surface)
