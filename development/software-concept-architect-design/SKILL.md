---
name: software-concept-architect-design
description: >-
  Use when the user explicitly invokes $software-concept-architect-design. Completes a Daniel Jackson concept design
  with the user. Confirm the alignment, then write the design record.
metadata:
  language: en
  translation_of: software-concept-architect-design-cn
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# Software Concept Architect · Design

Complete the concept design with the user: confirm the three alignment sections, then write the
design record. Run only on explicit `$software-concept-architect-design` invocation. Continue into PRD or
implementation only when already authorized. If `software-concept-architect-prd` or `software-concept-architect-build` is
missing, deliver the model and name the missing step.

## Design principles

- **Familiarity.** Use a familiar concept, or a variant of one, when it meets the need.
- **Specificity.** Each concept serves one purpose. Do not add a second concept for the same purpose.
- **Integrity.** Synchronization may exclude some of a concept's behavior. It may not make the
  concept do something its own specification disallows.
- **Two arguments.** Contract → OP → concept purpose; concept selection and synchronizations →
  application scenarios → application purpose. Local validity does not prove overall fitness. The
  single-purpose criterion applies to concepts, not mechanically to applications.
- **Evidence.** Source facts, and label inferences and open decisions. Absence of a counterexample
  is not proof. Pages, entities, and code modules are only candidate clues.

## Design process

Confirm each part with the user. Mark anything not yet confirmed as pending, and do not record it
as a confirmed fact.

1. **Check facts** — With the user, identify beneficiaries, application purpose, current state,
   desired outcome, and constraints. In an existing system, trace actual entry points, state
   ownership, failure paths, and tests. Separate current from desired behavior. If the purpose is
   not yet stated, mark it open.
2. **Propose the inventory** — Write the concept inventory from `references/artifacts.md` and ask
   which concepts to include. After confirmation, write state and actions from
   `references/spec-format.md`. External identity is a type parameter with no assumed fields.
3. **Review seams** — Read `references/criteria.md`. Give all eight conclusions for each candidate.
   Leave disputes for the user to decide.
4. **Confirm scope, then compose** — Ask the user to confirm dependencies and subsets using
   `references/sync-notation.md`. Then write syncs from the specification contract, and check
   under-synchronization, over-synchronization, the synchronization diagram, and the MVP.
5. **Write the record** — Correct an evidenced misfit using the qualification standard. Write
   confirmed alignment into the design record. Keep pending items in exclusions and open decisions,
   and block only the portion that depends on them.

## Design artifacts

Field rules are in `references/artifacts.md`.

Alignment, confirmed with the user: concept inventory, application purpose and scenarios,
dependencies and subsets.

Design record, written after confirmation: Concepts, Synchronizations, synchronization diagram,
exclusions and open decisions.

## Standards

| Standard | Use |
| --- | --- |
| [Qualification](references/criteria.md) | whether a concept qualifies |
| [Specification contract](references/spec-format.md) | how to write purpose, state, actions, OP, and synchronizations |
| [Composition](references/sync-notation.md) | synchronization rules, the synchronization diagram, dependencies, and the MVP |

## Completion

- Every alignment item has a confirmation mark. Pending items appear only under exclusions and open
  decisions, with the portion they block.
- The concept purpose and the application purpose each have evidence of fulfillment, or are marked
  open.
- An entry that requires a response states success and refusal. The synchronization diagram,
  dependencies, and MVP meet the composition standard. The specification meets the contract.

For a first pass together, read `references/example-reserving.md`. For definitions and local
conventions, read `references/sources.md`.
