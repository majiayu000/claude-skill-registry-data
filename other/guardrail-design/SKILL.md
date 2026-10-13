---
name: guardrail-design
description: >-
  Fires when a fellow needs to decide how an AI product is stopped from doing the
  wrong thing — "design the guardrails", "when does a human sign off", "how do we
  handle failures / bad outputs", "what confidence threshold should we auto-approve
  at", "where do we put the human in the loop". Returns a guardrail spec: every
  failure mode placed on a cost-of-error × volume matrix, a three-layer stack (rules
  in code → confidence threshold → human sign-off) sized per mode, a derived
  confidence threshold, and a human-sign-off trigger for every high-cost / low-
  confidence path. Do NOT fire to derive the acceptable failure rate or pick the
  autonomy level (use eval-first-spec), to lay out the whole component pipeline (use
  compound-system-architecture), or to decide whether a human can now be REMOVED
  because accuracy has held (use refine-flywheel).
type: generator
supersedes: none
---

# Guardrail Design

## What it does

Turns "how do we stop it doing something bad?" into a spec a build can enforce. The
fellow brings the failure taxonomy, the chosen autonomy level, and the cost of one
failure per mode (from `eval-first-spec`). This skill places each mode on a
cost-of-error × volume matrix, assigns a three-layer guardrail stack — rules in code,
a confidence threshold, human sign-off — sized to the quadrant, derives the confidence
threshold from the acceptable failure rate, and writes a sign-off trigger for every
path where a high-cost failure could ship on low confidence. The output is the filled
[template.md](template.md). It refuses one guardrail applied to everything, and it
refuses a felt confidence number.

## The Icarus reframe

A guardrail is not one thing you bolt on the end. It is three layers, each cheaper than
the next, each sized to a single number: cost-of-error × volume. Rules in code catch the
knowably-wrong for free and run on everything. A confidence threshold catches the
uncertain — but only if the threshold is *derived* from the acceptable failure rate and
calibrated against real outcomes, never a 0.8 that "looks safe". Human sign-off is the
most expensive layer, so it is spent only where a failure is costly enough to be worth a
person's minute — and it must be spent there, because the one thing you can never do is
let a catastrophic-cost action ship on a model's confidence alone. The move that a
generic prompt never makes: match the mechanism to the quadrant, which means *adding* a
human where cost is high and *removing* the human where cost is low.

## When to use / When NOT

Use when the eval-first spec exists (a failure taxonomy, an autonomy level, a
cost-of-one-failure per mode) and the question is now what mechanism enforces it. This
skill is the depth build of component 4 — validate & guardrails — in the compound-system
architecture. Trigger phrases: "design the guardrails", "when does a human sign off",
"how do we handle failures", "what confidence threshold", "where's the human in the loop".

| Not this skill | Use instead | Why |
|---|---|---|
| "What acceptable failure rate per mode / which autonomy level L0–L4" | `eval-first-spec` | That *derives* the rate and picks the level from cost-of-one-failure. This skill consumes both and builds the mechanism that holds them. Run it first; it hands this the taxonomy and the rates. |
| "Design the whole AI system / the component pipeline / the effort split" | `compound-system-architecture` | That names component 4 exists. This designs what is inside it. Compose: the architecture says "a guard sits here", this says "here is the guard, layer by layer, sized to cost × volume". |
| "We've held accuracy for a month — can we drop the human sign-off now" | `refine-flywheel` | That promotes autonomy as an eval result, never by feel. This designs the guard at the *current* level; removing a layer as autonomy climbs is the flywheel's job, gated by a re-run of the eval set. |
| "Structure the pilot / price it / what's the commercial success metric" | `pilot-six-term-sheet` | Commercial, not correctness. |

If no eval-first spec exists — no taxonomy, no cost-of-one-failure — do not invent them
to fill the matrix. Ask the one question that unblocks it (what does one failure cost,
and how often can it happen?) or route to `eval-first-spec`. A guardrail sized against
made-up costs is worse than none: it looks rigorous and guards nothing.

## Method

Copy this checklist:

```
Guardrail Design progress:
- [ ] Step 1: Pull the inputs from eval-first-spec (taxonomy, level, cost, rate)
- [ ] Step 2: Band each mode — cost-of-error × volume → quadrant → guardrail class
- [ ] Step 3: Assign the three-layer stack per mode, in order, with a fail-mode
- [ ] Step 4: Derive the confidence threshold from the acceptable rate + calibration
- [ ] Step 5: Write a sign-off trigger for every high-cost / low-confidence path
- [ ] Step 6: Cost the stack and feed it back to cost-per-outcome
- [ ] Step 7: Run the kill line before returning
```

**Step 1 — pull the inputs.** From `eval-first-spec`: the failure taxonomy (the named
modes — Miss, False alarm, Confidently wrong, Wrong format, Too slow, Silent failure, plus
any product-specific), the chosen autonomy level L0–L4, the cost-of-one-failure per mode,
and the derived acceptable rate per mode. Tag each `[Fact]` / `[Assumption]`. If a mode
has no cost-of-one-failure, its guardrail cannot be sized — send it back, do not guess.

**Step 2 — band and place.** Give each mode a cost band and a volume band.

| Cost-of-error band | Test (loaded cost of one undetected failure) | Acceptable rate tends to |
|---|---|---|
| Catastrophic | Irreversible: safety, regulatory breach, data loss, or worth many outcomes | → 0 |
| High | Reversible but expensive: remediation, lost deal, trust; worth > one outcome | Tight |
| Low | A shrug: the user self-corrects; worth < one outcome | Loose |

| Volume band | Test (the operational line, not an arbitrary count) |
|---|---|
| Low | One reviewer can attend to *every* instance of this mode within its SLA without dropping the day job |
| High | Reviewing every instance is impossible or unaffordable; only the flagged subset gets a human |

There is no Medium band. A mode that feels "Medium" rounds **up** to High for stack-sizing,
never down: if you cannot review *every* instance within its SLA, it is High — it gets the
confidence gate + exception review, not a promise of full per-item review you cannot keep.

Place each mode on the matrix; read off its guardrail class:

| | Volume Low (reviewable) | Volume High (not fully reviewable) |
|---|---|---|
| **Catastrophic** | Q1 — code hard-block on the knowable-bad + human sign-off on the action; confidence never gates alone; **fail-safe** | Q2 — code hard-block + conservative confidence gate + human on flagged exceptions; monitor residual; **fail-safe** |
| **High** | Q3 — confidence gate + human sign-off below τ; **fail-safe** | Q4 — code rules + confidence gate, human on exceptions only, alert on rate breach; **fail-safe** on the action |
| **Low** | Q5 — confidence gate + log; no human; **fail-open** | Q6 — code rules only; accept residual; monitor aggregate; no per-item human; **fail-open** |

Two laws fall out of the matrix. First: a Catastrophic or High mode may never rest on
model confidence alone — it carries a code hard-block, a human sign-off, or both. Second:
a Low-cost mode carries no per-item human review — a sign-off you cannot afford is one you
will quietly stop doing. If your grid puts the same stack in every cell, you have not
designed guardrails; you have picked a habit.

**Step 3 — the three-layer stack.** Every output passes the layers in order, cheapest
first. The matrix decides which layers are *active* for each mode; layer 1 always runs.

| Layer | What it is | Catches | Cost |
|---|---|---|---|
| 1. Rules in code | Deterministic checks: schema, ranges, hard limits, denylist of banned actions, idempotency, rate limit, PII redaction, heartbeat | The knowably-wrong, and Silent failure | ~free, runs on 100% |
| 2. Confidence threshold | An independent score per output; below τ → escalate or refuse | The uncertain | cheap; needs calibration |
| 3. Human sign-off | Route to a named person before the action commits | The costly-and-uncertain | expensive; ration it |

Layer 2's score must be independent of the reasoning model — a judge, or a historical
pass-rate lookup — matching the architecture rule that component 4 cannot be component 3b.
A model grading its own output is not a guardrail. State a **fail-mode** for each mode:
fail-safe (block / hold / refuse on timeout or missing signal) for Catastrophic and High;
fail-open (ship and log) is permitted only for Low.

**Step 4 — derive the threshold.** τ is the confidence score above which output
auto-proceeds. It is derived, not chosen:

> Set τ = the lowest score whose calibration bucket (and every bucket above it) shows a
> measured failure rate ≤ acceptable_rate(mode).

You need a calibration curve: bucket golden-case outputs by score, measure the actual pass
rate in each bucket. Without that curve, τ is `[Hypothesis]`; the safe interim is to route
the whole mode to human sign-off until the curve exists. A raw "the model says 90%" is
opinion (0.1 on the ladder) — the Confidently-wrong mode is exactly the model being sure
and wrong, so its self-report cannot be the guard against it.

**Step 5 — the sign-off trigger.** For every path that reaches human sign-off, fill a row:
trigger (which mode × which confidence band), reviewer (one named role), SLA (how long they
have), fail-mode (what happens on timeout). Every Catastrophic and High mode must have a
trigger here, or the kill line fails.

**Step 6 — cost the stack.** flagged_volume × review_minutes × loaded_rate is a real line
in cost-per-outcome. If the guardrail blows the budget from `eval-first-spec`, the honest
outcomes are: tighten what gets flagged, lower the autonomy so fewer actions need guarding,
or concede the wedge is not economic. Do not silently widen τ to make review affordable —
that un-derives Step 4.

**Step 7 — the kill line.** Run the self-check at the foot of [template.md](template.md).

## Evidence standard

Money moved 1.0 → behaviour observed 0.7 → artefact shown 0.5 → verbal commitment 0.3 →
opinion 0.1. Here the ladder scores the two numbers the whole spec rests on: the
**cost-of-error** and the **volume** per mode, and the **confidence calibration**. A
cost-of-error argued from opinion ("that would be really bad", 0.1) cannot size a
guardrail; it needs an artefact or behaviour — a real incident, a regulation, a remediation
invoice, a measured event rate. The confidence threshold is `[Fact]` only when a
calibration curve backs it (behaviour, 0.7); a felt 0.8 is opinion and is flagged owed.
Tag every cost, rate, volume, and threshold `[Fact]` / `[Assumption]` / `[Hypothesis]`. A
guardrail spec is done when every Catastrophic/High mode has a code block or a sign-off
trigger, τ is derived not felt, and the stack's cost is written back into cost-per-outcome.

## Gotchas

- **The uniform stack.** "Input validation + output validation + a human reviews it" applied
  identically to every output. It wastes sign-off on the Low-cost high-volume modes — so in
  practice that review silently gets skipped — and under-guards the Catastrophic case, where a
  schema check is not a sign-off. The matrix exists to break this habit; a grid with one class
  in every cell is the auto-fail.
- **Uncalibrated confidence.** Treating the model's self-reported certainty as the threshold.
  LLM self-confidence is not calibrated and is highest on the Confidently-wrong mode. A real τ
  needs an independent score measured against golden-case outcomes. No calibration curve → no
  threshold, only a number; route to human until the curve exists.
- **Sign-off that fails open.** The human is named as the guard, but on timeout the action ships
  anyway "so we don't block the user". On a Catastrophic or High mode that turns the guard into
  theatre. High cost fails safe — it holds — or it is not a guard.
- **Rubber-stamp by over-flagging.** Routing everything to a person does not make it safe; a
  reviewer facing 500 approvals a shift approves by reflex, which is the L2 rubber-stamp failure
  from `eval-first-spec`. Over-flagging destroys the guard as surely as under-flagging. Size the
  flagged volume to what one reviewer can actually attend to within the SLA.

## Examples

[examples/sample.md](examples/sample.md) — Barrier Intelligence's gas-safety alerting built
as a guardrail spec: the counter-intuitive finding that for a safety product the risky
auto-action is *suppression*, not alerting; a Miss placed Catastrophic × low-true-volume with
a deterministic LEL hard-block that no confidence score may gate; a False alarm placed High ×
high-volume where a derived τ suppresses sensor noise but a code rule forbids auto-dismissing
any soft anomaly in a manned zone; and a human sign-off, fail-safe, that a shift safety
engineer must give before any potential hazard is permanently closed.

## Related skills

- `eval-first-spec` (07, sibling) — derives the acceptable failure rate per mode, the autonomy
  level, and the cost-of-one-failure. This skill consumes all three; it does not re-derive them.
  Its golden cases are the calibration set that Step 4's threshold is measured against.
- `compound-system-architecture` (07, sibling) — names component 4 (validate & guardrails) and
  the rule that it must be independent of the reasoning model. This skill is the depth build of
  that one component. The architecture says a guard sits there; this says what it is.
- `refine-flywheel` (08) — promotes autonomy as an eval result. When accuracy has been earned and
  a guard layer can come off, that decision is the flywheel's, gated by re-running the eval set —
  not this skill's, and never by feel.
- `pilot-six-term-sheet` (07, sibling) — the commercial contract. Guardrail cost lands in this
  skill's cost-per-outcome, which the term sheet prices against; keep the boundary.
- Supersedes nothing. New skill; no prior guardrail spec exists in the pack to replace.
