---
name: fleet-urls
description: >
  Resolve URLs for cross-referencing across the fleet. Given a project name,
  branch, file path, task ID, or PR number — produces the correct clickable
  GitHub and Mission Control URLs. Use whenever you need to include links
  in PRs, task comments, board memory, or IRC messages.
  Triggers on: "resolve urls", "get links", "fleet urls", "cross reference".
user-invocable: true
---

# Fleet URL Resolver

Generate correct clickable URLs for any fleet artifact. **Use this skill whenever
you produce output that references code, tasks, PRs, or files.**

## Configuration

URL templates and project mappings are in `config/url-templates.yaml` at the fleet root.
Read it to resolve project names to GitHub owner/repo.

## How to Resolve URLs

### Step 1: Identify your project

Read `config/url-templates.yaml` → `projects` section to get `owner` and `repo`.

### Step 2: Build URLs using the templates

Given:
- `project`: nnrt
- `branch`: fleet/software-engineer/3402f526
- `task_id`: 3402f526-78c2-455f-b7fb-f21765d67593
- `pr_number`: 3
- `files`: [nnrt/core/engine.py]
- `sha`: 8223d7c

Resolve from `config/url-templates.yaml`:
- `owner`: cyberpunk042
- `repo`: Narrative-to-Neutral-Report-Transformer

Produce:

| Reference | URL |
|-----------|-----|
| PR | `https://github.com/cyberpunk042/Narrative-to-Neutral-Report-Transformer/pull/3` |
| Compare | `https://github.com/cyberpunk042/Narrative-to-Neutral-Report-Transformer/compare/main...fleet/software-engineer/3402f526` |
| File | `https://github.com/cyberpunk042/Narrative-to-Neutral-Report-Transformer/blob/fleet/software-engineer/3402f526/nnrt/core/engine.py` |
| Commit | `https://github.com/cyberpunk042/Narrative-to-Neutral-Report-Transformer/commit/8223d7c` |
| Task | `http://localhost:3000/boards/828d80ab-6bda-4d23-9da3-a670f14ea710/tasks/3402f526-78c2-455f-b7fb-f21765d67593` |

### Step 3: Use in markdown

Always use markdown link format: `[display text](url)`

```markdown
**PR:** [#3 — Fix test collection](https://github.com/.../pull/3)
**Compare:** [main...fleet/sw-eng/3402f526](https://github.com/.../compare/main...fleet/software-engineer/3402f526)
**File:** [`nnrt/core/engine.py`](https://github.com/.../blob/fleet/software-engineer/3402f526/nnrt/core/engine.py)
**Commit:** [`8223d7c`](https://github.com/.../commit/8223d7c)
**Task:** [Fix test collection](http://localhost:3000/boards/.../tasks/...)
```

## Board ID

The fleet board ID is available from your TOOLS.md (`BOARD_ID` field).
Use it for MC task URLs.

## Rules

- **EVERY** reference to a file, commit, PR, branch, or task MUST be a clickable link
- **NEVER** paste bare file paths without GitHub URLs
- **NEVER** reference a task without its MC URL
- **NEVER** reference a PR without its GitHub URL
- Read `config/url-templates.yaml` once at session start and cache the values