---
name: detection-engineering
description: Detection engineering skill for writing, testing, and tuning Sigma, YARA, YARA-L, Suricata, Snort, Zeek, KQL, SPL, EQL, Chronicle, and Elastic detection rules. Covers ATT&CK coverage mapping, telemetry gap analysis, false-positive tuning, detection-as-code pipelines, and validation with Atomic Red Team and Caldera. Use to design durable detections backed by tests.
---

# Detection Engineering

## Operating Rules

- Start from a threat behavior, not a single IOC. Rules expire; behaviors persist.
- Every rule ships with: hypothesis, data source, ATT&CK mapping, false-positive notes, response action, and a test.
- Tune for analyst time, not raw event volume. A noisy critical is a broken critical.

## Authoring Workflow

1. State hypothesis: actor, technique, observable, data source, confidence.
2. Identify telemetry: process, file, registry, network, auth, cloud, email, identity, EDR fields.
3. Draft rule in the platform's native DSL; keep selectors readable; comment non-obvious filters.
4. Generate matched and unmatched test events; run in a dry-run pipeline.
5. Validate with Atomic Red Team / Caldera tests; record true positive evidence.
6. Tune: add allow-lists with reasons and review dates; never silently broaden.
7. Ship with a runbook: triage steps, expected next queries, containment.

## Coverage Strategy

- Maintain a matrix of ATT&CK techniques × data sources × rule IDs × last-tested date.
- Track gaps as backlog items with prerequisite telemetry (e.g., enable Sysmon 1/3/10/11).
- Score detections on durability, fidelity, and response cost.

## Output Contract

- `rules/<platform>/<id>.yml` with metadata block.
- `tests/<id>/` with positive and negative pcaps, EVTX, or JSON.
- `coverage.csv`: ATT&CK × rule × status × last_validated.
- `runbooks/<id>.md`: analyst playbook.
- `release-notes.md`: what changed, why, expected volume delta.

## Example: Sigma skeleton

```yaml
title: Suspicious encoded PowerShell
status: experimental
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    Image|endswith: '\\powershell.exe'
    CommandLine|contains: ' -enc '
  condition: selection
falsepositives:
  - admin scripts, SCCM
level: medium
```

KQL equivalent (untested):

```kql
DeviceProcessEvents
| where FileName =~ "powershell.exe"
| where ProcessCommandLine has " -enc "
```
