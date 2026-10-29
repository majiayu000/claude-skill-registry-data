---
name: engram-index
description: Index a codebase AND memorize what matters about it — build the code graph, then write durable, evidence-labeled memories (stack, invariants, sharp edges, build/test procedures). Trigger on "index this repo", first session in a repository, or when the engram stale-index reminder fires.
---

# engram-index

Index the code graph, then **memorize the codebase** — the graph alone is
structure; memory is understanding. Evidence-first, always.

Depth on demand: `references/rea-process.md` (the full evidence-first
process) · `references/memorization-catalog.md` (exact write formats).

## Contract

1. Structure comes from `scan_repo` — never from reading files by hand first.
2. Every memorized claim carries an evidence label: `[proven]`, `[likely]`, or `[guessed]`.
3. Every memory written is read back — **an index that cannot be recalled is not an index.**
4. No claim without a tool call behind it. If you cannot prove it, label it `[guessed]` or omit it.
5. Recurring workflows become procedures — an index without runbooks is only half an index.

## Workflow

### 0. Scope (skip if fresh)

Check staleness first. If the repo is already indexed and little changed,
skip to phase 2 (delta-memorize) — don't rescan for nothing.

```
recall({ "query": "repo overview build test invariants" })
```

If recalled memories describe this repo adequately, go to phase 2.
Otherwise continue.

### 1. Surface map

```
scan_repo({ "path": "/absolute/path/to/repo" })
architecture({ "limit": 20 })
graph_health({})
```

Read the architecture output: central symbols (core abstractions), bridges
(critical paths), communities (modules). This is the structural truth —
do NOT open files to "get a feel".

### 2. Memorize

Write memories — one concern per memory, title first. Exact formats:
`references/memorization-catalog.md`. In short:

```
write_memory({ "content": "[proven] <claim> — evidence: <tool + what it showed>" })
```

Memorize, in order of value:
- **Stack + layout** — languages, framework, key directories (`[proven]` from the graph's file entities)
- **Invariants** — naming rules, boundary rules, layering (e.g. "domain crates must not depend on adapters — check-contracts.sh enforces") (`[likely]` if from names alone, `[proven]` if a check/script enforces it)
- **Sharp edges** — bridge symbols ("change_impact shows X is a bridge; touching it ripples into N areas"), god modules, known-tricky paths (`[proven]` via `change_impact`)
- **Core abstractions** — the top 3-5 central symbols, one line each on their role

Memorize procedures — the commands that build/test/verify, AND the
recurring workflows this repo actually performs (indexing, triage,
release, dogfood — whatever the repo's rhythm is):

```
procedure_put({ "name": "verify", "trigger": "before handoff", "steps": ["<exact command>"] })
```

Only procedures you have seen work (from READMEs, CI configs, or this
session). Label untested steps in the trigger field ("untested").
Check what already exists first — `procedure_list({})` — and re-put to
update, don't duplicate.

`write_memory` and `procedure_put` are this skill's authorized writes:
structure-derived memories and repo runbooks. Conceptual entities and
relationships are **not** written here — after indexing, run an
`engram-distill` pass to bridge concepts to the code this scan discovered.

### 3. Verify (write → read-back)

Probe with three recall queries a future agent would actually ask:

```
recall({ "query": "build command" })
recall({ "query": "<top central symbol name>" })
recall({ "query": "<one invariant you wrote>" })
```

If a probe returns nothing (or garbage), the memory was written badly —
rewrite it with more distinctive wording, then re-probe. Do not skip this.

### 4. Report

Concise, no file dumps: N symbols, M modules, core abstractions (top
PageRank), bridges to respect, what was memorized, confidence split
(proven/likely/guessed counts), unknowns worth investigating later.

## When it fails

- `scan_repo` errors → report the error; do not fall back to reading files
  as a "quick index" — that produces structure-free memory.
- Empty architecture → repo may be empty/non-code; say so, stop.
- Read-back probes fail after one rewrite → report which memories didn't
  stick; do not silently continue.

## Anti-patterns

- Reading source files to summarize the repo before scanning (the graph is the map).
- Writing unlabelled claims ("the auth is in middleware" — proven? guessed?).
- Memorizing trivia (file counts, boilerplate names).
- One giant memory blob instead of one-concern-per-memory.

## Final check

- What am I missing in the overview?
- Is every claim labeled and evidenced?
- Would these memories survive a refactor of the code they describe?
- Did all three probes come back?
