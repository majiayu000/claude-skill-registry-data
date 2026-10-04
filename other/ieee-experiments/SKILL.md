---
name: ieee-experiments
description: >-
  Design and audit IEEE communications simulation and numerical-results sections for JSAC, TWC,
  TCOM, WCL, and CL. Covers benchmark schemes, Monte-Carlo protocol, BER/SER/outage/rate/EE
  metrics, SNR/antenna/user sweeps, analysis-vs-simulation validation, convergence and
  complexity, learning-based evaluation, ISAC rate-CRB/detection tradeoffs, robustness, and
  empirical/ray-tracing/testbed evidence. Use for planning or checking results: benchmark
  selection, simulation setup, Monte-Carlo validation, neural-network evaluation, CRB/ISAC
  tradeoffs, fairness boundaries, or reviewer-risk audits.
---

# IEEE Communications — Simulation and Numerical Results

Use this skill to make the evidence earn the claims in a PHY/network communications paper. Every
contribution in the Introduction must have a result that could falsify it; for analytical papers,
every derived expression must be validated by Monte-Carlo simulation; every figure answers one
question.

## Core stance

- **Results test claims, not showcase wins.** Map each contribution to the curve/table that
  supports it before running anything.
- **Validate analysis with simulation.** If the paper derives a closed-form expression (outage,
  BER, rate, coverage), Monte-Carlo markers must sit on the analytical curve — that agreement *is*
  the proof the derivation is correct. Note asymptotic slope (diversity order) where claimed.
- **Fairness is declared, not assumed.** State the comparison's boundary: same power budget, same
  CSI assumption, same bandwidth/antennas, same channel realizations across schemes.
- **No fabrication.** Do not invent curves, gains, benchmark numbers, or "matching" between theory
  and simulation. Use `[PLACEHOLDER]` for results not yet run and list what the user must produce.

## When to open extra files

| File | Open when |
|---|---|
| [references/experiment-design.md](references/experiment-design.md) | Choosing the system/channel setup, benchmark schemes, communications metrics, Monte-Carlo protocol, convergence/complexity, learning-based evaluation (NMSE/generalization/inference cost), ISAC dual metrics (CRB/detection + rate–CRB tradeoff), and robustness (imperfect CSI/hardware) tests |
| [references/tables-and-claims.md](references/tables-and-claims.md) | Structuring result tables, mapping each table/figure to a claim, table/prose division of labour, and IEEE table conventions |

## The evidence ladder (design in this order)

```
1. Validation            do Monte-Carlo markers match the analysis (curves), and is the
                         asymptotic slope (diversity order / DoF) as claimed?  [analytical papers]
2. Performance           does the scheme beat conventional and prior-art schemes on the key
                         metric (sum rate, BER, outage, EE, ...)?
3. Operating regimes     behaviour swept across SNR, #antennas, #users, power, blocklength, K-factor
4. Design analysis       is each design choice necessary (compare reduced "w/o" variants)?
5. Convergence & cost    does the iterative algorithm converge; complexity order vs benchmarks
6. Robustness            graceful degradation under imperfect CSI, hardware impairments, mismatch
```

Not every paper needs all six. An optimization paper centres on rungs 2–5; an analytical paper
must clear rung 1 first. A method paper that stops at rung 2 is usually under-evaluated; a letter
(WCL/CL) may show only rungs 1–3 for space — see the `ieee-letter` skill.

## Workflow

1. **List the contributions** (from the Introduction). For each, write the single result that
   would convince a skeptic and the one that could falsify it.
2. **Choose benchmark schemes** across categories (see experiment-design.md): proposed,
   conventional/heuristic, prior-art (same setting), an upper bound (relaxed/genie/perfect-CSI),
   and a lower bound (random/equal-power/no-optimization). Label each category. For a learning-based
   paper, always include the **model-based method it replaces** (LS/MMSE/WMMSE) and, for deep
   unfolding, the parent iterative algorithm at full and at matched `L` iterations.
3. **Choose metrics** that match the claim — not just the headline. Add a tail/distributional
   metric (outage, CDF, worst-user rate) for stability claims, and a cost metric (complexity
   order, runtime, energy efficiency) for efficiency claims.
4. **Plan parameter sweeps:** which quantity on the x-axis (usually SNR/transmit power), what is
   swept as curve families (#antennas, #users, K-factor), and the regime that exposes the claim.
5. **Set the Monte-Carlo protocol:** number of independent channel realizations, what is averaged,
   confidence/smoothness, and **the same channel seeds across all schemes** for paired comparison.
6. **Plan analysis-vs-simulation validation** (analytical papers): which expressions get a
   simulation overlay, and the asymptotic check.
7. **Plan convergence/complexity** for any iterative algorithm (SCA/ADMM/AO/fractional
   programming): objective-vs-iteration curve plus per-iteration complexity order.
8. **Declare the fairness boundary** in words (see below).
9. **Map every planned figure/table to one claim;** drop anything that answers no question.
10. **Return** the design as a claim→result→metric→figure matrix, plus a gap list.

## Declare the fairness boundary

When no standard public benchmark exactly matches the setting:

> Since no existing scheme fully matches the considered setup, representative implementable schemes
> are adopted under the same power budget, CSI assumption, and bandwidth.

Then classify each scheme (proposed / conventional / prior-art / upper bound / lower bound) and
state the shared resource constraint. This single move pre-empts the most common reviewer
objection ("the comparison is unfair").

## Output format

1. `Claim–result matrix:` `Contribution → Result (curve/table) → Metric(s) → Fig/Table → Status`.
2. `Benchmark schemes:` grouped by category, each labelled with its role and shared constraint.
3. `Simulation setup:` channel/system model, swept parameters, Monte-Carlo realizations.
4. `Validation plan:` which expressions get a simulation overlay; asymptotic-slope check.
5. `Convergence/complexity:` iteration behaviour + complexity order vs benchmarks.
6. `Gaps:` curves or numbers the user still needs to produce.
