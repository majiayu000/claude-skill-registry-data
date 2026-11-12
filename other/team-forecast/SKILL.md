---
name: team-forecast
description: "Orchestrates a full forecast round across nowcasting, core model, ML ensemble, judgment, risks, charts and brief."
---
<!-- Generated from .claude/skills/team-forecast/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /team-forecast — Team Forecast

**Category:** Team Orchestration · **Primary agent:** `fpas-modeler`

Orchestrates a full forecast round across nowcasting, core model, ML ensemble, judgment, risks, charts and brief.

Arguments: whatever the user wrote after the command name.

## Purpose
Orchestrate a full forecast round with a team: freeze and check data, run nowcasts, the core model, BVAR and ML forecasters in parallel, combine them, log overlays agreed with stakeholders, build risks and charts, and deliver a reviewed brief. The output is a reproducible round package with stated risk balance.

**Use it when** a regular forecast round requires several models and contributors.

**Do not use it when** one analyst can run the round alone (`/forecast-round`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Frozen data vintage
   - Approved models
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `fpas-modeler` — primary agent; coordinates the work and integrates results
- `dfm-nowcasting-specialist` — Builds dynamic factor models and nowcasts
- `time-series-deep-learning-specialist` — Builds deep sequence and foundation-model forecasters
- `bayesian-var-specialist` — Builds Bayesian VARs
- `forecast-combination-specialist` — Combines forecasts
- `scenario-risk-analysis-specialist` — Designs scenarios and risk assessments
- `stakeholder-liaison-specialist` — Interfaces with stakeholders and counterparts
- `visualization-dashboard-specialist` — Designs charts and dashboards
- `policy-brief-writer` — Writes policy briefs and notes

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Workflow
1. Phase 1: data-engineer freezes the vintage; data-quality checks run
2. Phase 2 (parallel): nowcast, core model, BVAR and ML forecasters run
   - Validate lego assemblies before running (`python tools/lego.py validate`)
3. Phase 3: forecast-combination-specialist combines; stakeholder-liaison-specialist logs overlays with stakeholders
4. Phase 4 (parallel): scenario-risk-analysis-specialist builds risks; visualization-dashboard-specialist builds charts
5. Phase 5: policy-brief-writer drafts the brief; economic-reasoning-specialist and policy-relevance-specialist review; archive the package

## Checkpoints with the user
- End of Phase 1: confirm the data cut-off
- End of Phase 3: approve the combined forecast and overlays
- Before release: approve the brief

## Common pitfalls
- Models run on different vintages
- Overlays agreed but not logged
- Revisions from the previous round left unexplained

## Output
`forecasts/<round>/`

The round folder holds the frozen vintage, all model outputs, the combination, overlay log, risks, charts, brief and review records.

## Gate / verdict
- Reproducible; overlays logged; risk balance stated
- All models use the frozen vintage
- Revisions from the previous round are explained

## Suggested next steps
- `/retrospective`
- `/policy-brief`
