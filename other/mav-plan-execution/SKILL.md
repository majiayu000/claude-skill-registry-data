---
name: mav-plan-execution
description: How to execute an implementation plan step-by-step. Covers the execution loop, verification discipline, failure handling, progress tracking, crash recovery, and acceptance criteria. Adapts behaviour based on whether the caller is solo (autonomous) or guided (human checkpoints). Used as a dependency from workflow skills.
user-invocable: false
disable-model-invocation: true
---

# Plan Execution

Execute an implementation plan step-by-step. Each step is implemented, verified, and committed before moving to the next. Progress is tracked durably on GitHub so it survives session loss.

## Execution Mode

- **Solo mode** (called from do-issue-solo): work autonomously. Only pause when genuinely blocked or when the issue is ambiguous. Press through recoverable problems.
- **Guided mode** (called from do-issue-guided): provide checkpoints to the user. Pause when uncertain, report progress at natural break points.

## Retry Budget (canonical)

**Two fix attempts, then mav-systematic-debugging, then
escalate per mode.** This is the single retry budget for implementation
work — other skills reference this rule rather than defining their own.
If the same fix fails twice, the diagnosis is wrong: step back and think
differently, never retry the same change a third time.

## Execution Loop

### 1. Load the Tasks

Read the task list from one of:
- The tasks comment on the GitHub issue (if working from do-issue)
- The task list directly (if invoked standalone)

```bash
# The tasks comment id lives in the task-progress marker
uv run maverick task-progress read <repo> <issue>   # -> .comments.tasks
gh api "repos/<repo>/issues/comments/<id>" --jq '.body'
```

### 2. Check for Prior Progress

If resuming after a crash or new session:
- Parse the checkboxes in the tasks comment (`- [x]` = done, `- [ ]` = pending)
- Cross-reference with `git log` — if commits exist for tasks that aren't checked off, the comment update was lost. Check them off now (step 3.6).
- Resume from the first genuinely unchecked task.

### 3. Execute Each Task

For each task in the list:

1. **Mark in-progress** — note which task you are working on
2. **Implement** — make the change described in the task
3. **Verify** — run verification (lint, typecheck, tests) per the mav-local-verification skill
4. **Fix if needed** — apply the retry budget above
5. **Commit** — descriptive message referencing the issue number, using conventional commits
6. **Mark complete** — check the task off durably:
   ```bash
   uv run maverick tasks check <repo> <issue> <n>
   ```
   The command is idempotent, edits exactly one checkbox, and goes
   through the App identity when configured. Never PATCH the comment
   body by hand.

Never batch multiple tasks into one commit unless they are trivially related (e.g. a one-line change and its import).

### 4. Run Full Verification Suite

After all steps are complete, run the project's full verification suite:
lint, type checking, all tests. Fix any issues found. Do not proceed to
acceptance criteria with failing checks.

## Failure Handling

Apply the retry budget: diagnose → fix → re-verify, at most twice; then
mav-systematic-debugging; then escalate per mode.

### Escalation by Mode

| Situation | Solo | Guided |
|---|---|---|
| Step fails after the retry budget | Apply mav-systematic-debugging. If still stuck, ask user for help. | Ask user for help immediately after 2 attempts. |
| Design assumption proves wrong | Reassess against the design. Adjust approach if confident. Only ask user if the change is fundamental. | Pause and discuss with user before adjusting. |
| External blocker (API down, missing dependency) | Document the blocker and ask user. | Document the blocker and ask user. |
| Unsure about implementation approach | Try the most likely approach. If it doesn't work, try the alternative. Ask user only as last resort. | Ask user which approach to take. |

### What NOT to Do

- **Do not skip a failing verification.** Fix it first.
- **Do not move to the next step with a broken codebase.** Each commit must leave the codebase working.
- **Do not silently change the design.** If the plan needs to change, update the plan comment (`uv run maverick issue comment update --kind plan`) and (in guided mode) inform the user.
- **Do not retry the same fix repeatedly.** The budget exists because a repeated identical fix means the diagnosis is wrong.

## Guided Mode Checkpoints

In guided mode, provide brief progress checkpoints at natural break points:

- **After every 3-4 steps:** "Steps 1-4 complete. Moving to steps 5-8. Everything on track."
- **When something unexpected happens:** "Step 3 revealed that the API response format differs from what the design assumed. I've adjusted the parsing logic. Continuing."
- **After all steps complete:** "All 7 steps complete. Full verification suite passes. Ready for acceptance criteria check?"

Keep checkpoints brief — one or two sentences. Do not ask for approval to continue unless something went wrong.

## Acceptance Criteria Check

After all steps are complete and the full verification suite passes:

1. Re-read the original issue requirements
2. Walk through each acceptance criterion and confirm it is satisfied by the implementation
3. If any criterion is not met:
   - Identify what is missing
   - Add additional steps to address it
   - Execute those steps using the same loop above
4. Run the full verification suite again after any additions

Do not proceed to code review until every acceptance criterion is met and all checks pass.

<!-- maverick-plugin-version: 4.0.2-dev -->
