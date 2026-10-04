---
name: premortem
description: "Use before committing to a heavy or irreversible plan — imagine it's 6 months later and this failed; enumerate why, score each mode, derive early-warning signals and preventive guardrails."
domain: quality
model_tier: high
workspaces:
  - engineering
packs:
  - analysis-workbench
trust:
  level: professional
  confidence: medium
install:
  default: false
  removable: true
---

# premortem

> Forward-looking imagined-failure analysis. Sibling of
> [`blameless-post-mortem`](../blameless-post-mortem/SKILL.md) (which
> analyses what actually went wrong after the fact) and
> [`risk-officer`](../risk-officer/SKILL.md) (which scores pre-commit
> risks per likelihood × impact). This skill adds the prospective frame:
> "Assume total failure at horizon H — reconstruct why."

## When to use

Before committing to a plan that is:

- Heavy to execute (multi-sprint, multi-team, or high coordination cost), or
- Irreversible or costly to reverse (schema migration, public API change,
  infrastructure restructure, major dependency swap, architecture decision).

Trigger phrasing: "premortem this", "what if this fails?", "imagine it's 6
months later and this shipped badly", "help me stress-test this plan".

Do NOT use when:

- The failure is already evidenced — root cause is known → use
  [`systematic-debugging`](../systematic-debugging/SKILL.md).
- Analysing something that already failed in the past →
  use [`blameless-post-mortem`](../blameless-post-mortem/SKILL.md).
- The plan is trivial or fully reversible — overhead exceeds value.

## Procedure

### 1. State the plan and set the horizon

Summarise the plan in one sentence: *"We are doing X for outcome Y, touching
Z."* Set the prospective-failure frame explicitly: *"Assume total failure at
horizon H (e.g. 6 months post-launch). What went wrong?"*

If the plan cannot be summarised in one sentence, it is not reviewable — stop
and ask for scope clarification.

### 2. Enumerate failure stories

Generate failure scenarios across multiple angles (people, process, technical,
external, timing). Each scenario is a short narrative in past tense: *"We
shipped, but adoption collapsed because …"*

For each scenario:

- Invoke [`adversarial-review`](../adversarial-review/SKILL.md) to attack the
  plan's assumptions and surface hidden coupling or over-engineering.
- Invoke [`risk-officer`](../risk-officer/SKILL.md) to assign L × I (likelihood
  × impact) scores to each failure mode.

Do NOT re-implement L × I scoring inline — delegate to `risk-officer`.

### 3. Derive early-warning signals and preventive guardrails

For each top failure mode (sorted by L × I from `risk-officer`):

1. **Early-warning signal** — what would you observe *first* if this failure
   mode were activating? Name a concrete, observable indicator (metric, alert,
   user behaviour, team signal). This is the load-bearing output.
2. **Preventive guardrail** — one specific change to the plan, process, or
   rollout strategy that reduces the likelihood of this failure mode. Keep it
   executable; flag as `accept` if no practical guardrail exists.

### 3b. Compress into the four-part failure register

When the pre-mortem accompanies a plan artefact (a roadmap, an ADR, a design
doc), compress the analysis into the **four-part failure register** — the
fixed, comparable shape the roadmap template's optional `## Pre-mortem`
section consumes:

1. **Three most probable causes of death, ranked** — one paragraph each,
   naming the concrete mechanism by which the plan most plausibly dies.
   Mechanisms, not topics: "the gate's two inputs are unmeasurable from this
   corpus" is a cause; "measurement risk" is not.
2. **One untested hidden dependency** — the assumption the plan relies on but
   never tests.
3. **One modification that makes failure survivable** — a concrete plan change
   that converts a fatal outcome into a recoverable one.
4. **One tripwire metric with a horizon** — a measurable signal plus a
   threshold and deadline that says early that cause #1 is materializing.

The register was validated blind against this repo's own closed nulls
(3 of 4 registers named the actual failure cause at rank 1 —
`agents/evidence/analysis/premortem-blind-retro-validation.md`). The hits were
all failures of *measurability*; the miss was a mechanism that worked but
added nothing — weight the register toward "can this experiment answer its
question" and state redundancy risks explicitly.

### 4. Optional memory write-back

If the analysis surfaces a pattern worth preserving for future decisions:

1. Run a dedup pre-check: call `retrieve()` over the same key-space (plan type,
   affected paths, decision area). If a match is found, propose a
   `frequency`/`supersedes` update to the existing entry rather than a new one.
2. Draft a `historical-patterns` candidate and send it to `/memory propose` per
   [`docs/contracts/analysis-memory-loop.md`](../../docs/contracts/analysis-memory-loop.md).
3. Never auto-promote. Human action drives `/memory promote`.

## Output format

1. **Ranked prospective failure modes** — L × I ordered list (from `risk-officer`)
2. **Early-warning signal per failure mode** — concrete, observable indicator
3. **Preventive guardrails** — one per failure mode (or `accept` with rationale)
4. **Four-part failure register** (when accompanying a plan artefact) — three
   ranked causes of death · one untested hidden dependency · one
   survivable-failure modification · one tripwire metric with a horizon
   (step 3b; feeds the roadmap template's optional `## Pre-mortem` section)
5. **Optional memory candidate** — drafted to `/memory propose` if the pattern
   clears the admission gate (≥ 2 distinct file paths OR ≥ 3 future decisions)

## Do NOT

- Do NOT invent strawman failure modes — each must be grounded in the actual
  plan's structure, assumptions, or dependencies.
- Do NOT re-implement L × I scoring — invoke `risk-officer`; don't duplicate
  its five-lens framework inline.
- Do NOT present speculation as evidence — premortem is imaginative framing,
  not a prediction; label scenarios as prospective.
- Do NOT auto-promote memory candidates — `/memory propose` is the intake;
  `/memory promote` requires explicit human action and passes
  `check_memory_proposal.ts`.

## Gotchas

- Premortem is **forward-looking** — it imagines a future failure to improve
  the present plan. `blameless-post-mortem` is backward-looking — it analyses
  a past failure. Do not conflate them.
- The **early-warning signal** is the load-bearing output, not the doom list.
  A failure mode without a detectable signal cannot be caught in time — flag
  it explicitly.
- Failure stories in past tense ("we shipped, and then X happened") are more
  generative than abstract risk statements. Force the past-tense narrative.

## See also

- [`risk-officer`](../risk-officer/SKILL.md) — L × I scoring; invoked in
  Step 2. Not duplicated here.
- [`adversarial-review`](../adversarial-review/SKILL.md) — assumption attack;
  invoked in Step 2. Not duplicated here.
- [`blameless-post-mortem`](../blameless-post-mortem/SKILL.md) — post-hoc
  analysis of an actual failure; backward-looking counterpart to this skill.
- Invocation surfaces: `/analyze premortem`, `feature:plan`, `roadmap-create`
  (surface the premortem step as optional before committing to a plan).
