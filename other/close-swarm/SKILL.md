---
name: close-swarm
description: >-
  Use when a manager session is asked to close its child sessions — checks that
  no child work is lost, moves follow-ups into the manager's task file, settles
  branches and worktrees, archives sessions. Not for finishing this session
  (finish-session).
---

# Close the Swarm

## Overview

Closes child sessions of a swarm — one named child, the finished ones, or all —
without losing what they did. For every child it checks what could be lost,
carries the child's follow-ups into the manager's task file, settles the
branch and the worktree, marks the row closed and archives the session. It
ends with the list of everything still open.

## Context

<context>
A swarm is one manager session and the child sessions it started. Its ledger
is the manager's task file: `## Swarm` holds one bullet per child with the
child's task file, branch and worktree; each child keeps a `## Status` section
and its Definition-of-Done checkboxes in its own task file.

Each session finishes ITSELF with `finish-session`: goal check, commit, push,
archive. A child runs it as the last step of its work; the manager runs it
after the swarm is closed. This skill does not repeat that work. It does what
no single session can do for itself: look across the children, make sure
nothing is left on an unmerged branch, in an uncommitted file or in a report
that disappears with the session, and keep the ledger true.

What gets lost without it: follow-ups that live only in a child's last
message, branches nobody merged, worktrees left on disk, sessions never
archived.
</context>

## Rules & Constraints

<rules>
1. **Files, not memory.** Start from the manager's task file on disk.
2. **Only a finished child is closed.** Finished means: state `done`, every
   Definition-of-Done item ticked, its work committed. Anything else stays
   open and is listed with what is missing.
3. **Never close or archive a child that is `blocked on operator`.** It waits
   for an answer; closing it throws the question away.
4. **Nothing is destroyed to get a clean list.** Never remove a worktree that
   has uncommitted files or an unmerged branch. Never delete a branch that is
   not merged. Never stash, reset or discard a child's files.
5. **The branch is the operator's decision.** An unmerged branch is settled by
   the operator: merge it, drop it, or keep it. Do not merge on your own, and
   do not push to the main branch. Ask, and leave the child open until the
   answer comes.
6. **No re-run of the child's evidence.** State as fact only what git proves —
   committed, pushed, merged. Every other claim of the child is carried as
   `by the child's report`. Its checks can take hours and are its own job.
7. **Do not finish the child's work.** An unfinished child is asked to finish;
   the manager does not edit the child's code or tick its boxes.
8. **A host tool that refuses is reported verbatim**, and that row stays as it
   was.
9. **Commit the manager's file by explicit path.** Never `git add -A`.
</rules>

## Instructions

<step_by_step>

1. **Read the ledger and pick the children**
   - Read the manager's task file from disk. No `## Swarm` section → say so in one line and stop.
   - The children to close: the one the operator named; or every child when the operator asked to close the swarm or everything that can be closed. Rows already marked `closed` are skipped.
   - Find the main branch: `git symbolic-ref --short refs/remotes/origin/HEAD` when there is a remote, else the branch the manager's checkout is on.

2. **Nothing-lost check — for every picked child, before anything is changed**
   - Read the child's task file: from the working tree for a shared checkout, from its branch (`git show <branch>:<path>`) for a child with its own branch, and from its worktree when the file is modified there.
   - Collect, per child:
     - the state, and the unticked Definition-of-Done items;
     - uncommitted files: `git -C <worktree> status --porcelain` for its own worktree; in a shared checkout, uncommitted changes to the files the child owns;
     - commits not pushed: no remote branch for its branch, or `git rev-list --count origin/<branch>..<branch>` above zero (say "no remote" when the repository has none);
     - a branch not merged: `git rev-list --count <main>..<branch>` above zero;
     - follow-ups in its file that are not yet in the manager's file;
     - a session still open, where the host can tell. A tool that lists the subagents of THIS session cannot tell: a child session is a separate session, and "not in that list" says nothing about it.
   - Print this as one block under its own title, `Could be lost`, before you close anything, and keep that block in the final message, apart from `Still open`. An empty list is still printed, as the line `Could be lost: nothing`. Name every item in this block itself — the file, the branch, the child — even when the same item appears again under `Still open`; never replace it with a pointer to another part of the message.

3. **Sort each child**
   - `blocked on operator` → not closed (rule 3). Name the question it waits for.
   - Not finished — state not `done`, an item unticked, or uncommitted files → not closed. The child ends its own work with `finish-session`. Where the host has a tool that sends a message to a session, send the child that request; where it has none, say in one line that the operator passes it on. Do not close it from outside.
   - Finished, own branch not merged → not closed yet (rule 5). Ask the operator: merge, drop or keep. Stop on this child until the answer.
   - Finished, and its branch is merged, or the operator has decided to drop or keep it, or it worked in the shared checkout with everything committed → close it, step 4.

4. **Close a finished child**
   - Move every bullet of the child's `## Follow-ups` into `## Follow-ups` of the manager's file, each marked with the child it came from: `- <follow-up> (from <child title>, <child task file>)`. Carry the child's `Not verified:` items the same way — they are open questions too.
   - Remove its worktree when it has one, the worktree is clean and the branch is merged or dropped by the operator's decision: `git worktree remove <path>`. Delete the branch only when it is merged (`git branch -d`), or dropped on the operator's word.
   - Mark the child's bullet under `## Swarm` with `closed` and the date.
   - Archive the session: look at the tools of this session for one that archives another session (e.g. a session-archive tool in the Claude desktop app). It exists and the child's `finish-session` has not archived the session already → archive it. No such tool → say in one line that this host cannot archive a session from here and the operator archives it in the host's interface.
   - Commit the manager's task file alone: `git commit <manager task file> -m "docs(tasks): close child <title>"`.

5. **Report what is still open**
   - Order of the message: `Could be lost`; what was closed; any question to the operator (the decision about a branch); then `Still open`. The message ends with a list titled `Still open`:
     - every `## Swarm` row not closed, with the reason;
     - every unmerged branch of the swarm;
     - every remaining worktree of the swarm (`git worktree list`);
     - every item of `Could be lost` that still holds.
   - `Still open: nothing` only when all four are empty.
   - The manager's Definition-of-Done item `Swarm closed` is ticked only when `Still open` is empty — tick it and commit the manager's task file again, by explicit path. Otherwise leave it unticked.
   - Last line: when nothing is open, say that the manager's own final check and commit is `finish-session` in this session — it checks the manager's Definition of Done and commits the ledger. When something is open, say that `finish-session` will stop on the `Swarm closed` item until it is settled.
   - Do not run `finish-session` yourself from here; the operator asks for it.

</step_by_step>

## Verification

<verification>
- [ ] The `Could be lost` list was printed before any child was closed.
- [ ] No child was closed that is `blocked on operator`, unfinished, or has an unmerged branch without the operator's decision.
- [ ] No worktree with uncommitted files was removed; no unmerged branch was deleted or merged by the manager.
- [ ] Every closed child's follow-ups are in the manager's `## Follow-ups`, marked with the child.
- [ ] Every closed row is marked `closed`; the manager's file was committed by explicit path.
- [ ] The session was archived with the host's tool, or the one-line notice was given.
- [ ] The message ends with `Still open`, and `Swarm closed` is ticked only when that list is empty.
</verification>
