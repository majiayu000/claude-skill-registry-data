---
name: sync-tasks
description: Compare active kotgent tasks with repository guidance, plans, code, tests, TODOs, and Git history, and report task/repository drift with evidence and proposed CLI commands. Use when the user asks to sync, reconcile, map, or compare the kotgent backlog with the current repository. This workflow is always read-only.
disable-model-invocation: true
---

# Sync Tasks

Build an evidence-backed reconciliation report. Use the `kotgent` CLI for tracker reads and `git` plus
ordinary file inspection for repository evidence. Do not use an MCP server, SDK, direct daemon request,
or helper script.

## Stay read-only

Do not run `task add`, `task claim`, `task comment`, `task review`, `task done`, `task unlink`, `task move`,
`task dep`, `task delete`, `project init`, `project delete`, or `project restore`. Do not edit repository
files. Suggested commands belong only in the report.

Treat successful `task` and `project` stdout as JSON and failure stderr as JSON. Exit `2` means this skill
built an invalid command and stderr may be plain usage text; stop and report it exactly. Never retry a
deleted-project error or restore/reinitialize a project.

## Establish the project and task snapshot

1. Require `git` and `kotgent`, resolve `git rev-parse --show-toplevel`, and read the root
   `.kotgent.json`. Stop if the file is missing or its `id` is not a UUID.
2. Read both `kotgent project list` and, only if needed, `kotgent project list --archived`. Record whether
   the exact UUID is live or archived. An unknown UUID is an error. An archived project may still be read,
   but label it and do not propose an automatic restore.
3. Run `kotgent task list --project <project-uuid>`. Select only rows whose state is exactly `todo` or
   `in_progress`.
4. Run `kotgent task show <ref>` for every selected row. Use the full detail, including body,
   dependencies, linked sessions, and activity; do not reconcile from list titles alone.
5. Record HEAD, branch or detached state, and `git status --short` so the report identifies its snapshot.

## Inspect repository evidence in this order

1. Read applicable `AGENTS.md` and `CLAUDE.md` files first. Treat them as constraints, not backlog items.
2. Find active plan and backlog files. Exclude completed, superseded, archived, or historical plans unless
   they explain a mismatch.
3. Inspect the implementation and tests named by tasks or plans. Use exact symbols, paths, assertions,
   and observable behavior as evidence.
4. Search tracked content for relevant `TODO` and `FIXME` markers. Do not promote every marker into a
   task; require a concrete match to intended repository work.
5. Inspect relevant Git history with focused `git log`, `git show`, or `git blame`. Use commit IDs when
   history proves completion, replacement, or architectural change.
6. Include relevant uncommitted and untracked work from `git status`; never treat a clean HEAD as the
   whole repository when the worktree contains evidence.

Match by scope, acceptance behavior, identifiers, and changed paths. Title similarity alone is not proof.

## Classify the mapping

Assign every tracker task and every concrete repository-only work item exactly one primary label:

- `aligned`: task scope and current repository intent agree.
- `drifted`: both exist, but scope, assumptions, dependencies, or acceptance evidence disagree.
- `missing in repo`: a kotgent task has no current repository evidence.
- `missing in kotgent`: current repository intent has no matching active kotgent task.
- `duplicate`: two or more active kotgent tasks represent the same work; name the canonical ref.

For each row, cite evidence as `path:line`, symbol/test name, task activity entry, worktree path, or commit
ID. State uncertainty instead of upgrading a weak textual similarity into a fact.

## Report without applying

Report the project UUID/status and Git snapshot, then the mapping grouped by label. Include task ref,
state, concise scope, repository counterpart, evidence, and consequence. List repository-only items too.

For every proposed tracker change, print the exact supported `kotgent` command with concrete refs,
project UUID, body, and dependency direction. There is no CLI command to rewrite an existing title or
body; for `drifted`, propose a replacement add and a separately confirmed delete instead of inventing an
update command. Mutations require either a proven current kotgent pane or a supplied session ID. Never
probe IDs found in task `sessions`, read `KOTGENT_SESSION_ID` as identity, or infer the current session
from names, cwd, other environment values, or recency. If needed, use at most one ref-less
`kotgent task show` to prove current-pane resolution: accept
only success or the exact free-session error; this permits the implicit current-pane command form but
does not reveal an ID. If neither form is available, say `session ID required` rather than guessing or
printing a misleading runnable command. Do not execute any proposed command.
