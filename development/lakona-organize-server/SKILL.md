---
name: lakona-organize-server
description: Audit, explain, or reorganize a Lakona game server without imposing one universal folder tree. Use when reviewing Server directory smells, deciding where Shared, Server.App, or Server.Hotfix code belongs, replacing technical-layer junk drawers with clearer domain locality, aligning namespaces after moves, or validating a proposed server layout while preserving the user's own architectural choices.
---

# Organize a Lakona Server

Preserve Lakona's runtime and assembly seams while treating the directory tree
inside those seams as project-owned design. Make evidence-backed
recommendations and keep harmless variation when it expresses the user's model.

## Workflow

1. Read the target project's instructions, relevant README sections and any
   architecture documentation it provides before judging the tree. Do not
   require the Lakona source repository or its contributor documentation.
   Inventory the Shared, stable App, Hotfix, generated,
   configuration, and test projects. Complete this step when every relevant
   assembly boundary and scoped instruction is accounted for.
2. Establish the requested outcome: diagnosis, options, a proposed tree, or an
   implemented reorganization. Treat stated user preferences as design input.
   For an advisory request, stop at findings and alternatives; for an
   implementation request, carry the selected direction through validation.
3. Read [layout-heuristics.md](references/layout-heuristics.md). Classify every
   recommendation as either a hard Lakona boundary or a soft layout heuristic.
   Complete this step when no preference is presented as a framework
   requirement.
4. Map business capabilities across assemblies. Inspect change clusters,
   namespaces, fully qualified type names, reflection or configuration strings,
   project includes, source-scan tests, and documentation. Complete this step
   when every proposed move has a dependency and reference inventory.
5. Present or choose the smallest coherent improvement. Prefer the project's
   existing domain language and explain meaningful tradeoffs. Keep technical
   folders that have one clear reason to change; reshape only folders whose
   mixed responsibilities make ordinary changes scatter.
6. When authorized to edit, move complete responsibility clusters, then update
   imports, configuration, tests, and docs. Decide namespace/type renames
   separately: HotfixComponent identity is `Type.FullName`. Renames, effective
   component set changes (including stateless helpers), and State binding
   changes require restart. A file move preserving identity can remain reloadable.
   Preserve assembly references, public contract shapes, serialized state, and
   numeric protocol IDs unless the user separately requested their evolution.
7. Split large source files only where the extracted responsibility has a
   stable name and boundary. Prefer internal helpers or partial files when a
   separate public abstraction would add ceremony without ownership.
8. Search for stale paths and namespaces, build every affected project, and
   run focused tests plus source-shape guards. Complete the task only when all
   moved symbols are accounted for and the old organization has no unintended
   references.

## Decision Standard

Use three labels in an audit:

- **Boundary violation**: code crosses a Lakona stability or ownership seam and
  should be corrected.
- **Change-locality smell**: the current tree repeatedly scatters one business
  change; offer a domain-oriented alternative.
- **Preference**: multiple structures are sound; preserve or ask for the
  user's choice.

Treat names such as `Services`, `Contracts`, or `State` as signals to inspect,
not automatic violations. Judge what changes together, who owns it, and
whether the folder communicates that ownership.

## Validation Scope

Apply the validation steps to affected contracts, reusing existing coverage and
adding tests only where meaningful coverage is missing. For non-behavioral,
low-impact edits, use relevant static checks. A test command may also satisfy
the build when it covers the same graph and configuration. Once relevant checks
and required stage gates pass, stop unless new changes, failures, or a concrete
unresolved risk justify more verification. Report any unverified outcomes.

## Completion Report

Report the hard boundaries preserved, optional choices made by the user or
inferred from project evidence, files moved, references updated, and validation
performed. Keep unresolved layout preferences visible instead of presenting
one taste as the only correct architecture.
