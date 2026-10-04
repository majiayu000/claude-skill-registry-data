---
name: structure-discovery
shapes: [structure-discovery]
description: >
  Find the hidden pattern that organizes the mess. Use for "these look related but
  we can't say how", classification with suspicious gaps, reverse-engineering an
  undocumented system or format, "is there a symmetry we're not using?", scale-free
  or fat-tailed data, or generating conjectures from computed special cases.
---

# Structure Discovery

**Problem shape:** many observations, one suspected hidden regularity — an
unnamed axis, an unexploited symmetry, an undeciphered format, a topology
forced by constraints. The move: make the structure explicit and falsifiable,
then let it predict something you haven't seen yet.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [mendeleev](../../agents/genius/mendeleev.md) | many known items with a suspected hidden ordering — tabulate, leave explicit gaps, predict the gaps' properties |
| [noether](../../agents/genius/noether.md) | hidden regularity via invariance — find the symmetry group, quotient the search space, treat symmetry breaking as signal |
| [kekule](../../agents/genius/kekule.md) | components with known connection constraints, unknown structure — count the bonds and let the count force the shape |
| [vonneumann](../../agents/genius/vonneumann.md) | the problem looks isomorphic to a solved one in another field — find the mapping, import the solution |
| [rejewski](../../agents/genius/rejewski.md) | black-box system to reconstruct from outputs — structural invariants, exploit the procedure around the algorithm |
| [champollion](../../agents/genius/champollion.md) | undeciphered format with a partial parallel (bilingual) sample — anchor known fragments and propagate |
| [ventris](../../agents/genius/ventris.md) | no parallel text exists — grid the internal regularities, then test by prediction |
| [poincare](../../agents/genius/poincare.md) | qualitative behavior before quantitative solution — topological equivalence, structural stability |
| [mandelbrot](../../agents/genius/mandelbrot.md) | pattern repeats across scales; distribution has fat tails being treated as mild randomness |
| [ramanujan](../../agents/genius/ramanujan.md) | need many candidate patterns fast — compute 50+ special cases, conjecture, then **mandatory prover handoff** (never ship unverified) |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. A discovered structure must predict something checkable
   — a gap's properties, a next case, an invariant — or it is decoration.
4. ramanujan output is conjecture by definition: chain a prover
   (`tools/genius-invoker.sh compose ramanujan lamport -- "<problem>"` or
   hand to dijkstra) before anything ships.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The pattern is wanted for a narrative, with no willingness to test its
  predictions.
- The data is too sparse to distinguish structure from apophenia — say so.
