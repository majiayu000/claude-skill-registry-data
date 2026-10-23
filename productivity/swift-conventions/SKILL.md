---
name: swift-conventions
description: "Use when writing or reviewing Swift: API naming and labels, concurrency and actors, errors, reference ownership and memory access, linter configuration."
---

# swift-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the design of Swift declarations and call sites (§1, §2) and,
since 2026-10-02, concurrency, errors, reference ownership and linter configuration (§3 to §6), each from the
language project's own guide or tool README (`references/origin.md`).

**Special status**: 🟡. Not read, so absent from the block: SwiftUI, the formatter, the linter's rule
catalogue, and the platform vendor's developer documentation. A review of those areas gets no rule from here;
it says "no source read".

## When
As soon as a Swift declaration is added or renamed, during `code` (6) or `tdd` (5), and in `review` (8) of
any change that touches a public or module-level name.

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Naming and fluent usage | a type, method, property or protocol is named | [`01-naming.md`](./references/01-naming.md) |
| 2 | Parameters, labels, documentation | a signature is written, a label chosen, a public declaration documented | [`02-parameters-labels-docs.md`](./references/02-parameters-labels-docs.md) |
| 3 | Concurrency | an async function, task, task group, actor, main-actor annotation or shared type is written | [`03-concurrency.md`](./references/03-concurrency.md) |
| 4 | Errors | a function can fail, an error type is defined, a throwing call is written, cleanup must survive a failure | [`04-errors.md`](./references/04-errors.md) |
| 5 | Reference ownership and memory access | a class holds another class, a closure is stored, a delegate link is declared, an in-out argument is passed | [`05-ownership-memory.md`](./references/05-ownership-memory.md) |
| 6 | Linter configuration | the linter config, an inline disable or a baseline changes | [`06-linting.md`](./references/06-linting.md) |

## Output / checkpoint
Declarations whose use sites read as the guidelines require, checked by writing the call at its use site and
reading it. Checked by `review` (8).

## Guardrails
No comments in the code produced; documentation comments on the public declarations of a published module
are the product and follow §2.5. Never rename a published declaration without the deprecation path of the
project.

## Origin
Rewritten from the Swift API design guidelines, credit and pinned commit in
[`references/origin.md`](./references/origin.md).
