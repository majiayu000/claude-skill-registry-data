---
name: task-tree
description: Operate on superRA/ task trees. Use to query frontier, DAG, or tree views; create or restructure tasks; edit statuses; serve dashboards; or migrate legacy PLAN.md/RESULTS.md.
user-invocable: true
---

# Task Tree

## Core Concepts

- **Task** — an immediate subdirectory of a task directory or the rootless `./superRA` forest that contains `task.md`. `attachments/` is always an asset container, never a task. A leaf task has no child task directories.
- **Filesystem hierarchy is the task hierarchy.** `walk_plan()` discovers children by scanning subdirectories.
- Retained files are companions, not task nodes — classification, placement, and lifecycle in `../using-superra/references/task-companion-files.md`.
- **Dependencies are sibling-only.** `depends_on` values are sibling directory names within the same parent.
- **Parent status rolls up** from children automatically — `approved` only when all active (non-parked) children are `approved`; `archived` and `postponed` children are excluded.
- **DAG order vs. display order.** The dependency DAG controls execution order; numeric directory prefixes (`01-load`, `02-merge`) control display order only. Independent.

## CLI Setup

Bootstrap a fresh project's wrapper from the loaded skill directory (`<skill-dir>` = the directory holding this `SKILL.md`; substitute the real path), then use the wrapper for everything after:

```bash
uv run --script <skill-dir>/scripts/cli.py wrapper init   # writes superRA/superra (planner/main bootstrap)
./superRA/superra wrapper init                             # refresh an existing wrapper; idempotent
```

## Reading the Tree

Run the committed `./superRA/superra` wrapper created above — contributors inside the superRA checkout substitute `uv run --script skills/task-tree/scripts/cli.py`. Every `superra …` example below and in the references denotes it:

```bash
./superRA/superra task tree            # tree with status badges
./superRA/superra task frontier        # dispatchable leaf tasks
./superRA/superra task dag 01-data     # dependency DAG for a subtree (Mermaid)
./superRA/superra task tree --json     # JSON output
./superRA/superra dashboard --no-open  # idempotent; starts or reuses a server and prints this worktree's scoped URL
```

**Deep-link a dashboard task:** append `#/<task-path>` to the scoped URL from `dashboard --no-open`. `<task-path>` is the `task read` locator (no `superRA/` prefix, empty for the tree root). Use the emitted URL as-is — its URL-encoded `?wt=` selector handles worktree-name collisions.

## Task File Format

```yaml
---
title: "Merge with Fund Characteristics"
status: not-started
depends_on:
  - 01-load-raw-data
---

## Objective

Left join holdings with fund characteristics on fund_id x date.
Use CRSP-style merge conventions. Validate row counts post-merge.

## Results

Left join preserved all 4.7M holdings rows.
Quarterly characteristics were matched to monthly holdings by nearest prior date.

## Review Notes
> [BLOCKING] Inner join used instead of left join
```

Field-by-field anatomy and body-section ownership: `references/task-file-contract.md` §Task Anatomy.

## Routing — operate on the tree

| To do X | See |
|---|---|
| Create / rename / link / move tasks; bulk status propagation; append results programmatically | `references/commands.md` |
| Read or resolve task comments (the read/resolve loop; comments also surface via `superra task read`) | `references/commands.md §Comments` |
| Validate tree structure, fix status inconsistencies, diagnose orphaned `depends_on` entries | `references/commands.md §Diagnostics` |
| Task-file anatomy, fields, status/dependencies, inherited context, results shape, stale-content, figure embedding | `references/task-file-contract.md` |
| Task companion-file classification, placement, reproducibility, promotion, and maturation | `../using-superra/references/task-companion-files.md` |
| Objective writing, task splitting, placement, durable homes, update-task lifecycle, retroactive task-tree creation | `../superplan/references/task-tree-design.md` |
| Migrate legacy `PLAN.md` + `RESULTS.md`, or upgrade `superRA/` v1 → v2 | `references/internals.md §Migration` |
| Dashboard server mechanics (idempotent ensure-running, task URLs, artifact export) | `references/internals.md §Dashboard` |
| Modify the skill itself (data layer, hooks, scripts) | `references/internals.md`; hook coverage details live in `§Hook Architecture` |

Intentional task path changes go through `superra task move` (`task rename` for same-parent compatibility), never raw `mv` / `git mv`. It resolves the fallout — relative Markdown links tree-wide and sibling-only `depends_on` edges — so run the move directly rather than rewriting links or rewiring dependencies by hand first. Mechanics and cross-parent dependency rules: `references/commands.md §Move / rename a task`.
