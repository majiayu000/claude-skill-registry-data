---
name: concept-model
description: Apply concept modeling principles to design, implementation, and maintenance by defining independent concepts around user purposes and coordinate their collaboration with synchronization rules.
metadata:
  language: en
  translation_of: concept-model-cn
  version: 1.2.0
---

# Working with concept modeling

Follow the structural pattern proposed by Daniel Jackson and Eagon Meng: build applications from concepts and synchronizations.
Concepts are fully independent services; synchronizations are event-based rules that mediate between them.

## Purpose

- One concept, one clear user-facing purpose.
- Fulfill the purpose with complete behavior.
- Use a representative behavioral history to explain how the purpose is fulfilled; define behavior through state and action specifications.

## Independence

- Each concept manages its own state; mutable state is not shared.
- Concepts are independently understandable; they neither invoke other concepts’ actions nor query their state.
- Keep references to external objects polymorphic, without depending on their concrete types or internal structure.

## Composition

- Concepts define behavior; synchronizations define collaboration.
- Synchronizations match action completions, query the required state, and invoke subsequent actions.
- Application-specific cross-concept rules belong in synchronizations, which depend only on concept specifications.
- Composed behavior must still conform to each concept’s specification.

## Engineering additions

The following conventions belong to this skill; they are not presented as the authors’ original wording or distinctive principles.

### Scope and separation

- Reuse before modeling: reuse capabilities that have mature, replaceable implementations and carry no rules that differentiate this product; keep only a thin concept or entry contract for those with a user purpose, and leave pure technical mechanisms out of the model.
- Concepts carry only this product's business rules and invariants; reused components stay behind ports and adapters, and their models stay out of concept state.

### Implementation

- Actions uphold preconditions, outcomes, and invariants.
- Make the observable outcomes of failure, retries, and concurrency explicit.
- Verify concept contracts and composition purposes separately.

### Maintenance

- Assign responsibility before adding structure; limit changes to what is needed.
- Preserve behavior when refactoring; make intentional changes explicit.
