---
name: runbook
description: >
  Write an operational runbook. Use when the user says "write a runbook",
  "on-call documentation", "how to operate this service", "alert runbook",
  "troubleshooting guide for ops", "what to do when this alert fires",
  "operational procedures", or needs to document how to run, troubleshoot, or
  respond to a service - even if they don't explicitly say "runbook".
---

## Overview

Based on the **Google SRE Book**. A runbook is the operational contract for a service: how to start it, stop it, diagnose it, and recover it. Google SRE's standard: a runbook should be executable by an on-call engineer who has never seen the service before. If it requires tribal knowledge, it's not a runbook - it's an assumption.

The test: can an on-call engineer follow this runbook at 3am with a degraded service, no time to research, and adrenaline affecting their cognition? If not, it's not operational-grade.

## Workflow

### Step 1: Write the service overview

```
Service: [your service]
Owner team: [your team]
On-call rotation: [who gets paged]
SLO: [availability target, e.g. 99.9% uptime]
Dependencies: [upstream services this depends on]
Dependents: [downstream services that depend on this]
Dashboards: [links]
Logs: [how to access]
Alerts: [link to alerting config]
```

### Step 2: Document steady-state operations

What does normal look like?

**Health check:**
```bash
# Command to verify the service is healthy
curl https://[your service]/health
# Expected response: {"status": "ok", "version": "x.y.z"}
```

**Key metrics (normal ranges):**

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Error rate | < 0.1% | 0.1-1% | > 1% |
| p99 latency | < 200ms | 200-500ms | > 500ms |
| CPU usage | < 60% | 60-80% | > 80% |

### Step 3: Document alert runbooks

For each alert, write a response procedure:

```
Alert: [Alert name]
Severity: [SEV1/SEV2/SEV3]
Fires when: [condition]
Impact: [what users experience]

Diagnosis:
  1. Check [dashboard link] for [specific signal]
  2. Run: [command] - Expected: [output]
  3. Check: [logs location] for [error pattern]

Common causes:
  A. [Cause] - Fix: [command or action]
  B. [Cause] - Fix: [command or action]

If none of the above: escalate to [team/person]
```

### Step 4: Document common operations

List every routine operational task with exact commands:

**Restart the service:**
```bash
kubectl rollout restart deployment/[service-name] -n [namespace]
kubectl rollout status deployment/[service-name] -n [namespace]
```

**Scale up:**
```bash
kubectl scale deployment/[service-name] --replicas=[n] -n [namespace]
```

**Rollback a deploy:**
```bash
kubectl rollout undo deployment/[service-name] -n [namespace]
# Verify rollback succeeded:
kubectl rollout status deployment/[service-name] -n [namespace]
```

### Step 5: Document recovery procedures

For each failure mode, step-by-step recovery:

```
Failure: [service is unresponsive / returning 5xx / high latency]
Verify: [how to confirm this is the problem]
Recover:
  1. [first action]
  2. [second action]
  3. [verify recovery: command - expected output]
Escalate if: [condition that means this runbook is insufficient]
```

### Step 6: Document escalation paths

Who to call when the runbook doesn't work:

| Situation | Contact | How |
|-----------|---------|-----|
| Database issue | [DB team] | [PagerDuty / Slack] |
| Network issue | [Infra team] | [contact] |
| Vendor outage | [Vendor support] | [ticket URL] |

### Step 7: Add a testing section

How does an on-call engineer practice with this runbook in a non-emergency?
- Chaos engineering scenarios
- Runbook review frequency (recommend: quarterly)
- Last tested: [date]

## Anti-Patterns

**1. Runbook that requires tribal knowledge**
Bad: "Check if the DB is having issues." (how? where? what to look for?)
Good: "Run `psql -h [host] -U [user] -c 'SELECT count(*) FROM pg_stat_activity'` - if > 100 connections, connection pool exhaustion is likely."

**2. Commands without expected output**
Bad: "Run the health check command."
Good: "Run: `curl https://[your service]/health` - Expected: `{"status":"ok"}`. If you see `{"status":"degraded"}`, proceed to Step 3."

**3. No escalation path**
Bad: Runbook ends with "investigate further."
Good: Every runbook has an explicit "escalate if" condition and names who to escalate to.

**4. Runbook never tested**
Bad: Runbook written once, never validated in a real incident.
Good: Run quarterly fire drills. Note the last tested date in the runbook.

## Quality Checklist

- [ ] Service overview complete (owner, SLO, dependencies, links)
- [ ] Normal operating metrics defined with ranges
- [ ] Every alert has a response procedure with exact commands
- [ ] Commands include expected outputs (not just what to run)
- [ ] Common operations documented step-by-step
- [ ] Recovery procedures cover the top 3 failure modes
- [ ] Escalation path named and reachable
- [ ] Last tested date recorded
- [ ] Executable at 3am by someone unfamiliar with the service
