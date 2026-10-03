---
name: semantic-blast-radius
description: Build the canonical cross-file impact graph with compiler or LSP evidence plus independent ast-grep and rg searches. Use when a nontrivial API, type, shared helper, state machine, or public contract change requires callers, implementations, dependents, tests, and "what else can break." Not for routine local edits or generic reviews. Report partial coverage when a relevant language or edge class is unavailable.
---

# Semantic Blast Radius

Use the repository's compiler, type checker, language server, `ast-grep`, and
`rg` as complementary evidence. Build a proof-carrying impact map before edits.

This skill is the single owner of the impact graph. When
`ast-grep-callchain-audit` or `call-chain-invariants` is also active, do not ask
each skill to rediscover the whole map. Give them this graph: AST review adds or
challenges structural edges; invariant review classifies verified nodes into
applicable product surfaces.

Use this graph schema:

| Node or edge | Canonical identity | Evidence | Boundary or surface | Status |
|---|---|---|---|---|

Include roots, definitions, producers, consumers, callers, callees, state or
serialization boundaries, dynamic wiring, tests, and the unresolved frontier.
Version the graph by repository revision plus the changed-root set.

## Required workflow

1. Confirm the relevant compiler, type checker, or language server is available
   for each language in scope. Mark unsupported language coverage `partial`.
2. Resolve each important name to its definition with LSP, `ast-grep`, or an
   exact `rg` search before tracing it.
3. Ask `ast-grep-callchain-audit` for structural edge evidence when that skill
   applies. Merge its results into this graph rather than creating a second
   inventory. Map imports, exports, implementations, overrides, callers,
   callees, types, and parameter flow with native symbol tooling.
4. Inspect exact source around each verified definition and boundary.
5. Search strings separately for routes, events, queues, RPC methods, SQL,
   configuration keys, dependency injection, templates, and generated wiring.
6. Ask `call-chain-invariants` to classify actual product axes and surfaces when
   the invariant fans out. Add its applicability evidence to the same graph.
7. Identify focused tests for every changed root and downstream boundary.
8. Run the compiler or type checker, linting, and focused tests after mutation.
9. Reconcile disagreements before reporting a verified result.

Derive the search depth from the number of roots, implementation fanout, and
boundary crossings. Batch related searches and deduplicate symbols. Stop when
every acceptance-relevant boundary has evidence, not when the same graph has
been restated through another tool. If a real access or context limit stops
expansion, report the remaining frontier as `partial`.

Read [references/native-workflow.md](references/native-workflow.md) for the search sequence. Read [references/evidence-contract.md](references/evidence-contract.md) before making completeness, dead-code, or blast-radius claims.

## Strong preference rule

Begin with the narrowest tool that matches the evidence gap. Use `rg --files`
for files, `rg` for literals, `ast-grep` for structure, and LSP/compiler tools
for symbol and type relationships.

Use explicit text searches for these cases:

- string-based route, event, queue, RPC, SQL, configuration, template, or dependency-injection wiring;
- reflection, code generation, macro expansion, registry tables, or serialized method names;
- unsupported languages or file types;
- a stale, incomplete, or unhealthy index;
- exact source evidence that the graph result does not include.

Do not treat a text search alone as proof of callers, implementations, or type flow.

## Read-only boundary

For a read-only request, do not mutate. For an authorized change, use the
repository's normal edit workflow after the impact map is complete.

## Output contract

Report these sections when they apply:

- changed or reviewed symbol;
- definitions and implementations;
- direct callers and callees;
- transitive dependents and boundary crossings;
- affected types, contracts, state, and tests;
- dynamic or generated edges from the independent check;
- items that also need a change or human awareness;
- language-tool health, search limits, and excluded scope.

Downstream skills should return graph deltas, applicability labels, or disputed
edges. Merge those once. Do not present three overlapping call-chain reports to
the user.

State the compiler, type checker, LSP, structural searches, text searches,
planned roots, truncated frontiers, and fallback methods in the evidence ledger.

Mark each conclusion as `verified` or `partial`. A result is `partial` when language support, dynamic dispatch, generated code, search limits, or inaccessible scope can hide an edge.
