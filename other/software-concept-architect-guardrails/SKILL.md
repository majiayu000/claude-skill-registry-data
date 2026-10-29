---
name: software-concept-architect-guardrails
description:
  Runs concept-spec guardrails in audit, concept, drift, pipeline, sync, or map mode only when the
  user explicitly invokes $software-concept-architect-guardrails. Use to create, backfill, compare, or map colocated
  concept specifications.
compatibility:
  File read/write and Grep/Glob; optional boundary-injection runtime requires Claude Code hooks and
  jq
metadata:
  language: en
  translation_of: software-concept-architect-guardrails-cn
  author: ontology-of-everything
  version: "1.1.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# Software Concept Architect · Guardrails

Focus: do existing specifications state module contracts clearly and correspond to facts and derived
maps? Run only on explicit `$software-concept-architect-guardrails` invocation. The workflow adapts
[wyx v0.26.0](https://github.com/jlifyio/wyx) under MIT (`LICENSE.upstream`); specifications use
this repository's Jackson dialect while runtime scripts retain upstream behavior.

## Authority Model

- `CONCEPT.md` defines purpose, state, actions, and operational principle; optional notes hold
  application context.
- `SYNCS.md` records app/include/sync coordination for application purposes and scenarios;
  when/where/then define rules and `// flow:` groups them.
- `PIPELINE.md` records sources, stages, outputs, invariants, triggers, and data boundaries without
  replacing synchronizations.
- `ARCHITECTURE.md` is a derived navigation map. Product dependencies come from the overall PRD, not
  synchronization edges.
- Backfill reconstructs evidenced contracts from implementation; drift compares implementation with
  contract. Neither proves fitness for purpose.

**Synchronization may restrict behavior, never extend the contract**: flag violating coordination
during backfill rather than legitimizing it. Coverage does not prove design correctness; accurate
maps do not prove code conformance. Label inferred purposes; an ideal OP cannot justify a defect.

## Modes

Use `$software-concept-architect-guardrails <mode> [path-or-description]`. A path means backfill, a description means
create, and no argument means discover candidates. Start with audit when the mode is absent or the
project has no specifications.

| Mode       | Output and required reference                              |
| ---------- | ---------------------------------------------------------- |
| `audit`    | Read-only coverage and command plan: `references/audit.md` |
| `concept`  | Concept candidates or CONCEPT: `references/concept.md`     |
| `drift`    | Read-only drift report: `references/drift-detection.md`    |
| `pipeline` | Pipeline candidates or PIPELINE: `references/pipeline.md`  |
| `sync`     | Coordination candidates or SYNCS: `references/sync.md`     |
| `map`      | Derived maps: `references/map.md`                          |

Route complex modeling to `software-concept-architect-design`, confirmed-model transcription to `software-concept-architect-prd`, and
fitness/independence/composition review to `software-concept-architect-review`.

## Constraints

- Read specifications, implementation, and project conventions first. Mark current defects during
  backfill; update specifications before implementation for confirmed new behavior.
- Present a draft or diff before unapproved writes. Complete already-authorized creation or repair;
  ask only for unresolved model choices or expanded scope. Discovery lists candidates; read-only
  audits do not write history or fixes.
- Keep one authoritative specification per concept, its PIPELINE beside it, cross-concept pipelines
  in the composition layer, and one SYNCS per synchronization package grouped by flow. Rebuild
  derived maps after specification changes when authorized.
- Before creating or reading CONCEPT/SYNCS or checking pipeline interfaces, read
  `references/spec-format.md` for behavior, interfaces, and dialect compatibility.
- Mark legacy wyx interactions, dependencies, known coupling, dispatching, coordination graphs, and
  `sync:` sections for migration rather than mixing dialects. When authorized, rewrite
  CONCEPT/SYNCS/PIPELINE together while preserving triggers, bindings, effects, and failure
  semantics.

Completion means the selected mode's definitions, relations, and references are evidenced; backfill
distinguishes facts, inference, and open decisions; reports name scan scope and repair direction;
maps are rebuilt from content rather than timestamps. For automatic injection read
`references/hooks-runtime.md`: hooks list specifications, flag staleness, and inject PIPELINE data
boundaries but do not validate semantic seams.
