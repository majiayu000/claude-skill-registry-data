---
name: team-fiscal
description: "Orchestrates a fiscal analysis package: DSA, multipliers, microsimulation, investment and risk, integrated into one report."
---
<!-- Generated from .claude/skills/team-fiscal/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /team-fiscal — Team Fiscal

**Category:** Team Orchestration · **Primary agent:** `debt-sustainability-analyst`

Orchestrates a fiscal analysis package: DSA, multipliers, microsimulation, investment and risk, integrated into one report.

Arguments: whatever the user wrote after the command name.

## Purpose
Orchestrate a fiscal analysis package: debt sustainability, fiscal multipliers, tax-benefit microsimulation, public investment and fiscal risks, all built on one macro-fiscal baseline and reconciled into a single report. The output is a package whose fiscal numbers agree across components and whose growth, debt and distributional effects are consistent.

**Use it when** a budget, fiscal reform, consolidation plan or fiscal framework must be assessed comprehensively.

**Do not use it when** only debt sustainability (`/debt-sustainability`) or distributional effects (`/distributional-analysis`) are needed.

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Fiscal and macro baseline
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `debt-sustainability-analyst` — primary agent; coordinates the work and integrates results
- `fiscal-multiplier-specialist` — Estimates and simulates fiscal multipliers
- `tax-benefit-microsimulation-specialist` — Builds tax-benefit microsimulation
- `public-investment-specialist` — Analyzes public investment
- `fiscal-risk-specialist` — Assesses fiscal risks
- `financial-programming-specialist` — Builds financial programming frameworks
- `policy-brief-writer` — Writes policy briefs and notes

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Workflow
1. Phase 1: align on baseline with financial-programming-specialist
2. Phase 2 (parallel): DSA, multipliers, microsimulation, investment and risk analyses
   - Growth effects of adjustment use the agreed multiplier range in the DSA
3. Phase 3: reconcile into one consistent package; check debt dynamics and macro-fiscal consistency
4. Phase 4: independent review; policy-brief-writer drafts the integrated report

## Checkpoints with the user
- End of Phase 1: approve the baseline
- End of Phase 3: review reconciliation issues

## Common pitfalls
- Components using different baselines
- DSA growth inconsistent with multipliers
- Microsimulation revenue that does not match the fiscal accounts

## Output
`forecasts/fiscal/<country>-<date>/`

The package holds the baseline, each component analysis, the reconciliation note and the integrated report.

## Gate / verdict
- Fiscal numbers reconcile across components
- DSA growth paths are consistent with the multiplier assessment

## Suggested next steps
- `/policy-brief`
