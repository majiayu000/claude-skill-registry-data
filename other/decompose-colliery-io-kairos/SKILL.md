---
name: decompose
description: Break an initiative, plan, or PRD into independently-grabbable Kairos tasks using tracer-bullet vertical slices.
argument-hint: "Initiative or document short code (optional if it's already in the conversation)"
disable-model-invocation: true
---

# Decompose

Break a plan into independently-grabbable Kairos tasks using vertical slices (tracer bullets).

## Process

### 1. Gather context

Work from whatever is already in the conversation. If the user passes a short code as an argument, `get_item` it — and if it's an initiative whose relationships list an attached PRD, `get_item` that too — and read the full content. If neither an argument nor a plan in the conversation exists, ask the user what to decompose.

### 2. Explore the codebase (if not already done)

If you have not already explored the codebase, do so to understand the current state of the code. Task titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft the tasks

Break the plan into **tracer bullet** tasks, following the **Vertical slice rules**. A **wide refactor** is the exception to that rule — slice it by **expand–contract** instead (see **Wide refactors**). Prefactoring becomes its own leading task(s) that the slices it enables block on. Every user story in the source material maps to a slice or goes on an explicit uncovered list.

### 4. Quiz the user

Present the proposed breakdown as a list of quoted titles, each marked "not yet created". The tasks do not exist yet, so they have no short code. Do not give them a temporary name ("Slice 1", "T1", "task A"). A number in the list is for the user's answer in this message only. For each proposed task, show:

- **Title**: the full title in quotes, in the domain glossary's words
- **Blocked by**: the quoted titles of the proposed tasks that must complete first, or the short codes of existing items
- **User stories covered**: the user stories that the task covers, as the short code of the PRD and the story number. Also show the stories that no task covers, so that nothing vanishes silently

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any tasks be merged or split further?

Iterate until the user approves the breakdown. The naming rules are in the `kairos-vocabulary` skill.

### 5. Publish the tasks to Kairos

Every task names a **board** (COLLIERY-A-0023): the team decides the board, and the board decides the team of the task. Default to the session's `team_board` (SessionStart context). With no `team_board`, find the board with `my_boards`. If more than one can hold the work, ask the user which. A slice for a different team is a **request**: name the delivery board of that team, and follow [CROSS-TEAM-FILING.md](../implement/CROSS-TEAM-FILING.md).

The **repository** is an optional link to the repo where an agent implements the task. It does not choose the board. Default to the session's `repository`. When the initiative spans repositories, ask the user which repo holds each slice. A slice that "touches both" is two slices, one per repo, joined by a `blocks` edge. `list_repositories` shows the directory.

Publish in dependency order — blockers first — so every blocking edge names a real short code. For each approved slice:

- `create_item(item_type: task, board: <delivery board>, repository: <slug>, parent: <initiative short code>, title: ..., content: ...)` using the **Task body template** (omit `repository` when the task has no code). The `parent` edge links the task to its initiative — the body carries no parent section.
- For each of its blockers: `link_items(source: <blocker short code>, target: <this task's short code>, relationship: blocks)`.

Columns and blocking edges are native to Kairos — new tasks go to the entry column of the board, and that's where they belong; leave them for the team to pull. The initiative itself stays untouched: decompose only adds children.

From here on, name each task only by the short code in the result of its `create_item`. Do not use its working title or its number in the step 4 list.

Finish by listing the created short codes in dependency order, each with its board and its repository (and, for a request, a note that it is in the support lane of that team).

Then offer `/kairos:grill-decomposition <initiative short code>`. It reviews the tasks as a set before a Ralph loop runs them: the slice boundaries, the `blocks` edges, criteria that the loop can check, and scope leaks.

## Reference

### Vertical slice rules

Each task is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Any prefactoring should be done first

### Wide refactors

A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own task blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a task blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify task — green is promised only there.

### Task body template

<task-template>
## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced code that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), add a context pointer to where that prototype code lives rather than inlining it.

## Acceptance criteria

Write them in Simplified Technical English: [The Simplified Technical English reference](../../../references/simplified-technical-english.md) (KAIROS-S-0009) is the source of truth. A criterion is a testable instruction, so it is procedural text — one instruction per criterion, active voice, present tense, 20 words or fewer, and the domain terms from section 4 rather than a synonym. A criterion nobody can read twice the same way is not a contract.

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
</task-template>
