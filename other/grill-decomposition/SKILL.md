---
name: grill-decomposition
description: Review the open tasks of a Kairos initiative as a set before a Ralph loop runs them — slice boundaries, order and risk, blocks edges, criteria that the loop can check, scope and repository leaks — and write each settled answer into the tasks. Pass an initiative short code.
argument-hint: "<initiative short code>"
disable-model-invocation: true
---

# Grill the tasks of an initiative

The arguments are: `$ARGUMENTS`

Run the `grilling` skill over the open tasks of one initiative, as a set. Read `grilling` first: it gives the interview loop, one question at a time. This skill says what to review and where each answer goes.

This is not a grill of each task. Most questions about one task are facts (which module, which test, which command), and you look facts up. The decisions are at the boundaries between the tasks. Expect a short session.

Tasks can come from `/kairos:decompose`, from triage, from a different session or from a person. Review them all the same way.

## 1. Load the set

1. Call `get_item` with the initiative short code (`PREFIX-I-NNNN`). If it does not find the initiative, tell the user and stop. With no argument, ask the user for the initiative. Do not guess.
2. Read the goals, the non-goals, the design and the `## Decisions` lines of the initiative. Also read its PRD and the ADRs that inform it.
3. Call `get_item` for each child task. Ignore a task in a done column. For each other task, record its column, its repository, its acceptance criteria and its `blocks` edges (both directions).
4. If each child task is in a done column, or the initiative has no child task, tell the user and point to `/kairos:decompose`. Stop.

Record the column of the initiative and of each task. At the end they must be the same.

## 2. Review the set

Ask across the whole set. Name each task by its short code, never by its place in a list ("the second task"). A task that you propose to add has no short code yet. Give it a quoted title marked "not yet created" (the `kairos-vocabulary` skill). Give your recommended answer with each question.

1. **Slice boundaries.** Is each task a vertical slice that proves something alone, or a layer that proves nothing until other tasks are done? For a layer, propose the merge or the split that makes it a slice.
2. **Order and risk.** Which task removes the most doubt? Recommend that it goes first. Then check each `blocks` edge:
   - Is it real, or only a result of how the work was cut?
   - Is an edge missing? For example, task B uses a table that task A adds. If no edge goes from A to B, propose it.
   - `/kairos:ralph-initiative` follows these edges. A wrong edge gives a wrong sequence, and a missing edge can run a task before its blocker.
3. **Done criteria.** For each acceptance criterion: can the Ralph loop show it with a command and its output, with no person? `implement` needs evidence for each criterion before it moves a task to Completed. "Works well" or "is clean" cannot be shown.
   - Propose a replacement that names a command and its output. Examples: a test that passes, a status code, a file that exists. Read [ACCEPTANCE-CRITERIA.md](../triage/ACCEPTANCE-CRITERIA.md) first.
   - A criterion that really needs a person is a manual check. Propose to move it to a `## Manual checks` list on the initiative. Put the short code of the task on it. Then the loop does not stop on it, and the user does the check after the loop.
   - Write each criterion in STE: one instruction, 20 words or fewer, one result ([the STE reference](../../../references/simplified-technical-english.md)).
4. **Scope and repositories.** Compare each task with the goals and the non-goals of the initiative.
   - Name each task that does work that a non-goal rules out.
   - Name each goal that no task covers.
   - Each task that changes code links to one repository. A task with no repository, or with a repository that is not where its code is: propose `set_repository`. A task that changes 2 repositories is 2 tasks with a `blocks` edge.
   - `/kairos:ralph-initiative` does not run a task whose repository is not this checkout. Say so.

## 3. Write as you go

When an answer settles, write it at once, before the next question:

- **A changed criterion, objective or scope:** `get_item`, then `edit_item` on the task.
- **A split or a new task:** `create_item` with `item_type: task`, `parent: <initiative>`, `board: <the board of the other tasks of the initiative>`, and `repository` when it has code. Use the task body template of `/kairos:decompose`. Name the task by the short code in the result from then on.
- **A merge:** move the text into one task with `edit_item`, then cut the other.
- **A cut task:** `cancel_item` with the reason. The task goes to the done column, marked Cancelled, and the reason stays on it. If the work comes back later, it is a new task.
- **An edge:** `link_items` or `unlink_items` with `relationship: blocks`, from the blocker to the blocked task.
- **A repository:** `set_repository`.
- **A manual check:** `edit_item` on the task to remove it, and on the initiative to add it under `## Manual checks`.

After each change to the set, read the changed tasks again. Write one short note on the initiative for each round: which tasks changed, and why.

## 4. Go back up

A design question is not a question about the cut. Examples: "a queue or a cron job?", "can a user cancel a part of an order?". When an answer shows that the design does not decide a behaviour, stop the review:

1. Do not decide it inside a task.
2. Tell the user that the design of the initiative has a gap, and name the gap.
3. Write the gap on the initiative.
4. Offer `/kairos:grill-initiative` on the initiative, or a talk with the user. Continue the review only after the design decides it.

## 5. Close

**Never call `transition_item`.** The user moves the initiative and the tasks.

When no open question is left:

1. Call `get_item` for each open task. Check that each task has one objective and criteria that a command can show. Check its repository and its `blocks` edges.
2. Give the sequence of the tasks in the order of their `blocks` edges, by short code and title. Then give what changed: the tasks added, cut, merged or split, the edges, the criteria, the manual checks.
3. Check that the initiative and each task are in the same column as at the start.
4. Ask the user to confirm. Then offer `/kairos:ralph-initiative <initiative short code>`.
