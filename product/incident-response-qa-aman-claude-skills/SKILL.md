---
name: incident-response
description: >
  Run a structured incident response. Use when the user says "we have an incident",
  "production is down", "service is degraded", "on-call response", "p0 incident",
  "something is broken in prod", "help me manage this incident", "incident commander",
  or there is an active production issue requiring coordinated response
  - even if they don't explicitly say "incident response".
---

## Overview

Based on the **Google SRE Book** by Beyer, Jones, Petoff & Murphy. Google's incident management framework establishes clear roles, communication protocols, and decision hierarchies that let teams respond to complex outages without chaos. The core principle: when systems fail, the response should be calmer and more structured than the incident itself.

Three SRE roles during an incident:
- **Incident Commander (IC)** - owns the response, makes decisions, delegates
- **Operations Lead** - makes changes to the system (the IC does not touch production)
- **Communications Lead** - handles stakeholder updates, keeps IC focused on the incident

## Workflow

### Step 1: Declare the incident

If in doubt, declare. It's always easier to stand down an incident than to escalate a non-incident that becomes one.

Set severity:

| Severity | Criteria | Response time |
|----------|----------|---------------|
| SEV1 / P0 | Total outage, revenue impact, data loss | Immediate - all hands |
| SEV2 / P1 | Significant degradation, major feature down | < 15 min response |
| SEV3 / P2 | Minor degradation, workaround available | < 1 hour response |

### Step 2: Assign the IC

One person owns the incident. The IC:
- Does NOT make changes to production themselves
- Delegates all technical actions to the Operations Lead
- Asks for status updates, not details ("what's the impact?" not "show me the logs")
- Makes the call to escalate, rollback, or stand down

### Step 3: Open the incident channel

Create a dedicated Slack channel or incident doc immediately. Post within 2 minutes:

```
INCIDENT: [service] [severity]
IC: [name]
Operations: [name]
Status: Investigating
Symptoms: [what users are experiencing]
Started: [approximate time]
```

### Step 4: Investigate - form hypotheses

Operations Lead: form a hypothesis before running commands.
- What changed recently? (deploys, config changes, dependency updates)
- What do metrics show? (error rate, latency, saturation)
- What do logs show?

SRE principle: change is the enemy of stability. Look at what changed first.

### Step 5: Communicate on a schedule

Communications Lead posts status updates every 15 minutes (SEV1) or 30 minutes (SEV2) even if nothing has changed. "We are still investigating" is a valid update. Silence breeds panic.

Internal update format:

```
[TIME] Status: [Investigating / Mitigating / Monitoring / Resolved]
Impact: [what users are experiencing]
Current action: [what the team is doing right now]
Next update: [time]
```

### Step 6: Mitigate before you fix

Mitigation = stop the bleeding. Fix = address the root cause.

Mitigation actions (in order of preference):
1. Rollback the most recent deploy
2. Disable the affected feature flag
3. Redirect traffic to a healthy region
4. Scale up capacity
5. Apply a hotfix (last resort - introduces new risk)

Apply the fastest, lowest-risk mitigation first.

### Step 7: Declare resolution

When user impact is resolved (not when root cause is found):

```
RESOLVED: [service] is restored
Duration: [start] to [end]
Impact: [who was affected, what was degraded]
Resolution: [what action resolved it]
Root cause: [preliminary - full postmortem to follow]
Next step: Postmortem within [48h for SEV1, 1 week for SEV2]
```

## Anti-Patterns

**1. IC also making production changes**
Bad: The incident commander is also running kubectl commands and checking logs.
Good: IC delegates all technical actions. Two roles, two people. IC stays at the strategic level.

**2. No regular status updates**
Bad: Stakeholders hear nothing for 45 minutes.
Good: Communications Lead posts every 15 minutes (SEV1). Even "still investigating" counts.

**3. Fixing root cause under pressure instead of mitigating**
Bad: "We know the bug, let me push a fix to prod."
Good: Rollback first, restore service, then fix properly in a controlled environment.

**4. Declaring the incident over when root cause is unknown**
Bad: Service is restored, incident closed, no postmortem scheduled.
Good: Resolution = user impact resolved. Root cause investigation continues. Postmortem is mandatory for SEV1/SEV2.

## Quality Checklist

- [ ] Severity declared with criteria
- [ ] Incident Commander assigned (not the same person as Operations Lead)
- [ ] Incident channel opened with initial status post
- [ ] Status updates posted on schedule (every 15-30 min)
- [ ] Mitigation prioritized over fix under pressure
- [ ] Resolution post includes: duration, impact, resolution action, postmortem date
- [ ] Postmortem scheduled before incident is fully closed
