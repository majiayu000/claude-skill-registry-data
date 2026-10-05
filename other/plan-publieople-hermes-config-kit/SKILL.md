---
name: plan
description: "Plan mode: write markdown plan to .hermes/plans/, no exec."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow]
    related_skills: [writing-plans, subagent-driven-development]
---

# Plan Mode

Use this skill when the user wants a plan instead of execution.

## Core behavior

For this turn, you are planning only.

- Do not implement code.
- Do not edit project files except the plan markdown file.
- Do not run mutating terminal commands, commit, push, or perform external actions.
- You may inspect the repo or other context with read-only commands/tools when needed.
- Your deliverable is a markdown plan saved inside the active workspace under `.hermes/plans/`.

## Output requirements

Write a markdown plan. **Two modes — detect which one fits the user's framing:**

### Mode A: Implementation Plan (default)
When the user says "build X", "implement Y", "add feature Z" — produce a concrete, actionable implementation plan.

Include, when relevant:
- Goal
- Current context / assumptions
- Proposed approach
- Step-by-step plan
- Files likely to change
- Tests / validation
- Risks, tradeoffs, and open questions

### Mode B: Comparative Analysis
When the user says "试试X", "考虑Y", "换成Z" (evaluating a technology/approach change) — produce a tradeoff analysis FIRST, not an implementation plan.

Include:
- **Compared to**: what the current approach is
- **Pros / Cons table**: dimensions like bundle size, features, maintenance, compatibility, licensing
- **Migration effort**: estimated work and risk areas
- **Recommendation**: recommend or recommend-against with clear reasoning
- **Quick-check option**: suggest trying on a branch to evaluate hands-on before committing

Choosing Mode B is a signal that the user wants to **decide before committing**. Save the analysis under `.hermes/plans/`, then wait for user direction before implementing.

If the user's intent is unclear between evaluating and implementing, ask: "要我做个对比分析还是直接写实施计划？"

## Save location

Save the plan with `write_file` under:
- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

Treat that as relative to the active working directory / backend workspace. Hermes file tools are backend-aware, so using this relative path keeps the plan with the workspace on local, docker, ssh, modal, and daytona backends.

If the runtime provides a specific target path, use that exact path.
If not, create a sensible timestamped filename yourself under `.hermes/plans/`.

## Interaction style

- If the request is clear enough, write the plan directly.
- If no explicit instruction accompanies `/plan`, infer the task from the current conversation context.
- If it is genuinely underspecified, ask a brief clarifying question instead of guessing.
- After saving the plan, reply briefly with what you planned and the saved path.
- If the target `.hermes/plans/` directory doesn't exist or is unwritable, fall back to `~/.hermes/plans/`.

## Extended: Migration Analysis (Greenfield Rebuilds)

When the user asks to **rebuild an existing codebase with a modern stack** while preserving the original design — inventory the current codebase first (see `references/migration-analysis.md`), then combine Mode A + Mode B into a migration analysis document.

The reference covers the full methodology: inventory → keep/rewrite map → stack selection → design fidelity table → phased plan → risk assessment.
