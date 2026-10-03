---
name: work-task
description: Execute the kotgent task linked to the current session, coordinate concurrent work, implement and verify repository changes, report meaningful progress or blockers, and submit the task for human review. Use when the user asks to work, continue, implement, finish, or resume a linked kotgent task.
---

# Work Task

Carry one linked task from `in_progress` to `review`. Use the `kotgent` CLI for tracker operations and
`git` for repository state and history. Do not use an MCP server, SDK, direct daemon request, or helper
script for kotgent.

## Read the task and repository first

Use the live kotgent pane as identity by default. Never read `KOTGENT_SESSION_ID` as identity or copy it
into `--session`. Outside a kotgent pane, require an exact session ID explicitly supplied by the invocation
context or user. Never infer one from provider conversation IDs, environment variables, names, cwd,
recency, or `kotgent list`. Keep one identity mode for the whole run.

Require `git` and `kotgent`, resolve the Git root, then run the pane form:

```text
kotgent task show
```

Use `kotgent task show --session <session-id>` only in explicit outside-pane mode.

Keep `task show`, `task comment`, and `task review` ref-less throughout this linked-task workflow. In
explicit mode `--session` names the caller while the CLI still resolves that session's current task.

Stop if the session is not linked. Require the returned task state to be `in_progress`; send `todo` work
through `take-task`, and stop for `review` or `done`. Read the complete body, dependencies, activity, and
linked sessions.

Read applicable repository instructions before editing, especially `AGENTS.md` and `CLAUDE.md`, then any
active plan or backlog referenced by the task. Capture `git status --short`, branch or detached state,
full HEAD, and relevant diffs. Preserve pre-existing user changes and never sweep an untracked
`.kotgent.json` into an unrelated commit.

Check `kotgent project list`; if the task's project is archived, report that fact and do not initialize,
restore, switch, or retry. An already-linked task may still be completed through comment and review.

## Coordinate before editing

Task links are non-exclusive. Treat another live, non-archived linked session, recent implementation
activity from another session, or overlapping worktree changes as a coordination risk unless the user
already established a division of work. Leave one evidence-rich coordination comment and stop for human
direction rather than racing:

```text
kotgent task comment -m <coordination-evidence-and-request>
```

Append `--session <session-id>` only in explicit outside-pane mode.

Keep the task `in_progress` and linked. Never use `unlink` as conflict handling.

## Implement and communicate

Follow repository rules and the task's acceptance evidence. Inspect before editing, make the smallest
complete change, and verify it with the repository's appropriate tests, builds, linters, or focused
checks. Do not invent scope beyond the task.

Add progress comments only when they give a human durable new information: a confirmed root cause, a
meaningful milestone, a scope change, a consequential design choice, or a verification result. Do not
post start announcements, running narration, repeated status, or estimates.

Re-read the task with the same ref-less identity form before a major or destructive change and before
final review. Require its ref to remain the original one so a changed session link cannot redirect the
workflow silently, and inspect new activity and linked sessions.

## Handle blockers

When completion needs a user decision, unavailable authority, external coordination, missing input, or a
failing prerequisite, leave one comment containing:

- what is blocked;
- evidence and commands already tried;
- the exact decision or input required;
- any safe partial work completed.

Ask the user for that decision and stop. Keep the task `in_progress`; do not move it to review, done, or
another session. Do not retry deleted-project failures.

## Submit for human review

Before review, inspect the final diff and status, run appropriate verification, and identify commits made
for this task. Build a review message containing the result, key files or behavior changed, every check
and its outcome, and either the relevant full commit IDs or the explicit sentence `Changes are not
committed.`

Then perform the only completion transition:

```text
kotgent task review -m <summary-checks-and-commits>
```

Append `--session <session-id>` only in explicit outside-pane mode.

For a long message, use the CLI's `-m -` stdin form without introducing a helper script. Confirm the
returned state is `review`, report the same summary to the user, and stop. Never run `task done`,
`task unlink`, or `task next` after review.
