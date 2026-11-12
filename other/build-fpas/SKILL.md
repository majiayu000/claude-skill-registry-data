---
name: build-fpas
description: "Designs and builds a forecasting and policy analysis system: core model, nowcasts, judgment layer, forecast process."
---
<!-- Generated from .claude/skills/build-fpas/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /build-fpas — Build FPAS

**Category:** Build · **Primary agent:** `fpas-modeler`

Designs and builds a forecasting and policy analysis system: core model, nowcasts, judgment layer, forecast process.

Arguments: whatever the user wrote after the command name.

## Purpose
Design and build a forecasting and policy analysis system: not only a core model but the process around it, including nowcasting tools for the near term, a judgment layer with an overlay log, forecast-story templates, a calendar with roles and sign-offs, and the training that lets a counterpart team run it. The output is a system that completes a full forecast round from a frozen data vintage.

**Use it when** an institution needs a regular, documented forecast process tied to policy decisions, or an existing process needs a model core, a judgment layer or better documentation.

**Do not use it when** only a model is needed (`/build-semi-structural`, `/build-dsge`) or a single forecast is needed (`/forecast-round`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Core model or approved model-spec
   - Data pipeline
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `fpas-modeler` — primary agent; coordinates the work and integrates results
- `dfm-nowcasting-specialist` — Builds dynamic factor models and nowcasts
- `stakeholder-liaison-specialist` — Interfaces with stakeholders and counterparts
- `visualization-dashboard-specialist` — Designs charts and dashboards

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Core model | semi-structural gap model, small DSGE, suite | Transparency versus structure |
| Near-term tools | bridge equations, DFM nowcasts, expert judgment | Accuracy of initial conditions |
| Judgment layer | add-factors, tuned shocks, conditioning on paths | Traceability of overlays |
| Cycle | monthly, quarterly; number of meetings per round | Workload and timeliness |
| Outputs | forecast report, risk scenarios, fan charts, policy rate path | Communication |

## Workflow
1. Define the forecast process calendar, roles and sign-offs
   - Data cut-off, nowcast, model runs, judgment meetings, sign-off, publication
2. Integrate core model, near-term nowcast tools and judgment-overlay log
   - Overlays recorded with reason, evidence and owner
3. Build the shock-decomposition and forecast-story templates
   - Templates link every story element to a decomposition or overlay
4. Run a mock forecast round on historical data and review lessons
   - Use a frozen vintage; evaluate the mock forecast against outturns
5. Prepare training material for the counterpart team
   - Hands-on exercises on the core model and the process (`/design-training`)
6. Register the model as a lego set (`/lego-map`): a baseplate plus bricks with declared studs (variables, units, timing) and stubs, so components can later be attached, detached or swapped

## Checkpoints with the user
- After the process design: confirm calendar and roles with the institution
- After integration: confirm the overlay rules
- After the mock round: agree changes before handover

## Common pitfalls
- A model without a process, or a process without documentation
- Overlays that are not recorded
- Near-term tools inconsistent with the core model's initial conditions
- Training that ends at the workshop with no follow-up

## Output
`models/fpas/<name>/ and docs/models/<name>/fpas-design.md (+ model.lego.json)`

The model folder holds the core model, nowcast tools, templates and run scripts; the design document covers the calendar, roles, overlay rules and the mock-round review; the lego manifest registers the model and its satellites. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- A full mock round runs end-to-end from a frozen data vintage
- Lego manifest passes `python tools/lego.py check`
- The overlay log is in place and used in the mock round
- Training material exists for the counterpart team

## Suggested next steps
- `/forecast-round`
- `/design-training`
- `/lego-map`
