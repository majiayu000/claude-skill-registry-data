---
name: ieee-trans-experiment-design
description: Deep-read an IEEE Transactions power-electronics paper, audit its claims against source evidence, and reverse-design reproducible, falsifiable, progressively degradable analytical, offline-simulation, controller/software-in-the-loop, HIL, low-power prototype, rated-hardware, or extension experiments. Use when a user asks to infer experiments from a paper, reproduce an experiment design, validate or falsify paper claims, design analytical/simulation/hardware validation, identify experimental gaps, or challenge claims such as full-range ZVS or global optimality. Do not use for prose polishing, figure drawing alone, ordinary literature search, statistical analysis of an already-defined dataset alone, or direct execution of high-voltage/high-power hardware tests.
---

# IEEE Transactions Experiment Design

Audit what the paper actually establishes, then design the smallest experiment chain that could reproduce, bound, or falsify its claims. Produce a plan, never invented results.

## Inputs

- Accept the paper PDF as the minimum input.
- Prefer the PDF plus supplementary material, code, models, raw data, and component or instrument datasheets.
- Record every supplied asset and its source identity. Mark absent or unreadable assets as `missing` or `unknown`; never assume they exist.
- Follow the user's language by default. Support Chinese, English, or bilingual output while preserving IEEE terminology, symbols, variables, units, subscripts, and abbreviations.

Read [workflow.md](references/workflow.md) for intake degradation and the fixed workflow. Read [evidence-policy.md](references/evidence-policy.md) before assigning evidence states or decision criteria.

## Required workflow

Execute these stages in order:

1. Source identity
2. Claim extraction
3. Evidence mapping
4. Technical audit
5. Experiment tiering
6. Support criteria
7. Falsification criteria
8. Missing assets
9. Safety gate
10. Output validation

Keep claim IDs stable. For every claim, separate the paper's observations from derived quantities, recommendations, and unknowns. Design at least one falsification path for every major testable claim; otherwise record why it is not testable from the available assets.

## Evidence and execution states

Use only:

- `SOURCE_FACT`: explicitly reported by the source and anchored.
- `DERIVED`: calculated from anchored inputs with a reproducible derivation.
- `RECOMMENDATION`: a proposed test, setting, baseline, or action.
- `UNKNOWN`: not confirmable from current materials.

Keep the overall execution status `NOT_EXECUTED` unless actual run logs and outputs are supplied and verified. A valid plan is not an executed experiment. If no runnable model exists, downgrade to modeling requirements and an experiment specification; do not claim simulation.

## Experiment layers

Select only the layers required by the claim and available assets:

- analytical
- offline simulation
- controller/software-in-the-loop
- HIL
- low-power prototype
- rated hardware prototype
- extension experiment

Read [experiment-tiers.md](references/experiment-tiers.md) for entry gates, evidence limits, and fallback paths. Read [electrical-engineering-checks.md](references/electrical-engineering-checks.md) for power-electronics-specific checks.

## Hard constraints

- Never invent instrument accuracy, bandwidth, sample rate, resolution, equipment rating, component rating, tolerance, pass threshold, or stop temperature.
- Never hide an unsourced numeric criterion in prose, procedures, asset names, or safety text.
- Never use a material failure limit directly as a test safety threshold.
- Never expand observations from selected figures or operating points into full-domain coverage.
- Never call a finite parameter scan globally optimal without an adequate convergence or globality argument.
- Never write `NOT_EXECUTED` work as verified, reproduced, simulated, or measured.
- Require laboratory SOP, qualified expert approval, verified ratings, protection, and emergency procedures before any high-voltage, high-power, energy-storage, grid-connected, or rotating-equipment experiment.
- Refuse direct hardware execution when these gates are not satisfied; provide a bounded plan or lower-risk layer instead.

## Output contract

Return, in this order:

1. Source identity
2. Claim-evidence table
3. Technical audit
4. Tiered experiment matrix
5. Experiment cards
6. Missing-assets register
7. Safety and expert-approval gates
8. Unknowns and limitations
9. Execution status
10. Recommended next action

Each experiment card must name target claim IDs, hypothesis, layer, required assets, variables, controls, disturbances, baselines, operating points, metrics, procedure, support criteria, falsification criteria, data outputs, reproducibility needs, safety gates, unknowns, and fallback. Express unsupported thresholds as `UNKNOWN — expert approval required`, not as numbers.

State explicitly:

- what the paper did;
- what is derived from the paper;
- what is recommended for future work;
- what cannot currently be confirmed.

## Validation

Before delivery:

- verify claim IDs and source anchors;
- verify all `SOURCE_FACT` items have anchors;
- verify criteria and safety values have allowed provenance;
- verify missing assets and fallback layers are explicit;
- verify hardware gates are closed unless authorization and SOP evidence exist;
- verify the output remains `NOT_EXECUTED` when no verified execution evidence exists.

When producing repository-compatible JSON candidates, reuse
[`validate_model_outputs.py`](../../scripts/validate_model_outputs.py); do not
add another validator unless a new deterministic failure mode cannot be
expressed there.

Read [rule-cards.yaml](references/rule-cards.yaml) only when applying or extending reusable rules. Preserve each rule's `classification`; never promote a single-paper rule to a TPEL norm.
