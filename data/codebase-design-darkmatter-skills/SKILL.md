---
name: codebase-design
description: Design or simplify packages and modules around cohesive implementations and small interfaces. Use when choosing module boundaries, evaluating an extraction, or improving code readability.
---

# Codebase design

**Keep each capability together, make it simple to use, and split it only when
the split improves understanding.**

A deep module hides substantial behavior behind a small interface. Strong
locality keeps the knowledge needed to change that behavior together. Apply
both when designing or simplifying code; file counts and short functions do not
measure either.

| Rule | Good example | Bad example |
| --- | --- | --- |
| **Organize by domain, then role.** | `billing/models/Invoice.ts` and `billing/services/InvoiceStore.ts`; a focused billing package can start at `src/models/`. | Unrelated billing, chat, and authentication code mixed into global `models/` and `services/`. |
| **Keep related implementation together.** | `Postgres.ts` owns an operation's SQL or typed queries, parameter bindings, and row conversion. | Understanding one query requires following several files that mostly forward calls. |
| **Expose complete operations.** | The caller uses `saveInvoice(invoice)`. | Every caller must encode the invoice, write rows, update the index, and interpret the result in the correct order. |
| **Extract to hide complexity or enable useful reuse.** | A local helper explains a retry policy; two adapters share a decoder with consistent errors. | `runQuery(sql)` merely calls `query(sql)`, adding another name and file to follow. |
| **Define each data contract once.** | When runtime validation is needed, define `InvoiceSchema`; infer `Invoice` from it. | Maintain a schema and a handwritten interface with the same fields. |
| **Convert execution models at the edge.** | Wrap the Promise-based database driver once; keep internal operations in Effect. | Convert `Effect → Promise → Effect` between internal layers. |
| **Own work through completion.** | Await persistence and cleanup before reporting success, or return an explicit task handle to its owner. | Start persistence in the background and immediately report that it succeeded. |
| **Keep line limits; allow justified exceptions.** | A cohesive 330-line adapter gets a documented, file-specific 350-line limit. | Disable the limit globally, or introduce forwarding files solely to satisfy it. |
| **Comment on reasons and invariants.** | “Reuse the delivery key so retries cannot create duplicate invoices.” | “Save the invoice.” |
| **Test observable behavior.** | Save the same delivery twice; verify that only one invoice exists. | Assert only that `saveInvoice` calls the private `insertRow` helper. |

Before extracting, ask: **What will the reader no longer need to understand
after this split?** If the answer is “nothing,” keep it local. A short or
single-use helper can still hide a meaningful decision; neither length nor call
count decides its value. A compile-time-only contract does not need a runtime
schema merely to follow this shape.

Keep explicit, thin public package entries and adapters for real external
interfaces. Remove internal forwarding chains that add navigation without
changing the contract. A module's contract includes ordering, failure, and
cleanup as well as its inputs and outputs.

Retain configured line limits; use 300 nonblank, noncomment lines when
introducing a file limit. Prefer a cohesive split when available, otherwise
document a narrow increase or exception in the lint configuration. Keep other
checks active and resolve diagnostics;
this guidance is not permission to suppress them.

Keep existing typed query tools when useful. Parameterized SQL may live with its
owning adapter when returned rows are validated and query behavior is verified.
A row generic is not validation. A readability change does not require adopting
an ORM or replacing the toolchain. In the source repository,
[ADR-0015](../../docs/adr/0015-cohesive-modules.md) records this decision; the
rules above also apply when an installed skill has no copy of that ADR.

When available, use [domain-organization](../domain-organization/SKILL.md) for
path and filename choices and
[ui-component-architecture](../ui-component-architecture/SKILL.md) for React
package boundaries.
