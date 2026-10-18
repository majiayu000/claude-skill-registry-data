---
name: docs-onboarding
description: Onboard an existing project into the scaffolded Harness wiki by inspecting code, docs and backlog, closing reconstruction decisions, then handing accepted flows to requirements-phase for architecture/spec compilation. Use after hi init or when initial wiki/spec context must be reconstructed.
---

# Docs Onboarding

Use this skill to turn an existing repository into initial Harness wiki context after `hi init`.

## Workflow

Before naming or rewriting domain concepts, read the canonical glossary in the
routed `requirements-grill` status artifact. Preserve its canonical terms;
route proposed terminology changes through `requirements-grill` instead of
silently renaming them.

1. Read repo guidance and the existing project-owned wiki guidance.
2. Read any existing backlog provider and wiki framework decisions. Resolve
   their locations from project guidance; `hi init` does not generate those files.
3. Discover backlog context:
   - Probe the pinned remote backlog provider first when connector/tool/auth access exists.
   - Inspect local backlog clues after that: existing specs, issue matrices, backlog markdown, project docs, and `.devpunks` metadata.
   - Treat remote backlog evidence and local clues as equally important and mandatory when available.
   - If either lane is missing or inaccessible, ask the developer for the backlog location or access path before assuming no backlog exists.
4. Build and persist the Project Map before asking developer questions.
5. Run a targeted `requirements-grill` against the Project Map for project-wide
   reconstruction decisions.
6. Activate `write-backlog`'s backlog-initialization branch to reconcile the
   Product/Backlog Root, Product Areas, Initiatives, `V*` context, and saved
   views from accepted wiki and provider evidence.
7. Update onboarding navigation and indexes using
   [references/artifact-contract.md](references/artifact-contract.md).
8. Hand every candidate existing flow accepted by the onboarding grill to
   `$requirements-phase` as an explicit human handoff, then stop. For each flow,
   name the exact `$requirements-phase` command and a brief carrying the
   confirmed onboarding grill status/log, its open per-flow decisions, its
   Project Map evidence, and its onboarding projection boundary. Requirements
   Phase compiles `create-architecture` before `create-spec`. The boundary lets
   an agent-ready spec and its mapped architecture reach `write-backlog` only
   when reconstructed evidence already supplies the exact existing Epic/Story
   and accepted projection authority required by that branch. Otherwise record
   the missing authority and exact human Finder invocation in the brief; the
   compiled pair is retained and the backlog delta returns blocked without
   provider mutation. Onboarding never invokes a Finder implicitly and does not
   create higher-level placement.

## Discovery Depth

Inspect entrypoints, routes/pages, commands, API handlers, schemas/models, tests, config/env examples, and existing docs.

Do not deep-read every implementation file by default. Deep-read implementation files only when needed to explain a flow, resolve a contradiction, or map a data boundary.

## Targeted Grill

Grill contradictions, missing backlog location, unclear feature ownership and
inferred requirements before either compiler runs. Observed code-only facts may
remain `Inferred` in the Project Map as evidence; they become accepted requirements
or design choices only through confirmed intent and the recorded grill decisions.
Carry unresolved per-flow material decisions in the step 8 handoff brief; an
inferred current implementation is not permission to choose architecture or
requirements.

## Resumability

Persist the Project Map and grill status before developer questions. On resume, continue from saved discovery/grill state instead of rescanning from zero.

## Guardrails

- Code can prove observed behavior, not original intent.
- Reconstructed spec history must be evidence-backed.
- Do not invent implementation notes, rationale, or tech-debt history without supporting artifacts.
- Use only `write-backlog` for physical provider mutation.
