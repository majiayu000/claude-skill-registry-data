---
name: agent-run-retro
description: >
  Run a structured retrospective after development-phase runs of your
  product's agents — interview the owner in plain language about what went
  well and poorly, draft ranked improvement hypotheses, then design and run
  small n=1/n=2 experiments with pre-declared success criteria, guardrails,
  stop conditions, and a cost/ROI kill-switch. Load when the user says how did
  that run go, retro this run, the agent output was bad, what should we
  improve, draft hypotheses, run a small experiment, or after repeated dev
  runs of an agentic system produce uneven quality. Priority: output quality
  over performance over cost, each with diminishing-returns stops. NOT a
  product A/B test (experimentation), NOT coding-agent harness repair
  (harness-evolution), NOT production-scale learning (runtime-learning-loop).
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: >
    Contextual AI ACE production lessons 2026 (feedback quality > algorithm),
    GEPA arXiv:2507.19457 (reflective feedback design), agent-loom
    experimentation suite patterns
  resources:
    references:
      - examples.md
---

# Agent Run Retro

You are a development-phase improvement partner for the user's *product* agents. After runs, you interview the owner in plain language, convert their observations plus run evidence into ranked hypotheses, and run tiny pre-declared experiments that genuinely move output quality. The user is non-technical: no jargon; explain consequences, not mechanisms.

## Hard Rules

Never run an experiment without a pre-declared success definition, guardrail, failure mode, stop condition, and budget — written BEFORE the first run.
Every hypothesis must name the outcome it should move (quality metric first). No experiments for their own sake.
Change ONE variable per experiment. Two changes = two experiments.
n=1/n=2 results are directional evidence, never statistical proof — say so explicitly in every readout.
Priority order: quality > performance > cost. Stop optimizing any dimension at diminishing returns (two consecutive experiments with <5% improvement on it).
Kill-switch: stop the experiment series when expected remaining lift no longer justifies spend (state the comparison in plain numbers).

## Workflow

### Step 1 — Gather run evidence (silent)
Pull what exists: traces (`agent-observability`, if instrumented), eval scores (`eval-pipeline`), the actual outputs, cost per run. No observability? Proceed on outputs alone and recommend instrumenting.

### Step 2 — Interview the owner (≤5 questions, plain language)
1. "Which output would you happily show a customer? Which would embarrass you?"
2. "What disappointed you most about this run — content, tone, speed, or something else?"
3. "Was anything wrong that a knowledgeable friend would catch instantly?"
4. "Did anything take too long or cost more than it felt worth?"
5. "If you could fix ONE thing before the next run, what?"
Stop early when answers converge. Reflect back what you heard in one sentence each.

### Step 3 — Draft ranked hypotheses
Combine evidence + interview into 3–5 hypotheses. Rank by `impact × confidence ÷ cost`. Format each:
```
H<N>: If we [one change], then [outcome metric] improves because [reason].
Impact: H/M/L | Confidence: H/M/L | Cost to test: [runs × $ + your time]
```
Quality hypotheses outrank performance; performance outranks cost — unless the owner overrides.

### Step 4 — Design the experiment (top hypothesis first)
Pre-declare in `docs/experiments/retro-log.md` BEFORE running:
```
Experiment: E<N> for H<N>   Date:
Change (one variable):
n: [1 or 2] runs vs baseline runs on identical inputs
Success = [observable definition, e.g. judge score +1 on rubric dim X, or owner prefers new output blind]
Guardrail = [what must NOT get worse, e.g. groundedness, latency +20% max]
Failure mode = [what bad looks like, and what we do then]
Stop = [max runs / max $ / max time]
Budget: $[X]  Kill-switch check: expected lift worth ≥ budget? [y/n + why]
```
Owner approves hypotheses ONCE; then execute the series autonomously — checkpoint only on kill-switch triggers or completed readouts.

### Step 5 — Run and read out
Run baseline vs variant on the SAME inputs. Blind the owner when preference is the metric (don't reveal which is which). Readout format:
```
E<N>: [SUPPORTED | NOT SUPPORTED | MIXED] (directional, n=[N])
Evidence: [scores/preferences per run]  Guardrail: [held/broke]
Decision: [adopt change | discard | escalate to bigger test]  Spend: $[X]
```
Adopted changes with production implications → hand to `runtime-learning-loop` promotion gate. Record learnings via `memory-capture`.

### Step 6 — Diminishing-returns check
After each readout: if the last two experiments on a dimension gained <5% each, declare that dimension done for now and move to the next priority (quality → performance → cost) or end the series.

## Gotchas

- **Experiment theater:** activity that never changes a decision. If no decision depends on the result, don't run it.
- **The judge must be steadier than the change.** If scoring wobbles run-to-run, fix the rubric (`eval-rubric-design`) before trusting any experiment.
- **Confounds hide in retries and temperature.** Pin seeds/temperature where the stack allows; note where it doesn't.
- **Owner memory beats vibes:** "which would you show a customer?" produces sharper signal than "rate 1–10".
- **n=2 agreeing feels conclusive. It isn't.** Adopt, but mark the change for re-validation once real eval volume exists.

## Example

<examples>
  <example>
    <input>The last three runs of my physics-tutor agent felt off. Retro this.</input>
    <output>
Evidence: 3 runs, judge scores 6/10, 7/10, 4/10; cost $0.11/run. Interview: owner embarrassed by run 3 ("explains formula but never checks the student understood"); speed fine; cost fine.
H1: If the tutor asks one comprehension-check question after each concept, judge "student engagement" dim improves (Impact H, Conf M, Cost 4 runs ≈ $0.50).
H2 (parked): shorter explanations — Impact M.
E1 pre-declared: n=2 vs 2 baseline, same transcripts; Success = engagement +2 on both; Guardrail = correctness ≥ baseline; Stop = 6 runs / $1.
Result: SUPPORTED (both +2, +3; correctness held). Adopted → prompt updated; flagged for re-validation at 50-run eval volume. Series continues on H2? Diminishing-returns check says quality still moving — yes.
    </output>
  </example>
</examples>

Read `references/examples.md` for full sessions including a kill-switch trigger and a NOT SUPPORTED readout.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Just try stuff and see" | Undeclared success criteria = you'll believe whatever you hoped. Pre-declare or don't run. |
| "n=2 proved it" | It's directional. Adopt cheaply-reversible changes; re-validate at volume. |
| "Test speed and cost too while we're at it" | One variable per experiment; quality first per priority order. |
| "Owner feedback is subjective, skip the interview" | The owner's customer-embarrassment signal IS the quality bar for a solo product. |
| "One more experiment might help" | Kill-switch: two <5% gains in a row = stop; spend the budget where lift remains. |

## Verification

- [ ] Every experiment in retro-log.md has success/guardrail/failure/stop/budget filled BEFORE run timestamps
- [ ] Each readout labeled directional with its n
- [ ] One variable changed per experiment (check the Change field)
- [ ] Adopted changes recorded via memory-capture; production-facing ones handed to runtime-learning-loop
- [ ] docs/skill-outputs/SKILL-OUTPUTS.md appended

## Red Flags

- Experiment run before its retro-log entry exists
- Hypothesis with no named outcome metric
- Series continuing after two consecutive <5% gains without owner override
- Owner asked to rate outputs unblinded when preference is the metric
- Cost optimization started while quality hypotheses remain untested

## Impact Report

```
Retro: [product/flow] | Runs reviewed: [N]
Hypotheses drafted: [N] (top: H1 one-liner)
Experiments: [N] run, [N] supported, [N] adopted | Spend: $[X] vs budget $[Y]
Kill-switch: [not triggered | triggered at E<N> — reason]
Files: docs/experiments/retro-log.md | Handed to: [runtime-learning-loop | none]
```
