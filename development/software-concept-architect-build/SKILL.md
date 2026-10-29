---
name: software-concept-architect-build
description: >-
  Generates implementations from confirmed concept models, defaulting to modular monoliths.
  Use only on explicit $software-concept-architect-build invocation.
metadata:
  language: en
  translation_of: software-concept-architect-build-cn
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# Software Concept Architect · Build

Map a confirmed concept model to verifiable, composable implementation. Run only on explicit
`$software-concept-architect-build` invocation; deliver a plan or code as requested. Continue confirmed
portions and route model gaps affecting implementation back to software-concept-architect-design.

## Concepts

- **Concept module**: partitions actions and their state relations by purpose, not by entity. The same
  identity can participate in several concepts. Use type parameters/opaque IDs for external identities;
  concepts never reference, call, or query each other. Encapsulate storage while exposing abstract
  state and actions to composition.
- **Synchronization rule**: a named causal rule outside concepts, expressing identifiable application
  policy that can be located, verified, and evolved independently. One entry can trigger several rules;
  one rule can serve several entries. Grouping preserves rule boundaries without requiring a file or
  package per rule.
- **Actions and queries**: actions are observable occurrences in the contract and may read or update
  state. Queries only return binding sets and produce no action completions. A request can occur as
  a Requesting/Web action without the requested action following.

## Constraints

- **Engineering baseline**: default to a modular monolith running in one process. Each concept,
  syncs, gateway, and shared module is an independently buildable and testable unit, assembled by
  server. Collaborate through public internal APIs; use Clean Architecture with dependencies toward
  domain and application contracts. Add layers for actual responsibilities, not empty or forwarding
  scaffolding. Honor confirmed project conventions; migration must be within the task scope.
- **Module boundaries**: business calls follow gateway → syncs → concepts. Concepts have no direct
  dependencies on each other; modules may use passive shared types as needed. Server may use public
  assembly entry points. Gateway holds syncs APIs, never concept implementations. Concepts own
  business state; syncs may retain necessary execution records.
- **Contracts and legibility**: composition produces only behavior permitted by each concept contract.
  Keep concept/action/parameter meanings aligned across specifications, code, and logs; map renames.
  Actions enforce preconditions, invariants, effects, and result cases. A false precondition does not
  automatically imply an error output; specify rejection results. Where queries cannot replace atomic
  checks at the write.
- **Rule execution**: use WYSIWID completion → binding → invocation semantics. When conjunctively
  matches named inputs/outputs; omitted fields are wildcards and empty patterns do not imply success.
  Where queries, filters, or computes zero/many binding sets; zero fires nothing, each set invokes then.
  Then uses constants or bound values; its calls have no implicit order. Subsequent outputs require
  new completion matches. State changes alone do not automatically trigger rules.
- **Correlation and permissions**: WYSIWID matches completions within one runtime flow and propagates
  that correlation. Batch actions also require object bindings; documentation groups are not runtime
  identities. Public actions/queries respect confirmed permissions. Connect rules through concept
  actions rather than hiding causality in direct sync-to-sync calls.
- **Failure and recovery**: handle no-match, rejection, and faults according to entry contracts; required
  responses must not be missing, crossed, or duplicated. Match errors and negative results by their
  respective cases. Define response, retry, compensation, or intentional ignoring and state consequences.
  Later failure does not erase completed actions; compensation need not restore state. Where recovery
  is required, persist rules, completions, bindings/invocations, and causal links; deduplicate by matched
  occurrence. External effects need separate idempotency guarantees.
- **Atomicity and progress**: implementations must realize abstract action atomicity; a database
  transaction alone does not make external effects atomic. Cross-concept transactions are optional,
  requiring contract permission, participating storage, and isolated external effects. Publish completions
  after commit or through a consistent outbox; failures still require results. Reachable cycles need
  termination, retry budgets, or controlled continuation with observable limit outcomes.

## Implementation

1. **Verify specifications**: read [the specification contract](references/spec-format.md), application
   purpose, concept model, both argument layers' assumptions, and project conventions. Trace actions,
   persistence, failures, and tests in existing code. Route model defects to design, transcription errors
   to PRD, and code violations here; update specifications before implementing confirmed new behavior.
2. **Map boundaries**: when defining project structure, read [architecture examples and counterexamples](references/architecture.md),
   then only the target language reference. Declare build units, public APIs, state owners, and assembly
   entry points. Queries preserve relations and zero/many bindings without accumulating getters.
   Place Requesting protocol adapters in gateway; keep concept signatures protocol-independent.
3. **Implement rules**: preserve policy boundaries and cross-entry reuse with named functions/rule
   objects. Simple compositions may use a mediator; consider an engine when conjunctive matching,
   independent rule evolution, or tracing makes handwritten scheduling complex. Both preserve the
   constraints above. Ordinary listeners do not automatically provide conjunction, historical correlation,
   or recovery. Flow indexes and causal records explain complete chains.
4. **Colocate and verify**: keep one CONCEPT per concept module and one SYNCS per syncs module,
   grouping flows inside it. Migrate staged specifications and update the PRD index. Build and test
   modules individually, then verify full assembly. Test OPs/invariants inside concepts,
   matching/bindings/branches per rule, and application purpose, concurrency isolation, and applicable
   failure recovery across rules. CI checks dependency graphs, public surfaces, layers, and read/write boundaries. Conformance
   does not establish purpose fitness; route counterexamples to the model. Delivery requires matching
   specifications/code, attributable executions, excluded actions neither called nor exposed, and no
   invented unresolved assumptions. Product subsets also require dependency closure, entries, remaining
   rules, resources, and build flags to be checked.

Select only [Rust / Axum](references/rust.md), [Java / Spring](references/java-spring.md), or
[TypeScript](references/typescript.md). Read [scaling](references/scaling.md) only for observed
navigation, build, or collaboration pain. The engineering baseline is repository policy;
read [sources](references/sources.md) when distinguishing theory from engineering conventions.
