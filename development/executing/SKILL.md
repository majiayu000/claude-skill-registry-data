---
name: executing
description: >-
  Runs a written plan task by task with checks and a final review. Use when a plan exists and the user says go, implement it, execute the plan, or build the planned feature. Not for writing plans, single edits or reviews.
license: Apache-2.0
metadata:
  level: "process"
  uses: "tdd debugging reviewing committing documenting"
  agents: "implementer reviewer explorer"
  tokens: "786"
---

Execute `docs/plans/<feature>/plan.md` task by task, verify each result yourself, review the whole feature once, and close the plan.

Uses: foma-skills:tdd (test-first tasks), foma-skills:debugging (a failure you don't understand), foma-skills:reviewing (final pass), foma-skills:committing (commit rule), foma-skills:documenting (decisions found); agents `implementer`, `reviewer`, `explorer` (wide code search).

## Steps
1. Find the plan: `## Where things live` in CLAUDE.md, else `docs/plans/<feature>/plan.md`. None: say so and point to foma-skills:planning, or do it directly if the change is small. Read the plan once. Resume at the first task whose Status is not `done`. `Started:` empty → set it to now (`date '+%F %H:%M'`).
2. Choose the path and say it in one line: 1–2 tasks → inline, you do them; more → one `implementer` agent per task, run one at a time.
3. Appetite check before each task (plan has `Appetite:`): time since `Started:` plus the work left clearly past the budget → stop, say how far over and offer the `cut first` item; the user picks. Cut: mark that item cut in the plan and go on. Extend: ask the new budget, replace `Appetite:` and reset `Started:` to now. Continue: append `— continue ok` to `Appetite:`. A plan whose `Appetite:` ends with `continue ok` is not checked again.
4. Per task: set `Status: doing` in the plan, then run it.
   - Inline: follow Steps, test-first where the task says so.
   - Agent: call the `implementer` agent with the Agent `model` param from the task's `Model:` line and a self-contained brief. Agent missing from `.claude/agents/`: use a general-purpose subagent with the same brief and say once that `/foma-skills:groundwork` installs them.
5. Check "Done when" yourself: read the diff (`git diff`), run the typecheck and the targeted test from CLAUDE.md `## Commands`. Pass → `Status: done`. Fail → one retry with the failure in the brief. Failing twice → `Status: blocked` plus the reason, stop, ask the user. A failing test you can't explain: foma-skills:debugging.
6. After the last task: run the full suite once, then one `reviewer` agent for the whole feature (brief: plan path, diff range). Fix must-fix findings, re-run the suite.
7. Commits via foma-skills:committing: per task only if CLAUDE.md says so, otherwise propose one at the end.
8. Close: append one retro line to the plan (what slowed us, what to change), move the plan folder to `docs/plans/archive/`. Decisions found on the way: foma-skills:documenting. Skip the move if any task is blocked.

## Rules
- Never trust an agent's report; read the diff and run the check.
- Keep tasks in plan order; deviate from the plan only after telling the user, with the reason.
- Per task run typecheck and one targeted test, not the whole suite.
- Never push; never commit unless the project's rule says so.
- Don't implement a delegated task yourself; re-brief or block it.

If you delegate a task to an agent, read `references/brief.md` for the brief template.

## Report
- Tasks: done N, blocked N (reasons).
- Review verdict and findings fixed.
- Suite: command, result.
- Retro: the one line.
- Not checked: <…>
