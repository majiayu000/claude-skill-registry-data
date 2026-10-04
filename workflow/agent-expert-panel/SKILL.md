---
name: agent-expert-panel
description: "Use this skill when a user wants to decide, design, audit, or repair a coordinated multi-agent or expert-team workflow for a project, Agent Skill, research process, product workflow, or content pipeline. Trigger on agent orchestration, expert panels, 多智能体协作, Agent 专家团, steward or coordinator roles, capability routing, handoff contracts, quality gates, failure recovery, budgets, or artifact ownership. Do not use it for simple parallel tasks, single-domain work, or merely executing an already-approved plan."
---

# Agent Expert Panel

Decide whether a task needs a coordinated expert team, then design the smallest reliable workflow. A panel is an accountable workflow, not a list of personas.

## Contract

Design or audit by default; never launch agents or invent evidence. Operationalize only when explicitly requested and supported by the host. Prefer one agent unless a panel adds enough quality or risk reduction to justify its cost.

## Procedure

1. **Intake:** capture outcome, acceptance evidence, inputs, capabilities, and material budget, privacy, approval, or rollback constraints.
2. **Fit:** form a panel only when separable work, distinct expertise, checking, or integration value outweighs operating cost. Never decide by task count alone.
3. **Path:** choose `direct`, `compact-panel`, or `full-panel`; reserve full for a reusable contract or implementation handoff.
4. **Ownership:** the steward owns the final outcome and trace. Each specialist owns one artifact with focused inputs, limits, a check, and a next owner.
5. **Preflight:** record tools, data sensitivity, budget, approval, and fallback. Mark each packet `match`, `mismatch`, or `clarify`; assume nothing.
6. **Flow:** default to sequential work; parallelize only independent packets with merge criteria. Handoffs need an owner, artifact, check, stop condition, and next owner. Gate publication, spend, sensitive transfer, and irreversible work.
7. **Failure:** stop on missing capability, replan repeated failure, return ambiguous work for evidence, and escalate irreversible or value-based conflicts.

## Output

- **Direct:** decision, reason, next action, and when to reconsider.
- **Compact (default):** assumptions, members, phases, handoffs, gates, checks, risks, fallback, and next action.
- **Full:** read `references/panel-specification.md` and apply its detailed contracts.

Do not silently execute a design request or emit a full specification for a small task.

## Resources

Read `references/panel-specification.md` only when the user asks for a reusable expert-team contract, an implementation handoff, or enough detail to operationalize an approved panel. Evaluation fixtures and packaging checks belong to the source repository; they are not runtime dependencies of this installable Skill.
