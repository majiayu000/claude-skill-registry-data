---
name: backtest
description: "Runs historical and pseudo-real-time backtests with information-set checks and regime-specific performance."
argument-hint: "[model name] [window]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /backtest — Backtest

**Category:** Validation & QA · **Primary agent:** `backtesting-specialist`

Runs historical and pseudo-real-time backtests with information-set checks and regime-specific performance.

Arguments: `$ARGUMENTS`

## Purpose
Backtest a model, forecast method, risk model or policy rule: how would it have performed if it had been used in the past with only the information then available? The output reports point and density performance against naive benchmarks, separately for calm and stress periods, with automated proof that no future information leaked in.

**Use it when** a forecaster, nowcaster, risk model or scenario generator is being validated or compared, or a policy rule's historical performance is in question.

**Do not use it when** the question is conceptual soundness of a structural model (`/validate-model`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Model code
   - Data vintages
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `backtesting-specialist` — primary agent; coordinates the work and integrates results
- `forecast-evaluation-specialist` — Evaluates forecasts

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Window | rolling, expanding | Adaptation versus stability |
| Data | real-time vintages, latest vintage with caveat | Realism of the test |
| Re-estimation | every origin, periodically, never | Practical realism |
| Scores | RMSE, MAE, log score, CRPS, coverage | What "good" means |
| Regimes | recessions, crises, high inflation | Stress-period evidence |

## Workflow
1. Define windows, horizons and the information set at each origin
2. Verify no look-ahead with automated checks
   - Check features, scaling, filters, hyperparameters and data vintages
3. Run the backtest; compute point and density scores against naive benchmarks
   - Equal-accuracy tests suited to nested or non-nested models
4. Report calm vs. stress-period performance

## Checkpoints with the user
- After design: confirm windows, horizons and regimes
- After results: confirm interpretation for use decisions

## Common pitfalls
- Final-vintage data treated as real time
- Tuning on the full sample
- Averages only
- Overstating small, insignificant differences

## Output
`validation/<model>/backtest-report.md`

The report documents the design, look-ahead checks, scores versus benchmarks with tests, and performance by regime.

## Gate / verdict
- No look-ahead verified
- Benchmarks included
- Significance tests accompany comparisons
- Use of non-real-time data is stated where vintages are unavailable

## Suggested next steps
- `/validate-model`
- `/forecast-round`
