---
name: ieee-methods
description: >-
  Write or audit IEEE communications Methods/System Model/Algorithm details for reproducibility:
  notation tables, simulation-parameter tables, solver settings, random seeds, channel/model
  assumptions, algorithm boxes, convergence statements, and complexity analysis. Use this when the
  user asks for "methods", "reproducibility checklist", "notation table", "complexity analysis",
  "algorithm box", "simulation parameters table", "复现性", "符号表", "复杂度", or wants a JSAC/TWC/TCOM/WCL/CL
  methods section checked for enough detail to reproduce. For drafting the broader paper argument
  use ieee-writing; for deciding which experiments to run use ieee-experiments.
---

# IEEE Methods and Reproducibility

Use this skill to turn a method description into a reproducible IEEE communications methods block.
It sits between `ieee-writing` and `ieee-experiments`: writing explains the idea; this skill makes
the implementation, notation, and complexity auditable.

## Core stance

- **Reproducible beats impressive.** A reviewer should be able to rebuild the main curve from the
  system model, parameter table, algorithm box, and solver/training details.
- **Define every symbol at first use.** If a variable appears in an equation, it needs a domain,
  dimension, unit when relevant, and role.
- **Separate assumptions from simplifications.** Assumptions define the studied regime;
  simplifications need a boundary or robustness check.
- **Complexity claims need variables.** State big-O in terms of antennas/users/subcarriers/RIS
  elements/iterations, not a vague "low complexity".
- **No hidden implementation.** Solver version, stopping tolerance, Monte-Carlo realization count,
  train/test split, and randomization policy are methods content, not footnotes.

## When to open extra files

| File | Open when |
|---|---|
| [references/reproducibility-checklist.md](references/reproducibility-checklist.md) | Auditing or writing system/channel setup, simulation-parameter tables, randomization, solvers, training data, hardware/testbed/ray-tracing settings, or reproducibility statements |
| [references/notation-and-complexity.md](references/notation-and-complexity.md) | Building notation tables, algorithm boxes, convergence statements, or big-O complexity analysis |

Use `ieee-writing` for full Section II/III prose, `ieee-experiments` for benchmark/metric design,
`ieee-figure` for result plots, and `ieee-latex` for IEEEtran formatting and compilation.

## Workflow

1. **Identify the method object:** system model, problem formulation, algorithm, analysis, neural
   network, simulation protocol, or testbed/ray-tracing setup.
2. **Extract the reproducibility variables:** topology, channel, signal model, optimization
   variables, metrics, solver/training setup, and random quantities.
3. **Build a notation table** for nontrivial papers: symbol, size/domain, meaning, first equation.
4. **Write the method in signal flow order:** input -> transformation/channel/optimization ->
   output -> metric. Avoid listing modules without explaining information flow.
5. **Add a parameter table** for experiments and shared settings. Put repeated constants there,
   not scattered through prose.
6. **For algorithms, add an algorithm box** with initialization, loop, stopping criterion, and
   returned variables. Label exact, approximate, and learned steps.
7. **State convergence and complexity honestly:** KKT/stationary/global only when proved; complexity
   per iteration plus total iteration count when applicable.
8. **Flag gaps** that prevent reproduction rather than filling them by guess.

## Output format

1. `Methods text:` polished IEEE prose or LaTeX for the requested method block.
2. `Reproducibility checklist:` `Item -> Present / missing / needs confirmation`.
3. `Notation and complexity:` notation table and complexity statement when relevant.
4. `Assumptions and boundaries:` CSI/channel/scope simplifications that need support.
5. `Missing inputs:` exact numbers, solver settings, data splits, or hardware details the author
   must provide.
