---
name: aiwf-incident-response-recovery
description: Use for suspected or confirmed security incidents involving compromised credentials, malware, ransomware, exposed services, data breaches, account takeover, malicious dependencies, suspicious activity, containment, evidence preservation, recovery, notification decisions, and post-incident improvement.
---

# AIWF Incident Response And Recovery

## Core Rule

Protect people and systems while preserving reliable evidence. Do not destroy, clean, rotate, isolate, notify, or restore before the scope, authority, evidence needs, and business impact are understood.

## Workflow

1. Establish incident commander, authorized scope, safety concerns, affected assets, discovery time, known indicators, business impact, and communication channel.
2. Create a case with `python scripts/create_incident_case.py --output <case-dir> --title <title> --owner <owner>`.
3. Record UTC events, source, collector, hashes, screenshots/log paths, access, and uncertainty without modifying originals.
4. Triage identity, endpoint, application, network, cloud, data, supply-chain, and third-party impact.
5. Propose containment options with evidence loss, service impact, reversibility, owner, and approval gate.
6. Eradicate only after containment and evidence needs are met. Recover from trusted sources and validate identity, data, service, monitoring, and backup integrity.
7. Determine notification duties using current official and qualified legal sources; do not make notification claims from memory.
8. Complete root-cause, control, owner, deadline, validation, and lessons-learned records.

Read `references/source-register.json` before current incident or notification guidance.

## Hard Gates

- Explicit approval is required before isolating hosts, disabling accounts, rotating credentials, blocking traffic, quarantining/deleting files, wiping/reimaging, restoring backups, contacting vendors, or notifying customers/regulators.
- Never communicate through a channel suspected of compromise.
- Do not run suspicious files, decryptors, cleanup tools, or exploit code on the affected host without an authorized plan.
- Do not claim legal chain of custody, forensic completeness, breach status, or recovery until supported.

## Output

Return current facts, uncertainty, timeline, affected assets/data, containment choices, approvals, recovery gates, communication plan, and residual monitoring.
