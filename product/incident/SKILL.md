---
name: incident
description: "Respond to a production outage: assess severity, mitigate first (roll back/flip a flag/scale), investigate safely, communicate, write a blameless postmortem. Use when prod is down, degraded, or errors spike."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (Google SRE golden signals, SEV levels, blameless postmortems, mitigation-first). Details in references/."
---

# incident

A live outage is not a debugging session. **Restore service first, understand why later.** Different from the `debug` skill, which is for local, non-urgent root-causing.

## What an AI agent must NOT do
An agent **never makes a unilateral risky change to production during an incident.** Mitigations that mutate prod — **rollback, feature-flag flips, scaling, failover, traffic shedding, config changes** — need **explicit human approval** before you run them.

You *may* autonomously: read dashboards/logs/traces, correlate "what changed", draft the status update, build the timeline, and *recommend* a specific mitigation with rationale — then wait for a human. Never run a write/mutating query on prod, never restart or flush state on a hunch, never post an external status update without sign-off.

## Lifecycle
Detect → Acknowledge (fast, so others know it's owned) → Assess severity → **Mitigate (stop the bleeding)** → Communicate → Resolve → Postmortem. Declare early; under-declaring costs more than over-declaring.

## Severity (classify by user/business impact, not cause)
- **SEV1** — major outage / data loss / breach; core function down for most users. Page on-call + IC, exec + comms, external status page.
- **SEV2** — significant degradation or a key feature down for many; workaround may exist. Page on-call + IC.
- **SEV3** — limited/partial impact, small subset. Business-hours, ticket.
- **SEV4** — cosmetic/negligible. Backlog.
Define exact thresholds (error %, users, duration) ahead of time so it isn't a mid-incident debate.

## Mitigate first (fastest → safest levers)
1. **Roll back the deploy** if impact started right after a release — usually the single highest-value action.
2. **Disable the feature flag** — instant, targeted, lower blast radius; preferred when the change is flag-gated.
3. **Scale up/out** for resource saturation. **Fail over** to a healthy replica/region. **Shed load** (rate-limit, degraded/read-only mode, circuit-break a failing dependency).
Default to **rollback** when a recent deploy correlates with onset and it's safe; **forward-fix** only when rollback is impossible (irreversible migration, data written in a new shape) or clearly riskier. Beware rolling back across incompatible schema migrations.

## Investigate a live system safely
"**What changed?**" first — recent deploys, config/flag flips, infra changes, traffic spikes, cert/secret expiry, DNS. Watch the **four golden signals**: latency (split success vs error), traffic, errors, saturation. Correlation ≠ causation — confirm with a second signal, but don't let analysis block mitigation. **Read-only on prod**: query replicas/logs/metrics, never speculative writes/restarts/flushes (they destroy evidence or widen the outage). `references/runbook.md`.

## Communicate
Regular updates even when "no change" — SEV1 every ~15–30 min, and always state the next-update time. Internal channel = technical + timeline; external/status page = plain-language impact, what you're doing, next update, no internal hostnames or blame. Use "monitoring", not "fixed", until confident.

## Blameless postmortem
Structure: summary; **impact** (duration, users/revenue, SLO/error-budget burn); **timeline** (timestamped); **root cause & contributing factors** (5 Whys, usually multi-cause); detection (how fast, alert gaps); what went well / badly / where we got lucky; **action items** each with an owner + due date + ticket. Blameless — ask "what made this failure possible?", not "who did it?". Turn action items into prevention: regression tests, new alerts, guardrails, runbook updates, automating the manual mitigation; tie repeated error-budget burn to pausing feature work. `references/postmortem.md`.

Done when: service is restored (via a human-approved mitigation), impact and timeline are recorded, comms went out, and a blameless postmortem with owned action items is written.
