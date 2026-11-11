---
name: pair-process-plan-tasks
description: "Breaks a refined user story into implementation tasks. Task-level idempotency: detects existing tasks and creates only missing ones. Appends condensed Technical Analysis + Task Breakdown (checklist, Dependency Graph, AC Coverage table, detailed tasks) to the story body. Composes /pair-capability-write-issue to update the story issue body. Tasks are documented inline in the story — no separate task issues are created."
version: 0.4.1
author: Foomakers
---

# /pair-process-plan-tasks — Task Breakdown

Transform a refined user story into specific, actionable implementation tasks. Task-level idempotency: detects existing tasks in the story body and creates only missing ones. Appends an integrated Technical Analysis + Task Breakdown section to the story issue body. Tasks live inside the story — no separate task issues are created in the PM tool.

## Process Profile

<!-- process-step: id=plan-tasks -->

Executable form of the **`plan-tasks`** step, and a composer of `define-bounded-contexts`. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Composed Skills

| Skill          | Type       | Required                                                   |
| -------------- | ---------- | ---------------------------------------------------------- |
| `/pair-capability-write-issue` | Capability | Yes — updates the story issue body with the Task Breakdown section |

## Arguments

| Argument | Required | Description                                                                                              |
| -------- | -------- | -------------------------------------------------------------------------------------------------------- |
| `$story` | No       | Story identifier (e.g., `#42`). If omitted, selects the highest-priority Refined story from the backlog. |

## Algorithm

### Step 0: Story Selection

1. **Check**: Is `$story` provided?
2. **Skip**: If provided, load the story from the PM tool and proceed to Step 1.
3. **Act**: If not provided, query the PM tool for stories in Refined state. Apply selection criteria:
   - **Priority**: P0 > P1 > P2
   - **Sprint need**: stories required for upcoming sprint
   - **Dependency chain**: stories unblocking other work
4. **Act**: Present recommendation and ask developer to confirm:

   > Recommend task breakdown for Story `#[ID]: [Title]` (Priority: [P0/P1/P2]).
   > Reason: [business value / sprint urgency / unblocks other work].
   > Proceed?

5. **Verify**: Story selected and loaded.

### Step 1: Detect Existing Tasks

1. **Check**: Read the story body. Look for a `## Task Breakdown` section with task entries (`- [ ] **T-N**:` or `- [x] **T-N**:`).
2. **Act**: Classify the state:
   - **No Task Breakdown section** → full breakdown needed (Steps 2–6).
   - **Partial tasks** (some T-N entries but gaps in AC coverage) → resume from first missing task (Steps 3–6).
   - **All tasks present with full AC coverage** → already complete. Offer selective update (Step 7).
3. **Verify**: Task state determined. Report:

   > Task state: [N existing tasks covering M/K ACs]. [Full breakdown | Resume from T-X | Already complete — offering update].

### Step 2: Technical Context Analysis

**Skip if**: Story body already contains Technical Analysis section.

1. **Act**: Analyze the story requirements against adoption files:
   - Read [architecture.md](../../../.pair/adoption/tech/architecture.md) for architectural patterns.
   - Read [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) for implementation choices.
   - Identify affected system areas (services/modules) relevant to the story.
2. **Act**: Present technical context summary to developer for validation.
3. **Verify**: Developer approves. Context established.

### Step 3: Task Identification

1. **Act**: Decompose the story into tasks by mapping acceptance criteria to implementation work:
   - Map each AC to one or more tasks.
   - Group tasks by system area (service/module) where helpful.
   - Identify task types: Development, Documentation, Configuration, Research.
   - Ensure every AC is covered by at least one task.
2. **Act**: Identify dependencies between tasks and determine execution order.
3. **Act**: Present task list to developer:

   > Proposed [N] tasks for `#[ID]`:
   > [Numbered list with task title, type, system area, estimated hours]
   > AC coverage: [all ACs mapped]
   > Approve or adjust?

4. **Verify**: Developer approves. Task list finalized.

### Step 4: Task Definition

For each task (skipping tasks that already exist in the story body):

1. **Act**: Define the task following the [task-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/task-template.md):
   - Task Information (ID, priority, hours, system area)
   - Summary and type
   - Description with implementation context
   - Acceptance criteria (deliverable, quality, integration, verification)
   - Implementation approach (design, modules, files, standards)
   - Dependencies (technical, task, resource)
   - Implementation steps
   - Testing strategy
2. **Verify**: Each task is complete and self-contained.

### Step 5: Assemble Task Breakdown Section

1. **Act**: Build the complete Task Breakdown section for the story body:
   - **Condensed Technical Analysis**: Keep strategy summary, data flow/pipeline order, key risks. Remove verbose detail.
   - **Task checklist**: `- [ ] **T-N**: [Title]` for each task.
   - **Dependency Graph**: ASCII block showing task dependencies (see [task-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/task-template.md) Task Breakdown Format).
   - **AC Coverage table**: Maps each AC to covering tasks.
   - **Detailed tasks**: Full task definition per task (from Step 4).

   Section ordering in the story body: Technical Analysis and Task Breakdown are the last content sections (after Notes, before footer).

2. **Verify**: All ACs covered. Dependency graph consistent with task dependencies. No orphan tasks.

### Step 6: PM Tool Update

1. **Act**: Compose `/pair-capability-write-issue` with `$type: story`, `$id: [story-id]` to append the Task Breakdown section to the story body. Tasks are documented inline in the story — do NOT create separate task issues.
2. **Verify**: Story body updated with Task Breakdown section.

### Step 7: Already-Complete Update (optional path)

Reached only when Step 1 detects all tasks are present with full AC coverage.

1. **Act**: Ask the developer what to update:

   > Story `#[ID]` already has a complete task breakdown. What needs updating?
   > 1. Add new tasks (new AC or scope change)
   > 2. Modify existing task definitions
   > 3. Update dependency graph
   > 4. Full re-breakdown

2. **Act**: For selected option, re-execute the corresponding steps.
3. **Act**: Compose `/pair-capability-write-issue` with `$type: story`, `$id: [story-id]`, and updated content.
4. **Verify**: Story updated.

## Output Format

```text
TASK BREAKDOWN COMPLETE:
├── Story:      [#ID: Title]
├── Tasks:      [N tasks created]
├── Types:      [Development: N, Documentation: N, Configuration: N]
├── AC Coverage:[K/K ACs covered]
├── PM Tool:    [Story updated with Task Breakdown section]
└── Next:       /pair-process-implement to start task execution
```

## HALT Conditions

- **No Refined stories in backlog** (Step 0) — nothing to break down.
- **Story not found or not Refined** (Step 0) — must be refined first (suggest `/pair-process-refine-story`).
- **PM tool not accessible** — cannot read or update stories.
- **Developer rejects task list** (Step 3) — must resolve before proceeding.
- **AC coverage gap** (Step 5) — every AC must be covered by at least one task.

## Graceful Degradation

- If `/pair-capability-write-issue` is not installed, warn and provide the formatted Task Breakdown section for manual PM tool update.
- If the PM tool is not accessible, produce the task breakdown content and ask the developer to update manually.
- If adoption files (architecture, tech-stack) are not found, skip technical context alignment and warn.

## Notes

- This skill **modifies PM tool state** — it updates the story body with the Task Breakdown section. No separate task issues are created.
- Task-level idempotency: re-invoking on a story with partial tasks appends only missing ones to the story body.
- The integrated Technical Analysis + Task Breakdown format positions these as the last content sections in the story body (functional sections first, technical sections last).
- Condensed TA retains: strategy summary, data flow/pipeline order, key risks. Removes verbose implementation detail that belongs in individual tasks.
- Task template reference: [task-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/task-template.md).
- Story template reference: [user-story-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/user-story-template.md).
