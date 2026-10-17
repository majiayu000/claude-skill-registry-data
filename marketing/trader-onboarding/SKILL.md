---
name: trader-onboarding
description: A structured ramp for a new programmatic trader, built on this library. A Week-1, Week-2, and Week-4 learning path that starts at the foundations, runs the read-only loops, shadows the media-planner agent on a real brief, and ends with a build specification graded by the qa-scrutinizer agent. Use when the user says "trader onboarding", "onboard a new trader", "learning path", "where do I start", "ramp a junior", "training plan", "new hire", or asks how to bring someone up to speed on the desk.
---

# Trader onboarding

The on-ramp for a new trader. The fastest return on this whole library is ramping new hires
to consistent, safe output, and this skill is the path that gets them there. It does not
re-teach programmatic from scratch. It sequences the skills, loops, and agents already in the
package into a Week-1, Week-2, and Week-4 arc, each week ending in something the new hire
produced and a more senior person can check.

The arc is deliberately read-before-write. A new trader learns to observe, diagnose, and
recommend on the read-only loops long before they touch a live budget. Authority to act
unsupervised is granted separately and explicitly. For who-approves-what and which loops a
trader may run unsupervised at each level, hand off to the `approval-and-escalation-governance`
skill. This skill builds the capability; that skill grants the authority.

## When to use this skill

- A new trader, junior, or analyst is joining the desk and needs a path from day one to
  productive.
- A manager asks "where do I start them", "what is the learning path", or "how do I ramp a
  junior".
- An experienced hire from a different platform needs to learn how this team and this library
  work, even if they already know programmatic.
- You want a repeatable training plan rather than ad-hoc shadowing.

This skill is the curriculum and the sequence. It is not the content: every step points into a
real skill, loop, or agent that does the teaching. It is also not the authority model. Whether
the new hire may run a given loop or approve a given change without supervision lives in
`approval-and-escalation-governance`, and the two are designed to be read together.

## Quick reference

| Phase | Goal | Anchor skill | Loops (read-only) | Agent | Deliverable |
| --- | --- | --- | --- | --- | --- |
| First day | Orientation and the map | `programmatic-foundations` | none | none | Glossary self-check passed |
| Week 1 | Read the language and the desk | `programmatic-foundations`, `dsp-selection` | `daily-pacing-sweep`, `anomaly-detection` (observe only) | none | A short read-out on one live campaign |
| Week 2 | Diagnose and recommend | the platform skills for your DSP | `delivery-and-deal-watch`, `brand-safety-monitor`, `weekly-optimization-pass` (observe, then draft) | shadow `media-planner` on a real brief | A media plan critique and one diagnosed constraint |
| Week 4 | Produce and be graded | `dv360-campaign-architecture` and the build skills | `pre-launch-qa-gate` (run the checklist) | produce a build, graded by `qa-scrutinizer` | A build specification with a scrutinizer score |

Progress through the arc is gated on the deliverable, not on time served. If the Week-2
deliverable is weak, repeat the week. The weeks are a minimum, not a ceiling.

## First day: orientation

Before any campaign, the new trader needs the map and the language. Keep day one to four
things, in order:

1. **Read the library README and the three-hats model.** Open the `programmatic-foundations`
   skill and read "Three hats: trader, analyst, account ops". A trader builds and optimizes
   the buy; an analyst measures and explains; account ops structures, QAs, and governs. The
   new hire is training for the trader hat, but they will hand off to the other two constantly,
   so they need to know where the seams are.
2. **Learn the glossary, then self-check.** Point them at the glossary in the
   `programmatic-foundations` skill and have them define, in their own words, the terms
   they will hear on day two: DSP, SSP, RTB, deal ID, PMP, Programmatic Guaranteed, line item,
   insertion order, pacing, frequency, viewability, IVT, Floodlight. This is the single
   reference they will return to all month, so they should know it exists and how it is
   organized.
3. **Learn the safe-by-default posture.** Read the loops README, specifically "The
   safe-by-default posture". Every loop in this library monitors, diagnoses, and recommends.
   None spends money on its own. A new trader who internalizes this on day one will not reach
   for the budget field when the right move is to write a recommendation and hand it up.
4. **Find the routing table.** Show them the "Which skill do I use" table in
   `programmatic-foundations`. They do not need to read every platform skill. They need to know
   how to find the one that owns the question in front of them.

End the day with the glossary self-check. If they cannot define the core terms, Week 1 starts
with the glossary, not the loops.

## Core process: the three-week arc

### Week 1: read the language and the desk

Goal: the new trader can read a live campaign and the daily signals without acting on them.

1. **Ground in the foundations.** Work through `programmatic-foundations`: the auction
   mechanics (first-price open auction, what a deal ID changes), the viewability standard, and
   the funnel model that ties each KPI to a stage. The single most common rookie error is
   judging a line item by a metric from the wrong funnel stage, so this is where it gets
   corrected first.
2. **Learn how a platform gets chosen.** Read `dsp-selection` so the new hire understands that
   the desk runs more than one DSP (this library covers DV360, Google Ads, Amazon DSP,
   StackAdapt, and The Trade Desk) and that the platform is a deliberate choice, not a default.
   Then have them focus their platform reading on the DSP they will trade first.
3. **Observe the read-only loops.** Sit them alongside the two daily loops, in observe-only
   mode:
   - `daily-pacing-sweep`: each morning, which live campaigns will miss flight, and the one
     recommended fix for each. The new hire watches how the pacing math is shown, not asserted.
   - `anomaly-detection`: the daily scan of the core metric set (spend, CPA or ROAS, CTR,
     viewability, win rate, conversions) against baseline. They learn what a real breakout looks
     like versus normal variation.
   They do not run these against a live account yet and they apply nothing. They read the
   output and explain back what each alert means.
4. **Week-1 deliverable.** A short written read-out on one live campaign: its objective and
   primary KPI, its current pacing status with the math, and any anomaly flagged that day with
   a plausible cause to check. A senior trader checks it for whether the KPI matches the
   objective and whether the pacing read is correct.

### Week 2: diagnose, recommend, and shadow a real plan

Goal: the new trader can walk a triage to a single binding cause and can critique a plan, still
without applying changes.

1. **Go deeper on the platform skills.** For the DSP they are trading, read the build and
   in-flight skills that own the levers: campaign architecture, bid strategy, targeting and
   audiences, deals and inventory, frequency and brand safety, and pacing and optimization (on
   DV360, the `dv360-*` set; on another platform, its matching set). The goal is to know which
   skill owns which lever, not to memorize every field.
2. **Move from observing to drafting on the diagnostic loops.** Now they draft the
   recommendation, and a senior reviews it before anything is acted on:
   - `delivery-and-deal-watch`: walk the troubleshooting triage in order (status, budget and
     flight, bid and win rate, targeting size, inventory or deal, creative, tracking) and read
     the impression-loss breakdown to name the one binding cause and its fix.
   - `brand-safety-monitor`: read viewability, invalid traffic, and verification flags against
     the quality bar and propose exclusions, each citing the breached signal and threshold.
   - `weekly-optimization-pass`: pull the goal-appropriate report, diagnose the single binding
     constraint, and propose exactly one change with its expected impact. One lever at a time
     is the rule they are learning to never break.
3. **Shadow the media-planner agent on a real brief.** This is the centerpiece of Week 2. Take
   a live or recent client brief and run the `media-planner` agent through it: objective to
   single primary KPI, channel and DSP mix, audience strategy, inventory approach, budget split
   across the funnel and flight, and the measurement plan. The new trader follows each step and
   sees how a brief becomes a plan a trader can build and a client can approve. Where the
   planner reaches for a sibling skill (`reporting-by-campaign-goal` to fix the KPI,
   `dv360-targeting-and-audiences` for the audience strategy, `dv360-deals-and-inventory` for
   the inventory mix), the new hire reads just enough of that skill to follow the decision.
4. **Week-2 deliverable.** Two things. First, a written critique of the shadowed media plan:
   does the primary KPI match the objective, is the budget split defensible for the funnel
   stages, are the assumptions named. Second, one campaign diagnosed end to end from
   `delivery-and-deal-watch` with the single binding cause, the evidence, and the proposed fix.
   A senior trader checks both. A weak critique means another week before Week 4.

### Week 4: produce a build and have it graded

Goal: the new trader produces a real artifact and learns to expect an adversarial check before
anything ships.

1. **Translate a plan into a build.** Take an approved media plan (the one shadowed in Week 2,
   or a fresh one) and produce a build specification: structure into insertion orders and line
   items with `dv360-campaign-architecture`, bid strategy per line, targeting and audiences,
   deals and inventory, frequency and brand-safety controls, and pacing and budget. This is the
   `programmatic-trader` agent's job, and the new hire does it as that agent would: a precise
   specification a person could traffic or express as a Structured Data File, not a vague plan.
2. **Run the pre-launch QA gate.** Before grading, run `pre-launch-qa-gate` against the build:
   the full pre-flight checklist with the launch-QA skill. The new trader learns that a build
   is not done when it is built; it is done when it passes QA. Collect every failed or missing
   item and fix it.
3. **Have the qa-scrutinizer agent grade it.** Submit the build to the `qa-scrutinizer` agent
   for an independent, adversarial review. The scrutinizer checks structure, bidding,
   targeting, deals, frequency, brand safety, creative, tracking, budget, and pacing against the
   launch-QA checklist and returns a score from 0 to 100, a verdict (ship, ship after fixes, or
   do not ship), and an itemized list of issues with the specific fix for each. The new hire
   reads the review, fixes the blockers and majors, and resubmits.
4. **Week-4 deliverable, the graduation artifact.** A build specification that the
   `qa-scrutinizer` agent passes (no open blockers), plus the new trader's written response to
   the review showing what they changed and why. This is the proof they can produce safe,
   launch-ready work and that they take the independent check seriously rather than arguing with
   it.

## Decision rules and thresholds

- **Gate on the deliverable, not the calendar.** Advance only when the week's deliverable
  passes the senior check. A new hire who breezes the Week-1 read-out can compress; one who
  struggles repeats the week. The weeks are minimums.
- **Read-only until authority is granted.** Through this entire arc the new trader applies no
  budget, bid, targeting, deal, or creative change to a live account. They produce
  recommendations and builds; a senior or the relevant approver acts. Which loops they may run
  unsupervised, and which changes they may approve, is set in
  `approval-and-escalation-governance`, not earned implicitly by finishing a week.
- **One lever at a time, always.** From the first diagnostic loop in Week 2, enforce the
  single-change rule. A new trader who learns to stack edits learns a habit that makes every
  later result unattributable.
- **A passing grade is a real bar.** Week 4 is not complete on a "ship after fixes" with open
  blockers. The `qa-scrutinizer` agent must return no blockers on the final artifact. Softening
  that defeats the purpose of the gate.
- **If the glossary self-check fails on day one, Week 1 starts with the glossary.** Do not run
  the loops with someone who cannot yet define win rate, viewability, or pacing; the loop output
  will not mean anything to them.

## Reference material

This skill is a sequence over the rest of the library. The teaching content lives in the linked
skills, agents, and loops:

- Foundations and the glossary: the `programmatic-foundations` skill, which holds the canonical
  glossary the new hire returns to all month.
- Platform choice: the `dsp-selection` skill.
- The agents the arc shadows: the `media-planner` agent (Week 2) and the `qa-scrutinizer` agent
  (Week 4), with the `programmatic-trader` agent as the model for the Week-4 build.
- The loops the arc runs read-only: `daily-pacing-sweep`, `anomaly-detection`,
  `delivery-and-deal-watch`, `brand-safety-monitor`, `weekly-optimization-pass`, and
  `pre-launch-qa-gate`. See the loops README for the safe-by-default posture and how to run a
  loop on demand or on a schedule.
- The authority model that complements this curriculum: the `approval-and-escalation-governance`
  skill.

## Templates and examples

A filled-in four-week plan for a new DV360 trader:

```
New trader: ramp plan (DV360 first platform)

Day 1  Orientation
  - Read programmatic-foundations: three hats, auction, funnel, routing table.
  - Glossary self-check: define DSP, SSP, RTB, deal ID, PMP, PG, line item, IO,
    pacing, frequency, viewability, IVT, Floodlight. PASS required to start Week 1.
  - Read the loops README: safe-by-default posture.

Week 1  Read the language and the desk
  - Foundations: auction mechanics, viewability standard, funnel model.
  - dsp-selection: why the desk runs multiple DSPs; focus reading on DV360.
  - Observe daily-pacing-sweep and anomaly-detection (no actions).
  - Deliverable: read-out on one live campaign (objective, primary KPI, pacing
    math, any anomaly + cause). Checked by a senior trader.

Week 2  Diagnose, recommend, shadow a plan
  - DV360 build + in-flight skills (architecture, bid, targeting, deals,
    frequency/brand-safety, pacing).
  - Draft on delivery-and-deal-watch, brand-safety-monitor,
    weekly-optimization-pass (senior reviews before any action).
  - Shadow the media-planner agent on the Q3 retail brief.
  - Deliverable: (1) critique of the shadowed plan, (2) one campaign diagnosed
    end to end with binding cause + fix. Both checked.

Week 4  Produce and be graded
  - Translate the approved plan into a build spec (programmatic-trader agent's job).
  - Run pre-launch-qa-gate; fix every failed item.
  - Submit to the qa-scrutinizer agent. Fix blockers and majors. Resubmit.
  - Graduation artifact: build spec with no open blockers + written response to
    the review. Authority to trade unsupervised is set separately in
    approval-and-escalation-governance.
```

## Common pitfalls

- **Letting time replace the deliverable.** "It has been four weeks" is not graduation. The
  passing artifact is. Hold the gate.
- **Skipping the glossary.** A new hire who half-knows the terms produces read-outs that look
  right and are subtly wrong (CPA on an awareness buy, win rate read without bid rate). The
  glossary self-check on day one prevents a month of that.
- **Granting authority by finishing the arc.** Completing Week 4 proves capability. It does not
  by itself grant the right to act on live budgets unsupervised. That is a separate, explicit
  decision in `approval-and-escalation-governance`. Conflating the two is how a new trader ends
  up making changes nobody approved.
- **Acting during the read-only weeks.** The whole point of starting on the read-only loops is
  that a new trader learns to diagnose and recommend before they can spend. If they start
  applying changes in Week 2, they have skipped the safest part of the ramp.
- **Treating the scrutinizer review as an obstacle.** A new trader who argues with the
  `qa-scrutinizer` agent instead of fixing the findings has learned the wrong lesson. The
  written response to the review is part of the graduation artifact precisely to build the habit
  of taking the independent check seriously.
- **Stacking edits.** Enforce one lever at a time from the first diagnostic loop. It is far
  harder to unlearn later.

## Sources

- This skill sequences the skills, agents, and loops in this repository; see `agents/` and
  `loops/` and the linked skills for the underlying content. (as of June 2026)
- The funnel-to-KPI model, auction mechanics, and viewability standard referenced here are
  defined and sourced in the `programmatic-foundations` skill. (as of June 2026)
- The loop format and the safe-by-default posture follow the loops README in this repository,
  whose format credit is the Forward Future Loop Library at
  signals.forwardfuture.ai/loop-library. (as of June 2026)
