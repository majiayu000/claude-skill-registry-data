---
name: review-todo
description: Turn a completed code review into a persistent workflow that immediately proposes the complete ordered implementation plan, waits for whole-plan approval, then implements and commits every accepted finding. Use after a review when the user invokes review-todo, says "turn this review into a todo list", "work through these review findings", supplies directives such as "fix 2, 3; ignore 7", asks to revise or approve the plan, or resumes review work. Do not use to perform the original code review.
argument-hint: '[fix 2,3 | ignore 7 | resume | go]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Todo

Turn the most recent completed review into a stateful plan-to-implementation workflow. Keep `.review-todo.md` at the repository root as the source of truth across turns and context compaction. It is temporary working state: never commit it, and remove it only after the workflow completes successfully.

The first response for a new review must contain the complete proposed disposition and implementation plan for every finding. Do not walk the user through findings one at a time. Make no production-code edits and no commits until the user has reviewed that whole plan and explicitly approved it.

## Instructions

### Step 1: Start or resume

1. Find the repository root. If the current directory is not in a Git repository, ask for the target repository before creating state; the workflow ends by committing changes.
2. Check for `.review-todo.md`:
   - If it contains an active workflow, resume it by default. Read it before using conversational context.
   - If the user clearly supplied a new review while an active workflow exists, do not overwrite it. Ask whether to resume the existing workflow or replace it with the new review.
   - If it is marked complete after an interrupted cleanup, report the recorded result and remove it.
   - If it uses an older one-finding-at-a-time format, preserve all recorded decisions and implementation results, inspect every remaining finding, and upgrade it to the complete-plan format before continuing.
3. For a new workflow, use the most recent completed review in the conversation or review text supplied by the user. If neither contains concrete findings, ask the user to provide or run a review.
4. Snapshot `git status --short` into the state file as the pre-existing worktree. These paths and hunks are not owned by this workflow.

An invocation may include decisions such as `fix 2, 3, 9; ignore 7`. Capture the review first so its stable IDs exist, then use every unambiguous directive when building the proposal. Initial directives shape the plan; they do not authorize code edits before the complete plan has been shown and approved.

### Step 2: Create the state file

Normalize concrete, actionable findings into `.review-todo.md` without changing their meaning:

- Reuse unique integer IDs already shown by the review; otherwise assign stable integer IDs in its original order. Never renumber them.
- Preserve severity, title, file and line, problem, impact, proposed fix, and source when available.
- Deduplicate restatements while retaining all source labels on the surviving item.
- Exclude review-process prose, comment-cleanup summaries, and other non-findings.
- Put findings already classified by the source review as `Improbable / Not Worth Handling` in `Source notes`, not the actionable queue. Reopen one only if the user explicitly asks.
- Record closely related findings together when they share a root cause, require one design decision, or must be implemented together. Do not group items merely because they touch the same file.

Use this shape, omitting empty optional fields:

```markdown
# Review Todo

- State: planning
- Created: 2026-08-15T14:00:00+02:00
- Updated: 2026-08-15T14:00:00+02:00
- Next: Build and present the complete plan

## Pre-existing worktree

- `M path/from-git-status`

## Related findings

- R1: Short root-cause name — findings 2, 3

## Findings

### 1. Short finding title

- Severity: should-fix
- Location: `src/example.ts:42`
- Related group: none
- Status: pending
- Source: code-review
- Finding: What is wrong and why it matters.
- Proposed disposition: fix
- Proposed approach: The concrete fix and its important constraints.
- Decision: —
- Implementation: —
- Commit: —

## Source notes

- Non-actionable review material worth preserving.

## Implementation groups

### G1. Short implementation outcome

- Findings: 1, 2
- Status: proposed
- Depends on: none
- Changes: Ordered, concrete implementation steps.
- Expected files: `src/example.ts`, `tests/example.test.ts`
- Verification: Exact checks or test scope.
- Commit: `fix: short subject`
- Result: —
```

Allowed finding statuses are `pending`, `planned`, `ignored`, `implementing`, and `implemented`. Allowed workflow states are `planning`, `plan-review`, `implementing`, `blocked`, and `complete`.

Write the file before presenting the plan. From then on, read it at the start of every turn and update `Next`, `Updated`, and the affected entries immediately after each plan revision, approval, or implementation result. Do not rely on the chat transcript as the only record.

### Step 3: Build and present the complete proposal

Inspect the current code for every finding before proposing the plan. Confirm its context, validity, dependencies, and likely files. If a finding is stale, already fixed, a duplicate, or a false positive, cite the evidence and propose ignoring it. Do not silently discard it; every actionable finding must have an explicit proposed disposition.

For every finding, record one of:

- `fix` with a concrete approach;
- `ignore` with a concrete reason;
- `needs discussion` with the exact material choice the user must make.

Apply unambiguous user directives by ID, including comma-separated IDs and ranges. A user-supplied approach replaces the default. If directives conflict or name an unknown ID, preserve the unambiguous parts and list only the ambiguous subset under open decisions.

Then write the complete ordered implementation plan immediately:

1. Partition all proposed fixes into the fewest logical implementation groups. Keep a fix with its tests, docs, generated output, and dependent findings in the same group. Split only changes that stand alone and can be committed independently.
2. Order groups by prerequisites and root causes before dependents and symptoms. Within a group, list the concrete changes in execution order.
3. Record the included finding IDs, dependencies, expected files, verification, and proposed `feat`, `fix`, or `chore` commit subject for every group.
4. Check the proposal against every actionable finding. Every ID must appear as a proposed fix, proposed ignore, or open decision, and every proposed fix must belong to exactly one implementation group.
5. Set the workflow state to `plan-review` and `Next` to `Await whole-plan approval`.

Present the whole proposal in one response:

- a compact disposition table covering every finding;
- all implementation groups in execution order, including changes, expected files, verification, and commit subjects;
- all open decisions together, with a recommendation for each;
- a compact count such as `Review todo: 5 proposed fixes · 2 proposed ignores · 1 open decision`.

Ask the user to approve the complete current plan or describe changes by finding or group. Do not edit production code, run implementation-only commands, stage files, or commit during this step.

### Step 4: Revise or approve the plan

Treat feedback as edits to the recorded proposal:

- `fix 2, 3` changes those findings to proposed fixes using their recorded approaches.
- `ignore 7` changes that finding to a proposed ignore. Record the user's reason; if none was given, record `Declined by user (no rationale given)` rather than inventing one.
- A user-supplied approach replaces the proposed approach and becomes an implementation constraint.
- A change to one finding may require regrouping, reordering, changing verification, or changing a commit subject. Recompute every affected part rather than leaving the plan internally inconsistent.

After any material revision, write the updated state file and present the complete revised plan again, not only the delta. Wait for approval of that current version unless the user explicitly combines the revision with approval, such as `Make that change and go`.

Accept `go`, `approve`, `implement this plan`, or equally explicit wording only after the complete current plan has been presented. Approval applies to the recorded proposal as a whole:

1. Resolve every `needs discussion` item first. Do not infer a choice from general approval.
2. Mark every approved proposed fix `planned` and record its approach as the decision.
3. Mark every approved proposed ignore `ignored` and record its reason.
4. Change implementation-group statuses from `proposed` to `planned`.
5. Set the workflow state to `implementing` and begin implementation.

If all findings are approved as ignored, mark the workflow complete, summarize the decisions, remove `.review-todo.md`, and make no commit.

### Step 5: Implement, verify, and commit

Process implementation groups in dependency order:

1. Mark the group's findings and group `implementing` and make exactly the recorded changes. Preserve unrelated and pre-existing worktree edits.
2. If implementation reveals a materially different design choice, stop that group, set the workflow to `blocked`, record the evidence and new choice required, and return it to the user. After the user decides, update and re-present the complete remaining plan before resuming unless they explicitly approve the revision in the same message.
3. Run verification proportional to the change. Add or update tests when the accepted finding requires them. Record commands and results in the affected findings and implementation group.
4. Mark the findings and group `implemented` only after verification passes.
5. Commit the group before starting an independent group. Follow the repository's commit policy:
   - Stage only files and hunks changed for this group; never use broad staging commands.
   - Never stage `.review-todo.md` or a pre-existing/user-owned hunk.
   - Preserve unrelated staged changes. If they cannot be excluded safely without disturbing the user's index, set the workflow to `blocked` and ask the user to clear or authorize index handling.
   - Inspect the staged diff before committing.
   - Use only `feat:`, `fix:`, or `chore:` with a short subject and no body by default.
   - Keep dependent code, tests, docs, and generated files in the same commit.
   - Never bypass hooks and never push.
6. Record the commit hash and subject in each included finding and in the implementation group.

When every planned finding is implemented and committed, set the workflow to `complete`. Verify that `.review-todo.md` is the only remaining workflow-owned uncommitted file, summarize implemented fixes, ignored findings, verification, and commits, then remove the file. If other changes remain, identify them as pre-existing or user-owned and leave them untouched.

## Examples

### Example 1: Start with direct decisions

User invokes `review-todo fix 2, 3, 9; ignore 7` immediately after a review with ten findings.

Actions:

1. Create `.review-todo.md` with findings 1–10 and stable IDs.
2. Inspect all ten findings. Incorporate fixes 2, 3, and 9 and ignore 7 into the proposal, and recommend dispositions for every other finding.
3. Write and present the complete disposition table and every ordered implementation group.
4. Wait for the user to approve that whole plan or request changes.
5. After explicit approval, implement, verify, and commit each independent group.
6. Report the commits and remove `.review-todo.md`.

### Example 2: Discussion changes the plan

The complete proposal replaces a public API for finding 4, but the user says, `Keep the old method as a deprecated compatibility wrapper until the next major release.`

Record the compatibility constraint, add wrapper coverage to verification, recompute affected groups, and present the entire revised plan. Do not start implementation until the user approves that version. If the user instead says, `Keep the wrapper and go`, update the plan and begin after confirming there are no unresolved decisions.

### Example 3: Resume after context loss

The user invokes `review-todo resume` in a later turn. Read `.review-todo.md`. If it is awaiting approval, present the complete current plan and counts again. If it is implementing or blocked, report completed groups and present the complete remaining plan or required decision. Do not reconstruct or renumber findings from memory.

## Troubleshooting

### No review is available

**Cause:** The skill was invoked without a completed review in context and no active state file exists.
**Solution:** Ask the user to paste the findings or run a review. Do not invent findings or create an empty state file.

### An active state file conflicts with a new review

**Cause:** A previous workflow did not finish.
**Solution:** Preserve the file and ask whether to resume it or replace it. Never merge two reviews or overwrite active decisions implicitly.

### A finding cannot be planned without a user choice

**Cause:** Multiple approaches have materially different behavior, compatibility, risk, or scope.
**Solution:** Include the finding and all such choices in the complete proposal as `needs discussion`, recommend one, and gather the decisions together. Rebuild and re-present the whole plan after the user decides.

### A finding changed during implementation

**Cause:** Current code or a dependency makes the approved approach unsafe or infeasible.
**Solution:** Record what was discovered, mark the workflow `blocked`, and ask only for the new material decision. Update and re-present the complete remaining plan before resuming; do not silently substitute a different design.

### A commit would include unrelated changes

**Cause:** A planned file already had user or another session's edits, or the index contains foreign changes.
**Solution:** Stage only workflow-owned hunks and inspect the staged diff. If ownership cannot be determined safely, leave the ambiguous hunk unstaged and ask the user rather than widening the commit.

### Verification or a commit hook fails

**Cause:** The implementation is incomplete, or a repository-wide check exposes a failure outside the changed scope.
**Solution:** Diagnose and fix failures caused by the implementation. Record genuine unrelated failures and keep the workflow `blocked` if they prevent a safe commit. Never weaken verification or bypass hooks.
