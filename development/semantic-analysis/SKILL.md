---
name: semantic-analysis
description: Understand code meaning — ASTs, call/flow graphs, structural search, taint basics, refactor safety.
version: 1
triggers: semantic analysis, ast, call graph, taint, code meaning, refactor safely
category: Engineering & code
blurb: Understand code's meaning — ASTs, call and flow graphs, structural search and refactor safety.
archetype: knowledge
example: Analyze what this code actually does, beyond its surface.
---

# Semantic Analysis (Code)

Text search finds strings; semantic analysis finds meaning. Parse the code, reason about symbols and flows, and act on structure — the backbone of safe refactors and real review.

## When to use
- Large-scale refactors or migrations (rename/reshape across a codebase).
- Security review (flows of untrusted data), dead-code hunts, dependency spelunking.
- Building code intelligence into tooling (linters, codemods, analysis scripts).

## Method
1. **Parse, don't regex**: use an AST (tree-sitter/compiler front-ends) for anything structural; regex only as last resort, with tests.
2. **Symbols & scopes**: resolve definitions/references before renaming; watch shadowing; know dynamic-dispatch limits (when static answers aren't possible).
3. **Call & data flow**: call graphs for impact analysis; data flow (source → transform → sink) for taint-style checks — untrusted input reaching exec/SQL/HTML = finding.
4. **Control flow**: paths, early exits, unreachable code; verify invariants on all paths, not just the pretty one.
5. **Structural search / codemods**: semgrep-style patterns for consistency checks; codemods for mechanical changes — always dry-run → diff review → tests → apply.
6. **Type & contract extraction**: infer expected types/contracts at boundaries; mismatches are bugs (any language).
7. **Similarity & intent**: near-duplicate detection for refactor candidates; embeddings/clustering for comprehension at scale (route, don't trust blindly).
8. **Evidence for reviewers**: findings with code pointers + severity; each claim re-runnable via a query/script checked into the repo.

## Quality gates
- [ ] Structural operations use AST tooling (or regex + tests if forced).
- [ ] Renames/codemods: dry-run diff reviewed + full test suite green.
- [ ] Taint/flow findings list source → sink with paths.
- [ ] Analysis queries/scripts versioned with the repo.

## Red lines
- No regex-driven refactors without verification; no "looks unused" deletions without reachability checks; never apply a codemod without tests.

## Related
`code-visualization` · `code-review-practice` · `mcp-engineering` (analysis tools for agents).
