---
name: incident-response-and-postmortems
description: Use when defining severity levels and on-call procedures, when creating a runbook for a critical service, when an incident is actively happening and a structured response is needed, or when writing a blameless postmortem after Sev1 or Sev2 resolution.
---

# Incident Response and Postmortems

## Overview

Define how the team detects, mitigates, communicates about, and learns from production incidents — *before* the first one. Output is `.forge/incident-response.md` — severity definitions with response times, the declare-mitigate-communicate-resolve-review flow, runbook template, blameless postmortem template, and the comms templates (internal and external). Pairs with `observability` (alerts feed the declare step) and `error-handling-and-resilience` (the failure modes alerts watch for).

## When to Use

- A service is going to production and there's no on-call process
- An incident just happened and the team handled it ad-hoc — write the process before the next one
- A postmortem is due and there's no template
- Severity levels are inconsistent across teams
- A runbook is needed for a critical service

## When NOT to Use

- Localhost-only or pre-prod systems with no users
- A trivial bug fix — that's `debugging-and-recovery`
- A near-miss that didn't affect users — log it, learn from it, but don't fire the full process

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We're too small for an incident process" | Incidents don't wait for headcount. The first Sev1 at 4 staff is when you learn the process you didn't build. |
| "We'll write the postmortem later" | Memory fades within 48h. Two weeks later the timeline is a guess. |
| "It was their fault" | Blame ends learning. Every "someone clicked the wrong button" is a system that allowed the wrong button to be clicked. |
| "Action items can wait until we have time" | Unowned action items are wishes. They never ship. |
| "We don't need severity levels — just fix everything fast" | Without severity, every alert pages every human. Fatigue sets in. The real Sev1 gets missed. |
| "Comms can be informal during the incident" | "Informal" means three different stories reaching three different audiences. Customers, board, and team need consistent, scheduled updates. |

## Red Flags

- No documented severity definitions
- A critical service with no runbook
- A postmortem that uses words like "negligence", "should have known", "failure to follow procedure" — blame language
- Action items in a postmortem without an owner and a deadline
- The same incident class recurring (auth outage, queue backup, DB lock) without an action item from the previous postmortem closed
- No external comms during a customer-visible outage
- The on-call hand-off has no documented context (no runbook, no recent incident summary)

## Core Process

### Step 1: Define severity levels

In `.forge/incident-response.md`:

| Sev | Definition | Response time | Examples |
|---|---|---|---|
| Sev1 | Service down or major data integrity issue | Page on-call immediately, all-hands within 15min | Site down, DB corruption, security breach |
| Sev2 | Major feature broken or significant degradation | Page on-call, response within 30min | Login broken, checkout failing, search down |
| Sev3 | Minor feature broken or low-impact degradation | Ticket, response within 4h business | Non-critical endpoint slow, edge-case bug |
| Sev4 | Cosmetic or no user impact | Ticket, response next business day | Typo, log noise, internal tool glitch |

### Step 2: Write the response flow

Five steps, in order:

1. **Declare** — anyone can declare. Use the standard channel (`#incident-active`). State: severity guess, what's broken, what's the impact.
2. **Mitigate** — restore service first. Root-cause investigation comes after. Acceptable mitigations: rollback, feature flag off, traffic shift, scale up.
3. **Communicate** — internal updates every 30min for Sev1, every 60min for Sev2. External status page updated within 15min of declare (Sev1) or 30min (Sev2). Comms owner is named, not "whoever notices."
4. **Resolve** — service restored, customer-visible impact ended. Mark resolved on status page.
5. **Review** — postmortem within 5 business days for Sev1/Sev2.

### Step 3: Create the runbook template

For every critical service (anything with a Sev1 or Sev2 potential), a runbook must contain:

- **Service summary** — what it does, what fails when it goes down
- **Owners** — primary on-call, escalation chain
- **Dashboards** — links to the observability dashboards (cross-ref `observability` skill)
- **Common failure modes** — top 5 with first-response steps
- **Mitigation playbook** — feature flag locations, rollback commands, traffic shift recipes
- **Escalation criteria** — when to page the next tier
- **Recovery verification** — how you know it's actually fixed (synthetic check, key metric returning to baseline)

Cross-reference the runbook URL in every alert (cross-ref `observability` rule: every alert has a runbook link).

### Step 4: Write the blameless postmortem template

In `.forge/incident-response.md`:

```markdown
# Postmortem: <one-line summary>

## Impact
- Severity: Sev1/2/3
- Duration: HH:MM start to HH:MM end (TZ)
- Affected: <number of users, % of traffic, $ if measurable>

## Timeline (UTC, all times verified from logs)
- 14:02 — Deploy v2.4.1 to production
- 14:08 — Error rate climbs above 5% on /api/checkout
- 14:11 — Alert fires; on-call paged
- 14:14 — On-call acks
- 14:22 — Mitigation: rollback to v2.4.0 initiated
- 14:26 — Rollback complete, error rate returns to baseline
- 14:31 — Incident resolved; status page updated

## Root cause
<what happened, mechanically. No blame language.>

## Contributing factors
- <missing alert, weak test, flaky dependency, slow rollback tooling, etc.>

## What went well
- <fast detection, clean rollback, good comms>

## What we learned
- <pattern that future work should respect>

## Action items
| ID | Action | Owner | Deadline | Tracking |
|---|---|---|---|---|
| AI-1 | Add integration test covering the checkout path | @owner | YYYY-MM-DD | LINK-123 |
| AI-2 | Reduce rollback time from 8min to <2min | @owner | YYYY-MM-DD | LINK-124 |
```

**Blameless rule:** the word "should have" is forbidden. Replace with "the system did not have." Every action item targets a system, not a person.

### Step 5: Define comms templates

Three audiences, three templates:

- **Internal status update** (every 30min Sev1 / 60min Sev2 in `#incident-active`): current status, mitigation in progress, ETA, next update time
- **External status page** (15min Sev1 / 30min Sev2): what's affected, what we're doing, when the next update is — no internal jargon
- **Customer comms post-resolution** (within 24h for Sev1, 72h for Sev2): impact summary, root cause in plain language, what we're doing to prevent recurrence

## Verification

- [ ] `.forge/incident-response.md` written
- [ ] Severity levels defined with response-time SLAs
- [ ] Every critical service has a runbook linked from its alerts
- [ ] Postmortem template includes timeline, impact, root cause, contributing factors, action items with owners
- [ ] Last 3 Sev1/Sev2 postmortems completed within 5 business days
- [ ] No postmortem in the last 90 days contains "should have" or blame language
- [ ] Every action item from the last 5 postmortems has owner + deadline (open or closed)
- [ ] External status page updated within SLA on the last 3 customer-visible incidents
