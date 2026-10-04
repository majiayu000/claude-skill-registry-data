---
name: bmc-implementation-plan-reporter
description: >
  Generates reports and implementation plans for the Solution team and Coding
  team: status, gaps, risks, handoffs, task breakdown by team, ownership, order,
  acceptance criteria. Use when reporting to Solution/Coding teams or producing
  implementation plan from the full improvement plan.
---

# BMC Implementation Plan & Reporter

The agent **reports** and **generates implementation plans** for the **Solution team** and **Coding team** workflow. Input: context briefs and FULL-IMPROVEMENT-PLAN.md. Output: reports and actionable implementation plans by team.

## When to Use

- User asks for a **report** for the Solution team or Coding team (status, gaps, risks, handoff).
- User asks to **generate implementation plan** for Solution team and Coding team workflow.
- After Phase 3: turn FULL-IMPROVEMENT-PLAN.md into team-specific task lists with ownership and handoff points.

## Scope

- **Reports:** Status summary, gaps (what is missing or broken), risks, handoff summary (what one team needs from another). Audience: Solution team, Coding team.
- **Implementation plan:** Task breakdown by team (Solution vs Coding), per task: title, owner, depends on, acceptance criteria, handoff (deliverable to the other team). Order tasks so dependencies and handoffs are respected.

## Workflow

1. **Before working:** Read `docs/team/knowledge/Reporter.md` if it exists. Read `docs/team/PROJECT-STATE.md` (cambios recientes, pendientes).
2. **Read** — FULL-IMPROVEMENT-PLAN.md, context briefs, and (if present) 02-investigation-and-discussion.md.
3. **Report** — Produce a short report (e.g. `docs/bmc-dashboard-modernization/REPORT-SOLUTION-CODING.md` or two files): executive summary, status by module/wave, gaps, risks, handoff points. Use clear headings for Solution team and Coding team.
4. **Implementation plan** — From the improvement plan steps, assign each step (or group of steps) to **Solution team** (design, specs, acceptance, UX) or **Coding team** (implementation, config, tests). Produce:
   - **Solution team plan:** Tasks (e.g. “Approve IA,” “Sign off Cotizaciones flow”), order, inputs from Coding, outputs to Coding.
   - **Coding team plan:** Tasks (e.g. “Implement nav,” “Wire /api/cotizaciones”), order, depends on Solution deliverables, acceptance criteria.
   - **Handoff table:** When Solution delivers X, Coding can start Y; when Coding delivers Z, Solution can validate W.

## Outputs

- **Report:** Markdown in `docs/bmc-dashboard-modernization/` (e.g. `REPORT-SOLUTION-CODING.md`): status, gaps, risks, handoffs.
- **Implementation plan:** Same folder (e.g. `IMPLEMENTATION-PLAN-SOLUTION-CODING.md`): Solution tasks, Coding tasks, handoff table, order.

## Conventions

- **Solution team:** Ownership of scope, UX, acceptance criteria, sign-off. Outputs: specs, approved IA, approved flows.
- **Coding team:** Ownership of implementation, config, tests, deployment. Outputs: code, env, docs, passing checks.
- **Handoff:** Explicit “Solution delivers A → Coding starts B”; “Coding delivers C → Solution validates D.”

## Reference

- Report and implementation plan templates: [reference.md](reference.md).
- Full improvement plan: `docs/bmc-dashboard-modernization/FULL-IMPROVEMENT-PLAN.md`.
- Context briefs: `docs/bmc-dashboard-modernization/context-briefs/`.
- Prompt: PROMPT-AGENT-TEAM-FULL-IMPROVEMENT-PLAN.md § Extended agent responsibilities.
