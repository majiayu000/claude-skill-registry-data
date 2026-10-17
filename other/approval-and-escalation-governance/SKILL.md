---
name: approval-and-escalation-governance
description: The human authority and escalation model for a programmatic desk. Who approves what, at which threshold, and how fast. Authority tiers (trader, senior, desk lead), an approval matrix template, escalation paths, service levels tied to the loops, and a capability model mapping trader levels to the loops they may run unsupervised. Use when the user says "approval matrix", "who approves", "escalation", "authority tiers", "service levels", "governance", "sign-off thresholds", "capability model", or "who signs off on this change".
---

# Approval and escalation governance

The safe-to-automate matrices in the platform skills gate the agent. This skill gates the
humans. "A human approves" is not a control until you say which human, above what threshold,
and within what time. This skill defines the authority tiers, the approval matrix, the
escalation paths, the service levels, and the capability model that turn "a person signs off"
into a specific, auditable decision.

It complements, and never replaces, the agent guardrails. A loop or an automation still reads,
diagnoses, and recommends; a person still approves before money moves. What this skill adds is
the answer to "which person, and by when". Read it alongside `dv360-api-and-sdf-automation` for
the agent-side safe-to-automate matrix it mirrors, and `change-management-and-incident-response`
for how an approved change is recorded, rolled out, and rolled back.

## When to use this skill

- Someone asks "who approves this", "what is the sign-off threshold", or "who can authorize a
  budget shift this size".
- You are setting up a new desk or client and need an approval matrix and escalation paths.
- A loop has produced a recommendation and you need to know who is allowed to apply it.
- You need to define how fast the team must respond to a pacing miss, an anomaly, or a client
  report (the service levels).
- You need to decide which loops a junior may run unsupervised and which require a senior in
  the loop (the capability model).

This skill is the human governance layer. It does not teach how to make a change (that is the
platform skills) or how to ramp a new trader (that is `trader-onboarding`). It says who is
allowed to approve a change, how quickly the team must act, and what each trader level may do
on their own.

## Quick reference: the three authority tiers

| Tier | Approves | Example changes | Cannot approve |
| --- | --- | --- | --- |
| Trader | Small, reversible, within-line changes | A bid change within the agreed step cap; a single creative swap; a frequency cap tweak within policy; an exclusion from `brand-safety-monitor` | Budget shifts above the senior threshold; any new supply path; any relaxation of a brand-safety control |
| Senior trader | Budget movement and material in-flight changes | A budget shift above the trader cap and below the desk-lead threshold; reallocation across line items in one pool; a targeting expansion | New supply paths; brand-safety relaxation; cross-client moves |
| Desk lead | Structural, risk-bearing, and policy changes | A new supply path or inventory source; any relaxation of a brand-safety or suitability control; a budget shift above the senior threshold; cross-advertiser changes | (Approves the above; escalates legal, contractual, or client-relationship calls beyond the desk) |

Two rules sit on top of the tiers. First, **a relaxation of a brand-safety or suitability
control is always a desk-lead decision**, regardless of how small it looks, because it changes
the universal floor and is easy to under-weigh. Second, **approval never moves money across
clients or advertisers at any tier without desk-lead sign-off**, because that crosses a budget
and contractual boundary a single trader cannot see.

## Core process: set the matrix, then run it

1. **Set the thresholds for the desk or client.** The tiers above are the structure; the
   numbers are local. Agree the bid step cap, the budget-shift thresholds between tiers, and the
   frequency-cap policy for this desk or this client, and write them into the approval matrix
   template below. Thresholds that live in someone's head are not controls.
2. **Match every loop recommendation to an approver.** When a loop produces a recommendation,
   look up the change type in the matrix and route it to the tier that owns it. A
   `budget-reallocation` proposal within one pool and under the senior threshold goes to a
   senior; a new supply path surfaced by `delivery-and-deal-watch` goes to the desk lead.
3. **Apply the service level.** Each loop has a response window (below). Acknowledge within the
   window even if the fix takes longer, so nothing sits silently past its clock.
4. **Escalate when the change exceeds the tier, the clock is breached, or the approver is
   unavailable.** The escalation paths below say where it goes next. Escalation is a feature,
   not a failure; the point is that nothing stalls and nothing gets approved by someone without
   the authority.
5. **Record the decision.** Who approved, what they approved, against which recommendation, and
   when. Hand the recorded change to `change-management-and-incident-response` for rollout and
   rollback. An approval with no record is not auditable and cannot be rolled back cleanly.

## Decision rules and thresholds

### Authority tiers, in detail

- **Trader.** Approves changes that are small, reversible, and contained to a line they own.
  The defining test: bounded step size, easy to reverse, no change to the safety floor, no new
  money. A bid change inside the agreed step cap, a creative swap, a frequency adjustment within
  policy, and applying an exclusion that `brand-safety-monitor` proposed all qualify. A trader
  cannot approve their own move beyond the cap, cannot open a new supply path, and cannot relax
  a brand-safety control.
- **Senior trader.** Approves budget movement and material in-flight changes: a budget shift
  above the trader cap and below the desk-lead threshold, a reallocation across line items
  inside one goal and budget pool, and a targeting expansion. A senior cannot approve a new
  supply path, a brand-safety relaxation, or any cross-client move; those rise to the desk lead.
- **Desk lead.** Approves the structural and risk-bearing changes: a new supply path or
  inventory source, any relaxation of a brand-safety or suitability control, a budget shift
  above the senior threshold, and any cross-advertiser or cross-client change. The desk lead
  escalates beyond the desk only for legal, contractual, or client-relationship decisions.

### Sign-off thresholds (set these per desk; the values are examples)

| Change | Trader | Senior | Desk lead |
| --- | --- | --- | --- |
| Bid change | Within the step cap (for example +/- 15 percent, once per day per line) | Above the cap, within policy | Account-wide bidding change |
| Budget shift | Up to a set floor (for example up to 10 percent of a line's budget) | Above the trader floor up to a higher ceiling (for example up to 25 percent, within one pool) | Above the senior ceiling, or across pools or clients |
| New supply path or inventory source | No | No | Yes |
| Brand-safety or suitability relaxation | No | No | Yes |
| Targeting expansion | No | Within one campaign | Cross-campaign or cross-advertiser |
| Cross-client or cross-advertiser move | No | No | Yes |

The percentages are placeholders. Set real numbers for the desk and record them in the matrix.
The structure (who can approve which kind of change) is the part that does not change; the
thresholds are local and must be written down.

### Escalation paths

- **The change exceeds the approver's tier.** Route up one tier: trader to senior, senior to
  desk lead. Never down. A change that needs a desk lead is not approved by a senior because the
  desk lead is busy; it waits or the desk lead delegates explicitly.
- **The service-level clock is breached.** If the owning tier has not acknowledged within the
  window, escalate to the next tier so the response does not stall. The clock is on
  acknowledgment, not on the full fix.
- **The approver is unavailable.** Named backup at the same tier first; if none, escalate up.
  Authority is by role, not by person, so coverage must be defined or the matrix has a hole.
- **A live incident (delivery is broken, spend is running away, a brand-safety breach is
  active).** This leaves the routine approval flow. Acknowledge immediately, contain first, and
  hand to `change-management-and-incident-response`. Containment of an active incident does not
  wait on a routine sign-off, but it is recorded and reviewed after the fact.

### Service levels tied to the loops

The loops set the cadence; these set the clock. Acknowledge within the window even when the fix
takes longer.

| Trigger (loop) | Acknowledge within | Resolve or escalate within | Owner |
| --- | --- | --- | --- |
| Pacing miss (`daily-pacing-sweep`) | Same trading day | Same trading day, or escalate to senior | Trader |
| Anomaly raised (`anomaly-detection`) | 1 business hour | Investigate same day; escalate if it is a real breakout | Trader or analyst |
| Delivery or deal failure (`delivery-and-deal-watch`) | Same trading day | Cause named and fix proposed same day; escalate a sell-side pause to the partner | Trader, then senior |
| Brand-safety or quality breach (`brand-safety-monitor`) | 1 business hour | Exclusion proposed same day; any control relaxation rises to desk lead | Trader to desk lead |
| Client report (`weekly-client-report`) | By the client's cadence | Reviewed by `qa-scrutinizer` and approved before send | Analyst, then approver |
| Business review (`business-review-prep`) | Ahead of the review date | Reviewed and approved for the client team | Analyst, then approver |
| Pre-launch sign-off (`pre-launch-qa-gate`) | Before launch | Clean sign-off from both the checklist and the independent review, or no-go | Account ops and desk lead |

A response time tied to nothing gets ignored. Tying each clock to the loop that raises the
signal is what makes the service level enforceable.

### Capability model: which loops a trader may run unsupervised

This maps trader level to autonomy on the loops. It is the human counterpart to the
safe-to-automate matrix: that matrix says what an agent may do unattended; this says what a
person at each level may run without a senior in the loop. Every loop in this library is
read-only and recommends rather than acts, so "run unsupervised" means produce the recommendation
without a senior reviewing the output, not apply a change. Applying a change is always gated by
the approval matrix above.

| Loop | Junior (in training) | Trader | Senior |
| --- | --- | --- | --- |
| `daily-pacing-sweep` | Observe only | Run unsupervised | Run unsupervised |
| `anomaly-detection` | Observe only | Run unsupervised | Run unsupervised |
| `delivery-and-deal-watch` | Draft, senior reviews | Run unsupervised | Run unsupervised |
| `brand-safety-monitor` | Draft, senior reviews | Run; control relaxations still rise to desk lead | Run; relaxations rise to desk lead |
| `weekly-optimization-pass` | Draft, senior reviews | Run unsupervised | Run unsupervised |
| `budget-reallocation` | Observe only | Run; the resulting move needs senior approval per the matrix | Run; approve within the senior threshold |
| `pre-launch-qa-gate` | Observe, then run the checklist | Run the checklist; `qa-scrutinizer` is the independent pass | Run; desk lead co-signs go-live |
| `weekly-client-report` | Draft, reviewed | Run; `qa-scrutinizer` reviews before send | Run; reviewed before send |
| `business-review-prep` | Draft, reviewed | Run; reviewed before the client team | Run; reviewed before the client team |

"Run unsupervised" never means "apply unsupervised". The output of every loop is a
recommendation; whether it can be acted on is governed by the approval matrix. Promotion through
this capability model tracks the `trader-onboarding` arc: a junior earns the trader column by
completing the ramp and producing a build the `qa-scrutinizer` agent passes, but the authority
itself is granted here, explicitly, not inferred from finishing the training.

## Reference material

- The agent-side matrix this mirrors: the `dv360-api-and-sdf-automation` skill, "Safe-to-automate
  matrix" and "Human-in-the-loop patterns". This skill is the human-side counterpart; keep the
  two consistent so the gate on the agent and the gate on the person agree.
- How an approved change is rolled out and rolled back, and how an incident is handled: the
  `change-management-and-incident-response` skill.
- The ramp that builds the capability this skill grants authority over: the `trader-onboarding`
  skill.
- The loops that the service levels and the capability model are tied to: see the loops README
  for the full set and the safe-by-default posture.

## Templates and examples

An approval matrix template, filled with example thresholds. Replace the numbers with the
desk's real values and keep it where the team and the agent can both see it.

```
Approval matrix: [Desk / Client name]    Effective: [date]    Owner: [desk lead]

Authority tiers
  Trader        : [names]
  Senior trader : [names]
  Desk lead     : [name]   Backup: [name]

Thresholds (set per desk)
  Bid step cap (trader)        : +/- 15% per line, max once/day
  Budget shift (trader)        : up to 10% of a line's budget
  Budget shift (senior)        : 10% to 25%, within one goal/budget pool
  Budget shift (desk lead)     : above 25%, or across pools or clients
  New supply path              : desk lead only
  Brand-safety relaxation      : desk lead only
  Targeting expansion          : senior within a campaign; desk lead across campaigns
  Cross-client move            : desk lead only

Service levels (acknowledge within)
  Pacing miss                  : same trading day        (trader)
  Anomaly                      : 1 business hour          (trader/analyst)
  Delivery/deal failure        : same trading day         (trader -> senior)
  Brand-safety breach          : 1 business hour          (trader -> desk lead)
  Client report                : client cadence, QA'd before send
  Pre-launch sign-off          : before launch, clean dual pass or no-go

Escalation
  Exceeds tier                 : up one tier (never down)
  SLA clock breached           : up one tier
  Approver unavailable         : named backup, else up one tier
  Live incident                : acknowledge now, contain, hand to change-management

Record every approval: who, what, against which recommendation, when.
```

A worked routing example:

```
Recommendation: weekly-optimization-pass proposes moving 18% of Line B's budget
to Line A (same goal, same pool), expected CPA improvement stated.

Routing: budget shift of 18% within one pool -> above the trader floor (10%),
below the desk-lead ceiling (25%) -> SENIOR approves.
Service level: not an incident; handled in the weekly pass cadence.
Record: senior name, the 18% Line B -> Line A move, the optimization-pass
recommendation ID, the date. Then change-management applies and logs it.
```

## Common pitfalls

- **"A human approves" with no named human.** The whole reason this skill exists. Always name
  the tier and, on the matrix, the person. An unnamed approver is an uncontrolled change.
- **Thresholds that live in someone's head.** If the bid cap and budget thresholds are not
  written in the matrix, two traders will apply two different numbers and the control is
  fictional. Write them down and date them.
- **Approving up a tier informally because someone is busy.** A senior does not approve a
  desk-lead change to keep things moving. Escalate or wait. The point of the tiers is that the
  right level of risk gets the right level of scrutiny.
- **Treating a brand-safety relaxation as small.** It changes the universal floor and is always
  a desk-lead call, no matter how minor the specific exclusion looks. This is the single easiest
  control to under-weigh.
- **Confusing "run a loop unsupervised" with "apply its output".** The capability model grants
  the first; the approval matrix gates the second. A trader who reads "run unsupervised" as
  "act unsupervised" has misread both this skill and the safe-by-default posture of the loops.
- **No clock on the response.** A recommendation with no acknowledgment window sits until
  someone happens to notice. Tie every response to the loop's service level so nothing stalls
  silently.
- **Approving without recording.** An approval with no record cannot be audited or cleanly
  rolled back. Hand every recorded approval to `change-management-and-incident-response`.

## Sources

- This skill is the human-authority counterpart to the agent guardrails in the
  `dv360-api-and-sdf-automation` skill (its safe-to-automate matrix and human-in-the-loop
  patterns) and to the safe-by-default posture in the loops README of this repository. (as of
  June 2026)
- The change types, thresholds, and loop triggers referenced here are defined in the platform
  skills and the loop files in this repository; this skill assigns the human approval authority
  over them rather than redefining them. (as of June 2026)
