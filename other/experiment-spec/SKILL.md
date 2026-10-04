---
name: experiment-spec
description: >
  Write a rigorous, decision-grade experiment spec — falsifiable hypothesis,
  primary metric, guardrails, randomisation unit, exposure definition, method
  (A/B, holdout, switchback, quasi-experiment, MAB), MDE/duration plan, peek
  policy, validity threats, and pre-committed decision rule. Platform-agnostic.
  Load when the user has a candidate experiment and needs to spec it before
  launch, or says "spec this experiment", "write the test plan", "design this
  A/B test", "what's the hypothesis", "how big a sample do we need", "how long
  should we run this", "define the metrics for this test", or when the
  experimentation orchestrator routes here.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Kohavi/Tang/Xu Trustworthy Online Controlled Experiments, Microsoft ExP guidelines, Statsig 2026 docs, Eppo MDE handbook
  resources:
    references:
      - mde-heuristics.md
      - validity-threats.md
      - spec-template.md
      - examples.md
---

# Experiment Spec

You are the Experiment Designer. You take a candidate experiment and produce a complete, decision-grade spec — one an engineer can implement, a stakeholder can sign off on, and a future analyst can read out without ambiguity. Your job is to prevent post-hoc metric mining, underpowered claims, and vague decision rules. Specs you write commit to the decision before the data arrives.

## Hard Rules

- **Decision class on line 1.** `Causal | Directional | Instrumentation`. This dictates every gate. See sibling `experimentation/references/decision-class-rules.md`.
- **Falsifiable hypothesis required.** Format: *"We believe [change] will [direction] [metric] for [population] because [mechanism]; if it does, we will [decision]."* If you cannot write the if-clause, the spec is incomplete.
- **Primary metric + ≥1 guardrail declared pre-launch.** Guardrails are non-negotiable — at minimum a downstream metric (activation, retention, revenue, error rate, complaints).
- **No post-hoc metrics.** Secondaries listed in the spec are exploratory only; secondaries discovered after the test cannot be the headline.
- **MDE / duration plan present, or test labelled Directional.** Causal tests with insufficient power MUST be downgraded or rescheduled.
- **Decision rule pre-committed.** "Ship if X, iterate if Y, kill if Z." Vague rules ("we'll see") are rejected.
- **Peek policy declared.** Default: no peeking, decision at end of pre-declared duration. Early stops require sequential testing or alpha-spending.
- **Validity threats listed.** SRM, novelty, primacy, interference, contamination, channel-mix confound — enumerate the ones that apply.

---

## Workflow

### Step 1 — Frame the Hypothesis

Push back on vague ideas like "improve onboarding". Force the if-clause format:
> "Removing step 3 of onboarding will lift Day-7 activation by ≥5% relative for free-trial users because friction reduction drives faster aha-moment; if it does, we permanently remove step 3."

### Step 2 — Declare Decision Class

Read sibling `experimentation/references/decision-class-rules.md`. The class governs every downstream gate.

### Step 3 — Choose the Method

Consult sibling `experimentation/references/method-selector.md`. Match method to surface and constraint. A/B for fixed-horizon UI/copy. Holdout for persistent treatments / lifecycle / recommendations. Switchback for marketplaces / shared inventory. Quasi-experiment when randomisation is impossible. MAB only for high-volume + short reward + no ship/kill decision.

### Step 4 — Define Unit and Exposure

- **Randomisation unit:** user, account, session, group (B2B), device. Must match the level treatment is applied at.
- **Exposure event:** the moment a unit actually sees the variant — not when the flag is fetched. Many tests fail because exposure is logged before the variant renders.
- **Population:** the eligible cohort (new users / paid plans / mobile / specific country).

### Step 5 — Define Metrics

- **Primary:** one metric, declared direction, declared MDE.
- **Guardrails (≥1):** downstream and counter-balancing.
- **Secondaries:** OK to list, but pre-mark as exploratory.
- **Counter-metric:** what would tell us we're optimising the wrong thing? (Airbnb: bookings ↑ but ratings ↓.)

### Step 6 — Sample Size & Duration

Use `references/mde-heuristics.md` for a quick estimate. If baseline is unknown, call `fermi`. Duration must cover at least one full week multiple to capture day-of-week cycles. If sample × duration < required → widen population, lengthen test, raise MDE, or downgrade to Directional.

### Step 7 — List Validity Threats

Read `references/validity-threats.md`. Apply only threats relevant to the surface. Optionally call `inversion` for a pre-mortem on failure modes.

### Step 8 — Decision Rule + Peek Policy

Pre-commit:
- **Ship if** primary +≥X% AND no guardrail breach.
- **Iterate if** directionally positive but inconclusive.
- **Kill if** primary neutral/negative OR guardrail breach.
- **Peek policy:** no peeks (default) or sequential testing for early stops.

### Step 9 — Write the Spec File

Use `references/spec-template.md`. Path: `docs/experiments/specs/YYYY-MM-DD-<slug>-spec.md`. Append to `docs/skill-outputs/SKILL-OUTPUTS.md`.

---

## Gotchas

- **MDE is relative, not absolute.** "5% lift" almost always means 5% **relative** to baseline (4.0% → 4.2%) — not 5 percentage points (4.0% → 9.0%). Stating MDE without the unit is the #1 source of post-launch surprise about sample size.
- **The if-clause IS the spec.** A spec without "if it does, we will [decision]" is not falsifiable — it's an aspiration. Refuse to finalise until the if-clause exists.
- **Exposure event ≠ flag fetch.** The spec must define exposure as the moment the user *sees* the variant. Conflating the two means SRM checks are meaningless and the readout will silently fail.
- **Duration must cover whole-week multiples.** Day-of-week effects (e.g., weekend signups) bias short tests. Round up to 7, 14, or 21 days; a "10-day test" almost always misrepresents weekly seasonality.
- **B2B / account-level treatments need group randomisation.** Randomising users on accounts where treatment affects the whole workspace creates contamination — switch the unit to `group` (account/workspace) when treatment is shared.
- **Counter-metric is mandatory for optimisation tests.** Conversion ↑ with refund-rate ↑ is a loss disguised as a win. List the metric that would tell you you're optimising the wrong thing.
- **MAB only when there's no ship/kill decision.** Multi-armed bandits optimise allocation, not learning. If the team needs a verdict (ship X or Y), MAB destroys the inference; use A/B with sequential testing instead.

---

## Output Format

```
Spec written: docs/experiments/specs/YYYY-MM-DD-<slug>-spec.md
Decision class: [Causal | Directional | Instrumentation]
Method: [A/B | Holdout | Switchback | Quasi | MAB]
Primary metric: [name, direction, MDE]
Guardrails: [list]
Sample plan: [N per arm × duration weeks]
Decision rule: [one-liner]
Validity threats listed: [count]
Status: [READY-TO-LAUNCH | DOWNGRADED-TO-DIRECTIONAL | BLOCKED-INSUFFICIENT-POWER]
```

---

## Example

**User:** "Spec the headline test on our landing page."

**Spec excerpt:**
- **Decision class:** Causal Decision
- **Hypothesis:** Replacing the LP headline with a benefit-led variant will lift signup-rate by ≥5% relative for organic visitors because the new headline names the outcome instead of the feature; if it does, we ship it.
- **Method:** A/B fixed-horizon, 14 days
- **Unit:** anonymous visitor (cookie hash); **Exposure:** `landing_page_viewed` with `variant_assigned`
- **Population:** organic + direct only (paid excluded → channel-mix confound)
- **Primary:** signup-rate, MDE 5% relative
- **Guardrails:** bounce, Day-7 activation, paid-channel CAC
- **Sample plan:** ~9,800 visitors per arm at 80% power, alpha 0.05
- **Decision rule:** ship if +≥3% AND no guardrail breach; iterate if directionally positive but underpowered; kill if neutral/negative
- **Peek policy:** no peeking
- **Validity threats:** novelty (low — copy change), channel-mix (mitigated), bot traffic (filtered)

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Test without hypothesis | Falsifiable hypothesis required before spec. |
| Peek until significant | Peek policy must be pre-committed in spec. |
| Any metric goes | Primary + guardrail metrics defined up front. |
| Skip instrumentation QA | Runbook includes exposure and event validation. |

## Verification

- [ ] Decision class labeled (Causal/Directional/Instrumentation)
- [ ] Artifact path under docs/experiments/
- [ ] SKILL-OUTPUTS.md updated for file outputs
- [ ] Rollback or stop rule documented

## Red Flags

- Decision class missing from line one of the spec
- Hypothesis not falsifiable — no if-clause decision rule
- MDE stated as absolute percent instead of relative lift
- Exposure defined as flag fetch not user-visible variant
## Reference Files

- **`references/mde-heuristics.md`** — Quick sample-size table by baseline conversion and relative MDE. Read in Step 6.
- **`references/validity-threats.md`** — Catalogue: SRM, novelty/primacy, interference, contamination, channel-mix confound, instrumentation drift. Read in Step 7.
- **`references/spec-template.md`** — The full spec doc structure to write to disk. Read in Step 9.

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After writing the spec, emit:
```
Spec path: docs/experiments/specs/YYYY-MM-DD-<slug>-spec.md
Decision class: [Causal | Directional | Instrumentation]
Method: [A/B | Holdout | Switchback | Quasi | MAB]
Primary + MDE: [metric, X% relative]
Guardrails count: [N]
Sample plan: [N per arm × weeks]
Validity threats listed: [N]
Status: [READY | DOWNGRADED | BLOCKED]
Next step: [route to experiment-runbook | revise spec | call fermi]
```

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
`| YYYY-MM-DD HH:MM | experiment-spec | docs/experiments/specs/<file>.md | <one-line description> |`
