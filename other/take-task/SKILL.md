---
name: take-task
description: Safely claim a specific or next eligible kotgent task from a free session, detect blocked or concurrent work, and immediately continue through the work-task workflow. Use when the user asks to take, claim, pick up, start, or work the next kotgent task, optionally naming a task ref.
disable-model-invocation: true
---

# Take Task

Claim work only from a free kotgent session. Use the `kotgent` CLI for tracker operations and `git` for
repository state. Do not use an MCP server, SDK, direct daemon request, or helper script.

## Resolve the caller identity

Use the live kotgent pane as identity by default. Never read `KOTGENT_SESSION_ID` as identity or copy it
into `--session`. Outside a kotgent pane, require an exact session ID explicitly supplied by the invocation
context or user and append `--session <session-id>` to the session-scoped commands below. Never infer an ID
from provider conversation IDs, environment variables, names, cwd, recency, or `kotgent list`. Choose one
mode for the whole run.

Require `git` and `kotgent` on `PATH` and a Git worktree, but make the pane form the first `kotgent task`
command:

```text
kotgent task show
```

Use `kotgent task show --session <session-id>` only in explicit outside-pane mode.

Interpret it strictly:

- Exit `0` means the session already holds a task. Report that task and stop; do not claim or call `next`.
- Continue only on exit `1`, empty stdout, no `status` field, and `error` exactly equal to the matching
  message: ``this session is not linked to a task — name one, or link one with `kotgent task claim <ref>` ``
  in pane mode, or `session '<session-id>' is not linked to a task — name one: kotgent task <command>
  <ref> --session <session-id>` in explicit mode.
- Treat every other response as a real failure and stop. Exit `2` is a command-construction bug whose
  stderr may be plain usage text.

Never use `task unlink` to make a session appear free.

## Resolve a candidate

When no ref was supplied:

1. Resolve the Git root, read its `.kotgent.json`, and require the exact project UUID in
   `kotgent project list`. If it is absent or archived, stop; never initialize, restore, switch, or retry.
2. Run:

   ```text
   kotgent task next --project <project-uuid>
   ```

3. Treat exit `3` with `{"task":null}` as normal absence of work and stop successfully. Treat any other
   nonzero exit as failure. Record the returned ref; do not call `next` again.

When a ref was supplied:

1. Run `kotgent task show <ref>` before claiming.
2. Require `task.state == "todo"` and `task.blocked == false`. Stop for blocked work and for
   `in_progress`, `review`, or `done`; never auto-claim those states.
3. Require the task's project UUID in `kotgent project list`. Stop if it is unknown or archived.
4. Run `kotgent task claim <ref>` exactly once.

Append `--session <session-id>` to `task next` and `task claim` only in explicit outside-pane mode.

Task links are non-exclusive. A successful claim is not proof of ownership.

## Detect parallel work after claiming

Immediately run ref-less `kotgent task show` again (with `--session` only in explicit outside-pane mode),
require its returned ref to match the claimed candidate, and inspect the refreshed task, complete activity
feed, and every linked session. Also inspect `git status --short`, the current branch or detached state,
full HEAD, and diffs relevant to the task.

Treat these as parallel-work signals unless the user already established a division of work:

- another non-archived, live linked session;
- comments or links from another session indicating active implementation;
- uncommitted changes overlapping the task that this session did not create;
- recent commits or task transitions showing someone else is already executing the same scope.

On any signal, leave one concrete coordination comment naming the sessions, paths, activity, or commits:

```text
kotgent task comment -m <coordination-evidence-and-request>
```

Append `--session <session-id>` only in explicit outside-pane mode.

Then stop with the task left `in_progress` and linked. Do not unlink it, claim another task, or race the
other worker.

If no conflict exists, immediately continue with the `work-task` workflow from this plugin, carrying the
ref, identity mode, refreshed detail, and Git snapshot forward. Do not stop after claiming and do not
claim the task again. Never run `task done`, and never run `task next` after review.
