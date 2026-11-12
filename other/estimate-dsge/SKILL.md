---
name: estimate-dsge
description: "Estimates a DSGE model by Bayesian methods with identification analysis, convergence diagnostics and fit evaluation."
---
<!-- Generated from .claude/skills/estimate-dsge/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /estimate-dsge — Estimate DSGE

**Category:** Estimation · **Primary agent:** `bayesian-dsge-estimation-specialist`

Estimates a DSGE model by Bayesian methods with identification analysis, convergence diagnostics and fit evaluation.

Arguments: whatever the user wrote after the command name.

## Purpose
Estimate a DSGE model with Bayesian methods so that the posterior is credible: identification checked before estimation, priors tested for what they imply, convergence demonstrated across chains, prior–posterior overlap reported, and fit evaluated with marginal likelihood, posterior predictive checks and out-of-sample forecasts. The output is an estimation report and an archived set of posterior draws that can be reused exactly.

**Use it when** a built and tested DSGE model (`/build-dsge`) must be taken to data for forecasting, shock decompositions or policy analysis.

**Do not use it when** the model has not passed steady-state and determinacy tests, or when calibration is the agreed approach (`/calibrate-model`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Built model
   - Calibration plan
   - Data pipeline
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `bayesian-dsge-estimation-specialist` — primary agent; coordinates the work and integrates results
- `state-space-kalman-specialist` — Builds state-space models
- `simulation-based-inference-specialist` — Estimates complex models with neural simulation-based inference
- `perturbation-solution-specialist` — Solves DSGE models by perturbation (1st-3rd order), pruning, and verifies determinacy and accuracy

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Observables | output, inflation, rates, exchange rate, trade, fiscal | Identification and fit |
| Measurement | measurement errors, trend treatment, data transformations | Interpretation of shocks |
| Sampler | random-walk Metropolis–Hastings, SMC, HMC/NUTS | Reliability with multimodal posteriors |
| Priors | literature-based, prior predictive tuned, endogenous priors | What the data must override |
| Sample | full, post-break | Stability of parameters |

## Workflow
1. Run prior predictive checks and identification diagnostics
   - Local identification (rank of the Jacobian); prior-implied moments versus data
2. Estimate with MCMC or SMC; run multiple chains and convergence diagnostics
   - R-hat, effective sample size, trace plots; mode-finding from several starts
3. Compare prior vs. posterior; flag weakly identified parameters
4. Evaluate fit: marginal likelihood, posterior predictive, out-of-sample forecasts
   - Historical shock decomposition and smoothed shocks checked for plausibility
5. Archive posterior draws and the exact run configuration

## Checkpoints with the user
- After identification diagnostics: confirm observables and priors
- After estimation: review weakly identified parameters and shock plausibility

## Common pitfalls
- Posteriors equal to priors reported as estimates
- Single-chain results
- Measurement errors absorbing the fit
- Large, persistent shocks soaking up misspecification

## Output
`docs/models/<name>/estimation-report.md`

The estimation report covers priors, identification, convergence, prior–posterior comparisons, fit and shock decompositions; draws and configuration are archived with the model. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Convergence diagnostics pass
- Identification issues documented
- Posterior draws archived
- Prior predictive checks are reported
- Smoothed shocks are reviewed for plausibility

## Suggested next steps
- `/validate-model`
- `/backtest`
