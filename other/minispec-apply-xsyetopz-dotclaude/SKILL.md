---
name: minispec-apply
description: Does the tasks of a MiniSpec change one at a time, runs the check of each task, and marks it done only after the check passes. Use when a change in `minispec/changes/` has open tasks, or after a handoff during a change.
argument-hint: "[change name]"
allowed-tools: Bash(minispec *)
---

<task>
Do the open tasks of a MiniSpec change in order.
The checked tasks in `tasks.md` are the record of the done work.
Each checked task is done and verified, so do not run its check again unless the user asks.
</task>

<procedure>

1. Find the state.
   Read `tasks.md`: the checked tasks are done, and the first open task is next.
   After a handoff, the handoff file `minispec/changes/<name>/handoff.md` names the same task.
   Run `minispec status <name>` only when `tasks.md` is not clear.
2. Read the files that the task needs: `proposal.md`, the spec, and `design.md` when they exist.
3. Do the task.
   Make only the change that the task names.
4. Run the check of the task.
   - The check is a command, so run it alone and read its result.
     The tool result shows the exit code, so do not add `echo $?`.
   - The task has no check, or the check is in prose: do not mark the task done.
     Report that the task has no runnable check, and write a command as the check in `tasks.md`.
   - The check fails: fix the cause and run it again.
5. Mark the task done in `tasks.md` by changing `- [ ]` to `- [x]`, only after the check passed.
6. Go to the next open task.
   When no task is open, use the skill `minispec-review`.
</procedure>

<back_to_planning>
A change can go back to planning from any step.
When you find during the work that a spec, the design, or the tasks are wrong:

1. Stop the work on the task.
2. Edit the wrong file now, so the edited plan replaces the old plan.
   Add, change, or remove tasks in `tasks.md`.
   Keep the tasks that are checked and still true.
3. Go on with the next open task.
   `minispec validate <name>` runs once, at the end, in `minispec archive`.

Do not keep two plans, and do not work around a wrong spec.
</back_to_planning>

<worktree>
Work in the linked worktree where you are.
`minispec` finds the root of that worktree, so it needs no clean main checkout and no folder outside the worktree.
</worktree>

<rules>
Do the task that is open, and do not widen it.
Do not mark a task done to move on.
The writer of the work does not approve it, so the review goes to another agent.
</rules>
