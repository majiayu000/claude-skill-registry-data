---
name: observability-ops
description: Make systems observable and operable — logs, metrics, runbooks, alert design, incident response, blameless postmortems.
version: 1
triggers: observability, logging, metrics, alerts, runbooks, incident response, postmortem
category: Engineering & code
blurb: Make systems observable and operable — logs, metrics, runbooks, alert design and blameless postmortems.
archetype: knowledge
example: Design the alerts and runbooks for this service.
---

# Observability & Ops — the SRE seat

If you can't see it, you can't run it. Ships include the signals and procedures to keep the service alive.

## When to use
- Launching or changing any service or automation that runs unattended.
- Designing alerts, dashboards, or on-call procedures.
- Incidents: detect → triage → mitigate → learn.

## Method
1. **Three signals**: structured logs (correlation ids), metrics (requests/errors/latency/saturation), traces or at least timings — at every edge.
2. **Alerts**: symptom-based (user-visible pain), few and actionable; every alert links its runbook; tune thresholds to reality; no noise storms.
3. **Runbooks**: one per failure mode — symptoms, check steps, mitigation, escalation, recovery verification.
4. **Incident flow**: acknowledge → assess blast radius → stabilize (rollback is the first option) → communicate status → fix → blameless postmortem with tracked actions.
5. **Backups**: tested restores, not just scheduled backups.
6. **No silent failure**: anything that can fail unattended has a health signal; jobs report success too (heartbeats).

## Artifacts
- Dashboards, alert definitions + runbooks, postmortems, restore-tested backup records.

## Quality gates
- [ ] Every service emits health, error-rate, and latency signals.
- [ ] Every alert has a runbook and an owner.
- [ ] Backups restore-tested at least once per season.
- [ ] Postmortem actions tracked to closure.

## Red lines
- No paging on causes nobody can act on; no unowned alerts.
- Never disable monitoring to make a problem "disappear".

## Related
`ci-cd-pipeline` (deploy+rollback) · `release-management` (post-release checks) · `backend-engineering` (hooks).
