---
name: make-plan
description: Create or revise a structured implementation plan on a kotgent task and work through its browser review rounds. Use when the user asks to make, write, revise, or review a kotgent plan before implementation.
---

# Make Plan

Produce an approved, task-owned plan through the `kotgent` CLI. Approval ends this workflow; it does
not start implementation. Keep existing Markdown plans usable when the user asks to revise one, and
migrate one to a task only when that is part of the request.

## Establish the task and caller

Read the repository's instructions, resolve its Git root, and check `git status --short` and
`kotgent --version`. Require a CLI with `kotgent plan` support. Use the current live pane as caller.
Outside a Kotgent pane, use `--session ID` only when the user or invocation context supplied that exact
Kotgent session ID. Never derive it from an environment variable, provider conversation, name, cwd,
recency, or `kotgent list`.

If the user named a task, read it with `kotgent task show REF`. Otherwise use `kotgent task show` to
resolve the linked task. Append the explicit `--session ID` to every caller-dependent command only in
outside-pane mode. If there is no linked task, inspect the repository's project backlog for the requested
work; create one focused task with the `kotgent:create-tasks` workflow when needed. Preserve its
provenance and project rules. Do not initialize/restore a project or guess a caller to get past a failure.

Keep one explicit task reference for all `plan` commands. Read `kotgent plan show REF`; a missing plan
is expected for a new task, but an authentication or connection error is not evidence of absence.

## Build a reviewable plan

Read relevant code, tests and user constraints. Ask one focused question at a time only when its answer
changes the plan; continue independent investigation while waiting. Do not fill missing requirements
with unrelated cleanup or speculative features.

Use [the document contract](references/document.md) for JSON, IDs, limits and dependencies. Explain the
outcome and constraints, the concrete implementation choices, focused tasks with file ownership and
verification, and any consequential unresolved decisions. Include dependencies only when they constrain
execution. Choose task boundaries that can be implemented and reviewed in separate worker worktrees.

Write the JSON to a temporary file. A document file is transport, not the authoritative plan. Put only
the `plan` member returned by `show`, never the whole `{plan, review, execution}` envelope:

```sh
kotgent plan put REF --base-rev REV < /absolute/path/plan.json
```

Use revision 0 for the first put. Read successful stdout as one JSON object and retain the daemon-issued
IDs and revision. On exit 3 / HTTP 409, fetch `show`, reconcile the operator's current text with the
intended changes, then retry against the new revision. Never blindly resend the old document. On a
400, repair the named fields. Exit 2 is a malformed command: correct its arguments before retrying.
Other failures stop this attempt with the exact command/error; they do not justify an alternate identity.

## Wait for review and incorporate it

Tell the user the task reference and its Plan link (`/tasks/<encoded-ref>/plan` on their Kotgent host).
Use the blocking review command as a standalone invocation, with a tool timeout longer than its wait:

```sh
kotgent plan review REF --wait 90 --json
```

Read `verdict`, `round`, the returned document, operator edit records and unresolved threads.

- `pending`: repeat with the same arguments. A dropped connection also prints pending; it may omit the
  document and round. Do not create a new round or treat a pending result as approval.
- `changes`: preserve the operator's edits, answer each substantive open thread with
  `kotgent plan reply REF THREAD -m 'answer'` (or `-m -` with stdin), and revise the plan where needed.
  Re-fetch before putting to avoid overwriting intervening changes. Then call
  `kotgent plan review REF --after-round N --wait 90 --json`, where N is the completed round addressed.
  Keep that same `--after-round N` on every pending retry. This opens exactly one successor, including
  when only answers changed; omitting the acknowledgement can return the old verdict indefinitely.
- `approved`: report the task reference and approved revision and end the planning workflow.

Do not mark blocks viewed, submit, approve, or impersonate an absent/operator caller. Those controls
belong to the human. Do not auto-resolve the human's questions just to remove them from the review.
Honor a user cancellation or scope change; a timeout alone does not cancel an open durable round.
