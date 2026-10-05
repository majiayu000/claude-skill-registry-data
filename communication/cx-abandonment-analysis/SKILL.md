---
name: cx-abandonment-analysis
description: Use to analyse chat and call abandonment, queue patience, and what a high FCR may be hiding when abandoned contacts never become tickets. Trigger for "abandonment rate", "customers hanging up in queue", "queue patience", "calls abandoned before answer", chat drop-off, survival curves, or FCR that looks too good because failures never enter the system.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Abandonment analysis

Abandonment is the contact that never became a conversation. It does not appear in
handle time, agent QA, or ticket-based FCR — but the customer still has the problem,
and many of them come back angrier through another channel.

**High FCR can hide abandonment.** If the customer hangs up in queue, closes the chat
widget, or gives up on the IVR, there is no ticket, no disposition, and no repeat to
measure. FCR looks fine because the failure never entered the denominator.

The analysis makes invisible demand visible and separates patience limits you can
influence from behaviour you can only observe.

## What counts as abandonment

Define it per channel before counting:

- **Voice** — caller disconnects while waiting for an agent (queue or ring), before a
  connected talk segment begins. Some systems also count very short answered calls;
  declare your threshold.
- **Chat** — session ends before first agent message, or before customer message if you
  measure bot-to-agent abandonment separately.
- **Callback offered but not completed** — customer requested callback and never received
  it, or abandoned during callback queue. Often tracked elsewhere; include if your
  service promise covers it.

Distinguish:

- **Queue abandonment** — staffing or routing problem
- **IVR / self-service abandonment** — menu or deflection problem
- **Post-answer immediate hang-up** — different diagnosis (wrong queue answered, long
  greeting, perceived wait misreported)

Do not merge these in one headline rate.

## Survival and patience curves (conceptual)

A **survival curve** shows, for contacts that entered queue at time zero, what share
remains waiting at each elapsed wait time. It answers: *at what wait do people leave?*

Shape interpretation:

- **Steep early drop** — customers have low tolerance for initial wait, or the channel
  signals wait poorly (no position, no ETA).
- **Cliff at a specific duration** — often matches a visible threshold (quoted wait
  time, music loop length, chat "you are number…" update interval).
- **Long flat tail then drop** — patient base waiting for specialist queue; cliff may
  mean capacity never arrived.

A **patience curve** is the hazard of abandoning given still waiting — the incremental
risk of leaving in the next interval. Rising hazard means each extra minute costs more
abandonments than the last.

You do not need to fit parametric models to use these. Plot empirical curves from your
own data: cohort entered queue → still waiting at 30s, 60s, 2m, 5m, 10m. The shape
names the intervention (staffing vs messaging vs callback offer).

## Censored waits

Contacts **answered** before abandoning have a wait time you never observe fully — they
would have abandoned at some later time, but an agent arrived first. Treating answered
contacts as "infinite patience" biases analysis.

**Right approach for patience estimation:**

- Use only **abandoned contacts** for observed patience times, or
- Use survival methods that censor answered contacts at their answer time (they left
  the risk set because of answer, not abandonment)

For operational reporting, also report **abandon rate by wait bucket** among those who
abandoned — simpler and still actionable.

Contacts near the end of your reporting window that are **still in queue** are
right-censored for abandonment. Exclude or treat separately; do not count them as
non-abandoners without noting they had no full opportunity to leave.

Say what you did. Censoring mistakes inflate or deflate abandonment rate depending on
direction.

## Queue patience vs staffing

Abandonment rises when offered wait exceeds what customers will tolerate — but
tolerance is not a universal constant you can import.

**Measure your own curves.** Do not invent industry benchmarks for acceptable wait or
abandon rate. Report your historical relationship between wait time and abandon
probability, by channel, queue and time of day.

Actionable splits:

| Pattern | Likely cause | Direction of fix |
| --- | --- | --- |
| Abandon up, ASA up, occupancy high | Under-staffed for volume | Staffing or defer non-urgent |
| Abandon up, ASA flat | Signalling — customers think wait is longer than it is | Position, callback, honest ETA |
| Abandon up on one queue only | Routing or skill bottleneck | Queue design, overflow |
| Abandon up after rule change | Misrouted volume hitting wrong queue | Routing audit |
| Chat abandon up, bot containment up | Bot failure without clean agent path | Handoff design |

**Callback and async escape valves** change the curve — they remove impatient customers
from the live queue and may improve answered rate without adding agents. Measure
whether callback fulfilment rate holds; offered callback that never arrives is worse
than honest wait.

## What abandonment hides from other metrics

Cross-check abandonment against:

- **Contact volume by channel** — voice abandon up, email volume up next day suggests
  channel switching, not resolution.
- **Repeat contact from same identity** — customers who abandoned and returned.
- **Complaints and social** — often the only record of abandon-only failures.
- **FCR and repeat rate** — computed on tickets only; report them with the caveat that
  abandoners are excluded from the denominator.

A falling ticket volume with flat or rising total demand signals deflection or
abandonment absorbing pain upstream.

## Traps

- **Abandon rate without wait-time context.** "5% abandon" is meaningless without
  distribution of waits before abandon and comparison to answered waits.
- **Counting vendor disconnects as customer abandon.** Establish event reason codes.
- **Short abandons as junk.** Sub-threshold abandons may be dial mistakes; very long
  threshold may hide deliberate queue test behaviour. Declare threshold, do not hide
  behind defaults.
- **Chat abandon at bot stage vs agent queue.** Mixing them blames agents for bot
  drop-off.
- **Comparing abandon across channels.** Patience differs by channel; one target for
  all is not meaningful.
- **Using abandon rate as the only service metric.** Low abandon with long ASA may mean
  customers wait forever without leaving — also a failure.

## Present results to the user

1. **Definitions used** — channel, thresholds, inclusion of IVR/bot stages, and censoring
   rules for answered and in-queue contacts.
2. **Abandon rate and trend** — by channel, queue, and interval of day/week.
3. **Survival / patience curves** from your data — empirical wait buckets, shape
   described in plain language. No invented benchmarks.
4. **Wait-time distribution** — abandoned vs answered, p50 and p90 where sample allows.
5. **FCR / ticket metric caveat** — explicit statement of what abandoners exclude from
   other dashboards.
6. **Cross-channel and repeat signals** — evidence abandoners return elsewhere.
7. **Diagnosis table** — pattern matched to likely cause for this operation.
8. **Ranked interventions** — staffing, signalling, callback, routing; each tied to
   the curve segment it addresses.
