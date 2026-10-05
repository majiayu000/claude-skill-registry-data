---
name: board-man
description: Board Manager subagent — sole interface to the GitHub Project board. Other agents delegate all `gh project` and `gh issue` reads/writes to board-man via Task. Owns ID caching, write serialization, and downloading plan comments to .workflow/temp/.
---

# board-man Skill

When invoked, spawn the **board-man** subagent (defined at
`agents/board-man/CLAUDE.md`) and pass it a single-line operation. board-man
returns a JSON object on stdout. Errors return
`{"error": "<msg>", "exit_code": <n>}` and never raise.

This skill is invoked **only by other agents** (coordinator, architect,
manager, coder, github-triage, pull-request) when `workflow.backend ==
github_project` in `agent.yaml`. It is not a user-facing skill.

## Calling convention

```
Task: board-man
Prompt: "<operation> <args>"
```

Operations are listed below. Arguments are positional; values that contain
spaces should be JSON-quoted.

## Operations

### Reads (parallel-safe)

| Operation | Args | Returns |
|-----------|------|---------|
| `list-column <COLUMN>` | column name (BACKLOG\|READY\|TODO\|IN-PROGRESS\|DONE) | `{items: [{issue, title, labels[], parent, plan_comment_id, parallel_group, status}, ...]}` |
| `list-open-prs` | (none) | `{prs: [{number, url, headRefName, comments_count, failing_checks, task_issue}, ...]}` |
| `next-task <REPO>` | repo identifier from agent.yaml.workflow.github_project.repo | `{issue, title, body, branch, parallel_group, repo, parent}` or `{none: true}` |
| `find-issue-by-marker <MARKER>` | text like `"[GH #123]"` | `{issue, item_id}` or `{none: true}` |
| `list-all-tracked-markers` | (none) | `{markers: ["[GH #123]", "[GH #456]", ...]}` |
| `verify-children-done <PARENT>` | parent issue # | `{all_done: bool, pending: [issue#, ...], done: [issue#, ...]}` |
| `download-plan <ISSUE> [<TASK_ID>]` | issue #, optional task-id for namespacing the temp dir | `{path, comment_id}` — file written to `.workflow/temp/<task-id-or-feature-slug>/plan.md` |

### Writes (serialized via `.workflow/temp/.board-man.lock`)

| Operation | Args | Returns |
|-----------|------|---------|
| `create-issue <TYPE> <TITLE> <BODY>` | TYPE ∈ {FEATURE, CHANGE, BUG}, title, body markdown | `{issue, url, item_id}` |
| `create-task-issue <PARENT> <TITLE> <BODY> <PARALLEL_GROUP> <REPO> <BRANCH>` | full task body using manager's task schema | `{issue, url, item_id, parent_issue}` |
| `post-plan-comment <ISSUE> <MARKDOWN>` | issue #, plan markdown | `{comment_id, url}` — also pins `<!-- plan-comment-id: N -->` into parent body |
| `add-comment <ISSUE> <MARKDOWN>` | issue #, body | `{comment_id, url}` |
| `set-status <ISSUE> <COLUMN>` | issue #, target column | `{ok: true, previous: <col>}` |
| `apply-label <ISSUE> <LABEL>` | issue #, label name | `{ok: true}` |

### Maintenance

| Operation | Args | Returns |
|-----------|------|---------|
| `refresh-cache` | (none) | `{cache_path, project_id, status_options}` — re-derives all IDs |
| `cleanup-temp [<HOURS>]` | optional staleness threshold in hours (default 24) | `{deleted: [path, ...]}` |

## Setup state

board-man reads `agent.yaml.workflow.github_project.{owner, number, repo}` and
caches resolved IDs in `.workflow/temp/.board-man-cache.json`:
- `project_id` (PVT_kwDO…)
- `status_field_id` and `status_options{BACKLOG, READY, TODO, IN-PROGRESS, DONE}`
- `parallel_group_field_id`

The cache is regenerated on `refresh-cache` or whenever a `set-status` call
returns 422 (option not found). The cache lives under `.workflow/temp/` so it
is auto-gitignored and freely regenerable.

If the cache is missing on first call, board-man invokes
`scripts/board-man-setup.sh --owner <o> --repo <r> --number <n>
--project-root <root>` to materialize it. If that fails, board-man returns
`{"error": "cache missing and setup failed: <reason>", "exit_code": 4}`.

## Concurrency

- Reads (`list-*`, `find-*`, `next-task`, `verify-children-done`,
  `download-plan`) may run in parallel.
- Writes (`create-*`, `post-plan-comment`, `add-comment`, `set-status`,
  `apply-label`) acquire `.workflow/temp/.board-man.lock` (flock-style) at the
  start and release on exit. Polls every 2s, gives up at 30s with
  `{"error": "lock timeout", "exit_code": 5}`.

## See also

- Agent body: `agents/board-man/CLAUDE.md`
- gh cheatsheet: `agents/board-man/api-cheatsheet.md`
- Provisioning script: `scripts/board-man-setup.sh`
