---
name: incident-automation
description: "A runbook written in a wiki decays silently: the dashboard is renamed, the"
---

# Incident Automation (Verbose)

## Core Patterns

### Runbooks as Code

A runbook written in a wiki decays silently: the dashboard is renamed, the
command changes, the service is replaced, and nobody notices until an outage.
An executable runbook is exercised, reviewed, and version-controlled like the
rest of the system.

Automate in stages, in this order:

1. **Gather** — collect the diagnostic state a human would collect. Read-only,
   safe to run at any time, and the highest-value step.
2. **Suggest** — interpret the state and print the likely next action.
3. **Act with confirmation** — perform the change after a human says yes.
4. **Act autonomously** — only for actions proven safe over many incidents,
   and only behind the guards in the next section.

```bash
#!/usr/bin/env bash
# runbooks/db-connections-exhausted.sh — stage 1 and 2 only
set -euo pipefail

echo "=== pool utilisation ==="
psql -Atc "SELECT state, count(*) FROM pg_stat_activity GROUP BY state"

echo "=== oldest queries ==="
psql -Atc "SELECT pid, age(now(), query_start) AS age, left(query, 100)
           FROM pg_stat_activity WHERE state = 'active'
           ORDER BY age DESC LIMIT 10"

echo "=== recent deploys (30m) ==="
./scripts/deploys-since.sh 30m

cat <<'NEXT'
Likely causes, in order:
  1. A slow query introduced by a recent deploy  -> check the deploy list above
  2. A connection leak (idle-in-transaction high) -> scripts/kill-idle-tx.sh
  3. Genuine load growth                          -> scripts/scale-pool.sh
Escalate to the database owner if utilisation stays above 90% for 10 minutes.
NEXT
```

Store runbooks in the repo next to the service, link them from the alert that
triggers them, and give each one an owner. Run the read-only stages on a
schedule in staging so breakage is caught before an incident, not during one.

### Auto-Remediation With Guardrails

Auto-remediation is triggered by a *symptom*. If the underlying cause is not
what the automation assumes, the action does not fix it — so the symptom
persists, the trigger fires again, and you have a loop. A restart loop is worse
than the original fault: it multiplies the outage, destroys the in-memory state
you needed for diagnosis, and hides the trend behind an apparently self-healing
service.

Four guards, all four required:

| Guard | Purpose | Typical shape |
|---|---|---|
| Rate limit | Bound the loop | ≤ 3 actions per target per hour |
| Circuit breaker | Stop and escalate on repeated failure | After 3 consecutive failures, disable and page |
| Blast radius | Prevent a fleet-wide action | Never more than 20% of instances, never the last healthy one |
| Preconditions | Confirm the world still justifies acting | Re-check health, quorum, freeze status at execution time |

```python
def maybe_remediate(target, signal):
    if freeze.active():
        return escalate("change freeze active", target, signal)
    if breaker.is_open(target):
        return escalate("circuit breaker open — repeated remediation failed",
                        target, signal)
    if rate_limiter.count(target, window="1h") >= 3:
        return escalate("remediation rate limit hit — likely a loop",
                        target, signal)
    if healthy_peers(target) < MIN_HEALTHY:
        return escalate("blast radius guard — too few healthy peers",
                        target, signal)
    if not signal.still_true():          # re-verify immediately before acting
        return audit.log("stand down: condition cleared", target, signal)

    before = snapshot(target)
    result = perform(target)
    audit.log(action="restart", target=target, trigger=signal.id,
              reason=signal.reason, before=before, after=snapshot(target),
              undo="scripts/rollback-restart.sh " + target.id,
              actor="auto-remediation")
    breaker.record(target, result.ok)
    if not result.ok:
        escalate("remediation failed", target, result)
```

Escalation is the default path, not the error path. Automation that cannot
safely act should hand a human a well-described situation, which is still a
large improvement over an unexplained page.

Track a remediation-success metric per rule. A rule that fires often and rarely
resolves the symptom is masking a defect — take it out and fix the defect.

### Alert Routing, Grouping, and Deduplication

Alert volume, not alert absence, is what breaks response. Reduce it in the
pipeline before it reaches a person.

- **Route by ownership.** Each alert carries a service label that maps to an
  owning team's rotation. Alerts that route to a shared catch-all get ignored,
  because no individual is accountable for them.
- **Deduplicate** on a stable fingerprint — alert name plus service plus a
  meaningful instance identity. Four hundred pods failing the same check should
  produce one notification.
- **Group** related alerts with a short wait so a cascading failure arrives as
  one message rather than forty.
- **Inhibit** downstream alerts while an upstream cause is firing: while
  `database-unreachable` is active, suppress the API error-rate and queue-depth
  alerts that are its consequences.
- **Silence with expiry.** Maintenance silences must have an end time.
  Open-ended silences are how a real alert stays muted for six months.
- **Tier by severity.** Only page-worthy alerts page; the rest become tickets or
  dashboard signals. If a class of alert has paged repeatedly with no action
  taken, it was never page-worthy.

Review the alert catalogue on a schedule and delete aggressively. Every alert
should answer: what customer impact does it indicate, what is the first action,
and who owns it. If any answer is missing, the alert is noise.

### Automating Incident Setup

The first minutes of an incident are largely clerical, and doing them by hand
delays diagnosis and produces an inconsistent record. One command should:

```
/incident declare sev2 "checkout latency above 5s"

  → create channel #inc-2026-0142-checkout-latency
  → create the incident record with severity, declarer, start time
  → page the on-call for the affected service; invite the service owner
  → post: runbook links, service dashboard, recent deploys, dependency status
  → open the timeline document and start recording
  → set the status page to "investigating" (SEV1/SEV2 only, comms lead confirms)
  → open a video bridge and pin the link
```

Then keep it fed. Every alert transition, deploy, rollback, scaling action, and
chatops command writes into the same timeline with a timestamp. The postmortem
record then assembles itself; see `incident-timeline-creation` for what belongs
in it and how the timestamps are used.

Automate the close as well: capture participants, duration, severity history,
and the raw timeline into the review document, and create the follow-up tickets
so the actions have owners before everyone disperses.

### ChatOps

Running incident actions from the incident channel gives you attribution,
timestamps, and shared context in one move. Someone joining at minute 40 can
read what has been tried instead of asking.

```
> /oncall who payments
  Primary: dsouza  Secondary: nakamura  Manager: patel

> /deploy status payments
  Current: v4.12.1 (deployed 13:47, 18 min before incident start)
  Previous: v4.12.0

> /rollback payments v4.12.0
  ⚠ Destructive action. Reply "confirm rollback payments v4.12.0" within 60s.

> confirm rollback payments v4.12.0
  Rollback started by @dsouza at 14:36:22 UTC. Job 88213.
  → recorded in timeline for INC-2026-0142
```

Design rules: read-only commands need no confirmation, destructive commands
require an explicit typed confirmation and a role check, every command echoes
its full effect back into the channel, and the bot acts through a scoped
identity that is itself audited. Never let chatops become a shortcut around
production access control — it should use the same authorisation as any other
path, just with better ergonomics.

### Measuring Toil to Pick Targets

Automate by evidence. For each recurring alert or manual procedure, record:

| Dimension | Question | Why it matters |
|---|---|---|
| Frequency | How many times per month? | Rare work rarely repays automation |
| Duration | Minutes of human attention each time? | The actual cost |
| Variance | Is the response identical each time? | Judgement resists automation |
| Reversibility | Can the action be undone? | Decides autonomy vs confirmation |
| Blast radius | Worst case if it fires wrongly? | Decides how many guards |
| Timing | Does it happen out of hours? | Night toil costs far more than daytime |

High frequency, low variance, reversible, small blast radius — automate fully.
Low frequency but high variance — write a better runbook and leave a human in
the loop. High blast radius — automate the diagnosis, never the action.

Track the outcome too: pages per week, out-of-hours pages, and median time to
mitigate. If automation has not moved those, it added complexity rather than
capacity.

### Auditability and Reversibility

Automation acts on production without a human at the keyboard, so the record it
leaves is the only account of what happened. Every action logs: trigger, actor
identity, reason, target, state before and after, outcome, and the exact undo
procedure. Write it to append-only storage that the automation itself cannot
rewrite.

Reversibility determines autonomy. Restarting a stateless pod, scaling a group,
shifting traffic, and disabling a feature flag are reversible — reasonable
candidates. Deleting data, rotating a credential other systems depend on,
terminating a stateful primary, and force-merging state are not — these require
human approval however confident the automation is.

Two more controls matter. First, give the automation scoped, short-lived
credentials rather than standing admin, so a compromised or buggy automation has
a bounded reach. Second, provide a global off switch that a responder can flip
in one command, and make sure everyone knows it — during a strange incident, the
ability to stop all automation and observe the system unassisted is often the
fastest path to understanding it.

## Common Anti-Patterns

❌ **Auto-restart with no attempt limit.** The loop turns a degraded service
into a full outage and destroys diagnostic state.
✅ Rate limit, circuit breaker, and page a human on repeated failure.

❌ **Remediation that hides a recurring fault.** Self-healing masks a defect
that is quietly getting worse.
✅ Track remediation frequency as a defect signal and fix the cause.

❌ **Acting on a stale trigger.** The alert fired four minutes ago; the world
has moved on.
✅ Re-verify preconditions immediately before acting.

❌ **A single alert channel for all services.** Shared ownership is no
ownership.
✅ Route by service to the owning rotation.

❌ **No inhibition rules.** One database failure pages twenty times and buries
the signal.
✅ Suppress downstream alerts while the upstream cause is firing.

❌ **Silences without expiry.** A maintenance mute outlives the maintenance by
months.
✅ Every silence has an end time and an owner.

❌ **Automated actions absent from the timeline.** The postmortem cannot explain
its own graphs.
✅ Every automated action writes to the incident timeline.

❌ **Automation holding standing admin credentials.** A bug or a compromise gets
unlimited reach.
✅ Scoped, short-lived credentials, and an audited identity.

❌ **Runbook scripts only ever run during incidents.** They break silently and
you find out at the worst moment.
✅ Exercise read-only stages on a schedule; review them like code.

❌ **Automating the interesting problem instead of the expensive one.**
✅ Measure toil first and automate what the data points at.

❌ **No way to turn it off.** Responders end up fighting their own automation.
✅ A one-command global kill switch that everyone knows.

## Incident Automation Checklist

- [ ] Every paging alert links an executable runbook with an owner
- [ ] Diagnostic collection automated before any action is automated
- [ ] Runbook read-only stages exercised on a schedule outside incidents
- [ ] Every auto-remediation has a rate limit and a circuit breaker
- [ ] Blast radius capped; never acts on the last healthy instance
- [ ] Preconditions re-verified immediately before acting
- [ ] Escalation to a human is the default when guards trip
- [ ] Remediation success rate tracked per rule
- [ ] Alerts routed by service ownership, not to a shared channel
- [ ] Deduplication, grouping, and inhibition rules configured
- [ ] All silences carry an expiry and an owner
- [ ] Declaration creates channel, record, timeline, and pages automatically
- [ ] Automated actions write into the incident timeline
- [ ] ChatOps destructive commands require confirmation and a role check
- [ ] Every action logged with actor, reason, before/after, and undo
- [ ] Audit log append-only and outside the automation's write scope
- [ ] Irreversible actions gated behind human approval
- [ ] Automation uses scoped, short-lived credentials
- [ ] Global kill switch exists and responders know the command
- [ ] Toil measured per alert; automation targets chosen from the data
- [ ] Page volume and time-to-mitigate tracked to prove automation helped
