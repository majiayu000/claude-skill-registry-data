---
name: status
description: "Report the current coding-session status: summarize staged, unstaged, and untracked files; identify the last task and whether its work is present or committed; report code-review coverage; summarize active plans or review todos; list remaining session work; and recommend the next task. Use when the user invokes status or asks 'where are we?', 'what changed?', 'what is left?', or 'what should I do next?' about the current coding session. Do not use for service health or deployment status."
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Status

Give a read-only snapshot of the current coding session. Reconcile conversation history, task state, Git changes, review coverage, and remaining work. Never edit files, update task state, stage changes, commit, or start the recommended task.

## Instructions

### 1. Collect evidence

Use these sources in order of authority:

1. The current conversation and any compacted session summary: the user's goal, work performed, review invocations, verification, decisions, and explicit unfinished items.
2. Active task state: harness-native plan or goal state when available, `.review-todo.md`, and any plan/checklist explicitly used in this conversation.
3. Current Git state: `git status --short`, staged and unstaged diffs, and untracked files.
4. Recent Git history: only to confirm session work that the conversation says was committed or that has disappeared from the working tree.

Do not search older agent sessions by default. If the current session context is unavailable, report unknown rather than inventing history; use `check-agent-logs` only when the user explicitly asks to recover an earlier session.

If the directory is not a Git repository, omit Git-specific checks but still report the task, review, task-list, and open-work sections.

### 2. Explain every changed file

Run:

```bash
git status --short
git diff --cached --stat
git diff --stat
git diff --cached
git diff
```

Report staged, unstaged, and untracked paths separately. Include all three categories when they exist; never prefer staged changes and hide the rest.

- Summarize what each path contains and its role in the change, grouped by logical concern when useful.
- Mark partially staged files and explain the staged and unstaged portions separately when they differ materially.
- Inspect safe, relevant untracked source and documentation files so they are not reduced to filenames. Do not open likely secrets, credentials, binaries, or large generated artifacts; identify those by type and path only.
- Label changes known from the conversation to belong to the user, another session, or pre-existing work. Do not assign ownership from filenames alone.
- For a very large mechanical or generated set, summarize the pattern and path count, then call out exceptions instead of narrating every repeated edit.
- If the tree is clean, say so. A clean tree does not mean the last session task never happened; check whether it was committed.

### 3. Identify the last task and reconcile it with Git

Name the most recent substantive user goal before the status request. Ignore incidental actions such as asking for status, committing, or checking a command unless one of those was itself the task.

From the conversation, reconstruct the files and outcomes that belong to that task. Compare them with the working tree and any confirmed session commit. Report exactly one coverage state:

- **Included** — the task's current work is represented in the changed files.
- **Partial** — only some task work is represented, or later edits are missing.
- **Committed** — the task work is absent from changed files because it was committed; include the commit hash and subject when confirmed.
- **Absent** — the task was discussed or attempted, but its expected work is neither changed nor committed.
- **Unknown** — the available session context cannot establish the relationship.

Distinguish unrelated working-tree changes from the last task. Do not imply that every changed file belongs to this session.

### 4. Report code-review coverage and freshness

Determine whether the `code-review` workflow ran on the last task's changes. Use one of these verdicts:

- **Current** — code-review ran after the latest substantive edit and covered the task's full change set.
- **Stale or partial** — code-review ran before later edits or covered only part of the task.
- **Not run** — the session evidence shows no code-review invocation for the task.
- **Unknown** — session history is insufficient to tell.

Name the reviewed scope and any resulting findings when known. An active `.review-todo.md` whose findings cite code-review is evidence that a review ran, but compare its scope with later changes before calling it current.

Do not count tests, linting, type checks, build checks, `git diff --check`, self-review, or a pre-commit hook as code-review. Report verification separately in one short line when it helps explain readiness. Do not run code-review as part of status.

### 5. Summarize any active task list

Check, in order:

1. `.review-todo.md` at the repository root.
2. An active harness plan or goal.
3. A concrete checklist or numbered findings list being tracked in the conversation.

For `.review-todo.md`, treat its recorded state as authoritative across context compaction. Report:

- workflow state and `Next`;
- counts for `pending`, `planned`, `implementing`, `implemented`, and `ignored` findings;
- what was completed in this session;
- the next recorded finding or implementation group;
- any blocker or unresolved decision.

For a plan or conversational list, report completed, in-progress, pending, and blocked items without rewriting the list. If sources disagree, state the discrepancy; do not modify either source. If no task list is active, say so plainly.

### 6. Find open session work and recommend one next task

Count as open only work supported by session evidence:

- an explicit user request that is not finished;
- a pending, implementing, or blocked task-list item;
- a failed or still-required verification step;
- a promised follow-up not yet performed;
- completed implementation still awaiting an explicitly requested review or commit.

A changed file alone is evidence of work, not proof of an open task. Do not turn unrelated or user-owned changes into session tasks.

Recommend exactly one next task, using this priority:

1. Resolve a blocker required for progress.
2. Finish the current in-progress task.
3. Follow the active task list's recorded `Next` item.
4. Run missing verification or code-review for otherwise complete session work.
5. Commit complete, verified, reviewed work when committing is already part of the user's workflow.

If nothing remains open, say `Recommended next: none — the session task is complete.` Do not invent optional work merely to fill the section.

## Output

Use this compact structure:

```markdown
## Changes

### Staged
- `path` — what is there

### Unstaged
- `path` — what is there

### Untracked
- `path` — what is there

## Last work
- Task: ...
- Coverage: Included | Partial | Committed | Absent | Unknown — evidence

## Review
- Code review: Current | Stale or partial | Not run | Unknown — evidence
- Verification: ...

## Task list
- Source and state, or `No active task list.`
- Completed: ...
- Next: ...

## Open tasks
- ... or `None.`
- Recommended next: exactly one task
```

Omit empty staged, unstaged, or untracked subsections, but never omit the entire Changes section. Keep file descriptions concrete and the other sections concise. Do not propose commit messages; `commit` owns committing and message generation.

## Examples

### Current work is uncommitted and unreviewed

The conversation shows the session adding retry support. `git status` shows an unstaged implementation and an untracked test, with unrelated staged config from the user. Report both ownerships, mark the retry task **Included**, mark code review **Not run**, say there is no active task list, and recommend finishing the test before review.

### Session work was committed and review todo remains

The working tree contains unrelated edits, while the conversation and recent log confirm the session's parser fix was committed. `.review-todo.md` has two implemented, one ignored, and one pending finding. Mark the last task **Committed**, report the review's freshness from its scope and later edits, summarize the finding counts, and recommend the recorded pending finding.

### Clean, completed session

The tree is clean, the last task is confirmed in a session commit, code-review ran after the final edit with no findings, and no plan or todo remains. Report the commit, mark review **Current**, list no open tasks, and recommend none.

## Troubleshooting

### Session history is missing

**Cause:** The skill runs in a fresh context without a useful compaction summary or persisted task state.
**Solution:** Still explain the working tree. Mark last-work coverage, review, and session-only tasks **Unknown** rather than inferring them from Git. Do not search old logs unless the user asks.

### The tree is clean but work happened

**Cause:** The last task may have been committed or reverted.
**Solution:** Use conversation evidence and a narrow recent-log check to distinguish **Committed** from **Absent**. Do not summarize unrelated historical commits.

### Task sources disagree

**Cause:** A persisted todo or plan is stale relative to a later user decision in the conversation.
**Solution:** Report both states and identify the newer explicit decision. Do not repair task files during this read-only workflow.

### The diff is too large or contains sensitive files

**Cause:** Generated output, binaries, vendored code, or likely credentials dominate the working tree.
**Solution:** Report paths, types, counts, and high-level patterns without reading secrets or dumping generated content. Say what was not inspected and why.
