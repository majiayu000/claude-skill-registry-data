---
name: roadmap
owner: baseline
description: Read-only view of the execution roadmap. Lists every epic with its per-status tallies, nests the still-open rows beneath their epic, collapses wholly-finished epics into one rollup line, and closes by naming the next planned task in file order. Four verbs — `list` (the reader's view), `tasks` and `epics` (filterable row and epic queries), `next` (the first planned task). Invoke any time to see what is left to build. Not a workflow phase; never writes; never starts or commits work.
disable-model-invocation: true
---

# roadmap — what is left, and what is next

A read-only reader over the execution plan named by `project.json → roadmap.path`, in the family of `standup` and `audit-baseline`: it reads state and reports, it never mutates. It is **not** a workflow phase — it does not enter the Track Guard ordering and never blocks a commit.

`standup` answers six questions and the roadmap is one of them, so it bounds the roadmap section and drops to tallies on a large plan. This command answers only that one question, so it never collapses open rows at any plan size. What collapses instead is the finished work — that is the bulk, and it carries no pickup.

## The verbs

```
node .claude/skills/roadmap/cli.mjs list  [--all] [--epic N] [--json] [--root <dir>]
node .claude/skills/roadmap/cli.mjs tasks [--epic N] [--status done|in-progress|planned] [--json]
node .claude/skills/roadmap/cli.mjs epics [--json]
node .claude/skills/roadmap/cli.mjs next  [--json]
```

| Verb | Answers |
|---|---|
| `list` | The whole plan as a reader sees it — header, rollup, open rows nested under their epic, and the next pickup. |
| `tasks` | Individual rows, filtered by `--epic` and/or `--status`. One line per row. |
| `epics` | One line per epic with its status and its done / in-progress / planned tally. |
| `next` | The first planned row in file order, plus the epic it belongs to. |

Every verb takes `--json` and prints the raw projection instead of the rendering. A missing plan file exits 2 with the path it looked for; a malformed filter exits 1 with the usage error.

## What `list` prints

```
Roadmap — docs/roadmap-execution-plan.md
13 epics · 78 rows · 66 done, 0 in progress, 12 planned

✅ Epics 1-7, 10, 12  (53 rows, all done)

Epic 8  ⬜  Codebugger explanation trace  (0/3 done)
  ⬜ A  Runtime-witness rule and the mcp-debugger declaration
  ⬜ B  The /codebugger session and the explanation trace

Next planned: Epic 8  A  Runtime-witness rule and the mcp-debugger declaration
```

- **The rollup** folds every wholly-done epic into one line, compressing consecutive numbers into ranges. A lone finished epic reads `Epic 4`, never `4-4`.
- **Open rows** are planned and in-progress rows. Every one of them renders, however many there are.
- **`--all`** expands the rollup: each epic gets its own header and its done rows render too.
- **`--epic N`** scopes the view to one epic. Naming an epic is itself a request to see it, so a scoped view never collapses.

Every rendered line is whitespace-collapsed, clipped to 96 characters, and stripped of C0/C1 control characters by `.claude/skills/lib/terminal-text.mjs`. Roadmap titles are repository-controlled content on its way to a terminal, and a row title in this repo already runs past 1000 characters.

## Ordering

`next` and the `Next planned:` line both mean **first in file order** — the first planned row reading the plan top to bottom. Neither resolves a dependency graph; sequencing the work is `sprint-planner`'s job, not this reader's.
