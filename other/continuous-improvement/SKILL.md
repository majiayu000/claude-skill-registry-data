---
name: continuous-improvement
description: "The purpose of a postmortem is to change the system, and that only works if people"
---

# Continuous Improvement (Verbose)

## Core Patterns

### Blameless Postmortems

The purpose of a postmortem is to change the system, and that only works if people
tell you what actually happened. Blame destroys that input directly: an engineer
who expects to be named for a mistake reports incidents later, describes them more
cautiously, and omits the detail that would have explained the failure. The cost is
not abstract — it shows up as longer detection times on the next incident.

Blameless does not mean vague. It means the analysis assumes people acted
reasonably given what they knew, and then interrogates why the situation made the
wrong action look right.

| Blaming framing | Blameless framing |
|---|---|
| "Sam deployed without running tests" | "The pipeline reported green while integration tests were skipped on a cache miss — the engineer had no signal" |
| "Ops missed the alert" | "The alert fired into a channel with 40 daily notifications; median acknowledgement there is 25 minutes" |
| "Someone should have caught this in review" | "The change spanned 1,400 lines across 3 services; no reviewer had context on all three" |

Each right-hand framing names something you can change this quarter. Each left-hand
framing names a person, and terminates the investigation.

**Structure that works:**

1. **Trigger.** Every incident at or above your severity bar, without exception —
   including the ones with an obvious cause. Consistency is what keeps the process
   from feeling like a punishment reserved for bad outcomes.
2. **Timeline first, separately.** Reconstruct what happened and when before
   discussing why. Doing both in one pass produces a narrative built around the
   first plausible theory in the room. See `incident-timeline-creation`.
3. **Causal analysis second.** Push past the proximate cause into the conditions.
   See `root-cause-five-whys`, and stop when you reach something you can change —
   "human error" and "insufficient testing" are places the analysis gave up.
4. **Within 5 business days.** Detail decays fast. A postmortem written three weeks
   later is a reconstruction of a reconstruction.
5. **Published broadly.** The org learns from incidents it did not experience. A
   postmortem readable only by the affected team wastes most of its value.

**Counterfactuals are the common failure.** "If the engineer had checked the
dashboard, this would not have happened" is not analysis — it describes a world
that did not occur. The useful question is why checking the dashboard was not the
obvious thing to do at that moment.

**Do near-misses too.** An incident that nearly happened contains the same
information at none of the cost. Teams that only review outages learn exclusively
from expensive lessons.

### Action Item Hygiene

This is where most improvement programs die: the analysis is good, the items are
written, and eighteen months later the same failure recurs and someone finds the
old postmortem recommending exactly the fix that was never built.

An action item without a named owner and a due date is decoration. Two mechanisms
cause this:

**Diffusion of responsibility.** "The platform team will add monitoring" belongs to
nobody. Every member assumes another member has it, and none of them do. A named
individual can delegate; a team name cannot.

**No forcing function.** Without a date the item has no priority relative to
feature work, and feature work always has a date.

```
❌ Improve monitoring on the payment service
❌ Team to review timeout configuration
❌ Consider adding circuit breakers

✅ PRO-412 — Add p99 latency alert on POST /checkout, 500ms threshold, 5m window
   Owner: Priya Raman      Due: 2026-08-07   Priority: P1  Source: INC-2026-118

✅ PRO-413 — Set client timeout on payments-gateway calls to 3s (currently unset)
   Owner: Marcus Webb      Due: 2026-08-14   Priority: P1  Source: INC-2026-118

✅ PRO-419 — Evaluate circuit breaker for the gateway client; write a one-page
   recommendation with a go/no-go
   Owner: Priya Raman      Due: 2026-09-01   Priority: P2  Source: INC-2026-118
```

Note what PRO-419 does: an item that is genuinely investigative gets a concrete
deliverable and a date anyway. "Consider X" becomes "produce a recommendation on X
by this date". Vagueness in scope does not license vagueness in ownership.

**Rules that hold up:**

| Rule | Reason |
|---|---|
| One named human per item | Shared ownership is no ownership |
| P1 items due within one sprint | Longer and they lose their incident context |
| Items live in the normal backlog | A separate "postmortem tracker" is a graveyard |
| Same workflow as feature work | Otherwise they never get sprint capacity |
| Linked to the source incident | Preserves the why when someone picks it up in 6 weeks |
| Completion rate reviewed monthly | The only thing that keeps the loop closed |

**Watch the completion rate, and act on what it says.** Below roughly 70% on-time
completion, the problem is usually intake rather than discipline: postmortems are
generating more remediation than the team has capacity to absorb, so everything
slips. The honest response is to generate fewer, larger, better-prioritised items —
three that ship beat twelve that rot. A remediation backlog older than 90 days
should be triaged explicitly: do it, or close it as "accepted risk" with a named
accepter. Both are respectable; leaving it open is not.

**Classify items by leverage.** After an incident, teams reflexively write
detection items — they are easy and feel productive.

| Class | Example | Leverage |
|---|---|---|
| Prevention | Make the failure impossible (type, constraint, guardrail) | Highest |
| Mitigation | Reduce blast radius when it happens | High |
| Detection | Alert faster | Medium |
| Response | Better runbook | Medium |
| Documentation | Note it somewhere | Lowest |

A postmortem producing five detection items and zero prevention items has not
finished asking why.

### DORA Metrics With Real Definitions

Four metrics, two dimensions. Throughput and stability must be read as a pair —
that pairing is the entire point, and it is what separates the framework from
vanity dashboards.

| Metric | Precise definition | Elite | High | Medium | Low |
|---|---|---|---|---|---|
| **Deployment frequency** | Distinct deploys reaching production users | On demand (multiple/day) | Weekly–monthly | Monthly–6 months | < every 6 months |
| **Lead time for changes** | First commit on the branch → serving production traffic | < 1 day | 1 day–1 week | 1 week–1 month | > 1 month |
| **Change failure rate** | Share of deploys causing degraded service requiring remediation (rollback, hotfix, patch) | 0–15% | 16–30% | 16–30% | 40–60% |
| **Failed deployment recovery time** | Failed deploy → service restored | < 1 hour | < 1 day | 1 day–1 week | > 1 week |

**Definitional traps that make the numbers lie:**

*Lead time starts at the first commit,* not at PR open, not at ticket start. Teams
that measure from PR open report excellent lead times while branches sit for two
weeks — they have measured their review speed and called it delivery speed.

*Change failure rate counts remediation, not severity.* A deploy that needed a
hotfix counts, even if no user noticed. Restricting it to customer-visible outages
reclassifies most of the signal away.

*Deployment frequency counts deploys reaching users,* not CI runs, not deploys to
staging. And a deploy of ten batched changes is one deploy — splitting releases to
inflate the number is the most common gaming behaviour, which is precisely why the
metric must never be a target.

*Recovery time is specifically for failed deployments,* not general MTTR. Deploy
failures are the ones you control most directly.

**Instrument from systems, not surveys.** Derive from git history, the deploy
pipeline, and the incident tracker:

```sql
-- Lead time per deploy: first commit on the branch to production
SELECT d.deploy_id,
       d.deployed_at,
       EXTRACT(EPOCH FROM (d.deployed_at - MIN(c.authored_at))) / 3600
         AS lead_time_hours
FROM deployments d
JOIN commits c ON c.deploy_id = d.deploy_id
WHERE d.environment = 'production'
  AND d.deployed_at >= NOW() - INTERVAL '90 days'
GROUP BY d.deploy_id, d.deployed_at;
```

Report **median and p85**, never the mean. Deploy-time distributions have long
right tails — one branch that sat for six weeks drags an average into fiction while
the median stays honest. The p85 is where the pain lives, and it is the number that
moves when you fix the process.

### Closing the Loop

A metric with no intervention attached is a dashboard. The loop that produces
improvement is small and explicit:

1. **Observe** a specific problem — "p85 lead time is 9 days; the branch-to-merge
   step accounts for 6 of them."
2. **Hypothesise** a cause — "reviews queue because only two people can approve
   changes to the billing module."
3. **Change one thing** — expand approvers to five, with a pairing session for
   context transfer.
4. **Measure** against the same definition, over a comparable window.
5. **Keep or revert,** and write down which.

Changing three things at once means learning nothing from the result. If two of
them are cheap and safe, doing them together is fine — just do not then claim to
know which one worked.

Attach interventions to metrics in writing: "merge queue introduced 2026-04-12;
lead time p85 6.1d → 2.3d over the following 6 weeks." A quarter of these entries
is a far better artifact than a quarter of dashboard screenshots.

**Retrospectives feed the same pipeline.** A retro whose output is a wall of
sticky notes and good feelings is a meeting. A retro produces at most two or three
items, with owners and dates, in the same backlog as everything else. The signal
that a retro process has failed is the same complaint appearing three sprints
running with no ticket attached — at that point the meeting is teaching people that
raising problems does nothing.

**Guard against Goodhart.** These metrics measure a system, not people. Attach them
to individual or team performance evaluation and they are gamed within a quarter:
releases split to raise frequency, incidents downgraded to lower change failure
rate, "hotfixes" reclassified as ordinary deploys. Compare a team against its own
history, never against another team with different constraints.

## Common Anti-Patterns

❌ **Postmortems that identify a person as the cause** — the analysis stops, and
future reporting slows.
✅ Name the conditions that made the action look correct at the time.

❌ **Stopping at "human error" or "insufficient testing"** — both are labels for an
unfinished investigation.
✅ Keep asking why until you reach something you can change.

❌ **Counterfactual reasoning — "if only they had checked"** — describes a world
that did not happen.
✅ Ask why the correct action was not the obvious one.

❌ **Action items owned by a team** — diffusion of responsibility guarantees they
sit untouched.
✅ One named individual, who may delegate but stays accountable.

❌ **Action items without due dates** — they have no priority against feature work,
which always has one.
✅ P1s due within a sprint, tracked in the normal backlog.

❌ **A separate postmortem action tracker** — a parallel backlog nobody
sprint-plans from.
✅ Same tracker, same workflow, same triage as feature work.

❌ **Postmortems that only produce detection items** — you have made the same
failure more visible, not less likely.
✅ Push for prevention and mitigation before settling for alerting.

❌ **Lead time measured from PR open** — hides the largest delay in most pipelines.
✅ Measure from the first commit on the branch.

❌ **Reporting deployment frequency without change failure rate** — throughput
without stability is half the picture and rewards recklessness.
✅ Always read the pair.

❌ **Mean lead time** — long-tail distributions make averages flattering and
useless.
✅ Median and p85.

❌ **DORA metrics in performance reviews or team leaderboards** — gaming follows
within a quarter.
✅ Team-internal instrument; compare against the team's own history.

❌ **Retros that generate discussion and no tickets** — the same issue returns
every sprint until people stop raising it.
✅ Two or three concrete items, owned and dated, per retro.

❌ **Only reviewing incidents that caused damage** — every lesson is bought at full
price.
✅ Review near-misses on the same terms.

## Continuous Improvement Checklist

- [ ] Every incident at or above the severity bar gets a postmortem
- [ ] Postmortems completed within 5 business days
- [ ] Timeline reconstructed before causal analysis begins
- [ ] Language describes conditions and systems, not individuals
- [ ] Analysis reaches a changeable condition, not "human error"
- [ ] Postmortems published beyond the affected team
- [ ] Near-misses reviewed as well as outages
- [ ] Every action item has one named owner
- [ ] Every action item has a due date; P1s within one sprint
- [ ] Items linked to their source incident
- [ ] Items tracked in the normal backlog with the normal workflow
- [ ] Prevention and mitigation items present, not detection only
- [ ] On-time completion rate reviewed monthly; > 70% sustained
- [ ] Items older than 90 days triaged: done, or closed as accepted risk
- [ ] DORA metrics derived from git, pipeline, and incident systems
- [ ] Lead time measured from first commit, reported as median and p85
- [ ] Change failure rate counts any deploy needing remediation
- [ ] Throughput and stability metrics always reported together
- [ ] Each intervention recorded against the metric it targeted
- [ ] Metrics never used to rank teams or individuals
- [ ] Retro output is a small number of owned, dated tickets
