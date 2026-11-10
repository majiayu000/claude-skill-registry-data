---
name: spec-implement
description: >
  Orchestrate parallel implementation of a feature specification by dispatching coder agents
  batch-by-batch with code review gates between batches. Use this skill when the user says
  "implement this feature", "start implementing", "run the spec", "execute the plan",
  "continue implementing", "approved, run it through", or wants to begin coding a previously planned feature from a
  specs/{feature}/ folder. Also use when the user says "/spec-implement" (or their host's
  equivalent invocation syntax) or drags a spec folder into the conversation and asks to
  implement it. This skill does NOT write code itself — it orchestrates coder subagents that
  work in parallel.
license: MIT
---

# Implement Feature

Orchestrate the parallel implementation of a feature specification by dispatching coder agents batch-by-batch. This skill reads a spec folder (created by `spec-create`), identifies the next batch of parallelizable work, spawns coder agents for each task, and runs a code review gate before moving to the next batch.

The orchestrator never writes code itself. Its job is to:
1. Parse the spec and determine what to do next
2. Give each coder agent exactly the context it needs
3. Verify the results via code review
4. Manage the fix loop if review finds issues
5. Track progress and commit completed batches

## Project config (read first)

Load `.spec-driven.yml`: walk up from the current directory to the home folder, and the first one
found wins (a `multi-repo` config only applies inside the repos it lists). If none is found, check
`~/.spec-driven/workspaces.json`, which maps each multi-repo config to its repo paths. Use the config
whose repos contain the current directory, because a workspace's repos can live in unrelated folders. Its values beat anything
you would detect or assume. This skill uses `layout`/`repos`, `commands` (lint/typecheck/test per repo or package), and `git.commit_style`.

**Multi-repo:** create worktrees in each repo a task touches, run each repo's own commands in review, and make the batch commit in every repo that changed, using the same subject line.

**No config?** If the `spec-setup` skill is available, run it first, then continue here. If it
isn't, detect what this skill needs from the repo, ask about anything ambiguous, and offer to save
the answers to `.spec-driven.yml` (keys: `layout`, `repos`, `tracker`, `git`, `commands`,
`specs_dir`).

## Orchestration Model

This skill's parallelism assumes your host can run multiple independent agents at once —
Claude Code's Agent/Task tool, Codex CLI's `spawn_agent`/`wait_agent`, Cursor's Subagents or
Background Agents, Antigravity's `invoke_subagent`, or whatever equivalent your host provides.
Use that mechanism throughout; give each dispatched agent only the context specified in Step 4
below, never the full conversation history.

If your host has no such mechanism, fall back to processing each batch's tasks sequentially in
the current session — implement one task fully, then the next — rather than skipping the batch.
The review gate (Step 6) still applies; run it as a distinct pass with a fresh, unbiased read of
the diff, even without a separate agent to run it in.

## Prerequisites

A `specs/{feature}/` directory containing:
- `README.md` with batch assignments and task status checkboxes
- `requirements.md` with feature context
- `tasks/task-{nn}-*.md` files (one per task, self-contained)

This structure is produced by the `spec-create` skill. If the user doesn't have a spec folder, suggest they create one first.

## Orchestration

### Step 1: Load the Spec

1. Read `specs/{feature}/README.md`
2. Read `specs/{feature}/requirements.md`
3. Parse the **Task Status** section in the README — look at the checkboxes:
   - `- [x]` = completed task (skip)
   - `- [ ]` = pending task (include)
4. Determine the **current batch**: the first batch that has any incomplete tasks
5. If all tasks in all batches are complete, report "All tasks complete!" and stop

This makes the skill **resumable** — if invoked on a partially completed spec, it picks up exactly where it left off.

### Step 2: Process Each Batch

For each batch starting from the current one, execute Steps 3 through 8 below, then advance to the next batch.

### Step 3: Prepare Batch Tasks

1. Read all incomplete task files for this batch from the `tasks/` subfolder
2. **Check for file overlaps**: scan the "Files to Create" and "Files to Modify" sections across all tasks in this batch. If any file appears in more than one task, warn the user:

   ```
   Warning: File overlap detected in Batch {N}:
   - {file-path} is modified by both task-{nn} and task-{mm}

   Options:
   1. Proceed anyway (risk of conflicts)
   2. Run these tasks sequentially instead of in parallel
   ```

   Wait for the user's decision before proceeding.

### Step 4: Dispatch Coder Agents

For each task in the batch, delegate the work to an independent agent using your host's
parallel-agent mechanism (see Orchestration Model above). Dispatch every task in the batch at
once so they run concurrently — or, without a parallel-agent mechanism, work through them one
at a time in the current session.

Read `references/coder-prompt-template.md` and construct each agent's prompt by filling in:
- **{requirements}**: full text of `requirements.md`
- **{completed_tasks_summary}**: for each previously completed task, a one-paragraph summary of what was implemented and what files were created/modified (extract from the task file's Description section plus any completion notes)
- **{task_content}**: full text of the task file being assigned

The coder agents should NOT commit their changes — the orchestrator handles commits after review.

**Pick each coder's model and effort from the task's tier.** Read the task's `## Complexity` tier
(treat a missing tier as `standard`), then look up `.spec-driven.yml` → `models.<tool>.<tier>` and
`effort.<tier>`, where `<tool>` is the host you're running in (`claude`, `codex`, `cursor`,
`antigravity`). Without those sections, use these defaults: Claude Code `light → haiku/low`,
`standard → sonnet/medium`, `deep → opus/high`; other hosts use the session's model.

- **Host can set a model per agent** (e.g. Claude Code's Agent tool `model` and `effort`
  parameters): dispatch each coder with its tier's model and effort.
- **Model not available** (not on your plan or provider, or rejected by the host): fall back to the
  session's model, say which task fell back and why, and suggest fixing `models:`. Don't stop the
  batch for this.
- **Host can't** (one model per session, as in Cursor or Codex): don't silently run deep tasks on a
  light model. Before dispatching a batch, compare its highest tier with the model you're running
  on. If the batch needs a stronger one, stop and say:
  `Batch {N} has deep tasks ({task-nn: reason}). Switch to {models.<tool>.deep} for this batch, then
  say "continue".` If the batch only has light tasks and you're on the deep model, mention that a
  cheaper model would do, but carry on.
- If the mapped value is `default`, use whatever model the session already runs, without
  recommending a switch.

Report the model used for each task in the batch summary.

**Isolate parallel coders in git worktrees when the host allows it.** Coders sharing one working
tree can clobber each other's edits and each other's lint/test runs. If your host can run an agent
in its own worktree (e.g. Claude Code's `isolation: "worktree"`), use it for every coder in a
batch of 2+ tasks; otherwise create them yourself — `git worktree add -b spec/{feature}/task-{nn}
../.worktrees/{feature}-task-{nn} HEAD` — and point each coder at its path. A single-task batch, or
a host with no way to give an agent a different working directory, runs in the main tree as before.

When the batch's coders finish, bring their work back into the main tree before the review gate:
commit inside each worktree (`wip: task-{nn}`), then `git merge --squash` each task branch into the
feature branch in task order, leaving the result unstaged. A merge conflict means the batch's tasks
weren't independent — stop, show the conflicting files, and ask the user how to resolve them. Remove
the worktrees and their branches (`git worktree remove`, `git branch -D`) once merged.

### Step 5: Collect Results

Wait for all coder agents in the batch to complete. Each agent should report:
- Files created
- Files modified
- A summary of what was implemented

If any agent fails (returns an error or crashes), note the failure and continue with the remaining results. Report the failure to the user after the batch.

### Step 6: Code Review Gate

Dispatch a single review pass in a fresh agent/session — not one of the coder agents from
Step 4, since the review needs an unbiased read of the diff it didn't write. Use your host's
parallel-agent mechanism if it supports spawning a distinct reviewer agent; otherwise perform
the review directly in the current session as its own clearly delimited pass.

Read `references/review-prompt-template.md` and construct the review prompt by filling in:
- **{batch_number}**: current batch number
- **{requirements}**: full text of `requirements.md`
- **{task_summaries}**: for each task in this batch, the task title and the coder agent's completion summary
- **{verification_commands}**: `commands.lint`/`typecheck`/`test` from `.spec-driven.yml` for each repo or package touched, or the project's own commands if there's no config (e.g., `pnpm lint && pnpm typecheck && pnpm test`)

Run the reviewer on the model for the **highest tier in the batch**, and never below `standard`: the
review is where deep mistakes get caught.

The review agent should:
1. Run lint, typecheck, and tests
2. Verify acceptance criteria and the tests named in each task file
3. Check that files integrate correctly (imports resolve, types match)
4. Check for security issues and code quality
5. Return a structured verdict: **PASS** or **FAIL** with specific issues

### Step 7: Fix Loop

If the review returns **FAIL**:

1. Parse the issues from the review (file paths, descriptions, suggested fixes)
2. Group issues by the task they most closely relate to (match file paths against each task's "Files to Create/Modify")
3. For each group, dispatch a coder agent (same mechanism as Step 4) with a fix prompt. Read `references/fix-prompt-template.md` and fill in:
   - **{issues}**: the specific issues for this task group
   - **{task_content}**: the original task file for context
4. After fix agents complete, re-run the review (Step 6)
5. **Escalate on repeat failure.** If a task's issues survive a fix cycle, run its next fix one tier
   higher (`light → standard → deep`). A `deep` task that still fails goes to `models.<tool>.escalate`
   (e.g. `fable`) at `effort.escalate`, if it's set and not `default`. Ask first if that model can
   bill to usage credits, as Fable can on some plans. Note every escalation in the batch report:
   a task that needed escalating was probably under-rated, which is useful feedback for future specs.

**Cap at 3 review cycles per batch.** If the third review still fails, stop and report to the user:

```
Batch {N} review failed after 3 cycles. Outstanding issues:
{list of remaining issues}

Options:
1. Fix these manually and re-run /spec-implement
2. Proceed to the next batch anyway
3. Stop here
```

### Step 8: Complete the Batch

After the batch passes review (or the user chooses to proceed):

1. **Update task files**: for each completed task, change the Status field from `pending` to `complete`
2. **Update README.md**: change `- [ ]` to `- [x]` for each completed task
3. **Commit the batch**:
   ```
   git add -A
   git commit -m "feat({feature}): complete batch {N} — {brief summary}"   # or the config's git.commit_style
   ```
4. **Report batch completion**:
   ```
   Batch {N} of {total} complete.

   Tasks completed:
   - task-{nn}-{name}: {one-line summary}
   - task-{mm}-{name}: {one-line summary}

   Review: PASS
   Commit: {hash}

   Next: Batch {N+1} has {count} tasks ready for parallel execution.
   ```

### Step 9: Final Integration Review

After all batches are complete:

1. Run lint and typecheck one final time
2. Dispatch a review pass (same mechanism as Step 6) to review the full scope of changes (all files modified across all batches)
3. Report the final status:

```
Feature "{feature}" implementation complete.

Batches completed: {N}/{N}
Total tasks: {T}

Verification:
- Lint: {PASS/FAIL}
- Typecheck: {PASS/FAIL}
- Integration review: {PASS/FAIL with notes}

Next steps:
- Review the changes
- Push and create a PR when ready
```

## Run-through mode (after approval)

Run-through applies when the user asks for it ("approved, run it through", "build, verify and
commit it") or when `.spec-driven.yml` has `pipeline.after_approval: run-through` and the user has
approved the spec. In that case, don't stop after Step 9. Continue:

```
Run-through progress:
- [ ] Implement all batches (Steps 1–9) — every review gate passed
- [ ] Verify — follow the spec-verify skill; every acceptance criterion PASS
- [ ] Checkpoint — follow the spec-checkpoint skill; every check passes, commit made
- [ ] Stop and hand off to spec-ship
```

1. **Gate on each stage.** Move on only if the previous stage fully passed. On any failure (a review
   gate exhausted its 3 cycles, a criterion FAILed or was SKIPPED, a check failed), stop the
   run-through and report where it stopped, why, and the command to resume (e.g. "fix X, then say
   'continue the run-through'").
2. **Verify, then checkpoint.** Follow those skills' own instructions in full, including the
   verification report. Don't shortcut them because you're running them in sequence.
3. **Never push.** The run-through ends at a local commit. Finish with the summary below and ask
   whether to run `spec-ship`. `spec-ship` still shows exactly what will be pushed and waits for a
   yes.
4. **No approval, no run-through.** If the spec hasn't been reviewed and approved in this
   conversation, or the user only said "implement", do the normal Steps 1–9 and stop.

```
Run-through complete for "{feature}":
- Implement: {N} batches, all review gates PASS
- Verify: {P}/{P} criteria PASS (specs/{feature}/verification-report.md)
- Checkpoint: {commit hash} — {subject}

Ready to push and open a PR. Run spec-ship? (it will show exactly what gets pushed first)
```

## Error Handling

- **Coder agent failure**: mark the task as failed, report to user, continue with remaining tasks in the batch. The review step will catch integration issues.
- **Lint/typecheck failure after fix attempts**: report the specific errors and ask the user whether to commit anyway or fix manually.
- **All tasks already complete**: report completion and stop.
- **Missing spec folder**: ask the user to provide the feature name or suggest creating a spec with `spec-create`.

## Key Principles

- **The orchestrator does not write code.** Its job is dispatch, review, and progress tracking. All implementation happens in coder subagents.
- **Each coder agent gets exactly one task.** This keeps each agent's context focused and manageable.
- **Completed task summaries are brief.** One paragraph per task — not the full file contents. This keeps coder agent prompts from growing unbounded as batches progress.
- **The review gate is non-negotiable.** Every batch gets reviewed before commit. This catches integration issues early rather than letting them compound across batches.
- **Progress is tracked in the spec files.** README checkboxes and task file status fields are the source of truth. This makes the skill resumable across sessions.
