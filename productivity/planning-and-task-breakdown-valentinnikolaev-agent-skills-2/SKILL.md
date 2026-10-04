---
name: planning-and-task-breakdown
description: Create an ordered implementation plan with dependencies and observable completion criteria. Use for planning work; not reviewing an existing plan.
---

# Planning and Task Breakdown

Turn an established goal or specification into executable steps. Adapted from Addy Osmani's `planning-and-task-breakdown` workflow; see the bundled license and repository third-party notice.

## Route precisely

- Use when the user asks for a plan, task breakdown, execution order, or handoff for work not yet implemented.
- Use `plan-review` to assess an existing plan without rewriting it, `review-spec` to assess requirements, and `code-review` for a completed diff.
- Do not expand a trivial one-step change into a multi-phase plan. Do not implement merely because the plan is complete.

## Build the plan

1. Read repository instructions, the requested outcome, authoritative requirements, current code boundaries, and available verification commands. Identify missing input that materially changes the approach; otherwise state a bounded assumption.
2. List independently observable deliverables. Map each explicit requirement to a step, including migration, data handling, interface compatibility, and recovery only where applicable.
3. Order steps by real dependencies. Prefer small vertical slices that leave a useful checkable state. Name parallel work only when interfaces and ownership are clear enough to avoid conflicting edits.
4. For each step, state its output, prerequisites, affected area, acceptance evidence, and the test or inspection that would expose failure. Avoid invented file paths and commands; verify named targets in the repository.
5. Place a checkpoint after a material integration boundary. Include rollback or recovery when a step can cause externally visible or irreversible effects.

## Report

Return the goal and sources, assumptions, ordered steps with dependencies and acceptance checks, risks or decisions that affect execution, and the first executable step. Show a compact requirement-to-step map when requirements are numerous. Respond in chat unless the user requested a plan file. A plan is not evidence that code has been implemented or tested.
