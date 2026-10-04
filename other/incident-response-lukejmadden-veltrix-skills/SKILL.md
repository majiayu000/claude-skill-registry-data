---
name: incident-response
description: 5-step incident response playbook. Use when a service is down, degraded, or experiencing errors.
---

Follow this playbook for every incident. No shortcuts.

## The 5 Steps

### 1. CONTAIN (first 5 minutes)
Stop the bleeding. Prevent further damage.
- Can we rollback to the last working version?
- Can we disable the broken feature without taking down everything?
- Is customer data at risk?
- Who needs to be notified right now?

### 2. DIAGNOSE (next 15 minutes)
Find the root cause using data, not guesses.
- Check logs: what changed? when did errors start?
- Check deployments: was there a recent deploy?
- Check external dependencies: is a third-party service down?
- Check metrics: traffic spike? memory leak? disk full?
- Form a hypothesis and verify before acting

### 3. FIX (next 30 minutes)
Apply the **minimum change** needed.
- Prefer reverting over forward-fixing
- If forward-fixing: change one thing, verify, repeat
- Do NOT refactor while fixing an incident
- Do NOT add new features while fixing an incident

### 4. VERIFY (next 15 minutes)
Confirm the fix works and has no side effects.
- Is the error gone from logs?
- Are affected customers able to use the service?
- Are metrics back to normal baselines?
- Run a smoke test on the critical path

### 5. POSTMORTEM (within 24 hours)
Document what happened so it doesn't happen again.
- **Timeline** — minute-by-minute of the incident
- **Root cause** — what actually broke and why
- **Impact** — who was affected, for how long, revenue impact
- **What went well** — what worked in the response
- **What went poorly** — where we lost time
- **Action items** — specific preventive measures with owners and dates

## Severity Classification

| Level | Description | Response time | Escalation |
|-------|------------|---------------|------------|
| SEV1 | Service down, data breach | Immediate | Human + all hands |
| SEV2 | Major feature broken | Within 1 hour | Human notified |
| SEV3 | Minor degradation | Within 4 hours | Automated |
| SEV4 | Cosmetic or non-blocking | Next business day | Ticket created |

## Communication Template

```
[STATUS: Investigating/Identified/Monitoring/Resolved]
Impact: [what's affected]
Started: [time]
Current action: [what we're doing right now]
Next update: [when]
```
