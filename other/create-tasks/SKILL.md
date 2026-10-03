---
name: create-tasks
description: Create focused kotgent backlog tasks from a user request, specification, issue list, or implementation plan, with repository and session provenance. Use when the user asks to create, add, file, split, or seed tasks in kotgent; do not use for comparing or reviewing an existing backlog.
---

# Create Tasks

Create only tasks justified by the request. Use the `kotgent` CLI for tracker operations and `git` for
repository identity and provenance. Do not use an MCP server, SDK, direct daemon request, or helper script.

## Honor the command contract

- Run each `kotgent` invocation as a standalone command. Do not pipe or post-process it inline, merge
  stderr into stdout, or append an `echo` of the status; those forms hide the command's real exit code or
  destroy the stdout/stderr contract.
- Treat successful `task` and `project` stdout as one JSON value. Treat failure stderr as one JSON object.
- Treat exit `2` as a command-construction bug: stderr may be plain usage text. Stop and report the exact
  command and stderr; do not retry it unchanged.
- Never run `project init`, `project restore`, or `project delete` in this workflow.
- Never delete already-created tasks to roll back a partial batch.
- Resolve the current session from the live kotgent pane by default. Never read `KOTGENT_SESSION_ID` as
  identity or copy it into `--session`. Use `--session` only for a caller outside a kotgent pane when the
  invocation context or user explicitly supplied the exact current session ID.

## Preflight

Complete every check before creating the first task:

1. Run `git --version` and `kotgent --version`. Stop if either command is unavailable.
2. Resolve the repository root with `git rev-parse --show-toplevel`. Stop outside a Git worktree.
3. Establish one identity mode before any tracker mutation:
   - In the normal pane mode, run a ref-less `kotgent task show`. Accept exit `0`, or exit `1` with empty
     stdout, no `status`, and `error` exactly equal to ``this session is not linked to a task — name one,
     or link one with `kotgent task claim <ref>` ``. Any other response means pane resolution failed; stop
     rather than adding `--session` from the environment.
   - Outside a kotgent pane, require an exact session ID explicitly supplied by the invocation context or
     user, then run `kotgent task show --session <session-id>`. Accept exit `0`, or exit `1` with empty
     stdout, no `status`, and `error` exactly equal to `session '<session-id>' is not linked to a task —
     name one: kotgent task <command> <ref> --session <session-id>`.
   Never infer an ID from a provider conversation, environment variable, name, cwd, recency, or
   `kotgent list`. Keep the chosen mode for the whole run.
4. Inspect `<root>/.kotgent.json` and resolve one of these project states:
   - If the file exists, require valid JSON and a UUID-shaped `id`. Run `kotgent project list`. If it
     contains that ID, record the live project UUID and run `kotgent task list --project <project-uuid>`.
   - If the descriptor's ID is absent from the live list, run `kotgent project list --archived`. Stop if
     that ID is archived; never restore it. If it is absent there too, leave the project unresolved so the
     first contextual `task add` adopts the committed descriptor.
   - If the file is absent, do not stop and do not run `project init`. Leave the project unresolved so the
     first contextual `task add` creates the descriptor and project.
5. Resolve the full commit with `git rev-parse HEAD`; stop if HEAD does not exist or is not a full SHA.
   Resolve the branch with `git symbolic-ref --quiet --short HEAD`; use the literal `detached` only when
   that command reports detached HEAD.
6. Select the exact active host label: `Codex`, `Claude Code`, or `Junie`.

## Shape the batch

- Derive the smallest task set that fully represents the request. Do not create cleanup, documentation,
  testing, refactoring, or follow-up tasks unless the request itself requires them.
- Give each task a specific action-oriented title and a body containing the relevant scope, constraints,
  and acceptance evidence from the request.
- Add a dependency only when the request explicitly states or necessarily defines that one task cannot
  begin before another finishes. Do not infer dependencies merely from list order or implementation taste.
- Plan the entire batch before mutating the tracker, including dependency direction: in
  `task dep add A --on B`, task A depends on task B.

## Add provenance and create sequentially

Append this visible footer to every body, after any task description:

```text
---
Created by: <Codex|Claude Code|Junie>
Git branch: <branch or detached>
Git HEAD: <full SHA>
```

Do not put the footer in an HTML comment or omit it from an otherwise empty body. Kotgent records the
actual acting session as the `created` activity author; do not duplicate an ambient session label in the
body as if it were authoritative identity.

Create one task at a time with concrete values. When preflight found a live project, include it from the
first command:

```text
kotgent task add <title> --body <body-with-footer> --project <project-uuid>
```

In explicit outside-pane mode only, append `--session <session-id>`.

When the descriptor was missing or not yet registered, omit `--project` from the first command. Let the
current session context create or adopt the repository project:

```text
kotgent task add <title> --body <body-with-footer>
```

In explicit outside-pane mode only, append `--session <session-id>`.

After that success, record the returned `project` UUID, read `<root>/.kotgent.json`, and require its ID to
match. Use the returned UUID explicitly for every remaining add. If the first add created the descriptor,
mention the untracked file in the result and do not stage, commit, or delete it unless the user separately
asks for that Git operation.

After each success, parse and record the returned `ref`. Create dependencies only after every required
task exists, using returned refs rather than constructing them:

```text
kotgent task dep add <dependent-ref> --on <prerequisite-ref>
```

Stop at the first failed add or dependency command. Preserve every successful task and dependency.
Report the successful refs in creation order, the exact failed command, exit code, and complete stderr.
Never issue compensating deletes.

Finish with the created refs, titles, dependency edges, project UUID, identity mode (and the explicit
session ID only in outside-pane mode), branch, HEAD, and whether this run created `.kotgent.json`. Say
explicitly when the batch is partial.
