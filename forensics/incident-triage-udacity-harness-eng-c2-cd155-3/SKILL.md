---
name: incident_triage
description: Use when a request requires investigating an incident, separating evidence from hypotheses, or choosing the next diagnostic checks.
---

# Incident triage

Start from observed incident state. Separate confirmed facts, working
hypotheses, and unknowns. A deployment preceding an error increase establishes
correlation, not root cause. Never convert `INVESTIGATING` into `RESOLVED`, or
`DEGRADED` into `HEALTHY`, without fresh evidence.

For an initial triage note, identify the incident, affected service,
environment, current health, measured impact, and current deployment. Then name
the smallest useful evidence-gathering steps. Prefer a fresh health snapshot,
deployment history, and service logs before recommending a production change.

Do not say that a restart, rollback, mitigation, or recovery occurred unless
the authoritative state confirms it. If evidence is incomplete, state what is
unknown and what observation would reduce that uncertainty.
