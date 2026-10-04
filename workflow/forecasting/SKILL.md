---
model_tier: high
name: forecasting
description: "Use when constructing the finance-side forecast — top-down vs bottom-up shape, confidence bands, retro-loop. Triggers on 'build the forecast model', 'reconcile top-down with bottom-up'."
status: active
tier: senior
domain: process
context_spine: [product, fiscal-period, customer-segment]
recommended_for_user_types: [finance, founder]
workspaces:
  - finance
packs:
  - finance-basic
trust:
  level: professional
install:
  removable: true
---

# forecasting

## When to use

- The annual plan or quarterly board pack needs a forecast model that survives a retro — not last quarter's number with a multiplier.
- Top-down (TAM × penetration × motion) and bottom-up (deal-level) calls have diverged and the reconciliation hasn't been written.
- A new finance-partner inherits a forecast and needs to rebuild the construction shape without inheriting the prior regime's optimism.

Do NOT use to qualify a single deal (route to `deal-qualification-meddic`), construct the RevOps commit list (route to `forecast-accuracy` (H10) — finance owns the shape, RevOps owns the call), or run capital-runway scenarios (route to `runway-cognition` (O3)).

## Cognition cluster

- **Mental model 9 — Hypothesis-driven thinking.** Each forecast is
  a falsifiable claim about a window. If the call cannot be falsified
  inside the window, the call is a narrative, not a forecast. See
  [`mental-models.md`](../../../docs/contracts/mental-models.md) § 9.
- **Mental model 29 — Premortem.** Before locking the call, write the
  post-window retro as if commit missed by 20 %. The premortem
  surfaces which construction inputs were riding on weak evidence;
  demote those before the call locks. See `mental-models.md` § 29.
- **Mental model 16 — Leading vs lagging.** Closed-won is lagging;
  pipeline coverage, segment conversion, and slot-completeness are
  leading. A forecast built only on lagging signals can confirm but
  not steer. See `mental-models.md` § 16.
- **Context-spine — product + fiscal-period + customer-segment.**
  Read the **product** slot for what is GA-shippable in the window;
  the **fiscal-period** slot for the cadence the model must
  reconcile against (monthly close vs quarterly board pack vs annual
  plan vs multi-year plan); the **customer-segment** slot for
  segment-historical close rates. See
  [`context-spine`](../../../docs/contracts/context-spine.md).

## Procedure

### Step 0: Inspect the construction shape

Read the fiscal-period slot. Decide between three shapes:

1. **Top-down** — anchor against TAM × penetration band × motion
   band. Healthy for annual plans and multi-year plans where
   bottom-up evidence is thin past one window.
2. **Bottom-up** — sum deal-level conviction (composes H10
   `forecast-accuracy` via the `forecast-construction-shape` ADR).
   Healthy for quarterly windows where deal evidence is fresh.
3. **Hybrid** — both, with an explicit reconciliation. Healthy when
   top-down and bottom-up diverge by more than the historical
   confidence band.

State the choice. A forecast without a stated shape inherits the
prior regime's shape silently.

### Step 1: Construct the call against the shape

For top-down: write `{tam, penetration_band, motion_band}` — every
input cites its source. Penetration bands are evidence ranges, not
single points; motion bands reflect channel mix.

For bottom-up: consume H10's commit-list against the
`forecast-construction-shape` interface. Sum commit-tagged ×
in-window close-rate per segment.

For hybrid: do both, then write the reconciliation. If top-down ≠
bottom-up by more than the confidence band, the divergence is the
forecast — not either number.

### Step 2: Calibrate the confidence band

Compute historical deviation from the last 4–8 windows of the same
fiscal-period cadence. Attach as `{plus_pct, minus_pct}`. A band
asymmetric on the downside is honest about prior misses; symmetric
bands silently pretend prior accuracy.

### Step 3: Premortem the construction

Write *"if the forecast misses by 20 %, the reason is ___."* For
top-down: which penetration / motion input was the load-bearing
assumption? For bottom-up: which anchor deals carry > 10 % of
commit? Demote inputs that the premortem can name as single-point
risks.

### Step 4: Emit the typed interface

Produce `forecast-band.json` per the `forecast-construction-shape`
ADR. H10 consumes the artifact for the commit-call. The fields:
`construction_shape`, `commit_value`, `best_case_value`,
`pipeline_value`, `confidence_band`, `retro_signature`,
`segment_scope`, `fiscal_period`, `construction_inputs`. Drop the
artifact in the location H10's `## Output` references.

### Step 5: Run the accuracy retro-loop

At window-end, compare predicted commit / best-case to actual
closed-won. Compute per-segment and per-construction-input miss
rate. Patterns that repeat for two windows become shape changes in
Step 0 (e.g. switching from bottom-up to hybrid because deal
evidence stopped predicting); one-off misses become input upgrades
in Step 1.

## Related Skills

**WHEN to use this**

- Constructing the finance-side forecast (annual plan, board pack, multi-year plan).
- Running the construction-shape retro and feeding it back into Step 0.

**WHEN NOT to use this**

- Single-deal qualification — route to [`deal-qualification-meddic`](../deal-qualification-meddic/SKILL.md).
- Commit / best-case / pipeline categorisation of deals — route to [`forecast-accuracy`](../forecast-accuracy/SKILL.md) (H10); H10 consumes against this skill's `forecast-band.json` interface.
- Cash-runway shape and fundraise-trigger heuristics — route to [`runway-cognition`](../runway-cognition/SKILL.md) (O3).
- Multi-statement scenario construction over base / upside / downside — route to [`scenario-modeling`](../scenario-modeling/SKILL.md) (O4).

Wing-4 handoff: this skill emits the `forecast-band.json` artifact
that `forecast-accuracy` (H10, Wing-3) reads. Per
`docs/contracts/adr-forecast-construction-shape.md`,
`docs/guidelines/wing4-handoff.md` § Chain 4.

## When the agent should load this

- "Build the annual forecast model."
- "Top-down and bottom-up disagree — reconcile them."
- "Why was last quarter's forecast off?"
- "Was machen wir bei der Forecast-Konstruktion anders?"

## Output

1. **`forecast-band.json`** *(Wing-3 / Wing-4 typed interface)* — `construction_shape`, `commit_value`, `best_case_value`, `pipeline_value`, `confidence_band`, `retro_signature`, `segment_scope`, `fiscal_period`, `construction_inputs`. Per `adr-forecast-construction-shape.md`.
2. **`construction-notes.md`** — shape chosen + why; per-input evidence; reconciliation note (hybrid only).
3. **`premortem.md`** — "if we miss by 20 %, the reason is ___"; tagged demotions from Step 3.
4. **`retro-deltas.md`** *(at window-end)* — predicted vs actual per construction input; shape-change recommendation if the pattern repeats.

## Gotcha

- A forecast without a stated `construction_shape` inherits last regime's shape silently. Always emit the field.
- Symmetric confidence bands lie about prior misses. If the last two windows missed on the downside, the band is asymmetric.
- Top-down models with single-point penetration assumptions are scenarios in disguise. Use bands.
- Hybrid models that don't write the reconciliation are top-down models with bottom-up garnish.

## Do NOT

- Do NOT collapse hybrid forecasts into a single number without keeping the divergence visible.
- Do NOT skip Step 4 — the typed interface is what makes H10 reproducible.
- Do NOT change the construction shape on a single-window miss; shape changes require a two-window pattern.

## Runnable example

End of FY: annual plan + Q1 commit both due.

- Step 0 — fiscal-period slot says `annual` + `quarterly`. Annual is top-down; Q1 is bottom-up.
- Step 1 — top-down: TAM $4.2B, penetration band 0.6–0.9 %, motion band SaaS-mid; expected $25–38M ARR. Bottom-up: H10 commit-list sums to $8.1M in Q1, segment close rate 78 %.
- Step 2 — last 4 quarters deviation: +6 % / –14 %. Confidence band attached.
- Step 3 — premortem: top-down anchored on penetration upper bound; demoted to 0.6–0.75 %. Bottom-up: two anchor deals tagged single-risk procurement; demoted.
- Step 4 — emit `forecast-band.json`: `construction_shape=hybrid`, commit $6.3M, best-case $8.1M, band +6/–14 %, retro_signature `quarterly | [+6, –14]`, segment_scope mid-market, fiscal_period `quarterly`.
- Retro — at quarter-end, actual $6.1M; band held. Annual top-down revisit in two quarters.
