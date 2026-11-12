---
name: build-cge
description: "Builds a CGE model (static or recursive-dynamic, single- or multi-region) with benchmark replication, closures, elasticity sensitivity and welfare decomposition."
---
<!-- Generated from .claude/skills/build-cge/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /build-cge — Build CGE

**Category:** Build · **Primary agent:** `cge-modeling-specialist`

Builds a CGE model (static or recursive-dynamic, single- or multi-region) with benchmark replication, closures, elasticity sensitivity and welfare decomposition.

Arguments: whatever the user wrote after the command name.

## Purpose
Build a computable general equilibrium model that replicates its benchmark data exactly, solves reliably, and traces how a policy reallocates production, factors and income across sectors and households. The output is a documented model whose results can be decomposed and defended, with closures and elasticities shown to matter or not.

**Use it when** the question involves economy-wide reallocation through prices: tax and tariff reform, carbon pricing, subsidy reform, productivity shocks by sector, trade agreements with sectoral detail, structural change over decades.

**Do not use it when** fixed-coefficient multipliers suffice (`/build-io-sam`), when short-run dynamics with nominal rigidities are central (`/build-dsge`, `/build-semi-structural`), or when bilateral trade flows and gravity are the main focus (`/build-trade-model`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Approved model-spec
   - Balanced SAM or global database
   - Elasticity sources
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `cge-modeling-specialist` — primary agent; coordinates the work and integrates results
- `input-output-sam-specialist` — Builds input-output, supply-use and social accounting matrix frameworks
- `trade-policy-simulation-specialist` — Simulates trade policy with quantitative trade models
- `tax-benefit-microsimulation-specialist` — Builds tax-benefit microsimulation
- `carbon-pricing-emissions-specialist` — Analyzes carbon pricing and emissions policy

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Time | static, recursive-dynamic, forward-looking | Adjustment paths; investment behavior |
| Regions | single country, multi-region (global database) | Terms-of-trade effects; data needs |
| Production nests | CES value added and intermediates; energy nests; Leontief intermediates | Substitution possibilities |
| Trade | Armington with CET exports; small or large country | Import and export responses; terms of trade |
| Households | one or many groups from the SAM; LES or other demand systems | Distributional detail |
| Closures | savings–investment, government, external, factor markets, numeraire | Results can change sign across closures |
| GTAP route (multi-region) | GEMPACK with the standard GTAP model, GAMS (for example GTAPinGAMS) | Solution method, decompositions, license needs |

## Workflow
1. Agree the structure: regions, sectors, factors, production nests, trade treatment and closures
   - Map the policy question to the sectors, factors and households that must be separate
   - Write the closure rules and justify each for the horizon
2. Calibrate to the SAM; implement as a complementarity problem; replicate the benchmark exactly
   - Check SAM balance first (`/build-io-sam` if the SAM must be built)
   - Source every elasticity with its sector definition and horizon
   - For a GTAP model: keep the aggregation mapping, record the database version and license, keep the database out of git, and follow `.claude/rules/gempack-code.md` for GEMPACK
3. Test homogeneity, Walras' law and numeraire invariance
4. Run policy scenarios under at least two closures; run systematic sensitivity on key elasticities
   - Use quadrature or Monte Carlo over elasticity ranges; report the spread
5. Report sectoral, welfare (EV/CV) and, where possible, household effects; document the model for handover
   - Decompose welfare into allocative, terms-of-trade and endowment effects
   - Link to microsimulation for household detail (`/distributional-analysis`)
6. Register the model as a lego set (`/lego-map`): a baseplate plus bricks with declared studs (variables, units, timing) and stubs, so components can later be attached, detached or swapped

## Checkpoints with the user
- After the structure note: confirm sectors, households and closures
- After benchmark replication: confirm the elasticity table and its ranges
- After first scenarios: confirm the results are interpretable before sensitivity runs

## Common pitfalls
- Results driven by an unexamined closure
- Elasticities borrowed from different aggregations or horizons
- Reporting GDP as welfare
- Treating static results as an adjustment path
- Committing or sharing a licensed global database (GTAP)

## Output
`models/cge/<name>/ (+ model.lego.json)`

The folder holds the SAM, calibration scripts, model code, the replication test, scenario and sensitivity scripts, the elasticity table with sources, the results pack with welfare decomposition and the lego manifest. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Benchmark replicated to tolerance
- Closure and elasticity sensitivity reported
- Lego manifest passes `python tools/lego.py check`
- Homogeneity and Walras' law tests pass
- Welfare is reported as EV or CV with its decomposition

## Suggested next steps
- `/trade-policy-analysis`
- `/carbon-pricing-analysis`
- `/distributional-analysis`
- `/validate-model`
- `/lego-map`
