---
name: build-hank
description: "Builds a heterogeneous-agent (HANK) model with household block, sequence-space solution and distributional outputs."
argument-hint: "[model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /build-hank — Build HANK

**Category:** Build · **Primary agent:** `hank-specialist`

Builds a heterogeneous-agent (HANK) model with household block, sequence-space solution and distributional outputs.

Arguments: `$ARGUMENTS`

## Purpose
Build a heterogeneous-agent New Keynesian model: a household block with idiosyncratic income risk and borrowing constraints, solved for its stationary distribution and sequence-space Jacobians, embedded in general equilibrium with firms and policy. The output is a model that delivers both aggregate and distributional impulse responses, matches key micro moments, and passes market-clearing and aggregation checks.

**Use it when** the distribution of income, wealth or marginal propensities to consume matters for the question: monetary and fiscal transmission through heterogeneity, distributional effects of policy, precautionary saving, inequality dynamics.

**Do not use it when** a representative-agent model answers the question (`/build-dsge`) or when static distributional incidence is enough (`/distributional-analysis`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Approved model-spec with household heterogeneity
   - Micro data targets
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `hank-specialist` — primary agent; coordinates the work and integrates results
- `neural-solver-specialist` — Solves high-dimensional economic models with neural networks
- `inequality-distribution-specialist` — Analyzes inequality and distribution
- `numerical-methods-specialist` — Specializes in numerical methods

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Asset structure | one asset, two assets (liquid and illiquid) | MPCs and wealth distribution |
| Income process | AR(1), richer processes from micro data | Risk and precautionary saving |
| Nominal rigidities | sticky prices, sticky wages | Transmission and income incidence |
| Solution method | sequence-space Jacobians, Reiter method | Speed and nonlinearity |
| Calibration targets | MPCs, wealth shares, liquid wealth, aggregate ratios | Distributional realism |

## Workflow
1. Implement the household block (endogenous grid method) and test it against known cases
   - Test against analytical cases and a representative-agent limit
2. Compute steady-state distribution and sequence-space Jacobians
   - Check grid convergence and distribution accuracy
3. Assemble general equilibrium; verify market clearing
   - Asset, goods and labor markets clear in steady state and along transitions
4. Calibrate to micro and aggregate moments
   - Targets from household surveys and national accounts; document gaps
5. Produce aggregate and distributional IRFs
   - Decompose consumption responses into direct and indirect effects
6. Register the model as a lego set (`/lego-map`): a baseplate plus bricks with declared studs (variables, units, timing) and stubs, so components can later be attached, detached or swapped

## Checkpoints with the user
- After the household block: confirm asset structure and income process
- After calibration: confirm micro targets and the fit
- After IRFs: confirm the distributional outputs needed

## Common pitfalls
- Coarse grids that distort the wealth distribution
- Calibrating MPCs without micro evidence
- Ignoring aggregation errors
- Over-interpreting the distribution from a one-asset model

## Output
`models/dsge/<name>-hank/ (+ model.lego.json)`

The folder holds the household block and tests, steady-state and Jacobian code, the GE assembly, calibration files, the aggregate and distributional IRF pack and the lego manifest. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Market clearing and aggregation checks pass
- Micro targets are matched or gaps documented
- Lego manifest passes `python tools/lego.py check`
- Grid-convergence and accuracy checks are reported
- Distributional IRFs are reported alongside aggregates

## Suggested next steps
- `/validate-model`
- `/distributional-analysis`
- `/lego-map`
