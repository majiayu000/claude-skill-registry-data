---
name: soc-operations
description: Security Operations Center skill for alert triage, detection engineering, incident response, log analysis, threat hunting, SIEM queries, EDR investigation, timeline building, IOC handling, escalation notes, containment recommendations, and analyst-ready reporting. Use for blue-team operations, suspicious event analysis, and defensive cybersecurity workflows.
---

# SOC Operations

## Operating Rules

- Preserve evidence and distinguish observed facts from hypotheses.
- Establish time zone, asset identity, user identity, data source, and log reliability before conclusions.
- Prioritize containment for active compromise while avoiding unnecessary business disruption.
- Map activity to MITRE ATT&CK when it improves communication, not as decoration.

## Triage Workflow

1. Summarize the alert: source, time, asset, user, rule, severity, and raw signals.
2. Validate signal quality: duplicates, known benign patterns, enrichment, and telemetry gaps.
3. Build a timeline of process, network, auth, file, registry, cloud, and identity events.
4. Decide disposition: false positive, benign true positive, suspicious, confirmed incident, or insufficient data.
5. Produce analyst notes with evidence, impact, containment steps, and next queries.

## Output Format

- `Disposition`: one clear status.
- `Evidence`: concrete events and timestamps.
- `Scope`: affected users, hosts, accounts, workloads, and data.
- `Actions`: containment, eradication, recovery, and monitoring.
- `Gaps`: missing logs, access needed, or assumptions.

