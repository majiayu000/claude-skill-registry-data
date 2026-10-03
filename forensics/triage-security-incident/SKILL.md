---
name: triage-security-incident
description: Triage suspected cybersecurity incidents through evidence-preserving collection, alert validation, UTC timeline construction, scope analysis, ATT&CK mapping, and containment and recovery decision support. Use for suspected account compromise, malware or ransomware, credential abuse, suspicious endpoint or cloud activity, data exfiltration, or service disruption. Do not use for offensive access, attribution claims, or unapproved response changes.
---

# Triage Security Incident

Turn incomplete alerts and artifacts into a defensible current assessment while preserving evidence and separating observation from inference.

Read [methodology](references/methodology.md) before collecting volatile evidence, mapping ATT&CK, or proposing containment.

## Establish the operating contract

1. Record the incident owner, decision authority, systems and identities in scope, evidence sources, collection authority, UTC reporting cadence, communication channel, legal or privacy constraints, and actions that require approval.
2. Treat analysis authority as read-only. Require explicit incident-commander approval before isolating systems, disabling accounts, revoking sessions, rotating credentials, blocking indicators, deleting artifacts, or changing production.
3. Preserve originals and analyze working copies. If preservation, authority, or chain-of-custody requirements are unclear, stop invasive collection and request direction from the incident owner or counsel.
4. Keep public communication, regulatory notification, customer notification, law-enforcement contact, and threat-actor contact with the authorized organization roles.

## Execute the triage

1. Open an incident record with a provisional severity, triggering question, first-seen time, reporter, affected service, business impact, and currently authorized actions.
2. Preserve evidence with source, collector, collection method or query, native time range and timezone, UTC normalization, export time, integrity hash where applicable, storage location, and access history. Prioritize volatile or short-retention sources when safe.
3. Validate the alert against raw telemetry, expected administration, deployment history, asset and identity context, clock skew, sensor health, and plausible benign explanations.
4. Build a UTC timeline. Label each entry `observed`, `inferred`, or `unknown`; link every observed event to an evidence ID and preserve the raw timestamp.
5. Scope identities, sessions, endpoints, workloads, cloud resources, email, applications, network paths, credentials, persistence, data accessed, and time window. Record both confirmed impact and searched-but-not-found areas.
6. Map only evidence-backed behavior to MITRE ATT&CK. Treat an indicator match as a lead until activity and context corroborate it.
7. Develop containment options with objective, supporting evidence, expected blast radius, reversibility, service impact, approver, rollback, and validation signal. Recommend the least disruptive option that meets the containment objective.
8. Define eradication and recovery criteria, evidence-retention needs, clean-state validation, credential sequencing, heightened monitoring, and recurrence checks.
9. Maintain an explicit queue of open questions, owners, next evidence, decision deadlines, and status-update time.

## Apply evidence rules

- Cite an evidence ID for every factual incident claim. Preserve exact queries, filters, tool versions, time windows, timezone assumptions, and known collection gaps.
- Keep `observed`, `inferred`, and `unknown` distinct. Assign `high`, `medium`, or `low` confidence to material inferences and list supporting and contradicting evidence.
- Treat IOCs, reputation matches, malware-family labels, and ATT&CK mappings as context, not standalone proof of compromise or attribution.
- Do not use `breach`, `exfiltration`, `persistence`, `eradicated`, or `contained` unless the recorded evidence and validation criteria support the term.
- Do not claim chain of custody when collection history or integrity controls are missing. State the limitation plainly.
- Minimize personal data, secrets, tokens, message content, and unrelated employee or customer activity in working notes and reports.

## Enforce safety constraints

- Never hack back, contact an adversary, pay a ransom, deploy offensive tooling, or access infrastructure outside the organization's authorized boundary.
- Do not execute samples, open suspicious attachments, or upload evidence to public sandboxes. Use an approved isolated analysis environment only when separately authorized.
- Do not power off, reboot, quarantine, delete, remediate, rotate, revoke, or block before considering evidence loss and receiving the required approval.
- Use out-of-band communications when the normal channel may be monitored, but only through the organization's approved process.
- Escalate suspected regulated-data exposure, insider activity, or legal-hold implications to the incident owner and counsel without making a legal conclusion.
- If active harm is underway, present the fastest reversible containment options and their evidence tradeoffs immediately; do not silently perform them.

## Return the output contract

Return these sections in order:

1. `Current assessment` — what is observed, likely, unknown, business impact, provisional severity, and next decision.
2. `Authority and scope` — incident owner, approved actions, systems, identities, time window, and exclusions.
3. `Evidence manifest` — evidence ID, source, collector or query, native and UTC time, hash or integrity note, storage, and limitation.
4. `Timeline` — UTC time, event, evidence ID, observation or inference label, confidence, and significance.
5. `Scope matrix` — entity, relationship, evidence searched, status, impact, and remaining question.
6. `ATT&CK map` — tactic and technique, observed behavior, evidence IDs, and confidence.
7. `Containment decision log` — option, objective, blast radius, reversibility, approval, execution status, and validation result.
8. `Recovery criteria and next actions` — owner, deadline, dependency, success signal, and next update time.
9. `Limitations` — missing telemetry, retention gaps, clock issues, unavailable owners, and unverified assumptions.

## Pass the quality gate

Before finalizing, verify that:

- Every material factual claim links to evidence and every inference is labeled with confidence.
- Timeline entries preserve native time and normalize consistently to UTC.
- Scope includes identities, sessions, systems, control-plane changes, and data impact where applicable.
- ATT&CK mappings describe observed behavior rather than speculation or actor attribution.
- Containment recommendations include approval, blast radius, evidence-loss risk, rollback, and verification.
- No report overstates containment, eradication, exfiltration, or attribution, and no unapproved state change was performed.
