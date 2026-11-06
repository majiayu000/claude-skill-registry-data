---
name: runbook-write
description: >-
  User-invoked as /runbook-write <incident-type>. Drafts a new operational
  runbook in docs/runbooks/ using the Aegis runbook template. Use to document
  how on-call responds to a given incident/fault class.
allowed-tools: Read, Grep, Glob, Bash, Write
invocation: /runbook-write <incident-type>
---

# Runbook Write

Draft a runbook for the incident type `$ARGUMENTS` (e.g. `memory-access-
violation`, `deadlock`, `resource-exhaustion`, `log-forensics-anomaly`).

## Steps

1. Cross-reference the fault class against the agents' declared consensus
   weights, `core/fault_codes.py`, and `IncidentMode` so the runbook matches
   real product classifications.
2. Write `docs/runbooks/<incident-type>.md` using the template below.
3. Add an index line to `docs/README.md` and `docs/runbooks/` index if present.

## Aegis runbook template

```markdown
# Runbook - <Incident Type>

- Fault class / mode: <fault_code / IncidentMode>
- Severity default: <P0|P1|P2>
- Owner / escalation: <team / on-call>

## Detection signals
- How Aegis surfaces this (events, ConfidenceLevel, SkepticVerdict cues).

## Triage (first 5 minutes)
1. <step> - expected: <result>

## Investigation
- Which analysis agents dominate (consensus weights), what RCAReport fields to
  read first, which dumps/logs to pull.

## Mitigation
1. <step> - idempotent? rollback? requires AEGIS_PROD_CONFIRMED?

## Escalation
- When to raise a HITLRequest / page on-call (PagerDuty) / post to the incident
  Slack channel.

## Verification & resolution
- How to confirm the incident is resolved and move to post-mortem.

## Related
- ADRs, playbooks, prior post-mortems.
```

## Output

Print the runbook path. Recommend the `incident-analyst` agent review the
mitigation/escalation steps for safety before the runbook is trusted.
