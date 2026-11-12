---
name: build-dsge
description: "Builds a DSGE model (small, medium or large) from approved spec: derivation, code, solution, tests, IRFs."
argument-hint: "[model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /build-dsge — Build DSGE

**Category:** Build · **Primary agent:** `open-economy-dsge-specialist`

Builds a DSGE model (small, medium or large) from approved spec: derivation, code, solution, tests, IRFs.

Arguments: `$ARGUMENTS`

## Purpose
Turn an approved model specification into a working, documented and tested dynamic stochastic general equilibrium model that is ready for estimation and independent validation. The output is not a forecast or a policy answer; it is a model whose steady state, dynamics and policy experiments behave as the specification says, with every parameter sourced and every friction justified.

**Use it when** the question needs structure: expectations and policy rules matter, a counterfactual policy or regime change is involved, welfare must be compared, or shocks have to be identified through theory rather than statistics.

**Do not use it when** a semi-structural gap model answers the question (`/build-semi-structural`), when the task is pure short-term forecasting (`/estimate-bvar`, `/nowcast`), or when distribution across households is central (`/build-hank`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Approved model-spec
   - Calibration plan
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.
4. **Confirm the model class and toolchain.** Small, medium or large (`.claude/docs/model-classes.md`) sets the depth of every step below. Agree the toolchain (Dynare/MATLAB, Julia, Python) with the user and check it is approved in `studio-config.yaml`.

## Agents
- `open-economy-dsge-specialist` — primary agent; coordinates the work and integrates results
- `perturbation-solution-specialist` — Solves DSGE models by perturbation (1st-3rd order), pruning, and verifies determinacy and accuracy
- `matlab-dynare-engineer` — Engineers MATLAB, Dynare, IRIS, RISE and Octave codebases; legacy model maintenance and migration
- `financial-frictions-dsge-specialist` — Builds DSGE models with financial frictions
- `symbolic-derivation-specialist` — Derives and verifies model equations with computer algebra
- `ipf-micro-specialist` — Builds microfounded IPF models with FX intervention, capital flow rules and occasionally binding external constraints

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Size of the model | small (3-equation core), medium (Smets–Wouters type), large (multi-sector, multi-agent) | Data needs, estimation feasibility, validation depth |
| Open-economy closure | debt-elastic premium, endogenous discount factor, portfolio cost | Persistence of external adjustment |
| Pricing of trade | producer-, local- or dominant-currency | Strength of expenditure switching and pass-through |
| Frictions | habits, investment adjustment costs, wage rigidity, financial accelerator, collateral constraints | Fit and amplification; each needs a stylized fact |
| Solution order | first order; second/third order with pruning; piecewise-linear or global for occasionally binding constraints | Validity for welfare, risk and constraint questions |
| Policy block | Taylor-type, inflation-forecast targeting, exchange-rate terms, fiscal rules | Determinacy region and policy experiments |

## Workflow
1. Implement the model in the chosen toolchain (Dynare/Julia/Python) with a clean parameter block
   - Derive optimization problems, first-order conditions, market clearing and, for open economies, the balance of payments; keep derivations in `docs/models/<name>/derivation.md`
   - For medium and large models, verify the derivation symbolically before coding
   - Separate files for parameters, steady state, model equations, shocks and run scripts; no hard-coded numbers in equations
2. Compute steady state; verify residuals and Blanchard-Kahn conditions
   - Derive the steady state analytically where possible and check it numerically
   - Map each steady-state ratio to its data target in the calibration sheet and report the gap
   - Report the determinacy region of the policy rule, not only that the baseline is determinate
3. Solve at the chosen order; check accuracy with Euler errors
   - First order for standard impulse responses and forecasts; higher order with pruning when risk, welfare or asymmetry matter
   - Occasionally binding constraints: solve explicitly and show where they bind
4. Produce IRFs for standard shocks; compare to spec expectations
   - Standard set: productivity, demand/preference, cost-push, monetary policy, fiscal, and for open economies foreign demand, foreign rate, risk premium, terms of trade and commodity prices
   - Check signs and magnitudes against empirical benchmarks (VARs, local projections) and explain every deviation through a mechanism
   - Produce variance decompositions and second moments versus data
5. Write tests and hand over to estimation and validation
   - Tests: steady-state residuals, identities (resource constraint, balance of payments, government budget), determinacy, IRF signs, reproducibility of a stored baseline
   - Write the model spec and a short model card; record versions and seeds
6. Register the model as a lego set (`/lego-map`): a baseplate plus bricks with declared studs (variables, units, timing) and stubs, so components can later be attached, detached or swapped

## Checkpoints with the user
- After the derivation: confirm the equation list and the frictions before coding
- After calibration: confirm the steady-state targets and any parameter labelled as an assumption
- After the first impulse responses: confirm the mechanics make economic sense before extending the model

## Common pitfalls
- Adding frictions to improve fit without a documented stylized fact
- Leaving the open-economy unit root unaddressed, or choosing a closing device that dominates dynamics
- Reporting welfare from a first-order solution
- Calibrating to a non-representative period (crisis, commodity boom) without saying so
- Treating shocks that absorb misspecification (for example, large risk-premium shocks) as structural explanations

## Output
`models/dsge/<name>/ (+ model.lego.json)`

The folder holds the parameter, steady-state, model and run files, the test suite, the calibration sheet, the derivation note, the impulse-response pack and the lego manifest. Documentation goes to `docs/models/<name>/`. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Determinacy verified
- Steady-state ratios match targets
- Accuracy report present
- Lego manifest passes `python tools/lego.py check`
- Every parameter has a source or an explicit assumption with a sensitivity check
- Impulse responses have documented signs and magnitudes with a mechanism for each

## Suggested next steps
- `/estimate-dsge`
- `/validate-model`
- `/lego-map`
