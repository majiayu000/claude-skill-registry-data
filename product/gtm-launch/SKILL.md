---
model_tier: inherit
name: gtm-launch
description: "Use when sequencing a launch — alpha / beta / GA waves, audience-by-wave logic, narrative beats per wave, engineering-readiness gates. Triggers on 'plan the launch', 'sequence GA'."
status: active
tier: senior
domain: product
context_spine: [product, customer-segment, channel-stage]
recommended_for_user_types: [gtm, founder]
workspaces:
  - gtm
packs:
  - gtm-marketing
trust:
  level: professional
install:
  removable: true
---

# gtm-launch

## When to use

- A product, feature, or major capability is approaching ship-readiness and the team needs a wave plan (alpha → beta → GA) keyed to audience and proof, not a date on a calendar.
- A launch is being planned date-first; the team needs to invert and plan readiness-first so an unmet gate stops a wave instead of leaking past it.
- A previous launch landed soft and the retro names "no audience-by-wave logic" or "narrative beats unclear per wave" as the cause.

Do NOT use to write announcement copy (route to `release-comms`),
lock the message stack (route to `messaging-architecture`), or plan
post-launch retention loops (route to `retention-loops`).

## Cognition cluster

- **Mental model 10 — Reversible vs. irreversible decisions.** A GA
  wave is largely irreversible: rolling back narrative and audience
  expectations after public launch costs more than re-shipping the
  product. Alpha and beta are reversible; treat them as the
  decision-quality buffer. See
  [`docs/contracts/mental-models.md`](../../../docs/contracts/mental-models.md) § 10.
- **Mental model 29 — Premortem.** Before the wave plan locks, write
  the post-mortem of the launch as if it failed. The premortem
  surfaces the gates that need to hold; the wave plan is the inverse
  of that list. See `mental-models.md` § 29.
- **Mental model 16 — Leading vs. lagging indicators.** Engineering-
  readiness signals (error rate, latency, support-load) are leading;
  pipeline lift is lagging. A wave plan that gates on lagging signals
  ships into a soft floor. See `mental-models.md` § 16.
- **Context-spine — product + customer-segment + channel-stage.**
  Read the **product** slot for shippable scope, the
  **customer-segment** slot for who hears the launch on which wave,
  and the **channel-stage** slot for where each wave's audience lives
  in the awareness → decision arc. See
  [`context-spine`](../../../docs/contracts/context-spine.md).

## Procedure

### Step 0: Inherit the message stack

Identify the locked `primary-message.md`, `supporting-proofs.md`, and
`audience-matrix.md` from [`messaging-architecture`](../messaging-architecture/SKILL.md).
If the stack is missing or unstable, stop and route back. A launch
plan without a locked message stack ships three different stories at
three different surfaces.

### Step 1: Run the premortem

Write the launch post-mortem **as if it has already failed**. Three
prompts: *"what did the segment hear that we did not say,"* *"what
broke in the first 48 hours,"* *"what did the alternative say first
and louder."* The premortem produces the failure-mode list the wave
plan must neutralise.

### Step 2: Define the gates per wave

For each wave (alpha · beta · GA), define **entry gates** and **exit
gates**:

- *Alpha entry:* engineering-readiness signal threshold (error rate,
  latency, instrumentation coverage). *Exit:* < N support tickets
  per 100 sessions on the load-bearing flow.
- *Beta entry:* alpha exit + audience-matrix proof exists for the
  beta audience. *Exit:* leading indicator (activation, time-to-
  first-value) clears threshold per `mental-models.md § 16`.
- *GA entry:* beta exit + narrative beats locked for the public
  segment. *Exit:* not applicable — GA is irreversible; the next
  wave is *post-launch retention*, handed to `retention-loops`.

### Step 3: Sequence the audience waves

Audience waves are not seniority waves. They are **proof waves**.
Each wave's audience is whichever segment generates the proof the
*next* wave needs. Order:

1. *Alpha audience* — the segment where the team can sit next to
   the user. Proof: load-bearing flow does not break under real use.
2. *Beta audience* — the segment whose adoption is the credibility
   anchor for GA. Proof: a quotable reference and an activation
   curve.
3. *GA audience* — the full ICP segment from the `customer-segment`
   slot. Proof: pipeline lift, narrative pickup, retention curve.

### Step 4: Assign narrative beats per wave

Each wave gets a narrative beat — the **one** thing the audience
remembers. Alpha beat = trust signal (we are not winging it). Beta
beat = proof signal (it works for someone like you). GA beat = the
primary message from `messaging-architecture` Step 1. Beats stack;
they do not contradict.

### Step 5: Validate the plan against the premortem

Validate each premortem failure mode against the wave plan: verify a
specific gate or beat neutralises it. Any failure mode without an
explicit neutraliser is a known leak — name it, do not bury it.
Validation passes only when every premortem item is either
neutralised or accepted-with-mitigation.

### Step 6: Hand back

Hand the artefacts to [`release-comms`](../release-comms/SKILL.md)
for announcement-surface drafting, to
[`editorial-calendar`](../editorial-calendar/SKILL.md) for cadence
mapping, and to [`launch-readiness`](../launch-readiness/SKILL.md)
for the merge-day checklist.

## Related Skills

**WHEN to use this**

- The unit of work is the wave plan (alpha · beta · GA) with gates and beats, not a single announcement.
- A launch needs readiness-gated sequencing instead of calendar-driven sequencing.
- The team can name the message stack but not which audience hears which beat in which wave.

**WHEN NOT to use this**

- Writing the announcement copy or press surface — route to [`release-comms`](../release-comms/SKILL.md).
- Locking the primary message and proofs — route to [`messaging-architecture`](../messaging-architecture/SKILL.md).
- Pre-merge ops checklist (rollout, rollback, monitoring) — route to [`launch-readiness`](../launch-readiness/SKILL.md).
- Post-launch retention design — route to [`retention-loops`](../retention-loops/SKILL.md).

## When the agent should load this

- "Plan the launch waves for the new pricing tier."
- "Wir starten den GA — gib mir die Alpha-Beta-GA Sequenz."
- "What are the entry gates for the beta wave?"
- "Premortem the launch and rebuild the wave plan from the failure list."
- "Sequence the audience waves around the proof we still need."

## Output

1. **`launch-premortem.md`** — three failure modes per prompt, ranked by carrying cost, each tagged with the wave that owns the neutraliser.
2. **`wave-plan.md`** — three waves (alpha · beta · GA) with entry / exit gates, audience, leading-indicator threshold per wave.
3. **`narrative-beats.md`** — one beat per wave (trust → proof → primary-message), with the line the team will not contradict on any surface during that wave.

## Gotcha

- Calendar-driven launches confuse a date with a gate. A date does not signal readiness; a gate does. The wave plan must hold even if the date slips two weeks.
- "Friends-and-family alpha" is alpha-shaped theatre — it produces the wrong proof for the next wave. Recruit an alpha audience that exposes the load-bearing flow.
- A premortem that produces only three failure modes was rushed; push for ten and keep the load-bearing three.

## Do NOT

- Do NOT write the announcement copy here — copy lives in `release-comms` downstream of locked beats.
- Do NOT collapse alpha and beta to save calendar time — alpha and beta produce different proofs.
- Do NOT lock GA without an explicit retention-loops handoff; an unowned post-launch fortnight is where most launches soften.

## Runnable example

Mid-market HR analytics tool launching workforce-analytics layer:

- Premortem: (a) CFOs hear "another tool" not "retention saving"; (b) HRIS plug-in misconfigured under load; (c) reference customer quote not contractually approved by GA.
- Wave plan — *Alpha:* 3 design-partner HR directors, gate = HRIS plug-in error-rate < 1 % under load. *Beta:* 10 HR leaders matching ICP, gate = activation curve hits 5 cohort-roll-ups per week. *GA:* full ICP segment, gate = quoted reference contractually approved.
- Narrative beats — *Alpha:* "we sat next to you while it worked." *Beta:* "an HR director like you saved 7 hours last board-quarter." *GA:* primary message from `messaging-architecture` Step 1.
- Hand-off → `release-comms` drafts the GA-wave surface; `retention-loops` owns the 30-day post-GA cohort.
