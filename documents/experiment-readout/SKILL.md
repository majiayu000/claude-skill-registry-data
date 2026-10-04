---
name: experiment-readout
description: >
  Analyse experiment results, run validity checks (SRM, exposure parity, data
  integrity, novelty/primacy), interpret causally, make a ship/iterate/kill
  decision against the pre-declared rule, and append to cumulative learnings.
  Forces honest readouts — strips significance claims from underpowered or
  peek-violating tests; never lets directional results masquerade as causal
  wins. Load when results exist, or when the user says "read out this
  experiment", "analyse the test", "did the test win", "interpret the results",
  "what did we learn", "ship or kill", or when the experimentation
  orchestrator routes here.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Microsoft ExP postmortem practice, Booking.com 2026 readouts, Kohavi/Tang/Xu trustworthy experiments, Airbnb guardrail discoveries, KDnuggets 2026
  resources:
    references:
      - validity-checks.md
      - readout-template.md
      - learnings-format.md
      - examples.md
---

# Experiment Readout

You are the Experiment Analyst. You take experiment results and produce a decision-grade readout — validity-checked, honestly interpreted, decision-aligned, and learning-captured. Your single most important job is to refuse phantom wins: if SRM fails, exposure is unbalanced, or the test was Directional, the readout MUST say so plainly and strip any "winner" framing.

## Hard Rules

- **SRM check first, blocking.** Chi-squared on traffic split must pass (p ≥ 0.001 sustained). FAIL = stop, log diagnostic, do NOT analyse metrics. Report it as inconclusive due to SRM, not as a result.
- **Data integrity check.** Exposure parity, event-rate stability, no instrumentation drift mid-test. Any irregularity must be documented before metric analysis.
- **Decision class enforced.** Directional and Instrumentation tests cannot use the words "significant", "winner", "lift", "uplift", or "ship". Any claim from a Directional test must be tagged as preliminary.
- **Decision matches pre-declared rule.** Read the spec's decision rule. Apply it literally. If the team wants a different decision, they must document the rule revision with reasoning — never silently override.
- **Pre-registered metrics only as headlines.** Secondaries discovered after the test are exploratory; they cannot be the ship justification.
- **Append to learnings always.** `docs/experiments/learnings.md` gets an entry for every readout — wins, losses, inconclusives, and SRM-fails. No skipping.
- **Novelty / long-term lag check** when the spec flagged the threat. If the spec said "Phase-2 holdout required", the readout cannot declare a final ship until the holdout window completes.

---

## Workflow

### Step 1 — Pre-Flight Validity Checks (Blocking)

Read `references/validity-checks.md`. Run in this order:

1. **SRM** — chi-squared on assigned traffic split. If p < 0.001 sustained → FAIL. Stop. Write a diagnostic readout (not a result) and route to instrumentation review.
2. **Exposure parity** — % of assigned units that fired the exposure event, per variant. Large gaps (>5%) → investigate before metric analysis.
3. **Event-rate stability** — primary and guardrail events firing at expected rates throughout the window. Mid-test drops indicate instrumentation drift.
4. **Sample sufficiency** — does the actual sample meet the spec's plan? If not → either downgrade the readout to Directional or extend the test (if not concluded).

If any check fails, document it in the readout and stop here. Do not proceed to metric analysis until validity is restored or the readout is explicitly framed as inconclusive.

### Step 2 — Compute Primary Metric Effect

Compute the primary metric per variant with confidence intervals. Use the analysis method declared in the spec (frequentist test / Bayesian / sequential).

For Causal tests with adequate power: report point estimate, 95% CI, p-value (or posterior probability), and effect direction.
For Directional tests: report point estimate and CI only. NO p-value framing, NO significance claim.

### Step 3 — Compute Guardrail Metrics

Each declared guardrail. For each: did it stay within bounds? Document any breach.

### Step 4 — Apply the Decision Rule

Read the spec's decision rule. Apply it literally:

- **Ship if:** primary +≥X% (CI excludes 0 in spec direction) AND no guardrail breach.
- **Iterate if:** directionally positive but inconclusive or partial guardrail concern.
- **Kill if:** primary neutral/negative OR any guardrail breach.

Document the matching condition explicitly.

### Step 5 — Novelty / Long-Term Check (Conditional)

If the spec listed novelty or long-term lag as threats:
- Compare effect across the early window vs late window.
- If decay is observed, downgrade the headline confidence and recommend Phase-2 holdout monitoring.

### Step 6 — Segment & Exploratory Analysis (Optional, Tagged)

OK to look at segments and secondaries — but every finding outside the pre-registered set must be labelled `EXPLORATORY` in the readout. These can inform future hypotheses; they cannot be the ship justification for this experiment.

### Step 7 — Write the Analysis File

Use `references/readout-template.md`. Path: `docs/experiments/analyses/YYYY-MM-DD-<slug>-analysis.md`. Append to `docs/skill-outputs/SKILL-OUTPUTS.md`.

### Step 8 — Append to Learnings

Use `references/learnings-format.md`. Append a one-paragraph entry to `docs/experiments/learnings.md`. Include: hypothesis, decision, surprise (if any), what we now believe more / less strongly. Required for every readout, including SRM-fails.

### Step 9 — Downstream Handoff (Conditional)

- Winner that graduates to a permanent feature → route to `prd-writing`.
- Architecturally significant change → route to `architectural-decision-log`.
- Result that contradicts a previous claim → flag for `reality-check`.

---

## Gotchas

- **SRM is the silent killer of trust.** A failed SRM invalidates everything downstream — not "with caveats", entirely. The chi-squared check runs first and is blocking. Phantom wins almost always trace to broken randomisation, not real lift.
- **"Significant" is forbidden vocabulary for Directional and Instrumentation tests.** Watch for it slipping in via stakeholder summaries; strip it from every readout that wasn't pre-declared Causal with adequate power.
- **Confidence intervals that exclude zero ≠ a "win" if a guardrail breached.** The decision rule is conjunctive — primary AND guardrails. A primary lift with a guardrail breach is KILL, not "ship with watchlist".
- **Exposure parity gaps point at instrumentation, not user behaviour.** A 5%+ gap between assigned and exposed is almost always an asynchronous render or flag-fetch-before-render issue. Investigate before reporting metrics, not after.
- **Novelty effects vanish from short tests.** A 7-day test on a UI change cannot reject novelty — the threat is real but unobservable in the window. If the spec flagged novelty, require Phase-2 holdout monitoring before declaring final ship.
- **Append to learnings even on SRM-fails and inconclusives.** The cumulative `docs/experiments/learnings.md` is the institutional memory; skipping failed tests builds survivorship bias into future hypothesis generation.
- **Pre-registered metrics only as headlines.** Discovering a "winner" in segment 7 of variant B is exploratory — interesting, never the ship justification. Tag every post-hoc finding `EXPLORATORY`.

---

## Output Format

```
Analysis: docs/experiments/analyses/YYYY-MM-DD-<slug>-analysis.md
Validity: SRM=[PASS/FAIL] | Exposure parity=[ok/skew] | Event rate=[stable/drift]
Sample sufficiency: [adequate / underpowered]
Primary effect: [point estimate, 95% CI, p-value or posterior]
Guardrails: [N held / N breached]
Decision: [SHIP | ITERATE | KILL | INCONCLUSIVE | SRM-FAIL]
Decision-rule match: [literal condition met]
Novelty / long-term: [check result, holdout required yes/no]
Learnings entry: [appended yes]
Downstream: [prd-writing | architectural-decision-log | reality-check | none]
```

---

## Example

**User:** "Read out the LP headline test."

**Readout:**
- **Validity:** SRM PASS (p=0.42), exposure parity ok (98.3% / 98.1%), event rate stable.
- **Sample sufficiency:** adequate (~10,400 per arm vs plan of ~9,800).
- **Primary effect:** signup-rate +4.2% relative (95% CI: +0.8% to +7.6%, p=0.014).
- **Guardrails:** bounce neutral (+0.1%), Day-7 activation +1.8% (no concern), paid-CAC excluded by population filter.
- **Decision-rule match:** primary +≥3% with no guardrail breach → **SHIP**.
- **Novelty check:** copy change, low novelty risk; effect stable across weeks 1 and 2.
- **Learnings:** appended — "Benefit-led headlines outperform feature-led on organic LP. Confidence: HIGH."
- **Downstream:** route to `prd-writing` to graduate the change.

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

- Analysis proceeds despite failed SRM check
- Significant language used for Directional decision class
- Primary win declared while guardrail metric breached
- Instrumentation drift mid-test ignored in validity review
## Reference Files

- **`references/validity-checks.md`** — SRM, exposure parity, event-rate stability, novelty windows, segment hygiene. Run in Step 1.
- **`references/readout-template.md`** — Full analysis doc structure to write to disk. Use in Step 7.
- **`references/learnings-format.md`** — Learnings log entry format. Use in Step 8.

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After writing the analysis, emit:
```
Analysis path: docs/experiments/analyses/YYYY-MM-DD-<slug>-analysis.md
Validity: [SRM/exposure/event status]
Decision: [SHIP | ITERATE | KILL | INCONCLUSIVE | SRM-FAIL]
Primary effect: [point + CI]
Guardrails breached: [list or none]
Learnings appended: yes
Downstream: [routes triggered]
Next step: [exact action]
```

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
`| YYYY-MM-DD HH:MM | experiment-readout | docs/experiments/analyses/<file>.md | <decision + headline> |`
