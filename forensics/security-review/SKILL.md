---
name: security-review
description: Review a proposed or implemented solution for security risks, threat coverage, control effectiveness, and security evidence. Use for focused architecture security reviews, threat-informed release checks, or security findings; do not use as penetration testing or as proof of compliance.
---

# Security Review

Produce an evidence-backed security assessment without inventing controls, classifications, test results, risk acceptance, or approval.

## Workflow

1. Read `AGENTS.md`, `architecture/toolkit-profile.yaml` when present, the requested review scope, architecture artifacts, code/configuration, deployment evidence, and prior security findings.
2. Establish assets, identities, data classifications, trust boundaries, entry points, privileged operations, external dependencies, deployment environments, and likely threat actors. Mark missing classifications or ownership as `To verify`.
3. Build the threat-and-control matrix in [references/security-review-method.md](references/security-review-method.md). Use a recognized threat method when required by the project; otherwise use a concise STRIDE-informed analysis without claiming exhaustive coverage.
4. Assess preventive, detective, responsive, and recovery controls. Verify implementation and test evidence rather than relying on design statements.
5. Report exploitable weaknesses, control gaps, unsafe defaults, unverifiable claims, and accepted residual risks separately. Include exact evidence and practical remediation.
6. Persist the review only when requested, using the configured review path or `architecture/reviews/SEC-NNN-<slug>.md`.

## Review Areas

- Identity, authentication, authorization, privilege boundaries, service identities, and emergency access
- Secrets, keys, certificates, rotation, and credential exposure
- Network boundaries, ingress/egress, private connectivity, segmentation, and administrative access
- Data minimization, encryption, integrity, retention, deletion, backup, restoration, and tenant isolation
- Input/output handling, injection, deserialization, file processing, SSRF, supply chain, and dependency provenance
- Logging, alerting, incident response, forensic usefulness, abuse detection, and security test coverage
- AI-specific threats when applicable: prompt injection, unsafe tool use, data exfiltration, model or retrieval poisoning, excessive agency, insecure output handling, and model/vendor trust

## Rules

- Treat scans and checklists as evidence inputs, not proof of security.
- Do not expose secrets, exploit live systems, perform destructive tests, or expand testing scope without explicit authorization.
- Distinguish design gaps from implementation defects and operational misconfiguration.
- Map each finding to an affected asset or boundary, credible threat, evidence, consequence, remediation, and owner when known.
- A risk exception requires scope, rationale, compensating controls, accountable owner, expiry/review date, and approval evidence.
- Never claim certification, compliance, or release approval.

## Output

Lead with the security posture and release-blocking findings. Include scope and limitations, assets and trust boundaries, threat-and-control matrix, prioritized findings, positive verified controls, residual risks, unverified items, and recommended owner/action.
