---
name: code-graph
description: How to read and refresh the generated code-structure graph at .claude/code-graph/graph.json (import/call relationships between files). Use before a broad exploration pass, for impact analysis ("what depends on this file"), or when the graph looks stale after structural changes.
---

# Code-structure graph

`.claude/code-graph/graph.json` is a generated, regex-based map of import/require/use
relationships between source files — a cheap alternative to re-grepping the whole
tree every time you need to know what points at what. It is **not** a full type-aware
AST graph; treat it as a fast first pass, not ground truth for something high-stakes.

## Reading it

It's a flat list of `{"from": "<file>", "to": "<imported-module-or-path>"}` edges.
For impact analysis ("what breaks if I change/remove this file"), grep the graph for
edges where `to` matches the target, then confirm the real ones by reading those
call sites — the graph can have false positives from string matching (e.g. a
require of a similarly-named module).

## Regenerating it

Run `./scripts/build-code-graph.sh` (or invoke the `graph-keeper` subagent, or
`/graph-update`) whenever:
- files have moved/been renamed at meaningful scale,
- a session's exploration keeps turning up edges the graph doesn't have, meaning it's
  gone stale,
- before a large refactor, so impact analysis is based on current reality.

Never hand-edit `graph.json` — it's a cache, and hand edits will just get overwritten
next regeneration. If the auto-generated edges are missing something structurally
important, that's a sign to improve `scripts/build-code-graph.sh`'s detection for this
repo's stack, not to patch the output.

## When a real AST tool beats the regex fallback

If this project has (or can install) a proper dependency-graph tool for its language —
`madge` (JS/TS), `pydeps`/`grimp` (Python), `go mod graph` (Go), `cargo modules`
(Rust) — prefer wiring that into `scripts/build-code-graph.sh` for this repo instead
of relying on the generic fallback. The regex scan exists so the template works with
zero extra installs everywhere; a real tool is strictly better when available.

## Structural lint, not just structure

`.claude/ast-grep/` (https://ast-grep.github.io/) is a separate, complementary tool:
where this graph answers "what points at what," ast-grep answers "does any code
match this exact structural pattern" — tree-sitter-based, so it doesn't false-positive
on strings/comments the way a regex would. It's wired into `scripts/run-checks.sh` as
an optional step, inert until you copy a rule from `.claude/ast-grep/rules-examples/`
into `.claude/ast-grep/rules/`. Reach for it when a review keeps flagging the same
kind of mistake by hand — codify it as a rule instead of re-finding it every time.
