---
name: estimate-bvar
description: "Estimates Bayesian VARs with prior choice, hyperparameter selection, conditional forecasts and out-of-sample checks."
---
<!-- Generated from .claude/skills/estimate-bvar/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /estimate-bvar — Estimate Bvar

**Category:** Estimation · **Primary agent:** `bayesian-var-specialist`

Estimates Bayesian VARs with prior choice, hyperparameter selection, conditional forecasts and out-of-sample checks.

Arguments: whatever the user wrote after the command name.

## Purpose
Estimate a Bayesian VAR for forecasting and scenario analysis, with priors chosen by a documented rule, stability and convergence checked, conditional and unconditional forecasts produced, and out-of-sample accuracy compared with simple benchmarks. The output is a BVAR whose forecasting value has been demonstrated, not assumed.

**Use it when** forecasting several macro variables jointly, producing conditional forecasts on assumed paths (policy rates, commodity prices, foreign demand), or building a benchmark for structural and ML models.

**Do not use it when** structural identification is the aim (`/estimate-var`, `/identify-shocks`), or many indicators at mixed frequencies drive the forecast (`/nowcast`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Data sheet
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `bayesian-var-specialist` — primary agent; coordinates the work and integrates results
- `tvp-regime-switching-specialist` — Builds time-varying parameter, stochastic-volatility, Markov-switching and structural-break models
- `forecast-evaluation-specialist` — Evaluates forecasts

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Prior | Minnesota, normal-inverse-Wishart, sum-of-coefficients, dummy-initial-observation, steady-state prior | Shrinkage and long-run behavior |
| Hyperparameters | marginal-likelihood maximization, hierarchical, fixed by rule | Fit versus overfitting |
| Size | small, medium, large | Information versus shrinkage needs |
| Volatility | constant, stochastic volatility | Density forecasts |
| Conditioning | hard conditions, soft conditions, structural scenarios | Interpretation of conditional forecasts |

## Workflow
1. Choose prior family and select hyperparameters by a documented rule
   - Transform variables consistently (levels, logs, growth rates) and state why
2. Estimate; check convergence and stability
   - Posterior draws with stable roots; MCMC diagnostics where samplers are used
3. Produce unconditional and conditional forecasts
   - Show which shocks deliver conditioning paths and whether they are plausible
4. Evaluate out-of-sample against random walk and AR benchmarks
   - Rolling origins; point and density scores; equal-accuracy tests

## Checkpoints with the user
- After variable and prior choice: confirm the specification
- After evaluation: confirm whether the BVAR is fit for forecasting use

## Common pitfalls
- Hyperparameters tuned on the evaluation sample
- Conditional forecasts requiring implausible shocks
- Ignoring stochastic volatility when densities matter
- Evaluating on revised data as if real time

## Output
`docs/models/<name>/bvar-results.md`; code and settings in `models/econometrics/<name>/`

The results document reports the prior and hyperparameters, diagnostics, forecasts and the out-of-sample comparison; code and settings allow exact rerun. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Out-of-sample comparison with benchmarks present
- Hyperparameter rule is documented
- Density forecasts are checked for calibration

## Suggested next steps
- `/forecast-round`
- `/validate-model`
