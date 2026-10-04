---
name: representation-and-possibility
shapes: [representation-and-possibility]
description: >
  When the notation is the obstacle and the option space was never enumerated.
  Use when the current vocabulary hides the solution, when a system claims to be
  exhaustive but nobody checked whether the space is searchable, when a forecast
  is too narrow because no one pushed the principle to its limit, or when you
  need the answer now and the proof afterwards.
---

# Representation and Possibility

**Problem shape:** the difficulty is not in solving but in *stating* — the
symbols, categories, or enumerated options in play are the constraint. Symptoms:
a problem that becomes trivial once renamed, a "complete" catalog nobody has
bounded, a roadmap whose option space stops at the adjacent, a result that is
intuitively obvious and formally unestablished.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [euler](../../agents/genius/euler.md) | the current notation or vocabulary obscures the solution — redesign the notation as infrastructure, delete what the abstraction does not need, enumerate exhaustively once the symbols carry their weight |
| [borges](../../agents/genius/borges.md) | a system claims completeness or exhaustiveness — audit whether the space is actually searchable, keep the map distinct from the territory, detect the self-reference that makes the catalog contain itself |
| [lem](../../agents/genius/lem.md) | the question is "what could this become?" and the standard forecast is too narrow — explore the possibility space systematically, push each principle to its logical extreme to see what breaks or emerges |
| [archimedes](../../agents/genius/archimedes.md) | you need the result before you can prove it — find it by physical intuition, analogy, or simulation, then prove it rigorously by a *second, independent* method (the two-stage discipline; stage one alone is not a result) |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. When archimedes is used, the heuristic stage and the proof
   stage are reported separately and labeled — an unproven heuristic presented
   as a result is the failure mode this shape exists to prevent.
4. Typical chain: euler renames until the structure is visible → borges bounds
   the space the new notation opens → lem pushes the surviving options to their
   extremes. Run via
   `tools/genius-invoker.sh compose euler borges lem -- "<problem>"`.
5. If no shape above matches, do not force a genius — use a standard team agent
   (INDEX.md routing rule).

## Refuse when

- The notation is fine and the problem is simply unsolved — renaming as
  displacement activity.
- The possibility exploration is asked to produce a *prediction* with a
  confidence attached: this shape maps what is possible, it does not forecast
  what is likely. Route probability to `estimation` or `decision-bias-check`.
- Only the heuristic stage is wanted and the proof stage is explicitly waived
  on a claim that will ship as established.
