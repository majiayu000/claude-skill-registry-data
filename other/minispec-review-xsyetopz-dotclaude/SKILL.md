---
name: minispec-review
description: Reviews a finished MiniSpec change with an agent that did not write it, then archives the change. Use when each task of a change in `minispec/changes/` is checked.
argument-hint: "[change name]"
allowed-tools: Bash(minispec *)
---

<task>
Get a review of the finished change from the `reviewer` agent, fix what it finds, and archive the change.
The writer of a change does not approve its own work, so you do not give the verdict.
</task>

<procedure>

1. Start the `reviewer` agent with `run_in_background` set to `false`, so the verdict comes back in this turn.
   Do not end your turn before the verdict comes.
   In the brief, give the path of the change folder, the lens (`code` for the diff, and `plan` when the plan changed), and the range of the diff.
   Do not give your own view of the result, because the agent must judge the result and not the story.
   The agent works in the same linked worktree, and it needs no clean main checkout.
2. Read the verdict.
   - `No blocking issues`: go to step 3.
   - `Issues found`: for each blocking or should-fix finding, add a task with a check command to `tasks.md`, then use the skill `minispec-apply`.
     Ask for a new review after the fixes.
   - `Could not review`: say why in your report, and ask the user.
3. Archive the change after the user agrees, or at once when the user asked for the archive:

   ```bash
   minispec archive <name> --yes
   ```

   The command merges the spec deltas into `minispec/specs/` and moves the change to `minispec/changes/archive/`.
4. Report the verdict, the findings that you fixed, and the archive path.
</procedure>
