---
name: team-dsge
description: "Orchestrates the full DSGE team: spec, build, solve, estimate, validate and document a structural model end to end."
argument-hint: "[model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /team-dsge — Team DSGE

**Category:** Team Orchestration · **Primary agent:** `open-economy-dsge-specialist`

Orchestrates the full DSGE team: spec, build, solve, estimate, validate and document a structural model end to end.

Arguments: `$ARGUMENTS`

## Purpose
Orchestrate the full DSGE team to specify, build, solve, estimate, validate and document a structural model, keeping builders and validators separate. The output is a documented, estimated and independently validated model, registered as a lego set, with blockers and open issues summarized for the user.

**Use it when** a new structural model is needed for policy analysis or forecasting and the project justifies a team.

**Do not use it when** a single build or estimation step is enough (`/build-dsge`, `/estimate-dsge`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Approved model-brief
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `open-economy-dsge-specialist` — primary agent; coordinates the work and integrates results
- `financial-frictions-dsge-specialist` — Builds DSGE models with financial frictions
- `perturbation-solution-specialist` — Solves DSGE models by perturbation (1st-3rd order), pruning, and verifies determinacy and accuracy
- `global-solution-specialist` — Solves models globally
- `bayesian-dsge-estimation-specialist` — Estimates DSGE models by Bayesian methods (MCMC, SMC) and checks identification, priors and fit
- `emde-lic-dsge-specialist` — Adapts structural models to emerging, developing and low-income economies
- `model-validation-specialist` — Performs independent model validation
- `technical-documentation-specialist` — Writes technical documentation

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Workflow
1. Phase 1 (sequential): open-economy and financial-frictions specialists draft the model-spec; user approves
2. Phase 2 (parallel): perturbation-solution-specialist builds and solves; global-solution-specialist prepares a nonlinear check; data-engineer prepares data
   - Register the model as a lego set as it is built (`/lego-map`)
3. Phase 3 (sequential): bayesian-dsge-estimation-specialist estimates; emde-lic-dsge-specialist reviews country fit
4. Phase 4 (independent): validation team validates — never the builders
5. Phase 5: technical-documentation-specialist writes the model card; summarize blockers and open issues for the user

## Checkpoints with the user
- End of Phase 1: approve the specification
- End of Phase 3: review estimation results
- End of Phase 4: review the validation rating

## Common pitfalls
- Builders validating their own model
- Estimation started before steady-state and determinacy tests pass
- Nonlinear checks skipped when constraints may bind

## Output
`models/dsge/<name>/ and docs/models/<name>/`

The model folder holds code, data, estimation results and the lego manifest; documentation holds the specification, calibration, estimation report, validation report and model card.

## Gate / verdict
- All phase gates met; validation rating is not FAIL
- Builders and validators are different agents, recorded in the report

## Suggested next steps
- `/model-release`
- `/forecast-round`
