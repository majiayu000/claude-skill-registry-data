---
name: incident-response
description: Contain an incident, verify recovery and preserve a factual postmortem. Triggers on "incident", "事故响应".
---

# Incident Response

## When to use

- Contain an incident, verify recovery and preserve a factual postmortem.

**Not for:** debugging for non-urgent diagnosis; shipping for planned releases.

## Steps

1. Assess impact and actual response authority; preserve timeline and evidence and avoid unapproved messaging.

2. Contain with authorized platform recovery before full root-cause diagnosis.

3. Check user impact and telemetry after each step; distinguish known facts from suspicions in authorized communication.

4. Diagnose after stabilization, verify durable fixes and prepare an approved postmortem with impact, cause and owned actions.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/postmortem/YYYY-MM-DD-<slug>.md` at the approved path.

## Verify

- Recovery has user-flow and operational evidence; timeline and follow-up remain factual and authorized.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/runbook-template.md](references/runbook-template.md) — runbook format for alert-linked playbooks
- [references/postmortem-template.md](references/postmortem-template.md) — blameless postmortem template + action-item tracking
- [references/dr-planning.md](references/dr-planning.md) — load during postmortem action-item planning for proactive DR; backup strategy, restore testing, DR drills, failover orchestration
