---
name: incident-response
description: Production incident handling covering triage, evidence gathering, mitigation, communication, and post-mortem practices.
compatibility: opencode
metadata:
  audience: debug-investigator
  purpose: incident-handling
---
## What I do

Provide a structured approach to handling production incidents — from initial triage through resolution and post-mortem. The goal is to minimize impact, preserve evidence, and prevent recurrence.

## When to use me

Load this skill when responding to a production incident, investigating an ongoing outage, or writing a post-mortem. The debug-investigator should load this alongside the debugging-investigation skill when the issue is in a production or production-like environment.

## Triage workflow

Triage determines what you do first. Get it wrong and you waste time on low-impact issues while critical ones burn.

### Severity assessment

Assess severity based on impact and urgency, not on how interesting the bug is.

| Severity | Criteria | Response time |
|----------|----------|---------------|
| **Critical** | Service is down, data loss is occurring, or a security breach is active. Revenue-impacting. All or most users affected. | Immediate. Drop everything. |
| **High** | Major feature is broken or significantly degraded. Large subset of users affected. Workaround exists but is painful. | Within 1 hour. |
| **Medium** | Feature is impaired but functional. Small subset of users affected. Reasonable workaround exists. | Within 4 hours. |
| **Low** | Cosmetic issue, minor inconvenience, or edge case. Few users affected. | Next business day. |

### Impact scope

Determine who and what is affected:
- **User impact**: How many users? Which user segments? Can they work around it?
- **Data impact**: Is data being corrupted, lost, or exposed? Is the damage ongoing?
- **Financial impact**: Is revenue being lost? Are SLA commitments being violated?
- **Blast radius**: Is the issue isolated to one service, or is it cascading?

### Immediate mitigation

Before investigating root cause, stop the bleeding:
- **Revert the last deployment** if the timing correlates and the deployment is revertible
- **Enable a circuit breaker** or feature flag to disable the broken path
- **Scale up** if the issue is load-related and more capacity buys time
- **Block the traffic pattern** if a specific request type is causing the problem
- **Failover** to a secondary system if one exists

Mitigation does not need to be elegant. It needs to be fast. A 5-minute mitigation that's ugly beats a 2-hour fix that's clean.

## Evidence gathering

Gather evidence systematically. Rushing to hypothesize without evidence leads to wrong conclusions and wasted time.

### Logs

- Pull logs from the affected service for the incident timeframe. Start with error-level logs, then expand to warn and info if error logs don't tell the full story.
- Check logs from upstream and downstream services. The root cause may not be in the service showing symptoms.
- Look for log volume anomalies — a sudden spike or drop in log output is itself a signal.

### Metrics

- **Error rates**: Compare current error rate to baseline. Identify which error types spiked.
- **Latency**: Check P50, P95, P99. A P99 spike with normal P50 suggests a subset of requests is affected.
- **Throughput**: Is request volume normal? A traffic spike may be the cause, not the symptom.
- **Resource utilization**: CPU, memory, disk I/O, network I/O, connection pool usage, thread pool usage.
- **Saturation**: Are any resources at or near capacity?

### Traces

- Find traces for failing requests. Follow the trace across service boundaries to identify where the failure originates.
- Compare traces for failing requests against traces for succeeding requests. What's different?

### Deployment timeline

- List all deployments to affected services in the past 24 hours. Include config changes, infrastructure changes, and dependency updates.
- Overlay the deployment timeline on the error rate graph. Correlation isn't causation, but it's the first thing to check.
- Check if any scheduled jobs, cron tasks, or batch processes started around the incident time.

### External factors

- Check status pages for cloud providers, CDNs, DNS providers, and third-party services.
- Check for unusual traffic patterns — DDoS, bot activity, or a viral link driving unexpected load.
- Check for certificate expirations, DNS TTL changes, or other infrastructure events.

## Communication

### Status updates

Communicate early and often. Silence is worse than "we're investigating."

- **First update** (within 15 minutes of detection): Acknowledge the issue, state the impact, say what you're doing. "We're aware of elevated error rates on the payments API. Users may see failed transactions. We're investigating."
- **Subsequent updates** (every 30 minutes during active incidents): State what you've learned, what you've tried, what you're trying next. "We've identified the issue as a database connection pool exhaustion. We're scaling up the connection pool and investigating the root cause."
- **Resolution update**: Confirm the issue is resolved, state the root cause, and commit to a post-mortem. "The payments API has recovered. Root cause was a missing index on the transactions table after yesterday's migration. A post-mortem will follow."

### Stakeholder notification

- **Engineering leadership**: Notify on Critical and High severity. Include impact scope and estimated time to resolution if known.
- **Product/business stakeholders**: Notify on Critical severity or when there's customer-facing impact. Use non-technical language focused on user impact, not technical details.
- **Affected teams**: If the incident involves another team's service, notify them immediately. Don't debug their system in isolation.

## Mitigation vs fix

These are different actions with different timelines. Do not conflate them.

**Mitigation**: Stop the impact. Revert a deploy, toggle a flag, block a traffic pattern, fail over to a backup. Goal: users stop experiencing the problem. Timeline: minutes.

**Fix**: Address the root cause so the problem doesn't recur. Write a patch, fix the configuration, add a missing index. Goal: the system is healthy without the mitigation in place. Timeline: hours to days.

Always mitigate first. A mitigated incident with an unknown root cause is far better than an ongoing incident with a known root cause and a fix that's 2 hours away.

After mitigation:
1. Verify the mitigation is working (error rates returning to baseline)
2. Investigate root cause with less time pressure
3. Deploy the fix
4. Remove the mitigation (if it was a temporary measure like a feature flag)
5. Verify the system is healthy without the mitigation

## Post-mortem format

Write the post-mortem within 48 hours of resolution, while memory is fresh. The post-mortem is blameless — it focuses on systemic causes, not individual mistakes.

```markdown
# Post-mortem: {Incident title}

## Summary
One paragraph: what happened, when, how long, who was affected.

## Timeline
Chronological sequence of events with timestamps. Include:
- When the issue started (or when it's estimated to have started)
- When it was detected and how (alert, customer report, manual observation)
- Key investigation steps and findings
- When mitigation was applied
- When the fix was deployed
- When the incident was declared resolved

## Impact
- Users affected: {count or percentage}
- Duration: {time from start to resolution}
- Revenue impact: {if applicable}
- SLA impact: {if applicable}
- Data impact: {if any data was lost or corrupted}

## Root cause
Clear explanation of why the incident occurred. Distinguish between:
- The trigger (what changed that caused the incident to start)
- The underlying cause (why the system was vulnerable to that trigger)
- Contributing factors (what made detection or resolution slower)

## What went well
Things that worked during the incident response. Detection speed,
mitigation effectiveness, team coordination.

## What went poorly
Things that didn't work. Slow detection, missing runbooks, unclear
ownership, missing monitoring.

## Action items
Concrete, assigned, time-bound actions to prevent recurrence.

| Action | Owner | Priority | Due date |
|--------|-------|----------|----------|
| {description} | {person/team} | {P0/P1/P2} | {date} |

Each action item should address a specific gap identified in the
"what went poorly" section. Avoid vague items like "improve monitoring"
— specify what monitoring to add and what it should alert on.
```

## Pattern recognition

When investigating, look for these common patterns:

- **Deploy-correlated**: Error rate spikes immediately after a deployment. Check the diff.
- **Load-correlated**: Errors increase with traffic. Look for resource exhaustion, connection pool limits, rate limits, or missing indexes.
- **Time-correlated**: Errors start at a specific time regardless of traffic. Check cron jobs, certificate expirations, DNS TTLs, cache expirations, or batch processes.
- **Data-correlated**: Errors affect specific users, accounts, or data shapes. Look for data integrity issues, missing records, or edge cases in input validation.
- **Cascade**: One service fails, causing downstream services to fail. Look for missing timeouts, circuit breakers, or retry amplification.
- **Slow bleed**: Error rate increases gradually over hours or days. Look for memory leaks, connection leaks, disk space, or log rotation failures.
- **Intermittent**: Errors come and go without clear pattern. Look for race conditions, connection pool contention, garbage collection pauses, or flaky upstream dependencies.

Each pattern suggests a different investigation path. Recognizing the pattern early saves hours of undirected debugging.
