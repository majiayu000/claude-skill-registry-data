---
name: torque:next
description: "Determine the single best next action based on current project state. Reads GSD state, SP plans, and git context to suggest exactly one command to run."
---

# Torque Next Action

Analyze project state and recommend exactly ONE next command. Think of this as a GPS for your development workflow.

## Procedure

### Step 1: Gather state

Same as `/torque:status` — read `.planning/`, `docs/plans/`, git state. But don't output the full status. Focus on determining the current position.

### Step 2: Decision tree

Work through this tree top-to-bottom. First match wins.

```
1. Is there an active bug or failing test?
   → `systematic-debugging`
   Why: Bugs block everything. Fix first.

2. Does .planning/ exist?
   ├─ YES (GSD project):
   │   a. Is there a HANDOFF.md in the active phase?
   │      → `/gsd:resume-work`
   │      Why: Paused work should be resumed before starting new work.
   │
   │   b. Is STATE.md showing a phase in "executing" with incomplete plans?
   │      → `/gsd:execute-phase` (continue)
   │      Why: Finish what you started.
   │
   │   c. Is a phase complete but not verified?
   │      → `/gsd:verify-work`
   │      Why: Verification before review.
   │
   │   d. Is a phase verified but not code-reviewed?
   │      → `requesting-code-review`
   │      Why: GSD has no review step — SP fills the gap.
   │
   │   e. Is a phase reviewed but not shipped?
   │      → `/gsd:ship` or `/gsd:pr-branch`
   │      Why: Ship cleanly — filters .planning/ commits from PR.
   │
   │   f. Are all phases in the current milestone complete?
   │      → `/gsd:audit-milestone` then `/gsd:complete-milestone`
   │      Why: Close out the milestone properly.
   │
   │   g. Is the next phase planned but not started?
   │      → `/gsd:execute-phase`
   │      Why: Plans exist, execute them.
   │
   │   h. Is the next phase discussed and spec'd but not planned?
   │      → `/gsd:plan-phase`
   │      Why: Context and spec exist, create plans.
   │
   │   h2. Is the next phase discussed but not spec'd (ambiguous scope)?
   │       → `/gsd:spec-phase`
   │       Why: Lock falsifiable requirements before planning.
   │
   │   i. Is there a next phase that hasn't been discussed?
   │      → `/gsd:discuss-phase`
   │      Why: Gather context before planning.
   │
   │   i2. Is this an AI/LLM phase that hasn't been designed?
   │       → `/gsd:ai-integration-phase`
   │       Why: Produce AI-SPEC.md with framework + eval strategy.
   │
   │   j. No more phases in roadmap?
   │      → `/gsd:new-milestone` or project complete
   │
   └─ NO (no .planning/):
       a. Does docs/plans/ exist with incomplete plans?
          → Re-read plans, continue execution
          Why: Pick up where you left off.
       
       b. No workflow state at all?
          → Ask: "New project or standalone feature?"
          → New project: `/gsd:new-project`
          → Existing codebase: `/gsd:map-codebase`
          → Quick standalone: `brainstorming`
```

### Step 3: Output format

```
## Next Action

→ `/gsd:plan-phase`

**Why**: Phase 3 ("Payment integration") has CONTEXT.md from discuss-phase
but no PLAN.md files yet. Planning is the next step before execution.

**Current position**: Milestone 1, Phase 3 of 7
**What this does**: Creates executable PLAN.md files with task breakdown,
dependencies, and wave assignments for parallel execution.
```

Keep it to ONE recommendation. If truly ambiguous, show at most two options with a clear default.

## Rules

- Never modify any files. This is read-only.
- Always explain WHY this is the next action.
- Show current position for context.
- One recommendation. Not a menu.
