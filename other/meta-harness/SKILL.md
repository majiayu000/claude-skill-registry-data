---
name: meta-harness
description: >-
  Run a Meta-Harness-style optimization loop NATIVELY — automatically search over the
  scaffolding around a FIXED base model (memory, retrieval, context construction, prompt
  templates, summarization, tool-selection logic) by proposing candidate variants, scoring
  each on a cheap deterministic eval, and keeping a Pareto frontier of quality vs cost — using
  native Agent / Workflow / loop tools instead of a standalone Python harness. Use this whenever
  the user wants to optimize, evolve, tune, distill, or search over a harness, scaffold, prompt
  system, memory or retrieval policy, context-assembly code, or summarizer while keeping the
  model fixed; whenever they mention Meta-Harness, harness optimization, scaffold evolution,
  automatic prompt/memory optimization, an evolutionary or Pareto search over candidate
  implementations, or "make the harness/agent better without retraining"; and whenever the gain
  must come from the code AROUND the model rather than the model weights. Reproduces the
  Meta-Harness paper's method natively, with no claude_wrapper.py and no metered solver API.
---

# Meta-Harness (native)

## What this is

**Meta-Harness optimizes the *harness*, not the model.** The harness is the code around a
fixed base model that decides what to store, retrieve, compress, and show while the model
works. You hold the model frozen and search over that scaffolding: propose candidate variants,
score each on a cheap deterministic eval, keep a **Pareto frontier** (quality up, cost down),
and iterate. The proposer is an LLM agent writing code; the inner loop is a cheap scorer.

The Stanford repo (`stanford-iris-lab/meta-harness`) ships a Python driver —
`claude_wrapper.py` (~720 lines) + `meta_harness.py` (~540 lines) — that **reimplements an
agent runtime to drive a headless Claude**: spawn a session, parse stream-json, track tool
calls, log everything, loop. **You already are that runtime.** So you run the same loop with
native tools (`Agent`, `Workflow`, `/loop`) and keep only the irreducible domain logic — a $0
scorer. The orchestration was never the hard part; your harness provides it.

This skill is the **method**, reusable for any harness-optimization task. A fully worked
example (optimizing proteus's campaign-memory summarizer) lives at `~/mh-proteus/` and is
walked through in `references/proteus-example.md`.

## When to use this

Strong fit when **several** of these hold (full criteria in `references/method.md`):

- The base model is **fixed** and the opportunity is better retrieval / memory / context /
  prompting / tool scaffolding. (This is the whole premise — if the gain must come from the
  model weights, this is the *wrong* tool: do RL/fine-tuning instead.)
- There are **repeated episodes / tasks**, not a one-off.
- There is a **cheap, deterministic eval** with a real success signal — or you can build one.
- The search set is **large enough to expose failure modes, small enough to iterate**.
- There are **recurring error patterns** a harness could fix systematically.

Poor fit: no stable eval loop, or purely subjective quality with no measurable criterion.

## The loop (mental model)

```
seed frontier with the incumbent harness (the thing to beat)
repeat until budget/convergence:
    PROPOSE   k candidate harness variants   (proposer agents write code)
    VALIDATE  each imports / type-checks      (cheap reject of broken candidates)
    SCORE     each on the held-out-protected eval set   ($0 deterministic scorer)
    FRONTIER  Pareto-merge (quality up, cost down), floor-respecting
FINAL: score the frontier once on the untouched TEST split
```

The proposer is the mutation+crossover operator. The frontier is the persistent search memory.
The held-out test split is touched exactly once, at the end — never during the search.

## The five things YOU supply (everything else is native)

The orchestration is native; the **domain** is yours. Build these five — templates in `assets/`,
how-to in `references/building-blocks.md`:

1. **Candidate interface** — one clean, swappable boundary (an ABC / Protocol). A candidate is a
   drop-in implementation. If your harness logic is tangled into one big function, extract the
   boundary first. → `assets/candidate_base-template.py`
2. **A $0 deterministic scorer + rubric** — the inner loop. It **must vary with the candidate**
   (see the frozen-replay trap below) and run with no LLM / no network so you can call it
   hundreds of times for free. → `assets/scorer-template.py`
3. **An eval corpus with a held-out split** — the tasks/records candidates are graded on, split
   so the test set shares no leaky structure with the search set.
4. **A proposer prior** — a short mini-SKILL the proposer agents load that steers them toward
   *mechanism-level* changes (not constant-tuning) and enforces anti-leakage.
   → `assets/proposer-prior-template.md`
5. **A frontier + run log** — the state carried across iterations (a JSON/JSONL pair, or just
   workflow variables). → `scripts/pareto.py` computes the frontier deterministically.

## Non-negotiable guardrails — read before you run

These are where naive harness searches silently fail. Full treatment in `references/method.md`.

- **The frozen-replay defect (the #1 trap).** If your eval *replays cached outputs* (a recorded
  run, a frozen trace), then a scaffolding candidate **cannot change the recorded result** —
  only the cost axis moves. A naive Pareto search then "wins" by emptying the context while the
  frozen quality score never drops, producing a confident, meaningless frontier. **Fix:** grade
  a quantity that genuinely varies with the candidate (retrieval relevance, compression
  fidelity, decision *counterfactuals*), and/or run quality as a **one-sided do-no-harm floor**
  rather than a maximize axis.
- **Held-out discipline.** The proposer must see only the search-set results and the frontier —
  never the test split. Score test once, at the end.
- **Anti-Goodhart floor.** The proposer is the most capable optimizer you have; it *will* exploit
  a soft metric. Put a hard floor on quality (and fix any known reward bugs) so it cannot win by
  degrading the thing you actually care about.
- **Anti-leakage.** Forbid candidates from hardcoding any value from the eval set. Candidates
  must generalize to unseen tasks.

## How to run it natively — pick a mode

| Mode | Use when | How |
|---|---|---|
| **Workflow** (default) | a real search; want parallel proposers, journaled + resumable | `assets/workflow-template.js` via the `Workflow` tool |
| **skill + `/loop`** | leanest; you act as the proposer yourself, serially | a mini-skill body looped with `/loop` |
| **Team** | rarely — durable, long-lived proposer/scorer/curator roles | `TeamCreate` + tasks + messaging |

Default to **Workflow** — it is the closest 1:1 to the Python harness and the best for an actual
search. The mapping from each Meta-Harness piece to its native equivalent, and full mode details,
are in `references/native-execution.md`.

## Procedure

1. **Frame the search.** Name the fixed model, the harness surface to optimize, the eval, the
   two Pareto axes (quality, cost), and the budget. Confirm fit against `references/method.md`.
   If you cannot name a cheap eval that *varies with the candidate*, stop and build one first.
2. **Build the five blocks** from `assets/` templates (or reuse an existing scaffold like
   `~/mh-proteus/`). Validate the scorer runs at $0 on the incumbent before going further.
3. **Baseline.** Score the incumbent harness + a trivial anchor; seed the frontier.
4. **Choose a mode** (default Workflow). Copy `assets/workflow-template.js`, set the working
   dir, candidate count `k`, rounds/budget, and the floor.
5. **Run the search.** Proposers write candidates; the $0 scorer ranks them; Pareto-merge each
   round. Watch the frontier move (quality held at/above floor, cost dropping).
6. **Inspect the frontier**, not just the best point — the cost/quality tradeoff curve is the
   product.
7. **Promote with re-validation.** A frontier winner is a *proposal*. Before it ships, score it
   once on the untouched test split, and (if the search used a proxy eval) validate the proxy
   ranking against the real metric. Never let an unvalidated candidate become the new incumbent.

## Files in this skill

- `references/method.md` — theory, full fit criteria, the frozen-replay defect, all guardrails,
  how to choose the objective. Read when framing a new search or unsure about fit.
- `references/native-execution.md` — the Meta-Harness→native mapping table and all three
  execution modes in depth (Workflow / loop / Team), including how scoring runs inside a Workflow.
- `references/building-blocks.md` — how to build each of the five blocks, with worked patterns.
- `references/proteus-example.md` — the end-to-end worked example at `~/mh-proteus/`.
- `assets/workflow-template.js` — the native search loop (the default mode). Parameterized.
- `assets/scorer-template.py`, `assets/candidate_base-template.py`,
  `assets/proposer-prior-template.md` — templates for the domain blocks you supply.
- `scripts/pareto.py` — deterministic Pareto-frontier computation over a results JSONL.
