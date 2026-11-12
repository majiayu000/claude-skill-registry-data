---
name: chart-pack
description: "Produces a chart pack from code: fan charts, shock decompositions, scenario comparisons, with consistent style and labelling."
---
<!-- Generated from .claude/skills/chart-pack/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /chart-pack — Chart Pack

**Category:** Documentation · **Primary agent:** `visualization-dashboard-specialist`

Produces a chart pack from code: fan charts, shock decompositions, scenario comparisons, with consistent style and labelling.

Arguments: whatever the user wrote after the command name.

## Purpose
Produce a chart pack for a forecast round, brief or presentation, generated entirely from code: fan charts, shock decompositions, scenario comparisons and supporting charts, each labeled with units, sources and vintage, accessible and consistent in style. The output regenerates from one command when data change.

**Use it when** model results must be communicated visually to decision-makers or in publications.

**Do not use it when** an interactive monitoring tool is needed rather than static charts; design a dashboard with the visualization specialist.

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Results files
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `visualization-dashboard-specialist` — primary agent; coordinates the work and integrates results
- `forecast-evaluation-specialist` — Evaluates forecasts

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Chart list | one chart per message | Focus |
| Uncertainty | fan charts, bands, scenario lines | Honesty |
| Format | publication, slides, web | Sizes and fonts |
| Style | studio template, institutional template | Consistency |

## Workflow
1. Choose a chart list matching the message
2. Generate charts from scripts (never by hand), with units, sources and vintage in the footer
3. Check accessibility (colors, fonts) and consistency
   - Color-blind-safe palettes; avoid dual axes and truncated axes that mislead
4. Archive scripts and outputs together

## Checkpoints with the user
- After the chart list: confirm messages
- After drafts: review readability

## Common pitfalls
- Too many series per chart
- Forecast charts without uncertainty
- Hand-edited charts that cannot be updated

## Output
`docs/briefs/<name>-charts/`; a Word file with the charts and their captions on request (`python tools/report.py docx <index.md> --out <file.docx>`)

The folder holds the scripts, the data behind each chart and the rendered charts.

## Gate / verdict
- Charts regenerate from one command; uncertainty is visible
- Every chart shows units, sources and vintage

## Suggested next steps
- `/policy-brief`
