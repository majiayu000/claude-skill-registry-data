---
name: nowcast
description: "Builds and runs a nowcasting system with release calendar, news decomposition and real-time evaluation."
argument-hint: "[target variable]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /nowcast — Nowcast

**Category:** Estimation · **Primary agent:** `dfm-nowcasting-specialist`

Builds and runs a nowcasting system with release calendar, news decomposition and real-time evaluation.

Arguments: `$ARGUMENTS`

## Purpose
Build and run a nowcasting system for current-quarter (or current-month) activity or inflation: indicators selected with their release timing, models estimated on a ragged edge, pseudo-real-time evaluation with vintages, predictive densities, and news decompositions that explain each update. The output is a nowcast with uncertainty and a schedule for regular updates.

**Use it when** official data arrive with delays and decisions need an estimate of current conditions, or a forecast round needs better initial conditions.

**Do not use it when** the horizon is several quarters ahead (`/estimate-bvar`, `/forecast-round`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Indicator data
   - Release calendar
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `dfm-nowcasting-specialist` — primary agent; coordinates the work and integrates results
- `high-frequency-data-specialist` — Handles high-frequency and alternative data
- `nlp-text-as-data-specialist` — Turns text into economic data
- `forecast-evaluation-specialist` — Evaluates forecasts

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Model | dynamic factor model, bridge equations, MIDAS, ML ensembles | Use of many indicators |
| Indicators | hard data, surveys, financial, alternative data | Timeliness and noise |
| Frequency | monthly, weekly, daily inputs | Update cadence |
| Density | model-based, empirical errors, conformal | Uncertainty reporting |
| Combination | single model, pooled | Robustness |

## Workflow
1. Select and validate indicators with release timing
   - Validate alternative data against official series before use
2. Estimate DFM/bridge/MIDAS (and optionally ML) nowcasts
3. Run pseudo-real-time evaluation with vintages
   - Compare with a simple benchmark at each point in the release calendar
4. Produce nowcast with predictive density and news decomposition
5. Set up a schedule for updating

## Checkpoints with the user
- After indicator selection: confirm sources and licenses
- After evaluation: confirm the system is accurate enough for use

## Common pitfalls
- Evaluation on revised data
- Indicators added without validation
- Point nowcasts without uncertainty
- News decompositions not reconciled with revisions

## Output
`forecasts/nowcasts/<target>-<date>.md`; model code in `models/econometrics/<name>/`

Each nowcast note reports the estimate, density, news since the last update and data used; model code supports scheduled updates. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Pseudo-real-time evaluation performed
- Predictive density provided
- Indicators are validated and licensed
- News decompositions accompany every update

## Suggested next steps
- `/forecast-round`
- `/chart-pack`
