---
name: review-tasks
description: Audit todo kotgent tasks against the current repository and recommend whether to keep, rewrite, merge, drop, or escalate them. Use when the user asks to review, groom, clean up, triage, or validate the todo backlog for completed, obsolete, conflicting, duplicate, absorbed, or incorrectly blocked tasks. This workflow is always read-only.
disable-model-invocation: true
---

# Review Tasks

Review only `todo` tasks and produce recommendations backed by repository evidence. Use the `kotgent` CLI
for tracker reads and `git` plus ordinary file inspection for repository evidence. Do not use an MCP
server, SDK, direct daemon request, or helper script.

## Stay read-only

Do not add comments, change state, edit dependencies, delete tasks, initialize or restore projects, or
edit repository files. In particular, do not run any mutating `task` or `project` subcommand.

Treat successful `task` and `project` stdout as JSON and failure stderr as JSON. Exit `2` is a
command-construction error whose stderr may be plain usage text; stop and report the exact command and
stderr. Do not retry a deleted-project error or restore/reinitialize a project.

## Collect the review set

1. Require `git` and `kotgent`, resolve the Git root, and read the root `.kotgent.json`. Stop if its project
   UUID is unavailable or invalid.
2. Determine whether that exact UUID is live with `kotgent project list` or archived with
   `kotgent project list --archived`. An archived backlog may be reviewed read-only; label it clearly.
3. Run `kotgent task list --project <project-uuid>`. Select only rows whose state is exactly `todo`.
   Other states may be comparison evidence, but never make them review candidates.
4. Run `kotgent task show <ref>` for every todo row. When a blocked task depends on another ref, read that
   dependency's detail as needed to evaluate the edge.
5. Record branch, full HEAD, and `git status --short` to identify the repository snapshot.

## Test each todo task

Read applicable `AGENTS.md` and `CLAUDE.md` first, then active plans/backlogs, implementation, tests,
relevant TODO/FIXME markers, uncommitted work, and focused Git history. Test each task for:

- work already implemented and verified in code or history;
- obsolete assumptions, APIs, product intent, or plans;
- conflict with current architecture or repository rules;
- duplicate scope with another active task;
- scope absorbed by a broader task or completed change;
- an incorrect blocker: the dependency is already satisfied, unrelated, reversed, or contradicted by
  current repository sequencing.

Do not call work completed from a matching filename or commit subject alone. Cite behavior, tests,
symbols, lines, or task activity. Treat ambiguous product decisions as human decisions.

## Recommend one outcome

Assign exactly one recommendation to each todo task:

- `keep`: still correct, distinct, and actionable; preserve it as written.
- `rewrite`: intent remains, but scope, assumptions, acceptance evidence, or dependency wording is stale.
- `merge`: another task should absorb it; name the target ref and the surviving scope.
- `drop`: current evidence proves it completed, obsolete, contradictory, or wholly absorbed.
- `needs human`: evidence conflicts or the decision is product/architecture policy rather than fact.

For a blocked task, separately state whether each edge is valid and why. Do not recommend dropping a task
solely because it is blocked.

Report the project status and Git snapshot, then one row per todo task with ref, title, blocked state,
finding, recommendation, target ref when merging, and precise evidence. End with counts by recommendation
and unresolved human decisions. Do not write comments, change states, edit dependencies, or delete tasks.
