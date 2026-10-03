---
name: ast-grep-callchain-audit
description: >
  Perform strict AST-based call-chain and code-quality audits with ast-grep.
  Use for code reviews, refactors, unfamiliar code, dead parameters, duplicate
  helpers, wrong call-site usage, stale functions, AI-generated slop, or
  multi-rail and multi-surface changes.
---

# AST-Grep Call-Chain Audit

Use this skill when a review must understand syntax, files, callers, callees,
types, parameter flow, and repeated implementations. Keep the review strict,
but label conclusions by evidence. An AST match is a candidate, not a defect.

## Ownership boundary

`semantic-blast-radius` owns the canonical impact graph. When it is active,
this skill contributes structural edges and counterexamples to that graph; it
does not produce a competing full blast-radius inventory. `call-chain-invariants`
owns product-surface applicability. This skill may discover a candidate sibling
but does not decide that every sibling shares the invariant.

## Start with the structural tool

Prefer the non-deprecated binary:

```bash
AST_GREP_BIN="$(command -v ast-grep || command -v sg)"
"$AST_GREP_BIN" --version
```

Homebrew installs `ast-grep`. It also provides `sg` as a compatibility alias,
but `sg` currently prints a deprecation warning. Use `ast-grep` in new commands.

Run read-only searches first:

```bash
ast-grep run --pattern 'api.post($PATH, $BODY)' --lang ts frontend/src
ast-grep run --pattern '$OBJ.$METHOD($$$ARGS)' --lang ts backend/src
ast-grep run --pattern 'function $F($$$PARAMS) { $$$BODY }' --lang ts backend/src
```

Use `--files-with-matches`, `--json=stream`, or `--inspect summary` when a
machine-readable or coverage-oriented result helps. Use `--rewrite` only after
the user requests a change and the matches are manually validated.

## Required audit workflow

1. Read the applicable `AGENTS.md` files and identify the language, build
   system, type checker, generated-code boundaries, and framework conventions.
2. Accept the review boundary and changed roots from the canonical impact graph
   when available. Otherwise define them locally. List changed files,
   neighboring modules, exports, route registrations, workers, and tests.
3. Build a syntax inventory. Search for definitions, imports, exports,
   re-exports, method calls, callbacks, constructors, and string-based names.
   Combine `ast-grep` with `rg` because AST search can miss dynamic dispatch,
   generated code, templates, reflection, and configuration references.
4. Map each relevant symbol from definition to callers, then through its
   callees and external sinks. Record file and line evidence for each edge.
5. Trace types and parameters across declarations, interfaces, overrides,
   overloads, destructuring, wrappers, serialization, and call sites. Run the
   repository type checker or linter when it can falsify the map.
6. Run variant searches across plausible sibling implementations, workers, and
   tests. Compare semantics and the selected helper, not only names. Return the
   candidates to `call-chain-invariants` for applicability classification when
   product fan-out is in scope.
7. Try to disprove each finding. Check public exports, framework discovery,
   callbacks, tests, dynamic callers, generated files, and dead-code settings.
   For changed money, auth, settlement, or recovery logic, also search durable
   comments, specifications, tests, and commit/PR history for current intent,
   acknowledged residual risk, and explicit non-goals.
8. Report structural results and candidates before proposing cleanup. Do not silently remove a
   parameter, helper, or branch unless the user asks for implementation.

## Dead parameters and stale functions

Treat a parameter as a cleanup candidate only when all of these hold:

- the body does not read it, pass it onward, or use it in a type-level branch;
- no interface, override, callback contract, public export, decorator, or
  framework registration requires its position or name;
- all known call sites can be updated without changing the external contract;
- tests and the type checker do not rely on the current signature.

An underscore-prefixed parameter can be intentional. A zero-result call search
does not prove that a function is dead. Check exports, re-exports, route tables,
dependency injection, event names, reflection, templates, generated code, and
dynamic imports before reporting it. Tell the user the exact evidence and give
the smallest safe cleanup suggestion.

## Detecting likely AI slop

Use “possible AI slop” as an evidence-backed label, never as a style insult.
Flag the signal and the proof together. Strong signals include:

- two near-identical helpers where one has real callers and the other has no
  callers or is wired to the wrong surface;
- a call site that selects a similarly named helper with the wrong rail,
  network, type, unit, or authorization semantics;
- parameters, imports, locals, comments, casts, or defensive branches with no
  observable purpose;
- a new abstraction that duplicates an existing native or shared helper;
- a comment or function name that claims an invariant the implementation does
  not enforce;
- a broad fallback, `any` cast, swallowed error, or copy-pasted condition that
  hides a missing contract check.

For each suspected slop item, report: location, observed symbol and callers,
expected symbol or invariant, actual behavior, why the mismatch matters,
confidence, and a minimal cleanup. Do not call code slop merely because it is
verbose, unfamiliar, or generated-looking.

## Evidence and output gate

Use this compact table while working. When a canonical impact graph exists,
return only new, disputed, or corrected edges:

| Symbol or invariant | Definition | Callers | Callees/sinks | Type/parameter result | Variants | Structural status |
|---|---|---|---|---|---|---|

Use only `EDGE_VERIFIED`, `PATH_PARTIAL`, or `PATH_OPEN` in the structural-status
column. Add `BUG STATUS: UNADJUDICATED` whenever the table contributes to a bug,
security, money, or decision-changing review. Structural verification proves
definitions, edges, types, and visible variants; it does not prove a violated
product contract, defect severity, or safe remediation. This skill must not
assign those conclusions.

State the search boundary and diagnostic gaps. Do not call a bounded AST sweep
exhaustive. Before saying “done,” include the searches used, the call-chain
edges checked, any dead parameter or slop candidates, and the tests or type
checks that support the structural claim. Send semantic candidates to the
owning adjudication workflow rather than promoting `EDGE_VERIFIED` to a verified
bug.

See [references/patterns.md](references/patterns.md) for reusable patterns and
the bundled `scripts/structural-search.sh` wrapper.
