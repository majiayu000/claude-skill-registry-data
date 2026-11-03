---
name: incident
description: Guide incident response for production outages, degradations, and failures. Always use this skill when a production system is down or degraded, an alert fired, users are impacted, or when the user says "we have an incident", "production is down", "the site is down", "errors are spiking", "PagerDuty fired", "help me triage this", "what's the blast radius", or when walking through a post-mortem. Also use when designing runbooks or on-call procedures. Use immediately. Do not attempt to triage without reading this skill first.
---

# Incident

An incident is a time-compressed debugging problem with real users impacted. The goals in order: restore service, limit blast radius, understand what happened, prevent recurrence.

Don't skip steps, but don't let process slow down mitigation either. Move fast on what you know; be explicit about what you don't.

## Phase 1: Triage (first 5 minutes)

Establish the facts before taking action:

**What is broken?**

- Is it a total outage (nothing works) or degradation (some things work, some don't)?
- Which services, endpoints, or features are affected?
- Are errors specific to a region, user segment, or data condition?

**What is the blast radius?**

- How many users are impacted? All users, a percentage, a specific cohort?
- What is the business impact? (Revenue, SLA breach, data loss risk?)
- Is it getting worse, stable, or recovering on its own?

**When did it start?**

- Look at your error rate and latency graphs and find the inflection point
- What changed around that time? Deploys, config changes, traffic patterns, cron jobs, dependency updates?

**Set an initial severity.** Be explicit; it determines communication expectations and who needs to be involved:

- **SEV1**: customer-facing, widespread impact, revenue or data at risk; all hands
- **SEV2**: significant degradation, partial impact; engineering and product engaged
- **SEV3**: minor degradation, workaround exists; engineering only

## Phase 2: Communicate early

Notify before you've fixed it. Stakeholders need to know something is happening, even if you don't know why yet.

Initial message (Slack/PagerDuty/status page) format:

```
[SEV1] [IMPACT] — What users are experiencing, in plain language
Started: ~HH:MM UTC
Affected: [what]
Status: Investigating. Next update in 15 minutes.
```

Update on a cadence (every 15–30 minutes for SEV1) even if nothing has changed. "Still investigating" is a valid update. Silence is not.

Assign roles explicitly if multiple people are engaged:

- **Incident commander**: owns the process, drives communication, makes escalation calls
- **Primary responder**: hands on the keyboard, investigating and mitigating
- **Comms lead** (for large incidents): writes status page and stakeholder updates

## Phase 3: Mitigate first, investigate second

Your first goal is to stop the bleeding, not to understand why it's bleeding.

**Rollback the most recent change.** If something deployed in the last 2 hours, roll it back; don't investigate whether it caused the problem, just roll back. If the incident resolves, you have your answer. If it doesn't, you've ruled out the most likely cause and can continue investigating with a clean baseline.

**Feature flags**: if the affected feature can be disabled, disable it. A degraded-but-functional service is better than a broken one.

**Traffic controls**: rate limit, circuit break, or shed load if the system is overwhelmed. Partial service is better than no service.

**Scale up (if appropriate)**: if load is the cause, throw more capacity at it while you investigate the root cause. Don't let a temporary capacity shortfall become a full outage.

**Prioritize mitigation actions that are fast and reversible.** Don't apply a surgical fix that takes 2 hours to develop when a rollback takes 5 minutes. You can fix it properly after service is restored.

## Phase 4: Root cause investigation

Once you've mitigated (or if you've ruled out quick mitigations), investigate:

**Observe the signals:**

- Error rates by endpoint, service, and dependency
- Latency percentiles (p50, p95, p99): a p99 spike with p50 stable often points to a subset of requests or a resource contention issue
- Saturation metrics: CPU, memory, connection pool usage, queue depth
- Dependency health: are upstream services healthy? Are downstream consumers backed up?

**Correlate with changes:**

- What deployed recently? (Code, config, infrastructure, dependencies)
- Did traffic patterns change? (Load spike, new bot traffic, geographic shift)
- Did any scheduled jobs or maintenance run recently?

**Narrow with binary search:** if you don't have a clear suspect, find the boundary between healthy and broken. Which requests succeed and which fail? Which data conditions trigger the problem? Which region or instance shows it first?

**Logs and traces**: search for errors at or just before the incident start time. Distributed traces are especially useful for pinpointing which service in a call chain is the slow or failing one.

## Phase 5: Resolve and verify

Once you believe you have a fix:

1. Apply it to a subset of traffic first if possible
2. Watch error rates and latency return to baseline: not just "no new errors," but back to normal
3. Confirm with real user reports if available
4. Declare the incident resolved only when metrics confirm recovery, not when the fix is applied

Post-resolution message:

```
[RESOLVED] [IMPACT] — Incident is resolved as of HH:MM UTC.
Duration: X hours Y minutes
Root cause: [brief description]
Fix applied: [what was done]
Post-mortem: [date/link]
```

## Post-mortem

Write one for every SEV1 and SEV2. The goal is learning, not blame.

**Timeline**: reconstruct the sequence of events with timestamps. When did the incident start? When was it detected? When were key actions taken? How long until mitigation? Until resolution?

**Root cause**: what specific condition caused the failure? Don't stop at the proximate cause ("the server ran out of memory"); find the contributing factors ("the server ran out of memory because a new feature loaded entire dataset into memory, which was safe on small datasets but not at production scale, and there was no load test that caught it").

**Five whys**: keep asking "why" until you reach an organizational or process factor, not just a technical one.

**Action items**: each action item needs an owner and a deadline. Categories:

- **Detection**: how do we catch this faster next time? (Alert tuning, better dashboards)
- **Response**: how do we respond better? (Runbook improvement, on-call training)
- **Prevention**: how do we stop this from happening? (Code change, process change, architectural improvement)

Blameless means the post-mortem focuses on systems and processes, not on who made a mistake. People make mistakes in proportion to the systems that allow them to.

## Runbook template

For known failure modes, write a runbook:

```markdown
## [Service/Scenario Name]

**Symptoms**: What you'll see in alerts and dashboards
**Blast radius**: Who/what is affected
**Likely causes**: Ordered by probability

### Investigation

1. Check [metric/log] for [what to look for]
2. Run [command] to [determine X]

### Mitigation options

- **Option A (fast)**: [steps], [expected outcome], [caveats]
- **Option B (thorough)**: [steps], [expected outcome]

### Escalation

If [condition], page [team/person].
```
