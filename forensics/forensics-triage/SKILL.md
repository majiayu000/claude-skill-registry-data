---
name: forensics-triage
description: Digital forensics and incident response triage skill for disk, memory, network, cloud, and endpoint artifacts. Covers Volatility 3, Velociraptor, KAPE, Plaso, Autopsy, Chainsaw, Hayabusa, Zeek, Arkime, EVTX, AWS/Azure/GCP audit logs, and timeline reconstruction. Use to extract IOCs, build incident timelines, and produce defensible analyst reports.
---

# Forensics Triage

## Operating Rules

- Preserve chain of custody: hash before and after handling; record acquisition method, examiner, and timezone (UTC preferred).
- Work on copies; mount images read-only; document every tool, version, and flag.
- Separate observation (`what the artifact says`) from inference (`what likely happened`).

## Triage Workflow

1. Collect: `KAPE` targets, `velociraptor` artifacts, memory via `winpmem`/`avml`, cloud logs via provider exports.
2. Parse: `plaso/log2timeline` for super-timeline; `chainsaw`/`hayabusa` for Windows EVTX; `volatility3` for RAM; `bulk_extractor` for carving.
3. Reconstruct timeline: anchor on initial access, then enumerate execution, persistence, lateral movement, collection, exfil, impact.
4. Extract IOCs: hashes, domains, IPs, mutexes, registry keys, scheduled tasks, services, cron, browser artifacts, cloud principals.
5. Correlate: cross-host, cross-cloud, identity-tier; build a narrative with ATT&CK mapping.
6. Report: timeline, scope, dwell time, attribution confidence, recommendations.

## Cloud and Identity Focus

- AWS: CloudTrail, GuardDuty, IAM Access Analyzer, Athena queries; assume-role chains.
- Azure: AAD sign-in/audit, MCAS, Defender; OAuth consent abuse.
- GCP: Cloud Audit, Workspace Login; service account key misuse.
- Identity: token theft, primary refresh token abuse, federation trust manipulation.

## Output Contract

- `chain-of-custody.md`, `acquisition.log`.
- `timeline.csv` super-timeline with annotations.
- `iocs.stix.json`, `findings.md` per host/account.
- `report.md`: executive narrative, root cause, dwell time, scope, recovery steps, lessons learned.
