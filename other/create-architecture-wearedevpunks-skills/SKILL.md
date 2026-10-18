---
name: create-architecture
description: Compile closed requirements-grill decisions into ARCHITECTURE.md before create-spec. Use for a new delivery or to refresh architecture after its sources change.
---

# Create Architecture

Compile a source-attributed explanation of the whole system. Every delivery
needs this artifact. The flow is `requirements-grill -> create-architecture ->
create-spec -> write-backlog`; `SPEC.md` need not exist to run this compiler.

## Steps

1. Read [artifact-contract.md](references/artifact-contract.md) for source
   readiness, authority, freshness, retention, and handoff. Read the grill status
   first, then the durable log. Reconcile stable question IDs, explicit
   supersession, and the current glossary. Read referenced evidence and routed
   learnings needed to establish the accepted scope. Stop with the contract's
   atomic `architecture-not-ready` result when material inputs are unresolved.
2. Resolve the planning surface and capability folder through
   [create-spec's folder-naming.md](../create-spec/references/folder-naming.md).
   Use `ARCHITECTURE.md` in that folder, applying the same identity and collision
   rules. Reserve the future sibling `SPEC.md` path without requiring or
   fabricating the file. Reuse an existing artifact only for the same capability.
3. Resolve and invoke the installed `$flow-lenses` skill on the accepted
   bounded flow. Trace intake, state, control, feedback, recovery, and handoff
   across linked abstraction levels. Account for every lens in its Flow Lenses
   with evidence, an explicit unknown, or a justified not-applicable result. Its
   candidate gaps remain candidates. Return each material gap to
   `requirements-grill` with its Altitude through the contract; compilation
   cannot accept a new mechanism or guarantee.
4. Compile a complete candidate using
   [ARCHITECTURE-TEMPLATE.md](assets/ARCHITECTURE-TEMPLATE.md). Start with actors,
   purpose, capability boundary, and canonical terms. Connect owners,
   authoritative state, entrypoints, critical flows, interfaces, dependencies,
   recovery, and observable completion across levels. Preserve every accepted
   detail through the contract's decision coverage; place accepted L3 Modules
   decisions in the template's **Modules and Interfaces** section. Assign stable
   block and flow selectors under the contract's **Spec traceability** rules;
   preserve exact grill entry
   anchors. Before SPEC exists, leave spec-code mapping explicitly pending.
   Explain how each low-level choice supports a system constraint; keep unknowns
   and parked work visible.
5. Resolve and invoke the installed `$show-me` skill to put the smallest useful
   views **inside the document**: a system map and applicable flow, state, or
   sequence views, each answering a distinct question. Use Mermaid for component,
   data, and control relationships; use pseudocode or shallow call/file trees
   when clearer. Place a short causal conclusion and question/evidence anchors
   beside each view. Preserve source labels, uncertainty, ownership, and order.
   Write context before detail in ASD-STE100 Simplified Technical English, keeping
   exact accepted glossary terms and technical identifiers.
6. Check the complete candidate against the contract before replacing the
   canonical artifact. Resolve relative links and selectors, cover every accepted
   detail, and check each visual against its sources. Validate Mermaid with an available
   parser or renderer; record what ran and any unavailable check. A syntax defect
   needs correction; unavailable rendering must remain a stated limitation.
   Remove template instructions and empty optional sections.
7. Save the complete artifact and apply
   [create-spec's wiki-bookkeeping.md](../create-spec/references/wiki-bookkeeping.md)
   to this artifact: use the architecture title, `ARCHITECTURE.md` path, and
   `Compiled` status in the existing planning indexes, applicable metadata, and
   maintained log. Before a spec exists, record only the architecture link.
   Preserve existing spec entries and unrelated work.
8. Follow the contract's path-limited retention and byte-verification procedure.
   Return its handoff only after retention succeeds. `create-spec` consumes that
   handoff next and completes spec-code mapping under the same contract before
   retaining the final pair. This skill performs no backlog/provider writes.
