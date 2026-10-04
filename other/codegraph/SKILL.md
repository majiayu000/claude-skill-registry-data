---
name: codegraph
description: >-
  Reach for this whenever doing a task well depends on knowing how the codebase
  actually fits together — and getting that wrong would mean reasoning from a
  guess. The need is almost always buried inside a larger task, never asked for
  directly, so recognize it from the work you're doing:
  — Exploring or scoping a new feature or change: where it would hook in, what it
  would touch, what already depends on the areas involved, before settling on an
  approach.
  — Assessing or reviewing something — a plan, an architecture or design doc, a
  PR, or a stretch of code — where the judgment hinges on whether its claims
  about how the parts depend on each other actually hold up against the real
  structure.
  — Debugging and problem-solving: tracing how a failure or a change propagates,
  or working from a symptom back to the code that feeds into it.
  — Any moment you are about to assert what uses what, what a change affects, or
  how pieces connect, where the alternative is inferring it from memory, a
  partial read, or grep.
  Across all of these the user will describe the bigger task, not the dependency
  question inside it — grounding that reasoning in the real wiring is your job,
  not theirs to ask for. codegraph answers it deterministically from actual
  import/require/include edges (JS/TS, Python, C++/Arduino), catching transitive,
  re-exported, path-aliased, and dynamic links that hand-tracing and grep miss.
  Treat it as the source of truth for how the code is wired before you reason
  from assumptions.
---

# codegraph

codegraph builds a **real dependency graph** of a codebase by parsing actual
`import` / `require` / `#include` statements — no LLM guessing, fully
deterministic. Once scanned, you query the graph instead of reconstructing
relationships in your head from greps. That distinction is the whole point: when
you hand-trace dependencies you reliably miss transitive chains, dynamic
`import()`, re-exports, and TypeScript path aliases. The graph already has them.

Reach for codegraph any time a question is fundamentally *"how is this codebase
wired together?"* — impact, dependents, cycles, layers, dead code, doc-sync.

## The one rule: scan first

Every query tool operates on an in-memory graph built by `codegraph_scan`.
Without a prior scan they return a "no graph loaded" error. So the first action
in any codegraph workflow is always:

```text
codegraph_scan({ root_dir: "/abs/path/to/project" })
```

`root_dir` must be **absolute**. The scan returns counts by language, doc-file
count, and parse errors. The graph then persists for the whole session (and to
an on-disk cache keyed by the root path, so a later scan of the same root is an
incremental rescan — only changed files re-parse).

Re-scan after you've made significant edits. Incremental rescans are
**mtime-based**, which has one sharp edge: an *unchanged* file that gains a
newly-resolvable import to a *newly-added* file — or an edit to a non-tracked
config like `tsconfig.json` — is not picked up until the importer itself is
touched. When in doubt, force a clean rebuild:

```text
codegraph_scan({ root_dir: "...", force: true })
```

## Tools at a glance

Pick the tool by the job. Full parameters and return shapes are in
`references/tools.md` — read it when you need exact field names or are wiring
codegraph into a hook/script.

| Job | Tool |
|---|---|
| **Build/refresh the graph** | `codegraph_scan` (always first) |
| Keep graph live as files change | `codegraph_watch_start` / `codegraph_watch_stop` |
| What does X import? | `codegraph_get_dependencies` |
| What imports X? (who breaks if X changes) | `codegraph_get_dependents` |
| Full blast radius of changing file(s) | `codegraph_get_change_impact` |
| Local neighborhood around a file | `codegraph_get_subgraph` |
| Why does A depend on B? (shortest chain) | `codegraph_get_path_between` |
| Which docs must be reviewed after a change | `codegraph_find_related_docs` |
| Codebase overview / most-depended-on files | `codegraph_get_stats` |
| Architectural tiers (topological layers) | `codegraph_get_layers` |
| Circular dependencies | `codegraph_find_cycles` |
| Dead-code candidates (zero in, zero out) | `codegraph_find_orphans` |
| Roots (nothing imports them) | `codegraph_find_entry_points` |
| Enumerate code files | `codegraph_list_files` |
| Enumerate documentation files | `codegraph_list_docs` |
| Dependency diagram (Markdown/GitHub) | `codegraph_export_mermaid` |
| Dependency diagram (Graphviz → SVG/PNG) | `codegraph_export_dot` |

File arguments are **fuzzy-resolved**: you can pass an absolute path, a path
relative to the project root (`src/auth/login.ts`), or just a unique filename
(`login.ts`). If a bare filename is ambiguous, the tool tells you — qualify it
with more of the path.

## Core workflows

These are the high-value sequences. They matter more than any single tool call.

### Before you edit, refactor, rename, or delete a file

This is codegraph's primary use. Do not start changing a shared file until you
know its blast radius — that knowledge changes *how* you make the edit (e.g.
keeping a signature backward-compatible because 14 files depend on it).

```text
1. codegraph_scan({ root_dir })                       # if not already scanned
2. codegraph_get_change_impact({ files: ["src/api.ts"] })
       → directlyAffected, transitivelyAffected, totalImpacted,
         blastRadius (a COUNT), coveragePercent
3. codegraph_get_subgraph({ file: "src/api.ts", depth: 2 })   # context to read first
4. codegraph_find_related_docs({ files: ["src/api.ts"] })     # docs to update too
```

Then make the change informed by what you found, and re-run
`codegraph_get_change_impact` if you want to confirm the surface you touched.

### "Is this safe to delete?" / "What uses this?"

```text
codegraph_get_dependents({ file: "src/legacy/helper.ts" })
```

`dependentCount: 0` means nothing imports it — a deletion candidate, but verify
it isn't a legitimate entry point (CLI, test, route) before removing. For files
that are *also* importing nothing, `codegraph_find_orphans` surfaces the fully
isolated dead-code candidates in one shot.

### Verify a completion claim (don't take "nothing else is affected" on faith)

When you — or another agent — claim a change was isolated, check it against the
real graph instead of asserting it from memory:

```text
codegraph_get_change_impact({ files: ["<the files that changed>"] })
```

If `totalImpacted` is larger than what was actually touched, the claim was
wrong. Pair with `codegraph_find_related_docs` to confirm no documentation was
left stale. This is exactly the check a completion-verification hook should run.

### Architecture review of an unfamiliar codebase

```text
1. codegraph_get_stats()        # size, languages, most-depended-on (core) files
2. codegraph_get_layers()       # tiers: layer 0 = leaf deps, up to entry points
3. codegraph_find_cycles()      # circular dependencies (each ring reported once)
4. codegraph_find_orphans()     # dead-code candidates
```

`mostDependedOn` from stats names the critical shared modules — the files where
a mistake propagates furthest. `find_cycles` and a deep `get_layers` together
tell you how tangled vs. cleanly-tiered the architecture is.

### "Why does A depend on B?"

```text
codegraph_get_path_between({ from: "src/index.ts", to: "src/db/pool.ts" })
```

Returns the shortest import chain `from → … → to`. If there's no forward path it
reports `found: false` plus a `reverseExists` hint (maybe B depends on A
instead).

### Visualize the graph

```text
codegraph_export_mermaid({ file: "src/api.ts", depth: 2 })   # paste into Markdown/GitHub
codegraph_export_dot({ max_nodes: 300 })                     # pipe to `dot -Tsvg`
```

Omit `file` to export the whole graph (capped by `max_nodes`, default 200;
over the cap it keeps the highest-degree nodes and sets `truncated: true`).
Scope to a `file` + `depth` for a readable neighborhood diagram.

## Things that will trip you up

- **Code index vs. docs index are separate.** `codegraph_list_files`,
  `get_stats`, and all dependency/impact tools operate only on **code** nodes
  (`.ts`, `.js`, `.py`, `.cpp`, …). Documentation (`.md`, `.mdx`, `.rst`,
  `.txt`) lives in a separate index. In a docs-only directory
  `codegraph_list_files` returns *nothing* — use `codegraph_list_docs`. (It will
  hint you toward `list_docs` in that case.)

- **`blastRadius` means two different things.** In
  `codegraph_get_change_impact` it is a **number** (count of changed +
  impacted files). In `codegraph_find_related_docs` it is an **array** of the
  affected code files. Read the field by the tool that returned it; don't assume
  it's a list.

- **External packages are never pulled in.** Manifests (`package.json`,
  `requirements.txt`, `go.mod`) are graphed, but edges only go to *local /
  workspace* dependencies — the npm/PyPI/Go-module universe is deliberately
  excluded.

- **Only local `#include "file.h"` for C/C++.** System includes
  (`#include <vector>`) are not edges.

## When NOT to use codegraph

codegraph maps *structural* dependencies — who imports whom. It does not do
semantic code search, "find me code that does X", or runtime/call-graph
analysis. For "where is the function that validates emails" use grep/search or a
semantic RAG tool, not codegraph. Use codegraph the moment the question turns to
*wiring*: impact, dependents, cycles, layers, dead code, doc-sync.
