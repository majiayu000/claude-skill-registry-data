---
name: session-status
description: >-
  Use when a session must record and report its own state — writes a Status
  block into its task file and opens the report with the state, the operator's
  part and what is left. Not for the project task list (tasks-overview) or goal
  check (check-goals).
---

# Session Status

## Overview

Writes the state of the current session into its task file and reports it in a
fixed order. The report opens with three lines — the state, what the session
needs from the operator, and how much is left — so that whoever sees only the
beginning of the message still sees what matters.

## Context

<context>
A session that says "done" or goes quiet leaves the reader guessing: finished,
waiting for an answer, or stopped half-way. Checkboxes in the task file say
what is delivered; they cannot say that the session is blocked, what it never
verified, or what the operator told it directly. This skill records exactly
that in a `## Status` section of the session's task file (the `tasks` role
from the project instructions).

It works in any single session. In a swarm — one manager session and its child
sessions — a child runs it before the end of every turn: the manager builds
its board from these files, and a host that notifies the manager of a finished
turn usually quotes only the beginning of the child's last message.
</context>

## Rules & Constraints

<rules>
1. **Only the task file is edited.** Do not continue the task, fix anything or
   touch another file inside this skill.
2. **Four states, nothing else**: `working`, `blocked on operator`, `done`,
   `failed`. Never write a state of your own wording, and never write
   `stalled` — only a manager derives that, from outside.
3. **A box is ticked only on evidence observed in this session.** Tick a
   Definition-of-Done item when this session delivered it and you saw the
   proof (a command result, the file). Never untick an item, and never tick
   one on the strength of a plan or a claim.
4. **`done` needs every item ticked.** With one item unticked the state is
   `working`, `blocked on operator` or `failed`.
5. **Unchecked is named, not hidden.** Anything delivered but not checked goes
   into `Not verified:`. "Nothing" is written only when nothing is unchecked.
6. **The three opening lines come first in the message**, before any greeting,
   summary or explanation.
7. **No task file → no invented one.** If the session has no task file and the
   user names none, say so in one line, give the report in chat only, and
   stop.
</rules>

## Instructions

<step_by_step>

1. **Find the task file of this session**
   - The file the user names; else the task file this session has been working on; else the one whose path the session was started with.
   - Read it from disk now. Do not rely on memory of its contents.

2. **Establish the facts**
   - **Done and left**: go through the Definition-of-Done items. Apply rule 3 to items this session delivered. Count the ticked items and the total.
   - **State**: `blocked on operator` when the session cannot make its next step without an answer, a decision, an approval or an action that only the operator can give; `failed` when the work cannot be completed as assigned; `done` when every item is ticked; otherwise `working`.
   - **Needs from the operator**: the concrete thing — the question with its options, the approval, the secret, the manual step — written so that the operator can act on it without opening the session. "Nothing" when nothing is needed.
   - **Not verified**: every claim of this session that was not checked.
   - **Follow-ups**: things noticed for later that are outside this task.
   - **Branch**: run `git branch --show-current` and `git status --porcelain`; when the branch has an upstream, `git rev-list --count @{u}..HEAD`. Say: the branch, whether the session's work is committed, whether it is pushed, and whether it is merged into the main branch when you can tell.
   - **Told directly by the operator**: instructions and decisions the operator gave in THIS session that change the assignment or that others who share the task should know. "Nothing" when there are none.

3. **Write the task file**
   - Add each follow-up as a bullet under `## Follow-ups` (create the section if it is missing). Do not duplicate a bullet that is already there.
   - Create or replace the `## Status` section, as the last section of the file, with exactly these plain bullets (not checkboxes):

     ```markdown
     ## Status

     - State: <working | blocked on operator | done | failed>
     - Needs from the operator: <the concrete thing, or "nothing">
     - Not verified: <list, or "nothing">
     - Branch: <branch; committed or not; pushed or not; merged or not>
     - Told directly by the operator: <list, or "nothing">
     - Updated: <date and time, from the `date` command>
     ```

   - Replace the old values; the section holds the current state, not a history.

4. **Commit the task file when the session has its own worktree**
   - Check: `git rev-parse --git-dir` and `git rev-parse --git-common-dir` print different paths → this session works in a worktree of its own. Others cannot see its working tree, so commit the task file alone, by explicit path: `git commit <task file> -m "docs(tasks): update session status"`.
   - Same path → a shared checkout. Do not commit; the file is read in place.

5. **Report**
   - The message begins with these three lines and nothing before them:
     1. `State: <state>`
     2. `Needs from the operator: <the concrete thing, or "nothing">`
     3. `Left: <N> of <M> Definition-of-Done items; not verified: <K>`
   - Then, each under its own short label: what is done; what is left; what is not verified; follow-ups; the branch line.
   - In a swarm: the last message of the turn is this report — begin that message with the same three lines.
   - Stop here. Do not go on with the task unless the user asks.

</step_by_step>

## Verification

<verification>
- [ ] The task file has a `## Status` section with the six labelled bullets and one of the four states.
- [ ] No Definition-of-Done item was ticked without evidence seen in this session; none was unticked.
- [ ] Every unchecked claim is under `Not verified:`; every follow-up is under `## Follow-ups`.
- [ ] No file other than the task file was edited; a commit was made only in an own worktree, and only of the task file.
- [ ] The message begins with the three lines: state, needs from the operator, counts.
</verification>
