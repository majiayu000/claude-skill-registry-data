---
name: incident-response
description: Use during and after a production incident. Covers triage, mitigation before diagnosis, communication, and blameless postmortems that produce action items someone actually does.
metadata:
  category: devops
  version: 1.0.0
  tags: [incident, oncall, postmortem, mitigation, runbook]
---

# Incident Response

## Purpose

Restore service quickly, then learn from what happened. The two mistakes that define bad incident response are debugging before mitigating, and a postmortem whose action items are never done.

## When to Use

- An active production incident.
- Writing a postmortem.
- Building runbooks and an on-call practice.
- Reviewing a pattern of repeated incidents.

## Capabilities

- Triage: severity assessment and impact scoping.
- Mitigation: rollback, feature flag, traffic shift, scaling.
- Incident command: roles, communication, and timeline keeping.
- Blameless postmortems and contributing-factor analysis.
- Runbook authoring.

## Inputs

- The alert, the symptom, and the user impact.
- Recent changes: deploys, config changes, flag flips, dependency incidents.
- The system's rollback and degradation options.

## Outputs

- Service restored, with the mitigation recorded.
- A timeline of what happened and what was done.
- A postmortem with owned, dated action items.

## Workflow

1. **Establish impact** — Who is affected, how badly, and is it growing? This determines severity and whether to wake more people.
2. **Mitigate before diagnosing** — If a deploy went out in the last hour, roll it back. Understanding *why* it broke can wait; users cannot. This is the single most important rule and the one most often violated by engineers who want to know the answer.
3. **Assign roles** — For anything beyond a small incident: an incident commander (decides), a communications lead (updates stakeholders), and operators (execute). The commander does not type.
4. **Communicate on a cadence** — Status updates at fixed intervals, even when the update is "still investigating". Silence is interpreted as chaos.
5. **Record the timeline as you go** — Timestamped actions and observations, in the incident channel. Reconstructing it afterwards produces a fiction.
6. **Postmortem within a week** — Blameless, focused on contributing factors, with action items that have an owner and a date.

## Best Practices

- Roll back first. A rollback is reversible; a forward fix under pressure is a new deploy written by tired people.
- The person who found the problem should not also be the person coordinating the response and updating stakeholders. Split the roles.
- "Human error" is not a root cause. The question is why the system allowed a single human error to cause an outage.
- An action item without an owner and a date will not be done. An action item that says "be more careful" is not an action item.
- Runbooks are written when things are calm and used when they are not. A runbook that has never been followed end to end is a hypothesis.
- Track the number of postmortem action items completed. It is the only metric that shows whether the process is real.

## Examples

**Triage order — mitigation precedes understanding:**

```text
09:41  Alert: checkout 5xx rate 14% (SLO burn 30x)
09:42  Confirm impact: ~1,400 users/min failing checkout. SEV-1 declared.
09:43  Check recent changes: deploy 4c9a1f at 09:38 (3 min before onset).
09:44  MITIGATE: roll back to 8b2d0e. No diagnosis attempted yet.
09:47  Error rate returns to baseline. Impact ended. Incident downgraded.
09:50  NOW diagnose: 4c9a1f added an unbounded query to the pricing path;
       under production cardinality it exceeded the 3s DB timeout.
```

Nine minutes of impact. The alternative — debugging first — would have been forty.

**A postmortem action item that will actually be done:**

```markdown
| Action                                                    | Owner | Due        | Type       |
|-----------------------------------------------------------|-------|------------|------------|
| Add a query-cost regression test to the pricing suite      | @maya | 2026-03-18 | Prevent    |
| Alert on p99 DB query duration > 1s, per query fingerprint | @sam  | 2026-03-21 | Detect     |
| Add a `--dry-run` explain check to the migration CI step   | @maya | 2026-03-25 | Prevent    |
```

Not: "Team to be more careful with database queries." That is not an action item; it is a wish.

## Notes

- Severity should be defined in advance, with examples. Debating whether something is a SEV-1 during the incident wastes the minutes that matter most.
- The postmortem's audience is the future engineer who has not yet made this mistake. Write for them, and they will not have to.
- Repeated incidents with the same contributing factor mean the previous postmortem's action items were not completed. That is a management problem, not an engineering one.
