---
model_tier: high
name: funnel-analysis
description: "Use when diagnosing where a SaaS or product funnel leaks — visitor → signup → activation → paid → retained — channel-agnostic, conversion-rate-driven."
status: active
tier: senior
domain: product
context_spine: [product, customer-segment, funnel-stage]
workspaces:
  - product
packs:
  - product-basic
trust:
  level: professional
install:
  removable: true
---

# funnel-analysis

## When to use

- Conversion to paid dropped and nobody knows which step broke.
- A new signup channel went live and you need to compare its funnel shape to the baseline.
- A board ask: "where does the money leak between landing page and paying customer?"

Do NOT use for ranking features, valuation, or OKR decomposition (see Related Skills). Funnel analysis is a **diagnostic**, not a roadmap.

## Cognition cluster

- **Mental model 16 — Leading vs. lagging indicators.** Paid is
  lagging; activation is leading; signup is upstream of both. A
  funnel decision built on the lagging stage can only confirm the
  miss; the leading stage names the binding fix. See
  [`docs/contracts/mental-models.md`](../../../docs/contracts/mental-models.md) § 16.
- **Mental model 13 — Occam's razor.** When a stage drops, the
  simpler explanation usually wins: *"acquisition mix shifted"*
  beats *"users no longer understand the product."* Pick the simpler
  cause; it changes the move. See `mental-models.md` § 13.
- **Mental model 3 — Pareto (80/20).** Drops are almost never
  uniform across segments; ~20 % of the segment × stage cells carry
  ~80 % of the loss. Segment before treating the average as
  actionable. See `mental-models.md` § 3.
- **Context-spine — product + customer-segment + funnel-stage.**
  Read the **product** slot for what activation can actually mean
  in-product (the activation event must be shippable), the
  **customer-segment** slot for which segments' switch-events the
  funnel is built for, and the **funnel-stage** slot for the
  position of each stage relative to the buying journey. See
  [`context-spine`](../../../docs/contracts/context-spine.md).

## Procedure

### Step 0: Inspect

1. Confirm the cognition cluster: this is **conversion diagnosis**, channel-agnostic. Paid social, organic, partner, and self-serve all share the same shape; only the inputs differ.
2. Confirm event tracking exists for all 5 stages. If even one stage is inferred, the analysis is unreliable — flag and proceed under that caveat.

### Step 1: Lock the 5 stages

1. The canonical SaaS funnel: **Visitor → Signup → Activation → Paid → Retained-D30**.
2. Activation is the load-bearing definition. Pick the **single event** that historically correlates with paid conversion — not "logged in", not "viewed dashboard". For most SaaS this is "completed first meaningful action" (sent first invoice, ran first query, invited first teammate).
3. Retained-D30 = still active 30 days after first paid charge. Earlier than D30 is noise; later requires more data.

### Step 2: Pull stage-to-stage conversion

1. Compute conversion rate at each step: `stage_n / stage_n-1`. Always use cohorts (signup-week or signup-month), never aggregate snapshots — aggregates lie when traffic mix changes.
2. For each rate, attach a 95% confidence interval. Tiny denominators give big bands; the band is half the story.
3. Plot a 12-week trend per rate. A single point is gossip; a trend is evidence.

### Step 3: Benchmark vs internal baseline

1. The right benchmark is **your own funnel one quarter ago**, not industry averages. Industry averages mix verticals so coarsely they're useless for action.
2. For each stage: is current rate within ±2 percentage points of trailing-quarter median? If not, that stage is the primary suspect.
3. If multiple stages move off-band simultaneously, the cause is upstream (acquisition mix change, broken instrumentation), not the stage itself.

### Step 4: Segment the broken stage

1. Take the suspect stage and segment by: channel · device · plan · geo · cohort week.
2. The drop is almost always concentrated in one segment, not uniform. Uniform drops point to instrumentation.
3. Anti-pattern: averaging across segments and treating the average as actionable. The average user does not exist.

### Step 5: Hypothesise causes

1. For the broken segment-stage, write 3 candidate causes. Rank by testability, not plausibility.
2. The cheapest experiment to falsify the top candidate is the next step — usually a UX change, a copy test, or an onboarding tweak.
3. If no cause is testable in under 2 weeks, the analysis is not yet sharp enough.

### Step 6: Validate

1. Recompute the broken rate after the experiment ships. Same cohort definition. Same window.
2. If the rate moves but the downstream rates don't follow, you fixed a vanity step. Keep going.

## Gotcha

- "Activation" defined as a low-friction event (signup confirmation, first login) gives you a flatter funnel that is useless for prediction. Activation must correlate with paid.
- Aggregate funnel rates that look stable can hide a 30-point drop in one channel masked by a 30-point lift in another. Always segment.
- D7 retention looks great compared to D30. Pick the metric that matches the contract length, not the one that flatters.
- Holiday weeks, deploys, marketing pushes, and refund days distort cohorts. Annotate the timeline; don't pretend a 5pp drop is real on a known holiday.

## Do NOT

- Do NOT use industry-average benchmarks as a target. They mix B2B with B2C, freemium with high-touch — the average is meaningless.
- Do NOT compare a 1-week cohort to a 12-week trailing median; sample size is too small to draw conclusions.
- Do NOT diagnose retention on a funnel without separating new-user retention from re-engaged-user retention.

## Related Skills

**WHEN to use this**

- Where in the funnel did conversion drop?
- Compare the funnel shape between two channels.

**WHEN NOT to use this**

- Pricing tier or unit-economics question — route to [`unit-economics-modeling`](../unit-economics-modeling/SKILL.md).
- Roadmap ranking from funnel findings — route to [`rice-prioritization`](../rice-prioritization/SKILL.md).
- Setting team OKRs around the diagnosed metric — route to [`okr-tree-modeling`](../okr-tree-modeling/SKILL.md).
- Valuing the business that owns the funnel — route to [`dcf-modeling`](../dcf-modeling/SKILL.md).

## When the agent should load this

- "Where is our funnel leaking?"
- "Why did paid conversion drop last month?"
- "Compare the funnel for paid social vs organic."
- "Diagnose this dropoff between signup and activation."
- "Is this drop real or instrumentation?"

## Output

1. **`funnel-table.md`** — 5-stage funnel with cohort rates, 95% CI, and 12-week trend (sparkline or compact ASCII). One row per cohort week or month.
2. **`segment-breakdown.md`** — table of the broken stage segmented by channel · device · plan · geo. Rates with CIs. Suspect segments highlighted.
3. **`hypothesis-list.md`** — top 3 causes for the broken segment-stage with cheapest-falsification experiment per cause and an explicit prediction for the next measurement.
