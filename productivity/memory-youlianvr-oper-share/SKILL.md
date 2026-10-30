---
name: memory
description: >-
  Memory and continuity: the RSI tree in `_memory/memora.db` — walk champions and
  pruned dead-ends before acting, branch and verdict nodes with provenance and
  supersedes edges, search report fragments by full text, render the graph on
  request — plus recovery of a lost session through the host's own store and
  structured capture of an unstructured brain dump.
---

# memory — the tree, report search, and session recall

> Home branch in Memora: `root/skill/memory`. Roots: `root/canon` (owner
> decisions), `root/workspace`, `root/project/<name>`, `root/skill/<name>`.

## Choosing a part

| Task | Part |
|---|---|
| Walk, branch, verdict or search `_memory/memora.db` and `_memory/reports/` | this page, inline: the memory CLI in `_scripts/` (`walk`, `branch`, `verdict`, `search`, `render`) |
| Recover a lost conversation or a past answer through the host's session store | `parts/sessions/` |
| Turn an unstructured brain dump or inbox batch into nodes without losing items | `parts/capture/` |

## Rules

- **Walk first.** Before a non-trivial task, walk the matching root and read the
  `promoted` champion and every `pruned` dead-end with its failure reason.
- **Write at entry, during the work and at exit.** A node carries its provenance,
  `parent_id`, a `supersedes` edge when it replaces something, and the period it
  holds for (`valid_from` / `valid_until`) kept apart from when it was recorded.
- **Search reports by fragment.** `search` reads `_memory/reports/` by section
  instead of pulling whole files into context.
- **Render only on request.** The graph file is generated, never committed, and
  regenerated whenever it is shown.
- **A hypothesis is labelled as one.** If a node was not measured or decided by
  the owner, it names its source or says it is unverified.
- **One writer.** A node created by another session is not this session's to
  commit; shared paths are claimed under `_memory/parity/`.

## Related

`planning` (task nodes and the task list), `grill-me` (recording decision
batches), `dev` (what to record as a lesson).
