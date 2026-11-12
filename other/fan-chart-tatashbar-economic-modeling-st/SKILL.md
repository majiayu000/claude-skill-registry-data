---
name: fan-chart
description: "Produces density forecasts and fan charts with documented uncertainty method and calibration checks."
---
<!-- Generated from .claude/skills/fan-chart/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /fan-chart — Fan Chart

**Category:** Analysis · **Primary agent:** `scenario-risk-analysis-specialist`

Produces density forecasts and fan charts with documented uncertainty method and calibration checks.

Arguments: whatever the user wrote after the command name.

## Purpose
Produce density forecasts and fan charts whose width and skew are defensible: the uncertainty method is documented, risk balance is explained, coverage is checked against past forecast errors, and every chart states its vintage and method. The output is a set of charts that communicate uncertainty honestly.

**Use it when** a forecast round, brief or DSA needs to show uncertainty around a central path.

**Do not use it when** discrete scenarios communicate the risks better (`/scenario-analysis`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Forecast models and error history
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `scenario-risk-analysis-specialist` — primary agent; coordinates the work and integrates results
- `forecast-evaluation-specialist` — Evaluates forecasts
- `visualization-dashboard-specialist` — Designs charts and dashboards

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Method | model-based densities, historical forecast errors, quantile regression, combinations | Width and shape |
| Skew | symmetric, judgmental balance of risks, model-based | Communication of risks |
| Bands | 50/70/90 percent | Readability |
| Variables | GDP, inflation, rates, debt | Coverage |

## Workflow
1. Choose the method (model-based, historical errors, quantile regression)
2. Compute densities and risk balance; check coverage on past forecasts
   - Explain any skew with identified risks
3. Render charts with consistent style; label vintage and method
   - Color-blind-safe palettes; units and sources on every chart

## Checkpoints with the user
- After method choice: confirm the approach
- After coverage checks: confirm the bands are credible

## Common pitfalls
- Bands too narrow from model-only uncertainty
- Skew without a stated reason
- Charts without vintage or method labels

## Output
`forecasts/<round>/fan-charts/`

The folder holds the chart files, the data behind them, and a note on method, risk balance and historical coverage.

## Gate / verdict
- Historical coverage is checked
- Method documented on the chart
- Skew is explained by identified risks

## Suggested next steps
- `/chart-pack`
- `/forecast-round`
