---
name: superplan
description: "Proactively plan or update superRA work. Requires superRA:using-superra. Use when starting or changing work, creating/revising superRA/, reflecting material decisions in the task tree, or on any request to grill, stress-test, or interrogate a loose idea into decisions."
---

# superplan — the PLAN phase

**First, load `superRA:using-superra` and `superRA:communicate` if not already loaded.**

**Harness plan mode active: load `references/harness-plan-mode.md` before proceeding.**

## Overview

Output: a `superRA/` task tree to execute.

Task-tree design judgment — objective/guidance writing, placement, splitting, context distillation, update-task lifecycle, retroactive creation — lives in `references/task-tree-design.md`.

**Announce at start:** "I'm using the superplan skill to create the task tree."

**Output location:** `superRA/` at the worktree root if in a worktree, otherwise the project root, unless the user specifies elsewhere. Commit the task tree before execution.

## Entry Assessment

Assess three dimensions before exploration or task design — creating a tree and updating one both pass through this.

- **Placement.** `superRA/` exists: place by `references/task-tree-design.md` §Placing Work in the Existing Tree. Legacy `PLAN.md` without a tree: offer migration (`task-tree` §Migration). Neither: the work becomes the first top-level task under `superRA/`.
- **Depth tier.** Choose from §Depth Tiers.
- **Routing path.** Forward planning (default), or **retroactive documentation** — code/results without task coverage need a `superRA/` record; same phases, per `task-tree-design.md` §Retroactive Task-Tree Creation. Structural cleanup of an existing tree is neither — that is the separate `references/consolidation.md` pass, entered on structural debt, not on new work needing placement.

Interactive canvas cadence (the default, and where light planning and execution move together): load `using-superra/references/interactive-mode.md`.

**Ask when unclear.** Placement or depth ambiguous, or the request too vague to aim exploration: run a scoping round per §Grilling — candidate placements from the descent, standard vs. thorough. Don't guess.

## Depth Tiers

A spectrum, not rigid modes — escalate mid-planning when complexity warrants. The tier mainly modulates Phase 1; Phase 4 is identical except thorough adds §Agent Review.

| Tier | Use for | Phase 1 |
|---|---|---|
| **Quick** | Minor updates, known additions, single-task changes — an objective rewrite after a scope revision, a well-understood subtask, a dependency adjustment. | Light scan of `superRA/`, skip deep exploration, design inline. |
| **Standard** (default) | New workstreams in familiar territory, a significant new branch, work a domain skill governs. | Explore project structure, load the domain skill, design tasks. |
| **Thorough** | Complex or unfamiliar projects, large scope across codebase areas, or an explicit request ("plan hard", "explore thoroughly", "detailed plan"). | Dispatch parallel exploration agents per `references/thorough-planning.md`; competing designs feed §Grilling. |

## Phase 1: Exploration

Read project structure, existing code, data directories, documentation, `CLAUDE.md`/`README.md`, and git history for relevant prior work, scaled to the tier (table above). Domain planning-survey gathering (data inventory, model primitives survey, manuscript assessment) begins here.

Exploration shifts placement or depth: revisit the entry assessment.

## Phase 2: Domain Setup & Scope

**Stop here, load the matching domain skill and follow its planning-stage reference per its own stage-load table.** Run its planning survey before any task structure is drafted: the survey lands in `## Details`, and the decisions it raises join the frontier for the Phase 3 round.

No implemented domain skill for the work: proceed to Phase 3, flag the gap to the researcher.

## Phase 3: Design & Task Decomposition

**Grill before decomposing.** Run the main round per §Grilling.

Then load `references/build-and-review.md`; follow its procedure.

## Phase 4: Review & Commit

### Self-Review

Run `references/build-and-review.md` §Self-Review.

### Agent Review

At thorough depth, dispatch `Stage: planning-review` before presenting the tree to the user. Explicit handoff-review requests enter the same step. Load `superRA:agent-orchestration` before writing the dispatch prompt.

**Planning reviewer:**
```
Prompt:
  Load `superRA:review-task` skill.

  Stage: planning-review
  Task: <task path or root>
  Review mode: handoff-readiness | design-review
  Context: <exploration synthesis, inline or path>
```

Review modes: `references/planning-review.md` §Review Mode — design-review for a newly authored tree, handoff-readiness once the design is settled.

Fix REVISE findings before User Review.

Quick and standard depth: skip this step unless the user asks for a handoff review.

### User Review

Present the tree (`superra task tree`) with the dashboard link. A tradeoff the assembled tree exposes as still unsettled re-enters §Grilling.

Per newly created task (especially top-level): state the existing concern you considered and why it does not cover the work.

### Execution Handoff

Commit `superRA/` atomically (`plan(add): <summary>` for initial authoring; full sub-step set in §User Feedback and Changing the Task Tree). Then execute the frontier in the current execution mode (`superRA:using-superra/references/main-agent.md` §Execution Modes).

## Grilling

**Put every unsettled decision to the researcher in frontier-ordered rounds**, each question carrying your recommended answer: `references/grilling.md`. Standard and thorough depth grill by default; quick depth skips it unless the researcher asks.

## User Feedback and Changing the Task Tree

Route task-tree changes through `references/changing-the-tree.md`.
