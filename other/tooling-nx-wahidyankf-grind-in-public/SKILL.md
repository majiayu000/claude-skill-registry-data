---
name: tooling-nx
description: >-
  Guides Nx workspace work under the Nx standard: selecting projects by the graph, adding a target only where a
  capability exists, tracing a stale cached pass to its missing input, and answering a module-boundary finding.
when_to_use: >-
  Use when adding a project or target to an Nx workspace, changing tags, target defaults, or named inputs, or when a
  cached or affected result looks wrong.
compatibility: Requires an Nx workspace with an exactly pinned Nx version.
---

# Nx Tooling

Every Nx rule is owned by [Nx Standards](../../../repo-governance/development/quality/stacks/nx-standards.md), and every
target rule by [Task Runner Target Standards](../../../repo-governance/development/testing-policy.md). The code inside
each project follows that project's own language and framework skills. This skill adds only the procedure and judgement
of working through the runner. Where a sentence here seems to state a rule, the standards decide.

## Start From What the Project Records

Read the repository adapter for the tag vocabulary, the dependency constraints, and how boundaries outside JavaScript
and TypeScript are enforced. Read the project's README for its targets and every omitted one. Then ask Nx what it
resolved rather than reading configuration alone, for example `nx show project <name>`, because inferred targets and
workspace defaults never appear in the project file.

## Select by the Project Graph, Not by Hand

Run change-scoped work through `nx affected` with the targets it needs. When a project you expected is missing from the
selection, that is the finding: look for the dependency or input Nx cannot see, declare it, and rerun. Listing the
project by hand makes this run pass and leaves the next one wrong. When one you did not expect appears, read the graph
before assuming Nx is wrong; an unexpected edge is often a real import.

## Add a Target Only Where a Capability Exists

Before adding a target, confirm the project can really do what the name claims: a unit target runs unit tests that
exist, and a coverage target measures something
[Meaningful Coverage](../../../repo-governance/development/quality/testing/meaningful-coverage.md) admits. An inferred
target the project cannot run is removed or excluded from inference, never left to pass on nothing. Record each omission
in the project's README with its reason.

## Cache Only Deterministic Targets

When a cached result is suspect, rerun the target with `--skip-nx-cache`. If the fresh run fails where the cached one
passed, the cache replayed a result its inputs did not determine. Find the missing input, usually a file another project
owns, an environment variable, or a tool version, add it to the target or a named input, and confirm the cache now
misses on that change. Turning caching off for the target hides the defect rather than fixing it, unless the target is
one the standard never caches.

## Answer a Boundary Finding at the Dependency

A module-boundary finding means one project reached another its tags forbid. Move the shared code to a project both may
depend on, or invert the dependency. Retagging a project or widening a constraint to pass the lint changes the
architecture, and that needs the owner's agreement, recorded in the adapter.

## Before Handing Off

- every new project carries tags from the recorded vocabulary, and the boundary lint passes;
- every new target names a real capability, and every omission is in the project's README;
- each new or changed cached target lists its full inputs and its outputs, and a run skipping the cache agreed with the
  cached one;
- affected selection picked up every project the change touches; and
- the change-scoped gate passed through `nx affected` rather than a hand-picked list.
