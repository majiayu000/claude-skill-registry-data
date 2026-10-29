---
name: software-concept-architect-prd
description:
  Transcribes a confirmed concept model into traceable PRD and colocated specification files only
  when the user explicitly invokes $software-concept-architect-prd. Use to preserve purposes, behavior,
  synchronizations, assumptions, exclusions, open decisions, and acceptance provenance without
  redesigning the model.
metadata:
  language: en
  translation_of: software-concept-architect-prd-cn
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# Software Concept Architect · PRD

Focus: how can a confirmed model be persisted without losing purpose, behavior, or acceptance
traceability? Run only on explicit `$software-concept-architect-prd` invocation. Input includes concepts,
synchronizations, dependencies, exclusions, and open decisions. Route model gaps to `software-concept-architect-design`
and code realization to `software-concept-architect-build`.

## Transcription Principles

CONCEPT owns the confirmed concept contract, SYNCS the coordination, and the overall PRD global
relations. Keep one authoritative location per element. Preserve both arguments and assumptions:
contract → OP → concept purpose; selection/sync → application scenario → application purpose.
Derive acceptance with provenance; complete files cannot repair model gaps.

**Synchronization may restrict behavior, never extend the contract**: record application restrictions
in SYNCS/the overall PRD while preserving the concept's allowed behavior. Flag contract-violating
coordination as a model gap for design revision.

## Transcribe

1. **Verify input** — Read the confirmed model, requirement sources, and existing documents. Inspect
   code only for module locations and indexing facts. Never let implementation differences silently
   rewrite the model.
2. **Choose locations** — Use the following layout. Stage centrally only until modules exist.

   ```text
   docs/prd/README.md
   <module>/CONCEPT.md or docs/prd/concepts/<name>.md
   <syncs>/SYNCS.md or docs/prd/SYNCS.md
   ```

3. **Write the overall PRD** — Preserve application purpose, end-to-end scenarios and their
   concept/sync basis, misfits, concept index with purpose and links, synchronization graph, product
   dependencies and subsets, exclusions, and open decisions. Put cross-concept assumptions and
   arguments here.
4. **Write specifications and acceptance** — Read `references/spec-format.md` and
   `references/templates.md`. Preserve the four CONCEPT sections, concept-local assumptions, and
   purpose argument; put application context in notes. Transcribe app/include/sync into one SYNCS
   file grouped by entry point or rule responsibility with `// flow:`. Derive acceptance separately
   from concept OPs, application scenarios, and behavioral contracts, each with provenance. Mark
   missing application goals as open rather than constructing them from concept purposes.
5. **Update consistently** — Make minimal edits to existing documents, refresh indexes and derived
   diagrams, and preserve human-maintained content. Leave implementation-time migration and sync
   package splitting to `software-concept-architect-build`.

Completion requires one authoritative location per model element; no lost definitions, relations,
assumptions, exclusions, or open decisions; independent CONCEPT sections; application instantiation
in SYNCS rather than legacy interactions/dependencies sections; acceptance linked to OP, application
scenario, or contract evidence; real sync declarations for every parameter, binding, and output;
preserved reachable failure behavior and empty-query semantics; and valid global links.

For the first transcription read `references/example-reserving.md`; for specification sources read
`references/sources.md`.
