---
name: swift-language
description: "Write or review Swift APIs, value models, dependency injection, error contracts, access control, formatting, and language-version migrations without imposing an app architecture."
---

# Swift API design and dependency boundaries

## Inputs

Read call sites, public clients, compiler/language modes, product vocabulary, side effects, and the smallest dependency seam needed for tests.

## Rules

- **LANG-001 — Review use, not spelling.** Name units, mutation, optionality, and failure at the call site. Do not rename stable persisted keys or public APIs merely for style.
- **LANG-002 — Choose semantic types.** Prefer values for independent snapshots and explicit reference ownership for shared identity. Use domain IDs and enums when distinctions prevent invalid states.
- **LANG-003 — Inject nondeterminism.** Pass the clock, ID generator, transport, or store where behavior depends on it. A closure or small protocol is enough; no dependency framework is mandatory.
- **LANG-004 — Make failure meaningful.** Separate absence, invalid input, cancellation, and operational failure. Preserve recovery information without exposing private details to UI or logs.
- **LANG-005 — Migrate deliberately.** Verify compiler support, language mode, deployment availability, and downstream clients separately. Avoid global format or architecture churn during a correctness fix.

## Workflow

1. Read a representative successful and failing call site before redesigning declarations.
2. Define ownership, preconditions, outputs, side effects, and complexity.
3. Apply the smallest typed change and preserve deliberate architecture conventions.
4. Add contract tests and compile affected clients before removing compatibility.

## Verify

Exercise boundary values, equality/hash identity, decoding old fixtures, locale/time-zone behavior, and error propagation. Build all affected public clients.

## Output

Return the API contract, rationale at real call sites, compatibility impact, and focused test evidence.

## References

- [API and dependency review](references/api-and-dependencies.md).
